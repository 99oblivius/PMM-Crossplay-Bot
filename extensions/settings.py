import lightbulb

from utils.logging import get_logger
log = get_logger()


settings = lightbulb.Group("settings", "Crossplay settings")


@settings.register
class Settings(
    lightbulb.SlashCommand,
    name="settings",
    description="Crossplay settings"
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        ...


@settings.register
class Setup(
    lightbulb.SlashCommand,
    name="setup",
    description="Initialize the default settings"
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        ...


loader = lightbulb.Loader()
loader.command(settings)
log.info(" - settings")
