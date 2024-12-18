from enum import Enum

__all__ = ("LastQueryMode",
"ColorSchemes",
"SearchWindowScreens",
"SearchWindowAligns",
"AnimationSpeeds",
"SearchPrecisionScore",)

class LastQueryMode(Enum):
    selected = "Selected"
    empty = "Empty"
    preserved = "Preserved"

class ColorSchemes(Enum):
    system = "System"
    light = "Light"
    dark = "Dark"

class SearchWindowScreens(Enum):
    remember_last_launch_location = "RememberLastLaunchLocation"
    cursor = "Cursor"
    focus = "Focus"
    primary = "Primary"
    custom = "Custom"

class SearchWindowAligns(Enum):
    center = "Center"
    centerTop = "CenterTop"
    leftTop = "LeftTop"
    rightTop = "RightTop"
    custom = "Custom"

class AnimationSpeeds(Enum):
    slow = "Slow"
    medium = "Medium"
    fast = "Fast"
    custom = "Custom"

class SearchPrecisionScore(Enum):
    regular = 50
    low = 20
    none = 0