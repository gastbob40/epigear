from datetime import datetime, timedelta

import discord


class EmbedsManager:
    @staticmethod
    def complete_embed(title, content=None):
        embed = discord.Embed(color=0x19D773) \
            .set_author(icon_url="https://cdn0.iconfinder.com/data/icons/shift-free/32/Complete_Symbol-512.png",
                        name=title)
        if content is not None:
            embed.description = content
        return embed

    @staticmethod
    def information_embed(title, content=None):
        embed = discord.Embed(color=0xEFCC00) \
            .set_author(icon_url="https://cdn0.iconfinder.com/data/icons/simply-orange-1/128/questionssvg-512.png",
                        name=title)

        if content is not None:
            embed.description = content
        return embed

    @staticmethod
    def error_embed(title, content=None):
        embed = discord.Embed(color=0xD72727) \
            .set_author(icon_url="https://cdn0.iconfinder.com/data/icons/shift-free/32/Error-512.png",
                        name=title)

        if content is not None:
            embed.description = content

        return embed

    @staticmethod
    def sanction_embed(title, content=None):
        embed = discord.Embed(color=0x0000) \
            .set_author(icon_url="https://cdn0.iconfinder.com/data/icons/tools-icons-rounded/110/Hammer-512.png",
                        name=title)

        if content is not None:
            embed.description = content

        return embed

    @staticmethod
    def secret_embed(title):
        embed = discord.Embed(color=0x0000) \
            .set_author(icon_url="https://f-scope.net/images600_/eyes-emoji-png.png",
                        name=title)

        return embed