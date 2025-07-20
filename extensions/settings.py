from hikari import ChannelType
import lightbulb
from rapidfuzz import process, fuzz

from components.database import Database
from components.gel_queries import (
    guild_set, 
    map_create, 
    map_disable,
    maps_get
)

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
        embed = EmbedBuilder.ok()
        embed.title("Queue Channel")
        embed.description(f"You successfully set the `Queue Channel` to <#{channel_set}>")
        await ctx.respond(embed=embed.build(), ephemeral=True)
        log.info(f"Queue Channel {channel_set} registered")


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
        embed = EmbedBuilder.ok()
        embed.title("Scores Channel")
        embed.description(f"You successfully set the `Scores Channel` to <#{channel_set}>")
        await ctx.respond(embed=embed.build(), ephemeral=True)
        log.info(f"Scores Channel {channel_set} registered")


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
        embed = EmbedBuilder.ok()
        embed.title("Staff Role")
        embed.description(f"You successfully set the `Staff Role` to {self.role.mention}")
        await ctx.respond(embed=embed.build(), ephemeral=True)
        log.info(f"Staff Role {self.role.name} registered")


maps = settings.subgroup("map", "Manage maps")


@maps.register
class MapAdd(
    lightbulb.SlashCommand,
    name="add",
    description="Add a map"
):
    name = lightbulb.string("name", "The name of the map. Case and whitespace sensitive")
    image_url = lightbulb.string("image", "The image url that matches the map.")
    
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, db: Database) -> None:
        if not ctx.guild_id: return
        await map_create(db.executor, guild_id=ctx.guild_id, name=self.name, image_url=self.image_url)
        embed = EmbedBuilder.ok()
        embed.title("Map Create")
        embed.description(f"You successfully added map `{self.name}`.")
        await ctx.respond(embed=embed.build(), ephemeral=True)
        log.info(f"Map {self.name} Added")


async def guild_maps_autocomplete_callback(ctx: lightbulb.AutocompleteContext[str], db: Database=lightbulb.di.INJECTED) -> None:
    value = str(ctx.focused.value) or ""
    guild_id = ctx.interaction.guild_id
    if not guild_id: return
    maps = [m.name for m in await maps_get(db.executor, guild_id=guild_id)]
    if not value:
        await ctx.respond(maps[:25]); return
    
    results = process.extract(
        value.lower(), (m.lower() for m in maps),
        limit=25, score_cutoff=30)
    await ctx.respond([maps[r[2]] for r in results])

@maps.register
class MapRemove(
    lightbulb.SlashCommand,
    name="remove",
    description="Remove a map"
):
    name = lightbulb.string("name", "The name of the map. Case and whitespace sensitive",
        autocomplete=guild_maps_autocomplete_callback)
    
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, db: Database) -> None:
        if not ctx.guild_id: return
        await map_disable(db.executor, guild_id=ctx.guild_id, name=self.name)
        embed = EmbedBuilder.ok()
        embed.title("Map Removed")
        embed.description(f"You successfully removed map `{self.name}`.")
        await ctx.respond(embed=embed.build(), ephemeral=True)
        log.info(f"Map {self.name} Removed")


loader = lightbulb.Loader()
loader.command(settings)
log.info(" - settings")
