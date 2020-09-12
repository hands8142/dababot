import discord
import datetime
import sys
from discord.utils import get
from discord.ext import commands

colour = discord.Colour.blue()

class info(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(name="핑", pass_context=True)
  async def ping(self, ctx):
    latency = round(self.client.latency * 1000)
    embed = discord.Embed(title="핑(ms)", colour=colour)
    embed.description = f"{latency}ms"
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

  @commands.command(name="내정보", pass_context=True)
  async def information(self, ctx):
    date = datetime.datetime.utcfromtimestamp(((int(ctx.author.id) >> 22) + 1420070400000) / 1000)
    embed = discord.Embed(color=colour)
    embed.add_field(name="이름", value=ctx.author.name, inline=True)
    embed.add_field(name="서버닉네임", value=ctx.author.display_name, inline=True)
    embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일", inline=True)
    embed.add_field(name="아이디", value=ctx.author.id, inline=True)
    embed.add_field(name="역할", value=' '.join([r.mention for r in ctx.author.roles]))
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

  @commands.command(name="서버정보", pass_context=True)
  async def serverinformation(self, ctx):
    embed = discord.Embed(colour=colour)
    embed.add_field(name="서버 이름", value=ctx.guild.name, inline=True)
    embed.add_field(name="서버 아이디", value=ctx.guild.id, inline=True)
    embed.add_field(name="서버 지역", value=str(ctx.guild.region).title(), inline=True)
    embed.add_field(name="서버 주인", value=ctx.guild.owner.display_name, inline=True)
    embed.add_field(name="서버 만들어진 날짜", value=ctx.guild.created_at.strftime("%y/%m/%d %H:%M:%S"), inline=True)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

  @commands.command(name="봇정보", pass_context=True)
  async def botinformation(self, ctx):
    guilds_count = len(self.client.guilds)
    members_count = 0
    for guild in self.client.guilds:
      members_count += len(guild.members)
    embed = discord.Embed(colour=colour)
    embed.set_image(url=self.client.user.avatar_url)
    embed.add_field(name="discord.py", value=discord.__version__, inline=True)
    embed.add_field(name="python", value=sys.version[:5], inline=True)
    embed.add_field(name="bot", value="1.0.1", inline=True)
    embed.add_field(name="user", value=members_count, inline=True)
    embed.add_field(name="server", value=guilds_count, inline=True)
    embed.add_field(name="creator", value="한동준#7865")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

  @commands.command(name="도움말", pass_context=True)
  async def ehdnaakf(self, ctx):
    embed = discord.Embed(colour=colour)
    embed.description = "https://dongz.ml/discord/discord-dababot/"
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)


def setup(client):
  client.add_cog(info(client))
