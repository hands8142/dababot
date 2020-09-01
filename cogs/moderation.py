import discord
import datetime
from discord.utils import get
from discord.ext import commands

colour = discord.Colour.blue()

class moderation(commands.Cog):

  def __init__(self, client):
    self.client = client

    
  @commands.command(name="청소")
  @commands.has_permissions(administrator=True)
  async def clear(self, ctx, number):
    number = int(number)
    if number >= 100 or number <= 0:
      embed = discord.Embed(colour=colour)
      embed.description = "1개부터 99개가지만 해주세요."
      embed.timestamp = datetime.datetime.utcnow()
      await ctx.send(embed=embed)
    else:
      await ctx.channel.purge(limit=number + 1)
      embed = discord.Embed(colour=colour)
      embed.description = f"{number}개를 삭제하였습니다."
      embed.timestamp = datetime.datetime.utcnow()
      await ctx.send(embed=embed)

  @commands.command(name="추방")
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(colour=colour)
    embed.description = f"{str(member)}을(를) 추방하였습니다"
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    
  @commands.command(name="밴")
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(colour=colour)
    embed.description = f"{str(member)}을(를) 밴시켰습니다."
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

  @commands.command(name="뮤트")
  @commands.has_permissions(administrator=True)
  async def mute(self, ctx, member: discord.Member = None):
    member = member or ctx.message.author
    await member.add_roles(get(ctx.guild.roles, name="Muted"))
    embed = discord.Embed(colour=colour)
    embed.description = f"{member.mention}를 뮤트 했습니다"
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

  @commands.command(name="언뮤트", pass_context=True)
  @commands.has_permissions(administrator=True)
  async def unmute(self, ctx, member: discord.Member = None):
    member = member or ctx.message.author
    await member.remove_roles(get(ctx.guild.roles, name='Muted'))
    embed = discord.Embed(colour=colour)
    embed.description = f"{member.mention}를 언뮤트 했습니다"
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)


  
def setup(client):
  client.add_cog(moderation(client))