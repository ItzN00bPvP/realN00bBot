from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from main import notauthorized


class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="admin", name="reloadcog", options=[
        create_option(
            name="cog",
            description="The cog you want to reload.",
            option_type=3,
            required=True
        )
    ])
    async def _microboinc_deletebyid(self, ctx: SlashContext, cog: str):
        if not ctx.author_id == 374245848659263488:
            await notauthorized(ctx)
            return
        self.bot.unload_extension(cog)
        self.bot.load_extension(cog)
        await ctx.send(f"Reloaded cog: {cog}")


def setup(bot):
    bot.add_cog(Slash(bot))
