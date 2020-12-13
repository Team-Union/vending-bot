import json
import os

import discord
from discord import HTTPException
from discord.ext import commands, tasks
from discord.ext.commands import errors
import hashlib

with open("db.json", "r", encoding="utf-8") as f:
    jpgtb = json.load(f)

with open("servers.json", "r", encoding="utf-8") as f:
    sc = json.load(f)

bot = commands.Bot(command_prefix="!자판기 ")
bot.remove_command('help')

# configuration
version = "1.2.0b"
try:
    from os import getenv

    token = getenv('Token')
    if not token:
        raise RuntimeError('토큰 없음')
except:
    token = "Nzg3MTk1MDc5MzE1MjkyMTkx.X9RajA.BGXpC5T5uaptVTmo1jTeN8IvEII"

h = hashlib.sha512()

# changelog
changelog = """
Added: \"상품수정\",
Alpha sign-off (v1.0.0)

Hotfix (v1.0.1)

Fixed: \"상품수정\" (v1.0.2)

Added: \"공지\", \"공지설정\" (v1.1.0)

Fixed: \"상품등록\" (v1.1.1)

Added: \"Auto-Updater\" (v1.2.0)

Deprecated: \"Auto-Updater\"
Added: Koreanbots server count updater (v1.2.0b)
"""
client = bot


@tasks.loop(minutes=20)
async def check_update():
    os.system("rm -rf /home/shs3182ym_gmail_com/vending-bot-update-checker")
    os.system("git clone https://github.com/TeamEnd/vending-bot.git "
              "/home/shs3182ym_gmail_com/vending-bot-update-checker")
    h.update(bytes(open("main.py", "r").read().encode('utf-8')))
    t = h.hexdigest()
    print(t)
    h.update(bytes(open("/home/shs3182ym_gmail_com/vending-bot-update-checker/main.py", "r").read().encode('utf-8')))
    g = h.hexdigest()
    print(g)
    if t != g:
        em = discord.Embed(
            title="업데이트",
            description="업데이트가 자동으로 진행됩니다. 잠시 봇 작동이 중지됩니다.",
            color=0x00FF00,
        )
        for i in bot.guilds:
            try:
                if int(sc[str(i.id)]["notice-channel"]) != 0:
                    await i.get_channel(int(sc[str(i.id)]["notice-channel"])).send(embed=em)
            except KeyError:
                pass
        print(1)
        os.system("sudo cp /home/shs3182ym_gmail_com/vending-bot-update-checker/main.py "
                  "/home/shs3182ym_gmail_com/japangibot/vending-bot/ -f")
        os.system("python3 main.py")
        exit(0)


@tasks.loop(minutes=10)
async def servers():
    from requests import post
    BASEURL = "https://api.koreanbots.dev"
    stoke = os.getenv("kbtoken")
    serverCount = len(bot.guilds)  # 서버 수

    response = post(f'{BASEURL}/bots/servers', headers={"token": stoke, "Content-Type": "application/json"},
                    json={"servers": serverCount})
    print(response.json())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})\nVersion = {version}\n-------------------")
    # check_update.start()
    servers.start()
    gozas = []
    for i in bot.guilds:
        for j in i:
            gozas += j.url
    t = "\n"
    print(f"Servers = {len(bot.guilds)}\nServer Links = {t.join(gozas)}")


@bot.event
async def on_command(ctx):
    try:
        jpgtb[str(ctx.guild.id)]
    except KeyError:
        jpgtb[str(ctx.guild.id)] = [[{
            "index": "1",
            "name": "등록된 상품 없음",
            "price": "등록된 가격 없음",
            "description": "등록된 설명 없음",
        }]]
    except HTTPException as e:
        jpgtb[str(ctx.guild.id)] = [[{
            "index": "1",
            "name": "등록된 상품 없음",
            "price": "등록된 가격 없음",
            "description": "등록된 설명 없음",
        }]]


@bot.after_invoke
async def after(ctx):
    with open("db.json", "w", encoding="utf-8") as f:
        json.dump(jpgtb, f, indent=4)
    with open("servers.json", "w", encoding="utf-8") as f:
        json.dump(sc, f, indent=4)


@bot.command()
async def 패치(ctx, ver: str = version):
    goza = changelog.split("\n\n")
    shanghaijo = "해당 버전의 내용 없음"
    for i in goza:
        if i.endswith(f"(v{ver})"):
            shanghaijo = i
    em = discord.Embed(
        title=f"자판기봇 업데이트 내역",
        description="",
        color=0x00FF00,
    )
    em.add_field(name=ver, value=shanghaijo)
    await ctx.send(embed=em)


