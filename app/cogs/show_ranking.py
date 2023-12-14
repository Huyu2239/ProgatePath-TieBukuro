import datetime
from mylib import database, utils


import discord
from discord.ext import commands, tasks

from mylib.constant import RANKING_CHANNEL_ID


class ShowRanking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.message: discord.Message = None
        self.show_ranking.start()

    async def update(self):
        if self.channel is None:
            self.channel = self.bot.get_channel(RANKING_CHANNEL_ID)
        ranking_data = await database.fetch_monthly_top_users()
        embed = discord.Embed(
            title="月間質問回答時間上位10名",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(),
        )
        for rank, row in enumerate(ranking_data, 1):
            if row.monthly_time == 0:
                continue
            user = self.bot.get_user(row.user_id)
            hours, minutes, seconds = utils.seconds_to_duration(row.monthly_time)
            embed.add_field(name=f"{rank}位/{user.mention}", value=f"{hours}時間{minutes}分{seconds}秒", inline=False)
        embed.set_footer(text="毎月1日にリセットされます。")
        try:
            await self.message.edit(embed=embed)
        except Exception:
            self.message = await self.channel.send(embed=embed)

    @tasks.loop(time=datetime.time(hour=8, minute=0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))))
    async def show_ranking(self):
        if self.channel is None:
            self.channel = self.bot.get_channel(RANKING_CHANNEL_ID)
        now = datetime.datetime.now()
        now = now.replace(minute=now.minute, second=0, microsecond=0)
        # if now.day != 1:
        #     return
        ranking_data = await database.fetch_total_top_users()
        embeds = []
        embed = discord.Embed(
            title="全期間質問回答時間上位10名",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now(),
        )
        for rank, row in enumerate(ranking_data, 1):
            if row.total_time == 0:
                continue
            user = self.bot.get_user(row.user_id)
            hours, minutes, seconds = utils.seconds_to_duration(row.total_time)
            embed.add_field(name=f"{rank}位/{user.mention}", value=f"{hours}時間{minutes}分{seconds}秒", inline=False)
        embeds.append(embed)
        ranking_data = await database.fetch_monthly_top_users()
        embed = discord.Embed(
            title="月間質問回答時間上位10名",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now(),
        )
        for rank, row in enumerate(ranking_data, 1):
            if row.monthly_time == 0:
                continue
            user = self.bot.get_user(row.user_id)
            hours, minutes, seconds = utils.seconds_to_duration(row.monthly_time)
            embed.add_field(name=f"{rank}位/{user.mention}", value=f"{hours}時間{minutes}分{seconds}秒", inline=False)
        embeds.append(embed)
        await self.channel.send(f"{now.year}年{now.month}月の結果{now.minute}", embeds=embeds)
        await database.reset_monthly_time()
        embed = discord.Embed(
            title="月間質問回答時間上位10名",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(),
        )
        embed.set_footer(text="毎月1日にリセットされます。")
        try:
            await self.message.delete()
        except Exception:
            pass
        self.message = None

    @show_ranking.before_loop
    async def before_show_ranking(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(ShowRanking(bot))