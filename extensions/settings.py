from hikari import ChannelType
import lightbulb

from components.database import Database
from components.gel_queries import guild_set

from utils.embeddings import EmbedBuilder

from utils.logging import get_logger
log = get_logger()


settings = lightbulb.Group("settings", "Crossplay settings")

setup = settings.subgroup("setup", "Setup most important settings")


@setup.register
class SetupQueue(
    lightbulb.SlashCommand,
    name="queue",
    description="Setup Queue Channel"
):
    channel = lightbulb.channel("channel", "The channel for players to join the queue from.", channel_types=[ChannelType.GUILD_TEXT], default=None)
    
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, db: Database) -> None:
        if not ctx.guild_id: return
        channel_set = self.channel.id if self.channel else ctx.channel_id
        await guild_set(db.executor, guild_id=ctx.guild_id, queue_channel_id=channel_set)
        embed = EmbedBuilder()
        embed.title("Queue Channel")
        embed.description(rf"\- You successfully set the `Queue Channel` to <#{channel_set}>")
        embed.ok()
        await ctx.respond(embed=embed.build(), ephemeral=True)


@setup.register
class SetupScores(
    lightbulb.SlashCommand,
    name="scores",
    description="Setup Scores Channel"
):
    channel = lightbulb.channel("channel", "The channel for players to see match scores in.", channel_types=[ChannelType.GUILD_TEXT], default=None)
    
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, db: Database) -> None:
        if not ctx.guild_id: return
        channel_set = self.channel.id if self.channel else ctx.channel_id
        await guild_set(db.executor, guild_id=ctx.guild_id, scores_channel_id=channel_set)
        embed = EmbedBuilder()
        embed.title("Scores Channel")
        embed.description(rf"\- You successfully set the `Scores Channel` to <#{channel_set}>")
        embed.ok()
        await ctx.respond(embed=embed.build(), ephemeral=True)


@setup.register
class SetupStaffRole(
    lightbulb.SlashCommand,
    name="staff",
    description="Setup Staff Role"
):
    role = lightbulb.role("role", "The staff member role.")
    
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, db: Database) -> None:
        if not ctx.guild_id: return
        await guild_set(db.executor, guild_id=ctx.guild_id, staff_role_id=self.role.id)
        embed = EmbedBuilder()
        embed.title("Staff Role")
        embed.description(rf"\- You successfully set the `Staff Role` to {self.role.mention}")
        embed.ok()
        await ctx.respond(embed=embed.build(), ephemeral=True)


loader = lightbulb.Loader()
loader.command(settings)
log.info(" - settings")
