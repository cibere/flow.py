from .base_object import Base
from typing import Self, Any

class Glyph(Base):
    r"""This represents a glyth object with flow launcher, which is an alternative to :class:`~flogin.jsonrpc.results.Result` icons.
    
    Attributes
    ----------
    text: :class:`str`
        The text to be shown in the glyph
    font_family: :class:`str`
        The font that the text should be shown in
    """

    __slots__ = "text", "font_family"
    __jsonrpc_option_names__ = {
        "text": "Glyph",
        "font_family": "FontFamily"
    }

    def __init__(self, text: str, font_family: str) -> None:
        self.text = text
        self.font_family = font_family
    
    @classmethod
    def from_dict(cls: type[Self], data: dict[str, Any]) -> Self:
        r"""Converts a dictionary into a :class:`Glyph` object.
        
        Parameters
        ----------
        data: dict[:class:`str`, Any]
            The dictionary
        """
        
        return cls(text=data['Glyth'], font_family=data['FontFamily'])
