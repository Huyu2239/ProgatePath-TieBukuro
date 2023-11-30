import datetime
import math

from discord.ext import commands

from mylib import database


class CountTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time_dict = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        if before.channel == after.channel:
            return
        if after.channel is not None:
            await self.on_member_join_voice_channel(member, before, after)
        if before.channel is not None:
            await self.on_member_leave_voice_channel(member, before, after)

    async def on_member_join_voice_channel(self, member, before, after):
        if after.channel.id not in self.bot.room_owner_dict.keys():
            return
        if member.id == self.bot.room_owner_dict.get(after.channel.id):
            return
        self.start_time_dict[member.id] = datetime.datetime.now()

    async def on_member_leave_voice_channel(self, member, before, after):
        if member.id == self.bot.room_owner_dict.get(before.channel.id):
            return
        if member.id not in self.start_time_dict.keys():
            return 
        start_time = self.start_time_dict[member.id]
        end_time = datetime.datetime.now()
        lecture_time = end_time - start_time
        user = await database.fetch_user(user_id=member.id)
        if user is None:
            await database.insert_user(user_id=member.id)
            user = await database.fetch_user(user_id=member.id)
            if user is None:
                return
        user.total_time += math.ceil(lecture_time.total_seconds())
        await database.update_user(user)

async def setup(bot):
    await bot.add_cog(CountTime(bot))
