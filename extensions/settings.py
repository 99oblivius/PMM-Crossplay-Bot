import lightbulb

from utils.logging import get_logger
log = get_logger()


loader = lightbulb.Loader()

#TODO MAKE THIS A SUBGROUP SOMEHOW
@loader.command
class YourCommand(
    lightbulb.SlashCommand,
    name="settings",
    description="Crossplay settings"
):
    ...


@loader.command
class Setup(
    lightbulb.SlashCommand,
    name="setup",
    description="Initialize the default settings"
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        ...