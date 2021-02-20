import discord
from discord.ext import commands, tasks
import json
import random

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!prefix', intents=intents)
bot.remove_command(name="help")

with open("db.json", "r", encoding="utf-8") as f:
    ads = json.load(f)

with open("servers.json", "r", encoding="utf-8") as f:
    sc = json.load(f)

# configuration
version = "2"
try:
    from os import getenv

    token = getenv('Token')
    if not token:
        raise RuntimeError('토큰 없음')
except:
    token = "token"

# changelog
changelog = """
"""


@bot.after_invoke
async def after(ctx):
    with open("db.json", "w", encoding="utf-8") as f:
        json.dump(ads, f, indent=4)
    with open("servers.json", "w", encoding="utf-8") as f:
        json.dump(sc, f, indent=4)


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    for i in bot.guilds:
        for j in await i.invites():
            print(f"{j} - {i.name}")


def embed(title, desc, color, fields=None):
    em = discord.Embed(title=title, description=desc, color=color)
    if fields is not None:
        for i in fields.keys():
            if type(fields[i]) == str:
                em.add_field(name=i, value=fields[i], inline=True)
            elif type(fields[i]) == list:
                em.add_field(name=i, value="\n".join(fields[i]), inline=True)
            else:
                em.add_field(name=i, value=str(fields[i]), inline=True)
    return em


@bot.command()
async def 도움(ctx):
    await ctx.send(embed=embed("도움말", "", 0xFF00, {
        "명령어": [
            '광고등록 링크 설명',
            '설명등록 색 제목 설명'
        ],
        "설명": [
            "",
            "색은 컬러 코드를 10진수로 써주세요"
        ]
    }))


@bot.command()
async def 광고등록(ctx, link: str = None, msg: str = None):
    if link is not None and msg is not None:
        ads[ctx.guild.id] = {
            "name": ctx.guild.name,
            "link": link,
            "msg": msg
        }
        await ctx.send(embed=embed("성공", "광고글이 등록되었습니다", 0xff00, {
            "입력한 인자들": [
                f"link = {link}",
                f"msg = {msg}"
            ]
        }))
    else:
        await ctx.send(embed=embed("오류", "명령어 인자가 올바르지 않습니다", 0xff0000, {
            "입력한 인자들": [
                f"link = {link}",
                f"msg = {msg}"
            ]
        }))


@bot.command()
async def 설명등록(ctx, color: int = 000000, title: str = None, msg: str = None):
    if title is not None and msg is not None:
        sc[str(ctx.guild.id)] = {
            "join-msg": {
                "title": title,
                "color": color,
                "desc": msg
            }
        }
        await ctx.send(embed=embed("성공", "설명이 등록되었습니다", 0xff00, {
            "입력한 인자들": [
                f"color = {color}",
                f"title = {title}",
                f"msg = {msg}"
            ]
        }))
    else:
        await ctx.send(embed=embed("오류", "명령어 인자가 올바르지 않습니다", 0xff0000, {
            "입력한 인자들": [
                f"color = {color}",
                f"title = {title}",
                f"msg = {msg}"
            ]
        }))


@bot.event
async def on_member_join(member):
    m = member
    try:
        shanghai = sc[str(m.guild.id)]["join-msg"]
    except KeyError:
        shanghai = {
            "title": "환영합니다",
            "color": 0xff00,
            "desc": "서버에서 설정한 환영 메시지가 없습니다."
        }
        sc[str(m.guild.id)] = {
            "join-msg": shanghai
        }
    title = shanghai["title"]
    color = shanghai["color"]
    desc = shanghai["desc"]
    adk = ads.keys()
    print(len(adk))
    print(ads)
    ad = ads[list(adk)[random.randint(0, len(adk) - 1)]]
    e = embed(title=title, color=color, desc=desc)
    e.add_field(name=f"광고 - {ad['name']}", value=f"{ad['msg']}\n\n{ad['link']}")
    await m.send(embed=e)


bot.run(token)
