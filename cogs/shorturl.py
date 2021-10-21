import pyourls3
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from config.config import roles, yourls_user, yourls_passwd
from config import config


class shorturl(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.yourls = pyourls3.Yourls(addr='https://mcatho.me/yourls-api.php', user=yourls_user, passwd=yourls_passwd)

    @cog_ext.cog_subcommand(guild_ids=config.slash_shorturl_create, base="shorturl", name="create", options=[
        create_option(
            name="url",
            description="The URL you want to shorten.",
            option_type=3,
            required=True
        ), create_option(
            name="tag",
            description="The TAG you want mcahto.me/<TAG>.",
            option_type=3,
            required=True
        )
    ])
    @commands.has_any_role(roles.admin, roles.servermod, roles.chatmod, roles.privateprojectaccess)
    async def _grant(self, ctx: SlashContext, url: str, tag: str):
        try:
            surl = self.yourls.shorten(url, keyword=tag)
            print(surl)
            await ctx.send(
                "URL got shortened:\nLong URL:```" + surl['url']['url'] + "```Short URL:```" + surl['shorturl'] + "```")
        except pyourls3.exceptions.Pyourls3APIError as e:
            await ctx.send(str(e))


def setup(bot):
    bot.add_cog(shorturl(bot))
