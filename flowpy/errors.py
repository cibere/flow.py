from typing import Any

__all__ = (
    "PluginException",
    "PluginMethodException",
    "SettingNotFound",
    "PluginExecutionError",
    "PluginNotInitialized",
)


class PluginException(Exception):
    r"""A class that represents exceptions with your plugin"""


class PluginMethodException(PluginException):
    r"""A class that represents exceptions that were raised while executing callback methods
    
    Attributes
    --------
    method: :class:`str`
        The name of the method that was being executed when the error occured
    error: :class:`Exception`
        The error that occured
    text: Optional[:class:`str`]
        Extra information
    """

    def __init__(self, method: str, error: Exception, *, text: str | None = None):
        super().__init__(
            f"An exception occured while running the {method!r} method: {text or error}"
        )
        self.method = method
        self.error = error
        self.text = text


class SettingNotFound(PluginException):
    r"""This gets raised when you try to access a setting key that doesn't exist
    
    Attributes
    --------
    name: :class:`str`
        The name of the setting key
    """

    def __init__(self, name: str) -> None:
        super().__init__(f"Setting {name!r} was not found.")
        self.name = name


class PluginExecutionError(PluginException):
    r"""A class that represents exceptions that were raised while executing callback methods
    
    Attributes
    --------
    method: :class:`str`
        The name of the method that was being executed when the error occured
    error: :class:`Exception`
        The error that occured
    parameters: list[Any]
        The parameters that were passed to the method
    """

    def __init__(self, method: str, parameters: list[Any], error: Exception):
        self.method = method
        self.parameters = parameters
        self.error = error
        super().__init__(
            f"An error occured while executing the {method!r} method: {error}"
        )


class PluginNotInitialized(PluginException):
    r"""This is raised when you try to access something that needs data from the initialize method, and it hasn't been called yet.
    """
    
    def __init__(self):
        return super().__init__("The plugin hasn't been initialized yet")
