from discord.ext.bridge import BridgeContext, BridgeExtContext, BridgeApplicationContext


# TODO: open ticket in py-cord to make BridgeExtContext ignore 'ephemeral'
async def defer(ctx: BridgeContext):
    if isinstance(ctx, BridgeExtContext):
        await ctx.defer()
    elif isinstance(ctx, BridgeApplicationContext):
        await ctx.defer(ephemeral=True)
