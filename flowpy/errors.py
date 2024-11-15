from typing import Any

__all__ = (
    "PluginException",
    "PluginMethodException",
    "SettingNotFound",
    "PluginExecutionError",
    "PluginNotInitialized"
)


class PluginException(Exception): ...


class PluginMethodException(PluginException):
    def __init__(self, method: str, error: Exception, *, text: str | None = None):
        super().__init__(
            f"An exception occured while running the {method!r} method: {text or error}"
        )
        self.method = method
        self.error = error
        self.text = text


class SettingNotFound(PluginException):
    def __init__(self, name: str) -> None:
        super().__init__(f"Setting {name!r} was not found.")
        self.name = name


class PluginExecutionError(PluginException):
    def __init__(self, method: str, parameters: list[Any], error: Exception):
        self.method = method
        self.parameters = parameters
        self.error = error
        super().__init__(
            f"An error occured while executing the {method!r} method: {error}"
        )

class PluginNotInitialized(PluginException):
    def __init__(self):
        return super().__init__("The plugin hasn't been initialized yet")