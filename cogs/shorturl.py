import pyourls3
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from config.config import roleslevel, yourls_user, yourls_passwd
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
    @commands.has_any_role(*roleslevel.ppa)
    async def _create(self, ctx: SlashContext, url: str, tag: str):
        try:
            surl = self.yourls.shorten(url, keyword=tag)
            print(surl)
            await ctx.send(f"URL got shortened:\n"
                           f"Long URL: ```{surl['url']['url']} ```"
                           f"Short URL: ```{surl['shorturl']} ```")
        except pyourls3.exceptions.Pyourls3APIError as e:
            await ctx.send(str(e))

    @cog_ext.cog_subcommand(guild_ids=config.slash_shorturl_create, base="shorturl", name="stats", options=[
        create_option(
            name="tag",
            description="The TAG you want to get the stats for mcahto.me/<TAG> or all.",
            option_type=3,
            required=True
        )
    ])
    @commands.has_any_role(*roleslevel.member)
    async def _stats(self, ctx: SlashContext, tag: str):
        if tag == "all":
            urls = self.yourls.stats()
            await ctx.send(f"General link statistics:\n"
                           f"Total Links: ```{urls['total_links']} ```"
                           f"Total Clicks: ```{urls['total_clicks']} ```")
            return
        try:
            urls = self.yourls.url_stats(tag)
            await ctx.send(f"Stats for shortened URL: ```{urls['shorturl']} ```"
                           f"Long URL: ```{urls['url']} ```"
                           f"Clicks: ```{urls['clicks']} ```"
                           f"Created: ```{urls['timestamp']} ```")
        except:
            await ctx.send(f"The TAG probably doesn't exist! `{tag}`", delete_after=10)


def setup(bot):
    bot.add_cog(shorturl(bot))
