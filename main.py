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

@client.register()
class Hello(
    lightbulb.SlashCommand,
    name="hello",
    description="Says hi back"
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Hiii cutie")


@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    if not event.is_human:
        return

    me = bot.get_me()
    if me is not None and me.id in (event.message.user_mentions_ids or list()):
        await event.message.respond("Pong!")

@bot.listen()
async def starting(_: hikari.StartingEvent) -> None:
    log.info("Loading: extensions")
    await client.load_extensions_from_package(extensions, recursive=True)
    log.info("Starting client")
    await client.start()

@bot.listen()
async def started(_: hikari.StartedEvent) -> None:
    log.info("Hikari started")


if __name__ == "__main__":
    database = Database()
    
    registry = client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
    registry.register_value(Database, database)
    
    bot.run(
        asyncio_debug=False,
        propagate_interrupts=True)
