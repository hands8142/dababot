import discord
import datetime
import warnings
import re
import requests
import bs4
import urllib
import aiohttp
import pokepy
import requests as rq
from discord.ext import commands
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
from urllib.request import HTTPError
from urllib.request import urlopen, Request

colour = discord.Colour.blue()


class util(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.CBSList = "http://m.safekorea.go.kr/idsiSFK/neo/ext/json/disasterDataList/disasterDataList.json"

    @commands.command(name="날씨")
    async def weather(self, ctx, *, location):
        embed = discord.Embed(
            title="날씨",
            colour=colour
        )
        Finallocation = location + '날씨'
        LocationInfo = ""
        NowTemp = ""
        CheckDust = []
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + Finallocation
        hdr = {
            'User-Agent': ('mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36')}
        req = requests.get(url, headers=hdr)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        ErrorCheck = soup.find('span', {'class': 'btn_select'})
        if 'None' in str(ErrorCheck):
            await ctx.send('검색 오류발생')
        else:
            for i in soup.select('span[class=btn_select]'):
                LocationInfo = i.text
                NowTemp = soup.find('span', {
                                    'class': 'todaytemp'}).text + soup.find('span', {'class': 'tempmark'}).text[2:]
                WeatherCast = soup.find('p', {'class': 'cast_txt'}).text
                TodayMorningTemp = soup.find('span', {'class': 'min'}).text
                TodayAfternoonTemp = soup.find('span', {'class': 'max'}).text
                TodayFeelTemp = soup.find(
                    'span', {'class': 'sensible'}).text[5:]
                CheckDust1 = soup.find('div', {'class': 'sub_info'})
                CheckDust2 = CheckDust1.find('div', {'class': 'detail_box'})
                for i in CheckDust2.select('dd'):
                    CheckDust.append(i.text)
                FineDust = CheckDust[0][:-2] + " " + CheckDust[0][-2:]
                UltraFineDust = CheckDust[1][:-2] + " " + CheckDust[1][-2:]
                Ozon = CheckDust[2][:-2] + " " + CheckDust[2][-2:]

                embed.add_field(
                    name="지역", value=f"{LocationInfo}", inline=True)
                embed.add_field(name="현재온도", value=f"{NowTemp}", inline=True)
                embed.add_field(
                    name="체감온도", value=f"{TodayFeelTemp}", inline=True)
                embed.add_field(name="정보", value=f"{WeatherCast}", inline=True)
                embed.add_field(
                    name="최저온도/최고온도", value=f"{TodayMorningTemp}/{TodayAfternoonTemp}", inline=True)
                embed.add_field(name="미세먼지", value=f"{FineDust}", inline=True)
                embed.add_field(
                    name="초미세먼지", value=f"{UltraFineDust}", inline=True)
                embed.add_field(name="오존 지수", value=f"{Ozon}", inline=True)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

    @commands.command(name="재난문자")
    async def get_cbs(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.CBSList) as r:
                data = await r.json()

        embed = discord.Embed(
            title="📢 재난문자",
            description="최근 발송된 3개의 재난문자를 보여줘요.",
            color=0xE71212
        )

        for i in data[:3]:
            embed.add_field(name=i["SJ"], value=i["CONT"], inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="포켓검색")
    async def sc(self, ctx, *, poke):
        pokemon = pokepy.V2Client().get_pokemon(str(poke))
        embed = discord.Embed(title=pokemon.name, colour=colour)
        embed.set_image(
            url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon.id}.png")
        embed.add_field(name="채력", value=str(
            pokemon.stats[0].base_stat), inline=True)
        embed.add_field(name="공격력", value=str(
            pokemon.stats[1].base_stat), inline=True)
        embed.add_field(name="방어력", value=str(
            pokemon.stats[2].base_stat), inline=True)
        embed.add_field(name="특수 공격", value=str(
            pokemon.stats[3].base_stat), inline=True)
        embed.add_field(name="특수 방어", value=str(
            pokemon.stats[4].base_stat), inline=True)
        embed.add_field(name="스피드", value=str(
            pokemon.stats[5].base_stat), inline=True)
        embed.add_field(name="타입", value=", ".join(
            ty.type.name for ty in pokemon.types), inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="멜론")
    async def music(self, ctx):
        embed = discord.Embed(
            title="노래순위",
            description="노래순위입니다.",
            colour=colour
        )
        targetSite = 'https://www.melon.com/chart/index.htm'
        header = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        melonrqRetry = rq.get(targetSite, headers=header)
        melonht = melonrqRetry.text
        melonsp = bs(melonht, 'html.parser')
        artists = melonsp.findAll('span', {'class': 'checkEllipsis'})
        titles = melonsp.findAll('div', {'class': 'ellipsis rank01'})
        for i in range(len(titles)):
            artist = artists[i].text.strip()
            title = titles[i].text.strip()
            embed.add_field(name="{0:3d}위".format(
                i + 1), value='{0} - {1}'.format(artist, title), inline=True)
            embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(util(client))
