import time

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice


class i2s(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="i2s", description="Gives you a seed to the ImageURL.", options=[
        create_option(
            name="imageurl",
            description="The URL to the Image",
            option_type=3,
            required=True
        )
    ])
    async def _i2s(self, ctx: SlashContext, imageurl: str = "pet N00bBot"):
        time.sleep(2)
        await ctx.send(content=f"The Seed of the ImageURL is: {hash(imageurl)}")


def setup(bot):
    bot.add_cog(i2s(bot))
