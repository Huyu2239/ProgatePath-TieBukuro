import asyncio

from discord.ext import commands

from mylib.constant import AUTO_CREATE_CHANNEL_ID


class RoomManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    async def on_member_join_voice_channel(self, member, _, after):
        if after.channel.id != AUTO_CREATE_CHANNEL_ID:
            return      
        auto_create_channel = after.channel
        if auto_create_channel.category is None:
            return
        room = await auto_create_channel.category.create_voice_channel(
            name=f"│{member.display_name}の質問部屋"
        )
        await member.move_to(room)
        self.bot.room_owner_dict[room.id] = member.id

    async def on_member_leave_voice_channel(self, member, before, _):
        if member.id != self.bot.room_owner_dict.get(before.channel.id):
            return
        def exit_check(__, _before, ___):
            return _before.channel.id ==  before.channel.id and len([member for member in _before.channel.members if member.bot is False]) == 0
        
        if len(before.channel.members) > 0:
            try:
                await self.bot.wait_for("voice_state_update", timeout=30, check=exit_check)
            except asyncio.TimeoutError:
                pass
        await before.channel.delete()
        del self.bot.room_owner_dict[before.channel.id]


async def setup(bot):
    await bot.add_cog(RoomManager(bot))
