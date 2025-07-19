import utils.uvloop as _
from utils.config import DISCORD_TOKEN

from components.database import Database
import extensions

import hikari
import lightbulb

import logging
from utils.logging import setup_logging, get_logger
setup_logging(logging.DEBUG)
log = get_logger()


bot = hikari.GatewayBot(
    intents=hikari.Intents.ALL,
    token=DISCORD_TOKEN)
client = lightbulb.client_from_app(bot)
bot.subscribe(hikari.StartingEvent, client.start)
bot.subscribe(hikari.StoppingEvent, client.stop)

@bot.listen()
async def starting(_: hikari.StartingEvent) -> None:
    log.info("Loading: extensions")
    await client.load_extensions_from_package(extensions, recursive=True)
    log.info("Starting client")
    await client.start()


if __name__ == "__main__":
    database = Database()
    
    registry = client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
    registry.register_value(Database, database)
    
    bot.run(
        asyncio_debug=False,
        propagate_interrupts=True)
