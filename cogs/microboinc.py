import discord
from time import time
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from main import notauthorized
from utils import mattapi, chards, leaderboard
from config.config import rootdir, apikeyselfcreationisallowed


class Microboinc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="microboinc", name="createapikey", options=[
        create_option(
            name="nickname",
            description="The nickname for microboinc!",
            option_type=3,
            required=True
        ),
        create_option(
            name="user",
            description="Only needed if you want to create an API-Key for some one else!",
            option_type=6,
            required=False
        )
    ])
    async def _microboinc_createapikay(self, ctx: SlashContext, nickname: str, user: discord.Member = None):
        apifor = ctx.author
        if user is not None and user != ctx.author:
            if not mattapi.isapilevelbyid(ctx.author_id, 2):
                await notauthorized(ctx)
                return
            apifor = user
        else:
            if not apikeyselfcreationisallowed:
                await ctx.send("This feature is currently disabled!")
                return

        success, res = mattapi.register(nickname, apifor.id)
        if not success:
            await ctx.send("Something went wrong:\n" + res)
            return

        apikey = res
        try:
            await apifor.send(content=f"Microboinc account created:\nNickname: {nickname}\nAPI-Key: {apikey}")
            await ctx.send(content=f"API-Key for {nickname}({apifor.mention}) created and send to their DMs.")
        except discord.Forbidden:
            await ctx.send(hidden=True, content=f"!Couldn't send API-Key to DMS!\n"
                                                f"!THIS MESSAGE IS ONLY VISIBLE TO YOU!\n"
                                                f"Microboinc account created for {apifor.mention}:\n"
                                                f"Nickname: {nickname}\n"
                                                f"API-Key: {apikey}")

    @cog_ext.cog_subcommand(base="microboinc", name="regenapikey", options=[
        create_option(
            name="user",
            description="Only needed if you want to regen an API-Key for some one else!",
            option_type=6,
            required=False
        )
    ])
    async def _microboinc_regenapikey(self, ctx: SlashContext, user: discord.Member = None):
        apifor = ctx.author
        if user is not None and user != ctx.author:
            if not mattapi.isapilevelbyid(ctx.author_id, 4):
                await notauthorized(ctx)
                return
            apifor = user

        success, res = mattapi.regen(apifor.id)
        if not success:
            await ctx.send("Something went wrong:\n" + res)
            return

        apikey = res
        try:
            await apifor.send(content=f"Microboinc API-Key regened:\nAPI-Key: {apikey}")
            await ctx.send(content=f"API-Key regened and send to their DMs.")
        except discord.Forbidden:
            await ctx.send(hidden=True, content=f"!Couldn't send API-Key to DMS!\n"
                                                f"!THIS MESSAGE IS ONLY VISIBLE TO YOU!\n"
                                                f"Microboinc account created for {apifor.mention}:\n"
                                                f"API-Key: {apikey}")

    @cog_ext.cog_subcommand(base="microboinc", name="deletebyid", options=[
        create_option(
            name="user",
            description="The User you want to delete.",
            option_type=6,
            required=True
        )
    ])
    async def _microboinc_deletebyid(self, ctx: SlashContext, user: discord.Member):
        if not mattapi.isapilevelbyid(ctx.author_id, 3):
            await notauthorized(ctx)
            return

        success, res = mattapi.deletebyid(user.id)

        if not success:
            await ctx.send("Something went wrong:\n" + res)
            return

        await ctx.send(content=f"User({user.mention}) has been deleted.")

    @cog_ext.cog_subcommand(base="microboinc", name="results", options=[
        create_option(
            name="appid",
            description="The appid form microboinc.",
            option_type=3,
            required=True
        )
    ])
    async def _microboinc_results(self, ctx: SlashContext, appid: int):
        if not mattapi.isapilevelbyid(ctx.author_id, 1):
            await notauthorized(ctx)
            return

        foname = f'{int(time())}_results{appid}.txt'
        fname = f'{rootdir}/results/{int(time())}_results{appid}.txt'
        suc, res = mattapi.getresultsbyappid(appid)
        if not suc:
            await ctx.send(f"Something went wrong: {res}")
            return

        f = open(fname, "w")
        f.write(res)
        f.close()

        await ctx.send(f"Here are the results for app: {appid}\nhttps://microboincresults.mcathome.dev/{foname}")
        #, files=[discord.File(fname)])

    @cog_ext.cog_subcommand(base="microboinc", name="leaderboard", options=[
        create_option(
            name="projectid",
            description="The ID from the project you want the leaderboard from!",
            option_type=4,
            required=True
        ), create_option(
            name="type",
            description="The type of chard you want!",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="Graph",
                    value="1"
                ),
                create_choice(
                    name="Pie",
                    value="2"
                )
            ]
        )
    ])
    async def _microboinc_leaderboard(self, ctx: SlashContext, projectid: int, type: str = "1"):
        fname = f'{rootdir}/leaderboards/{int(time())}_leaderboard{projectid}.png'

        if type == "1":
            success, res = mattapi.getleaderboardbyid(projectid)
            if success:
                leaderboard.graph(fname, projectid, res)
            else:
                await ctx.send("Something went wrong!")
                return
        elif type == "2":
            await ctx.send("Not implemented yet!")
        await ctx.send(content=f"The current Leaderboard for Project: {projectid}", files=[discord.File(fname)])

    @cog_ext.cog_subcommand(base="microboinc", name="progress", options=[
        create_option(
            name="projectid",
            description="The ID from the project you want the progress for!",
            option_type=4,
            required=True
        )
    ])
    async def _microboinc_progress(self, ctx: SlashContext, projectid: int):
        success, res = mattapi.getprogressbyappid(projectid)

        if not success:
            await ctx.send("Something went wrong:\n" + res)
            return
        await ctx.send(content=f"The process of the Project: {res['Name']}\n"
                               f"{res['TotalDone']} / {res['TotalGenerated']} ({res['TotalDone'] / res['TotalGenerated'] * 100}%)")


def setup(bot):
    bot.add_cog(Microboinc(bot))
