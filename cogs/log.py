import discord
from discord.ext import commands
import datetime
import os
import pymysql

mydb = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    passwd=os.getenv('DB_PASSWD'),
    database=os.getenv('DB_DATABASE'),
)

colour = discord.Colour.blue()


class log(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cursor = mydb.cursor()

    async def get_channel(self, guild_id):
        self.cursor.execute(
            f"SELECT channel_id FROM logs WHERE guild_id = {str(guild_id)}")
        result = self.cursor.fetchall()
        if result is not ():
            if result[0][0] is not None:
                channel = self.client.get_channel(int(result[0][0]))
                if channel is not None:
                    return channel
                else:
                    return None
            else:
                return None
        else:
            return None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await log.get_channel(self, member.guild.id)
        if channel is not None:
            embed = discord.Embed(
                title="유저가 서버에 입장했습니다.", description=f"< 입장한 유저 : {member.mention}\n", timestamp=member.joined_at, color=colour)
            embed.set_thumbnail(url=member.avatar_url_as(
                static_format="png", size=2048))
            embed.set_footer(text="멤버 입장 이벤트")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await log.get_channel(self, member.guild.id)
        if channel is not None:
            roles = ""
            for role in member.roles:
                roles += f"{role.mention} "
            embed = discord.Embed(
                title="유저가 서버에서 나갔습니다.", description=f"< 퇴장한 유저 : {member.mention}\n< 가지고 있던 역할 {roles}", timestamp=member.joined_at, color=colour)
            embed.set_thumbnail(url=member.avatar_url_as(
                static_format="png", size=2048))
            embed.set_footer(text="멤버 퇴장 이벤트")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        channel = await log.get_channel(self, payload.guild_id)
        if channel is not None:
            if payload.cached_message is not None:
                msg = payload.cached_message
                if msg.author.bot:
                    return

                embed = discord.Embed(
                    title="메시지가 삭제되었습니다.", timestamp=datetime.datetime.now(), color=colour)
                embed.add_field(
                    name="메시지 주인", value=f"{msg.author.mention} ( {msg.author.id} )", inline=True)
                embed.add_field(
                    name="메시지가 삭제된 채널", value=f"{msg.channel.mention} ( {msg.channel.id} )", inline=True)
                embed.set_thumbnail(url=msg.author.avatar_url_as(
                    static_format="png", size=2048))
                embed.set_footer(text="메시지 삭제 이벤트")
                if msg.content == "" and msg.attachments:
                    embed.add_field(
                        name="메시지 내용", value="*내용이 없습니다. (싸늘한 바람)*", inline=True)
                    embed.add_field(
                        name="파일", value="파일이 아래 업로드되었습니다.", inline=True)
                    await channel.send(embed=embed)
                    await channel.send(files=msg.attachments)
                elif msg.content != "" and msg.attachments:
                    embed.add_field(
                        name="메시지 내용", value=msg.content, inline=True)
                    embed.add_field(
                        name="파일", value="파일이 아래 업로드되었습니다.", inline=True)
                    await channel.send(embed=embed)
                    await channel.send(files=msg.attachments)
                else:
                    embed.add_field(
                        name="메시지 내용", value=msg.content, inline=True)
                    embed.add_field(
                        name="파일", value="*파일이 없습니다. (싸늘한 바람)*", inline=True)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="메시지가 삭제되었습니다.", description="메시지가 캐싱되지 않아 내용 및 파일을 불러오지 못했습니다.", timestamp=datetime.datetime.now())
                embed.add_field(
                    name="메시지가 삭제된 채널", value=f"<#{payload.channel_id}> ( {payload.channel_id} )", inline=True)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot and after.author.bot:
            return

        channel = await log.get_channel(self, before.guild.id)
        if channel is not None:
            embed = discord.Embed(
                title="메시지가 수정되었습니다.", timestamp=datetime.datetime.now(), color=colour)
            embed.add_field(
                name="메시지 주인", value=f"{after.author.mention} ( {after.author.id} )", inline=True)
            embed.add_field(
                name="메시지가 수정된 채널", value=f"{after.channel.mention} ( {after.channel.id} )", inline=True)
            embed.add_field(
                name="메시지로 이동하기", value=f"[메시지 바로가기](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id})", inline=True)
            embed.add_field(name="메시지 수정 전 내용",
                            value=f"내용 : {before.content}", inline=True)
            embed.add_field(name="메시지 수정 후 내용",
                            value=f"내용 : {after.content}", inline=True)
            embed.set_thumbnail(url=after.author.avatar_url_as(
                static_format="png", size=2048))
            embed.set_footer(text="메시지 수정 이벤트")
            if before.pinned == True and after.pinned == False:
                embed.add_field(name="변경된 사항", value="메시지 고정이 해제됨")
            elif before.pinned == False and after.pinned == True:
                embed.add_field(name="변경된 사항", value="메시지가 고정됨")
            elif len(before.embeds) != len(after.embeds):
                embed.add_field(name="변경된 사항", value="임베드가 변경됨")
            await channel.send(embed=embed)

    @commands.command(name="로그설정")
    @commands.has_permissions(manage_guild=True)
    async def log_channel(self, ctx, *args):
        self.cursor.execute(
            f"SELECT channel_id FROM logs WHERE guild_id = {str(ctx.guild.id)}")
        result = self.cursor.fetchall()
        if result is ():
            self.cursor.execute(
                f"INSERT INTO logs VALUES({str(ctx.guild.id)}, NULL)")
            mydb.commit()
        if args[0] == "지우기":
            self.cursor.execute(
                f"UPDATE logs SET channel_id = NULL WHERE guild_id = {str(ctx.guild.id)}")
            mydb.commit()
            await ctx.send("로그채널을 지웠습니다.")
            return
        if args[0] == "확인":
            channel = await log.get_channel(self, ctx.guild.id)
            await ctx.send(f"지금 설정 되어 있는 채널은 {channel.mention}입니다.")
            return
        if args[0] == "변경":
            if not ctx.message.channel_mentions:
                await ctx.send("/로그설정 <변경, 지우기, 확인> <#채널>로 해주세요")
            else:
                channel = ctx.message.channel_mentions[0]
                self.cursor.execute(
                    f"UPDATE logs SET channel_id = {str(channel.id)} WHERE guild_id = {str(ctx.guild.id)}")
                mydb.commit()
                await ctx.send(f"{ctx.author.mention} 로그 채널을 {channel.mention} 채널로 설정했어요.")


def setup(client):
    client.add_cog(log(client))
