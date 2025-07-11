from asyncio import create_task, sleep
import lightbulb


AUTO_DEFER = lightbulb.ExecutionStep("AUTO_DEFER")

async def _auto_defer(pl: lightbulb.ExecutionPipeline, ctx: lightbulb.Context) -> None:
    await sleep(2.5)
    if pl.failed: return
    if not ctx._initial_response_sent.is_set():
        await ctx.defer()

@lightbulb.hook(AUTO_DEFER)
def auto_defer(pl: lightbulb.ExecutionPipeline, ctx: lightbulb.Context) -> None:
    create_task(_auto_defer(pl, ctx))
