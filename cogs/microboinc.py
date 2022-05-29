import discord
from time import time
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from config import config
from main import notauthorized
from utils import stats, leaderboard, microboincapi
from config.config import rootdir, apikeyselfcreationisallowed


class Microboinc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_createapikey, base="microboinc", name="createapikey", options=[
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
        if (user is None or user == ctx.author) and not apikeyselfcreationisallowed:
            await ctx.send("This feature is currently disabled!")
            return

        if user is not None and user != ctx.author:
            await ctx.send("Not implementet yet!")
            return
            if not microboincapi.isapilevelbyid(ctx.author_id, 2):
                await notauthorized(ctx)
                return
            apifor = user

        success, res = microboincapi.register(nickname, apifor.id)
        if not success:
            await ctx.send(res)
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

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_regenapikey, base="microboinc", name="regenapikey", options=[
        create_option(
            name="user",
            description="Only needed if you want to regen an API-Key for some one else!",
            option_type=6,
            required=False
        )
    ])
    async def _microboinc_regenapikey(self, ctx: SlashContext, user: discord.Member = None):
        await ctx.send("not available yet")
        return;
        apifor = ctx.author
        if user is not None and user != ctx.author:
            if not microboincapiold.isapilevelbyid(ctx.author_id, 4):
                await notauthorized(ctx)
                return
            apifor = user

        success, res = microboincapiold.regen(apifor.id)
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

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_deletebyid, base="microboinc", name="deletebyid", options=[
        create_option(
            name="user",
            description="The User you want to delete.",
            option_type=6,
            required=True
        )
    ])
    async def _microboinc_deletebyid(self, ctx: SlashContext, user: discord.Member):
        await ctx.send("not available yet")
        return
        if not microboincapiold.isapilevelbyid(ctx.author_id, 3):
            await notauthorized(ctx)
            return

        success, res = microboincapiold.deletebyid(user.id)

        if not success:
            await ctx.send("Something went wrong:\n" + res)
            return

        await ctx.send(content=f"User({user.mention}) has been deleted.")

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_results, base="microboinc", name="results", options=[
        create_option(
            name="appid",
            description="The appid form microboinc.",
            option_type=3,
            required=True
        )
    ])
    async def _microboinc_results(self, ctx: SlashContext, appid: int):

        #if not microboincapiold.isapilevelbyid(ctx.author_id, 1):
        #    await notauthorized(ctx)
        #    return

        m = await ctx.send("fetching data please wait a moment.")
        foname = f'{int(time())}_results{appid}.txt'
        fname = f'{rootdir}/results/{int(time())}_results{appid}.txt'
        suc, res = microboincapi.getresultsbyappid(appid)
        if not suc:
            await m.edit(content=f"Something went wrong: {res}")
            return
        with open(fname, "w") as f:
            f.write(res)

        await m.edit(content=f"Here are the results for app: {appid}\nhttps://results.microboinc.com/{foname}")

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_leaderboard, base="microboinc", name="leaderboard", options=[
        create_option(
            name="projectid",
            description="The ID from the project you want the leaderboard from!",
            option_type=4,
            required=True
        ), create_option(
            name="type",
            description="The type of chart you want!",
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
        fname = f'{rootdir}/leaderboards/{int(time())}_leaderboard-{projectid}.png'

        if type == "1":
            success, res = microboincapi.getleaderboardbyid(projectid)

            if not success:
                await ctx.send(res)
                return

            if not res["entries"]:
                await ctx.send("There is not data yet!")
                return

            leaderboard.graph(fname, projectid, res)

        elif type == "2":
            await ctx.send("Not implemented yet!")
            return
        await ctx.send(content=f"The current Leaderboard for Project: {projectid}", files=[discord.File(fname)])

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_userleaderboard, base="microboinc", name="userleaderboard", options=[
        create_option(
            name="projectid",
            description="The ID from the project you want the leaderboard from!",
            option_type=4,
            required=True
        ), create_option(
                name="user",
                description="The User you want the stats for.",
                option_type=6,
                required=True
            ), create_option(
            name="type",
            description="The type of chart you want!",
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
    async def _microboinc_userleaderboard(self, ctx: SlashContext, projectid: int, user: discord.User, type: str = "1"):
        fname = f'{rootdir}/leaderboards/{int(time())}_userleaderboard-{projectid}.png'
        if type == "1":
            success, res = microboincapi.getleaderboardbyidforuser(projectid, user.id)

            if not success:
                await ctx.send(res)
                return

            if not res["entries"]:
                await ctx.send("There is not data yet!")
                return

            leaderboard.graph(fname, projectid, res)

        elif type == "2":
            await ctx.send("Not implemented yet!")
            return
        await ctx.send(content=f"The current Leaderboard from {user.mention} for Project: {projectid}", files=[discord.File(fname)])

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_progress, base="microboinc", name="progress", options=[
        create_option(
            name="projectid",
            description="The ID from the project you want the progress for.",
            option_type=4,
            required=True
        )
    ])
    async def _microboinc_progress(self, ctx: SlashContext, projectid: int):
        await ctx.send("not available yet")
        return;
        success, res = microboincapiold.getprogressbyappid(projectid)

        if not success:
            await ctx.send("Something went wrong:\n" + res)
            return

        await ctx.send(content=f"The process of the Project: {res['Name']}\n"
                               f"{res['TotalDone']} / {res['TotalGenerated']} ({(res['TotalDone'] / res['TotalGenerated'] * 100) if res['TotalGenerated'] != 0 else 0}%)")

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_stats_multipoints, base="microboinc", name="stats-multipoints",
                            options=[
                                create_option(
                                    name="projectid",
                                    description="The ID of the project you want the stats for.",
                                    option_type=4,
                                    required=True
                                )
                            ])
    async def _microboinc_stats_multipoints(self, ctx: SlashContext, projectid: int):
        fname = f'{rootdir}/stats/{int(time())}_stats-multipoints-{projectid}.png'
        m = await ctx.send("Please wait a moment, it can take a while to generate the Image.")
        success, res = microboincapi.gethistleaderboardbyid(projectid)

        if not success:
            await m.edit(content=res)
            return

        if not res["entries"]:
            await m.edit(content="There is not data yet!")
            return

        stats.multipoints(fname, projectid, res)
        await m.edit(content=f"Total points stats for Project: {projectid}", files=[discord.File(fname)])

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_stats_singlepoints, base="microboinc", name="stats-singlepoints",
                            options=[
                                create_option(
                                    name="projectid",
                                    description="The ID of the project you want the stats for.",
                                    option_type=4,
                                    required=True
                                ), create_option(
                                    name="user",
                                    description="The User you want the stats for.",
                                    option_type=6,
                                    required=True
                                )
                            ])
    async def _microboinc_stats_singlepoints(self, ctx: SlashContext, projectid: int, user: discord.User):
        m = await ctx.send("Please wait a moment, it can take a while to generate the Image.")
        userid = user.id

        fname = f'{rootdir}/stats/{int(time())}_stats-singlepoints-{projectid}-{userid}.png'

        success, res = microboincapi.gethistleaderboardbyid(projectid)
        if not success:
            await m.edit(content="Something went wrong!")
            return

        stats.singlepoints(fname, projectid, userid, res)
        await m.edit(content=f"Single points stats from: {user.mention} Project: {projectid}",
                     files=[discord.File(fname)])

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_stats_totalpoints, base="microboinc", name="stats-totalpoints",
                            options=[
                                create_option(
                                    name="projectid",
                                    description="The ID of the project you want the stats for.",
                                    option_type=4,
                                    required=True
                                )
                            ])
    async def _microboinc_stats_totalpoints(self, ctx: SlashContext, projectid: int):
        fname = f'{rootdir}/stats/{int(time())}_stats-totalpoints-{projectid}.png'
        m = await ctx.send("Please wait a moment, it can take up to a minute to generate the Image.")
        success, res = microboincapi.gethistleaderboardbyid(projectid)

        if not success:
            await m.edit(content="Something went wrong!")
            return

        stats.totalpoints(fname, projectid, res)

        await m.edit(content=f"Total points from Project: {projectid}", files=[discord.File(fname)])

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_stats_totalhourlypoints, base="microboinc",
                            name="stats-totalhourlypoints", options=[
            create_option(
                name="projectid",
                description="The ID of the project you want the stats for.",
                option_type=4,
                required=True
            )
        ])
    async def _microboinc_stats_totalhourlypoints(self, ctx: SlashContext, projectid: int):
        fname = f'{rootdir}/stats/{int(time())}_stats-totalhourlypoints-{projectid}.png'
        m = await ctx.send("Please wait a moment, it can take up to a minute to generate the Image.")
        success, res = microboincapi.gethistleaderboardbyid(projectid)
        if success:
            stats.totalhourlypoints(fname, projectid, res)
        else:
            await m.edit(content="Something went wrong!")
            return

        await m.edit(content=f"Totalhourlypoins stats from Project: {projectid}", files=[discord.File(fname)])

    @cog_ext.cog_subcommand(guild_ids=config.slash_mb_stats_singlehourlypoints, base="microboinc",
                            name="stats-singlehourlypoints", options=[
            create_option(
                name="projectid",
                description="The ID of the project you want the stats for.",
                option_type=4,
                required=True
            ), create_option(
                name="user",
                description="The User you want the stats for.",
                option_type=6,
                required=True
            ), create_option(
                name="internaluseridoverride",
                description="The internal ID from the user(overrides the discord user)",
                option_type=4,
                required=False
            )
        ])
    async def _microboinc_stats_singlehourlypoints(self, ctx: SlashContext, projectid: int, user: discord.User,
                                                   internaluseridoverride: int = None):
        await ctx.send("not available yet")
        return;
        m = await ctx.send("Please wait a moment, it can take up to a minute to generate the Image.")

        userid = internaluseridoverride
        username = f"OVERRIDE-{userid}"
        if internaluseridoverride is None:
            uisuc, uires = microboincapiold.getuserinfobyid(user.id)
            if not uisuc:
                await m.edit(content=f"User not found: {user.name}({user.id})")
                return
            userid = uires["User"]["ID"]
            username = uires["User"]["Username"]

        fname = f'{rootdir}/stats/{int(time())}_stats-singlehourlypoints-{projectid}-{userid}.png'

        success, res = microboincapiold.gethistleaderboardbyid(projectid)
        if success:
            stats.singlehourlypoints(fname, projectid, userid, username, res)
        else:
            await m.edit(content="Something went wrong!")
            return

        await m.edit(content=f"Singlehourlypoints stats from: {username} Project: {projectid}",
                     files=[discord.File(fname)])


def setup(bot):
    bot.add_cog(Microboinc(bot))
