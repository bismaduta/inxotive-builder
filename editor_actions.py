"""
EDITOR ACTIONS — Action schema, validator, state patcher.
Jantung sistem editor: LLM/UI hanya keluarkan JSON action → validator → state patch.

Action = { action: str, target: str, value: any }
  - action:  salah satu dari ALLOWED_ACTIONS
  - target:  path ke field di state (dot notation, e.g. "hero.headline")
  - value:   nilai baru (string, number, bool, array)

Alur:
  1. LLM/UI  →  action JSON
  2. validate(action, state)  →  tolak jika ilegal
  3. apply(action, state)     →  state baru
  4. render(state)            →  HTML preview baru
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple

# ═══════════════════════════════════════════
# SCHEMA: allowed actions & per-action validators
# ═══════════════════════════════════════════

ALLOWED_ACTIONS = {
    "set_text": {
        "description": "Ubah teks di section tertentu",
        "target_pattern": r"^(hero|features|about|cta)\.(headline|subtext|cta|eyebrow|button|heading|body)$",
        "value_type": "string",
    },
    "set_image": {
        "description": "Ganti gambar (URL atau upload_id)",
        "target_pattern": r"^(hero)\.",
        "value_type": "string",
    },
    "set_color": {
        "description": "Ubah warna brand",
        "target_pattern": r"^(design\.brand_primary|design\.brand_secondary|design\.brand_accent)$",
        "value_type": "hex_color",
        "validator": "_validate_contrast",
    },
    "swap_variant": {
        "description": "Ganti layout variant section",
        "target_pattern": r"^(features|hero|about|pricing|testimonials)$",
        "value_type": "string",
        "allowed_values": {
            "features": ["grid", "zigzag", "asymmetric-2col", "showcase", "icon-grid"],
            "hero": ["split", "centered", "full-bleed", "video", "showcase"],
            "about": ["standard", "right-image", "split"],
            "pricing": ["default", "compact"],
            "testimonials": ["default", "carousel"],
        },
    },
    "toggle_section": {
        "description": "Tampil/sembunyikan section",
        "target_pattern": r"^(hero|features|stats|about|testimonials|pricing|faq|cta|contact|team|gallery|process|logos)$",
        "value_type": "boolean",
    },
    "reorder": {
        "description": "Ubah urutan section",
        "target_pattern": r"^sections$",
        "value_type": "array",
    },
    "set_density": {
        "description": "Ubah kerapatan spacing section",
        "target_pattern": r"^(section\.\w+)$",
        "value_type": "select",
        "allowed_values": ["xl", "lg", "md", "sm"],
    },
    "set_font": {
        "description": "Ganti font display/body",
        "target_pattern": r"^(design\.font_display|design\.font_body)$",
        "value_type": "string",
    },
}

# ═══════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════

# Simple contrast ratio checker (WCAG 4.5:1)
def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def _relative_luminance(r: int, g: int, b: int) -> float:
    def linearize(c: float) -> float:
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

def contrast_ratio(color1: str, color2: str = "#FFFFFF") -> float:
    """Calculate WCAG contrast ratio between two hex colors."""
    l1 = _relative_luminance(*_hex_to_rgb(color1))
    l2 = _relative_luminance(*_hex_to_rgb(color2))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def validate_action(action: dict, state: dict) -> Tuple[bool, str]:
    """
    Validasi action sebelum diterapkan.
    Returns: (is_valid, error_message)
    """
    # 1. Action ada
    act = action.get("action", "")
    schema = ALLOWED_ACTIONS.get(act)
    if not schema:
        return False, f"Action '{act}' tidak dikenal. Allowed: {', '.join(ALLOWED_ACTIONS.keys())}"

    # 2. Target cocok pattern
    target = action.get("target", "")
    pattern = schema.get("target_pattern", "")
    if pattern and not re.match(pattern, target):
        return False, f"Target '{target}' tidak valid untuk action '{act}'. Pattern: {pattern}"

    # 3. Value type sesuai
    value = action.get("value")
    expected_type = schema.get("value_type", "")

    if expected_type == "string" and not isinstance(value, str):
        return False, f"Value harus string, got {type(value).__name__}"
    if expected_type == "boolean" and not isinstance(value, bool):
        return False, f"Value harus boolean, got {type(value).__name__}"
    if expected_type == "array" and not isinstance(value, list):
        return False, f"Value harus array, got {type(value).__name__}"

    # 4. Hex color valid
    if expected_type == "hex_color":
        if not isinstance(value, str) or not re.match(r"^#[0-9A-Fa-f]{3,6}$", value):
            return False, f"Value harus hex color (#RRGGBB), got '{value}'"
        # Check contrast against white text (common case)
        ratio = contrast_ratio(value)
        if ratio < 3.0:
            return False, f"Kontras terlalu rendah ({ratio:.1f}:1). Minimal 3:1 untuk aksesibilitas."

    # 5. Allowed values
    allowed = schema.get("allowed_values")
    if allowed and isinstance(allowed, dict):
        # Per-target allowed values
        for key, vals in allowed.items():
            if key in target or target in key:
                if value not in vals:
                    return False, f"Value '{value}' tidak valid untuk {target}. Pilihan: {', '.join(vals)}"
    elif allowed and isinstance(allowed, list):
        if value not in allowed:
            return False, f"Value '{value}' tidak valid. Pilihan: {', '.join(allowed)}"

    return True, ""


# ═══════════════════════════════════════════
# STATE PATCHER
# ═══════════════════════════════════════════

def get_nested(data: dict, path: str, default=None):
    """Get nested value using dot notation path."""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        elif isinstance(current, list) and key.isdigit():
            idx = int(key)
            current = current[idx] if idx < len(current) else default
        else:
            return default
    return current


def set_nested(data: dict, path: str, value) -> dict:
    """Set nested value using dot notation path. Returns new dict (immutable)."""
    import copy
    result = copy.deepcopy(data)
    keys = path.split(".")
    current = result
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value
    return result


def apply_action(action: dict, state: dict) -> Tuple[dict, Optional[str]]:
    """
    Apply validated action to state.
    Returns: (new_state, error)
    """
    valid, error = validate_action(action, state)
    if not valid:
        return state, error

    act = action["action"]
    target = action["target"]
    value = action["value"]

    # Build a path that works with content_models structure
    # Map friendly targets to actual model paths
    path_map = {
        "hero.headline": "hero.headline",
        "hero.subtext": "hero.subtext",
        "hero.eyebrow": "hero.eyebrow",
        "hero.cta": "hero.cta",
        "features.heading": "features.heading",
        "about.heading": "about.heading",
        "about.body": "about.body",
        "cta.heading": "cta.heading",
        "cta.subtext": "cta.subtext",
        "cta.button": "cta.button",
    }

    actual_path = path_map.get(target, target)

    if act == "set_text":
        new_state = set_nested(state, actual_path, str(value))
        return new_state, None

    elif act == "set_color":
        # Colors are at state level
        color_key = target.replace("design.", "")
        new_state = set_nested(state, color_key, str(value))
        return new_state, None

    elif act == "swap_variant":
        new_state = set_nested(state, f"layout.{target}", str(value))
        return new_state, None

    elif act == "toggle_section":
        current = get_nested(state, f"sections.{target}", True)
        # Can be True (show) or False (hide)
        sections = state.get("sections", {})
        import copy
        new_state = copy.deepcopy(state)
        if "sections" not in new_state:
            new_state["sections"] = {}
        new_state["sections"][target] = bool(value)
        return new_state, None

    elif act == "set_density":
        new_state = set_nested(state, actual_path, str(value))
        return new_state, None

    elif act == "set_image":
        new_state = set_nested(state, actual_path, str(value))
        return new_state, None

    elif act == "set_font":
        new_state = set_nested(state, actual_path, str(value))
        return new_state, None

    return state, f"Unknown action: {act}"


# ═══════════════════════════════════════════
# SUGGEST ACTIONS FROM LLM RESPONSE
# ═══════════════════════════════════════════

def parse_llm_response(llm_text: str) -> Tuple[List[dict], List[str]]:
    """
    Parse LLM response text into list of actions.
    LLM harus mengeluarkan actions dalam format:

    ACTION: {"action": "set_text", "target": "hero.headline", "value": "..."}
    ACTION: {"action": "set_color", "target": "design.brand_primary", "value": "#..."}

    Returns: (valid_actions, errors)
    """
    actions = []
    errors = []

    # Find all ACTION: {...} patterns
    for match in re.finditer(r'ACTION:\s*(\{.*?\})(?:\n|$)', llm_text, re.DOTALL):
        try:
            action = json.loads(match.group(1))
            actions.append(action)
        except json.JSONDecodeError as e:
            errors.append(f"Parse error: {e}")

    return actions, errors


def llm_to_actions(llm_text: str) -> List[dict]:
    """
    Cepat: langsung parse text ke actions tanpa error detail.
    """
    actions, _ = parse_llm_response(llm_text)
    return actions


# ═══════════════════════════════════════════
# UNDO STACK
# ═══════════════════════════════════════════

class UndoStack:
    """Simple undo/redo stack for editor state."""

    def __init__(self, max_size: int = 50):
        self._stack = []
        self._index = -1
        self._max_size = max_size

    def push(self, state: dict):
        # Remove any redo history
        self._stack = self._stack[:self._index + 1]
        self._stack.append(state)
        if len(self._stack) > self._max_size:
            self._stack.pop(0)
        self._index = len(self._stack) - 1

    def undo(self) -> Optional[dict]:
        if self._index > 0:
            self._index -= 1
            return self._stack[self._index]
        return None

    def redo(self) -> Optional[dict]:
        if self._index < len(self._stack) - 1:
            self._index += 1
            return self._stack[self._index]
        return None

    @property
    def can_undo(self) -> bool:
        return self._index > 0

    @property
    def can_redo(self) -> bool:
        return self._index < len(self._stack) - 1

    def to_dict(self) -> dict:
        return {
            "can_undo": self.can_undo,
            "can_redo": self.can_redo,
            "size": len(self._stack),
            "position": self._index,
        }


if __name__ == "__main__":
    # Demo
    state = {
        "hero": {"headline": "Test", "subtext": "Sub"},
        "design": {"brand_primary": "#4F46E5"},
    }

    # Test valid action
    action = {"action": "set_text", "target": "hero.headline", "value": "Garden Dining"}
    valid, err = validate_action(action, state)
    print(f"Action valid: {valid} {'(' + err + ')' if err else ''}")

    # Test contrast validation
    action2 = {"action": "set_color", "target": "design.brand_primary", "value": "#FFCC00"}
    valid2, err2 = validate_action(action2, {"design": {"brand_primary": "#FFCC00"}})
    print(f"Color action valid: {valid2} {'(' + err2 + ')' if err2 else ''}")

    # Test apply
    new_state, _ = apply_action(action, state)
    print(f"New state: {new_state}")

    # Test undo stack
    undo = UndoStack()
    undo.push(state)
    undo.push(new_state)
    print(f"Undo available: {undo.can_undo}")
    print(f"Redo available: {undo.can_redo}")
