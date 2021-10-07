from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from config import config


class Fix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(guild_ids=config.slash_fix, name="fix", description="If you have a problem this command helps you to fix it.")
    async def _fix(self, ctx: SlashContext):
        await ctx.send("<@257642666244833281> go do fix!")


def setup(bot):
    bot.add_cog(Fix(bot))
