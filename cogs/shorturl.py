import discord
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
            description="The TAG you want mcatho.me/<TAG>.",
            option_type=3,
            required=True
        )
    ])
    @commands.has_any_role(*roleslevel.ppa)
    async def _create(self, ctx: SlashContext, url: str, tag: str):
        try:
            surl = self.yourls.shorten(url, keyword=tag)
            embedvar = discord.Embed(title="URL got shortened", color=0x5500bd)
            embedvar.add_field(name="long URL:", value=f"{surl['url']['url']}", inline=False)
            embedvar.add_field(name="short URL:", value=f"{surl['shorturl']}", inline=False)
            await ctx.send(embed=embedvar)
        except pyourls3.exceptions.Pyourls3APIError as e:
            await ctx.send(str(e))

    @cog_ext.cog_subcommand(guild_ids=config.slash_shorturl_create, base="shorturl", name="stats", options=[
        create_option(
            name="tag",
            description="The TAG you want to get the stats for mcatho.me/<TAG> or all.",
            option_type=3,
            required=True
        )
    ])
    @commands.has_any_role(*roleslevel.member)
    async def _stats(self, ctx: SlashContext, tag: str):
        if tag == "all":
            urls = self.yourls.stats()
            embedvar = discord.Embed(title="General link statistics", color=0x5500bd)
            embedvar.add_field(name="Total Links:", value=f"{urls['total_links']}", inline=False)
            embedvar.add_field(name="Total clicks:", value=f"{urls['total_clicks']}", inline=False)
            await ctx.send(embed=embedvar)
            return
        try:
            urls = self.yourls.url_stats(tag)
            embedvar = discord.Embed(title="Statistics for the shortened URL", color=0x5500bd)
            embedvar.add_field(name="short URL:", value=f"{urls['shorturl']}", inline=False)
            embedvar.add_field(name="long URL:", value=f"{urls['url']}", inline=False)
            embedvar.add_field(name="clicks:", value=f"{urls['clicks']}", inline=False)
            embedvar.add_field(name="created:", value=f"{urls['timestamp']}", inline=False)
            await ctx.send(embed=embedvar)
        except:
            await ctx.send(f"The TAG probably doesn't exist! `{tag}`", delete_after=10)


def setup(bot):
    bot.add_cog(shorturl(bot))