@bot.command()
async def 공지(ctx, title, desc):
    em = discord.Embed(
        title=title,
        description=desc,
        color=0x00FF00,
    )
    for i in bot.guilds:
        try:
            if int(sc[str(i.id)]["notice-channel"]) != 0:
                await i.get_channel(int(sc[str(i.id)]["notice-channel"])).send(embed=em)
        except KeyError:
            try:
                sc[str(i.id)]["notice-channel"] = "0"
            except KeyError:
                sc[str(i.id)] = {
                    "notice-channel": "0"
                }
            em2 = discord.Embed(
                title="오류 - 공지 채널 미설정",
                description=f"{i.name} 서버의 공지 채널 설정이 되지 않음",
                color=0xFF00 << 8,
            )
            await ctx.send(embed=em2)


@bot.command()
@commands.has_permissions(administrator=True)
async def 공지설정(ctx, id: str = None):
    if id is None:
        id = ctx.channel.id
    try:
        sc[str(ctx.guild.id)]["notice-channel"] = id
    except KeyError:
        sc[str(ctx.guild.id)] = {
            "notice-channel": id
        }
    finally:
        em = discord.Embed(
            title="성공 - 공지 채널 설정",
            description="공지 채널이 설정되었습니다.",
            color=0x00FF00,
        )
        await ctx.send(embed=em)


@bot.command()
async def hellothisisverification(ctx):
    await ctx.send("! Tim23#9999(674813875291422720) Deleted User 00000000#2214(723354571115724805)")


@bot.command()
async def 상품보기(ctx, pid: int = 1):
    if True:
        sjt = []
        try:
            sjt = jpgtb[str(ctx.guild.id)]
        except KeyError:
            sjt = [[{
                "index": "1",
                "name": "등록된 상품 없음",
                "price": "등록된 가격 없음",
                "description": "등록된 설명 없음",
            }]]
        sjtl = len(sjt)
        if pid > sjtl:
            pid = sjtl
        lsd = sjt[pid - 1]
        em = discord.Embed(
            title=f"전체 품목 중 {pid} 페이지 ({15 * (pid - 1) + 1} - {15 * (pid - 1) + len(lsd)})",
            description="성공 - 상품 목록 보기",
            color=0x00FF00,
        )
        efo = []
        [efo.append(x["index"]) for x in lsd]
        eos = "\n".join(efo)
        efn = []
        [efn.append(x["name"]) for x in lsd]
        ens = "\n".join(efn)
        efp = []
        [efp.append(x["price"]) for x in lsd]
        eps = "\n".join(efp)
        if eos == "" or ens == "" or eps == "":
            eos, ens, eps = ("1", "물건 없음", "물건이 없습니다.")
        em.add_field(name="물건 번호", value=eos, inline=True)
        em.add_field(name="물건 이름", value=ens, inline=True)
        em.add_field(name="물건 가격", value=eps, inline=True)
        em.set_footer(text=f"Vending Bot {version}")
        await ctx.send(embed=em)


@bot.command(aliases=("help",))
async def 도움(ctx):
    em = discord.Embed(
        title=f"자판기봇 도움말",
        description="",
        color=0x00FF00,
    )
    eos = """
    !자판기 상품보기 (페이지)
    !자판기 상품설명 번호
    !자판기 상품등록 이름 가격 설명
    !자판기 상품삭제 번호
    !자판기 상품수정 번호 속성 값
    !자판기 공지설정 (채널ID)
    """
    ens = """
    (페이지)번째 페이지의 상품 목록을 봅니다.
    번호에 해당하는 상품의 설명을 봅니다.
    이름, 가격, 설명을 가진 상품을 등록합니다.
    번호에 해당하는 상품을 삭제합니다.
    번호에 해당하는 상품을 수정합니다.
    """
    em.add_field(name="명령어", value=eos, inline=True)
    em.add_field(name="설명", value=ens, inline=True)
    em.add_field(name="개발자", value="! Tim23#9999, \nDeleted User 00000000#2214",
                 inline=False)
    em.set_footer(text=f"Vending Bot {version}")
    await ctx.send(embed=em)


