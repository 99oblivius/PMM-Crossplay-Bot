from __future__ import annotations

from typing import Final

import hikari

EMBED_COLOR: Final[hikari.Color] = hikari.Color.from_hex_code("#DA47FF")
EMBED_ERROR_COLOR: Final[hikari.Color] = hikari.Color.from_hex_code("#A0013E")
EMBED_WARN_COLOR: Final[hikari.Color] = hikari.Color.from_hex_code("#ECAD37")
EMBED_OK_COLOR: Final[hikari.Color] = hikari.Color.from_hex_code("#28E732")

class EmbedBuilder:
    @classmethod
    def ok(cls) -> EmbedBuilder:
        cl = cls()
        cl._color = EMBED_OK_COLOR
        return cl

    @classmethod
    def error(cls) -> EmbedBuilder:
        cl = cls()
        cl._color = EMBED_ERROR_COLOR
        return cl

    @classmethod
    def warn(cls) -> EmbedBuilder:
        cl = cls()
        cl._color = EMBED_WARN_COLOR
        return cl

    @classmethod
    def info(cls) -> EmbedBuilder:
        cl = cls()
        cl._color = EMBED_COLOR
        return cl

    def __init__(self) -> None:
        self._title: str | None = None
        self._description: str | None = None
        self._color: hikari.Color = EMBED_COLOR
        self._fields: list[tuple[str, str, bool]] = []
        self._thumbnail: str | None = None
        self._image: str | None = None
        self._author: tuple[str, str | None] | None = None
        self._footer_override: tuple[str, str | None] | None = None

    def title(self, value: str) -> EmbedBuilder:
        self._title = value
        return self

    def description(self, value: str) -> EmbedBuilder:
        self._description = value
        return self

    def color(self, value: hikari.Color) -> EmbedBuilder:
        self._color = value
        return self

    def thumbnail(self, url: str) -> EmbedBuilder:
        self._thumbnail = url
        return self

    def image(self, url: str) -> EmbedBuilder:
        self._image = url
        return self

    def field(self, name: str, value: str, inline: bool = False) -> EmbedBuilder:
        self._fields.append((name, value, inline))
        return self

    def author(self, name: str, icon_url: str | None = None) -> EmbedBuilder:
        self._author = (name, icon_url)
        return self

    def footer(self, text: str, icon_url: str | None = None) -> EmbedBuilder:
        self._footer_override = (text, icon_url)
        return self

    def build(self) -> hikari.Embed:
        embed = hikari.Embed(
            title=self._title,
            description=self._description,
            color=self._color)

        for name, value, inline in self._fields:
            embed.add_field(name=name, value=value, inline=inline)

        if self._thumbnail:
            embed.set_thumbnail(self._thumbnail)
        if self._image:
            embed.set_image(self._image)
        if self._author:
            embed.set_author(name=self._author[0], icon=self._author[1])

        if self._footer_override:
            text, icon = self._footer_override
            embed.set_footer(text=text, icon=icon)

        return embed
