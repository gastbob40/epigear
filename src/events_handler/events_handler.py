import discord

from src.events_handler.on_message.on_message import OnMessage


class EventsHandler:

    @staticmethod
    async def handle_on_message(client, message, config):
        await OnMessage.handle(client, message, config)
