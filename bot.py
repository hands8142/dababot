import discord
import datetime
import os
import dotenv
from dotenv import load_dotenv
from discord.ext import commands, tasks
from itertools import cycle

load_dotenv()

owner = 683515568137175050

status = cycle([f'/도움', 'test중'])

client = commands.Bot(command_prefix="/")
client.remove_command('help')

@client.command(name="로드")
async def load(ctx, extension):
    if not ctx.author.id == int(owner):
        return
    else:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f":white_check_mark: {extension}을(를) 로드했습니다!")

@client.command(name="언로드")
async def unload(ctx, extension):
    if not ctx.author.id == int(owner):
        return
    else:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f":white_check_mark: {extension}을(를) 언로드했습니다!")

@client.command(name="리로드")
async def reload_commands(ctx, extension=None):
    if not ctx.author.id == int(owner):
        return
    else:
        if extension is None: # extension이 None이면 (그냥 !리로드 라고 썼을 때)
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    client.unload_extension(f"cogs.{filename[:-3]}")
                    client.load_extension(f"cogs.{filename[:-3]}")
                    await ctx.send(":white_check_mark: 모든 명령어를 다시 불러왔습니다!")
        else:
            client.unload_extension(f"cogs.{extension}")
            client.load_extension(f"cogs.{extension}")
            await ctx.send(f":white_check_mark: {extension}을(를) 다시 불러왔습니다!")


for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print('Discord.py 버전 : ' + discord.__version__)
    print("bot starting..")#봇 시작이라고 뜨게하기
    print("==========")
    guilds_count = len(client.guilds)
    members_count = 0

    for guild in client.guilds:
        members_count += len(guild.members)
    print("서버 수: " + str(guilds_count))
    print("멤버 수: " + str(members_count))
    change_status.start()

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("값이 없네요.")
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(colour=colour)
        embed.description = f"{ctx.message.author}님, 당신은 이 명령을 실행하실 권한이 없습니다."
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))



client.run(os.getenv('TOKEN'))