@bot.command()
async def 상품설명(ctx, n: int = 1):
    try:
        sjt = jpgtb[str(ctx.guild.id)]
        f = []
        for i in sjt:
            for j in i:
                f.append(j)
        if len(f) < n:
            n = len(f)
        elif n < 1:
            n = 1
        if not f:
            f = [{
                "index": str(len(f) + 1),
                "name": "등록된 상품 없음",
                "price": "등록된 가격 없음",
                "description": "등록된 설명 없음",
            }]
        k = f[n - 1]
        em = discord.Embed(title=f"{n}번 상품의 설명", description="", color=0x00FF00)
        em.add_field(name=k["name"], value=k["description"], inline=True)
        em.set_footer(text=f"Vending Bot {version}")
        await ctx.send(embed=em)
    except KeyError:
        k = {
            "index": "1",
            "name": "등록된 상품 없음",
            "price": "등록된 가격 없음",
            "description": "등록된 설명 없음",
        }
        em = discord.Embed(title=f"{1}번 상품의 설명", description="", color=0x00FF00)
        em.add_field(name=k["name"], value=k["description"], inline=True)
        em.set_footer(text=f"Vending Bot {version}")
        await ctx.send(embed=em)


@bot.command()
@commands.has_permissions(administrator=True)
async def 상품등록(ctx, name, price, *, description):
    sjt = jpgtb[str(ctx.guild.id)]
    f = []
    for i in sjt:
        for j in i:
            f.append(j)
    goza = {
        "index": str(len(f) + 1),
        "name": name,
        "price": price,
        "description": description,
    }
    print(str(int(len(f) / 15)))
    var = []
    try:
        var = sjt[int(len(f) / 15)]
    except IndexError:
        sjt.append([])
        var = sjt[int(len(f) / 15)]
    var.append(goza)
    jpgtb[str(ctx.guild.id)][int(len(f) / 15)] += goza
    em = discord.Embed(title=f"{name}(이)가 생성됨", description="", color=0x00FF00)
    em.add_field(name="물건 번호", value=str(len(f) + 1), inline=True)
    em.add_field(name="물건 이름", value=name, inline=True)
    em.add_field(name="물건 가격", value=price, inline=True)
    em.set_footer(text=f"Vending Bot {version}")
    await ctx.send(embed=em)


@bot.command()
@commands.has_permissions(administrator=True)
async def 상품삭제(ctx, v: int):
    sjt = jpgtb[str(ctx.guild.id)]
    var = sjt[int((v % 15) - 1)]
    print(str((v - int(v / 15) * 15)))
    print(str(var))
    del var[(v - (int(v / 15) * 15)) - 1]
    del jpgtb[str(ctx.guild.id)][int(v / 15)][int((v % 15) - 1)]
    em = discord.Embed(title=f"{v}번 물건이 삭제됨", description="삭제가 완료되었습니다.", color=0xFF00)
    em.set_footer(text=f"Vending Bot {version}")
    await ctx.send(embed=em)


@bot.command()
async def 상품수정(ctx, v: int = 1, property: str = None, value: str = None):
    if property is None or value is None:
        em = discord.Embed(title="오류", description="입력한 값 중 하나가 없거나 올바르지 않습니다!", color=0xFF0000)
        em.set_footer(text=f"Vending Bot {version}")
        return await ctx.send(embed=em)

    properties = {
        "이름": "name",
        "가격": "price",
        "설명": "description"
    }

    if property not in properties:
        em = discord.Embed(title="오류", description="수정할 속성이 올바르지 않습니다!", color=0xFF0000)
        em.add_field(name="가능한 속성", value="이름\n가격\n설명")
        em.set_footer(text=f"Vending Bot {version}")
        return await ctx.send(embed=em)

    property = properties[property]

    jpgtb[str(ctx.guild.id)][int(v / 15)][int((v % 15) - 1)][property] = value
    name, price = jpgtb[str(ctx.guild.id)][int(v / 15)][int((v % 15) - 1)]["name"], \
                  jpgtb[str(ctx.guild.id)][int(v / 15)][int((v % 15) - 1)]["price"]
    em = discord.Embed(title=f"{name}(이)가 수정됨", description="", color=0x00FF00)
    em.add_field(name="물건 번호", value=str(v), inline=True)
    em.add_field(name="물건 이름", value=name, inline=True)
    em.add_field(name="물건 가격", value=price, inline=True)
    em.set_footer(text=f"Vending Bot {version}")
    await ctx.send(embed=em)


@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.errors.MissingPermissions):
        em = discord.Embed(title="오류 : ", description="당신은 이 커맨드를 사용할 권한이 없습니다!", color=0xFF0000)
        em.set_footer(text=f"Vending Bot {version}")
        return await ctx.send(embed=em)

    elif isinstance(err, errors.CommandNotFound):
        return

    raise err


bot.run(token)