from .dmluku import DmLuku


async def setup(bot):
    await bot.add_cog(dmluku(bot))