import json

import discord
from discord import HTTPException
from discord.ext import commands

with open("table.json", "r", encoding="utf-8") as f:
    jpgtb = json.load(f)

bot = commands.Bot(command_prefix="!자판기 ")


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.event
async def on_command(ctx):
    try:
        jpgtb[str(ctx.guild.id)]
    except KeyError:
        jpgtb[str(ctx.guild.id)] = [[]]
    except HTTPException:
        sjt = []
        try:
            sjt = jpgtb[str(ctx.guild.id)]
        except KeyError:
            sjt = [[]]
        f = []
        for i in sjt:
            for j in i:
                f.append(j)
        goza = {
            "index": str(len(f) + 1),
            "name": "등록된 물건 없음",
            "price": "2147483647",
            "description": "Wild MISSINGNO. appeared!",
        }
        var = []
        try:
            var = sjt[int(len(f) / 15)]
        except IndexError:
            sjt.append([])
            var = sjt[int(len(f) / 15)]
        var.append(goza)


@bot.after_invoke
async def after(ctx):
    with open("table.json", "w") as f:
        json.dump(jpgtb, f, indent=4)


@bot.command()
async def hellothisisverification(ctx):
    await ctx.send("! Tim23#9999(674813875291422720) Deleted User 00000000#2214(723354571115724805)")


@bot.command()
async def 물건보기(ctx, pid: int = None):
    if pid is not None:
        sjt = []
        try:
            sjt = jpgtb[str(ctx.guild.id)]
        except KeyError:
            sjt = [[]]
        sjtl = len(sjt)
        if pid > sjtl:
            pid = sjtl
        lsd = sjt[pid - 1]
        em = discord.Embed(
            title=f"전체 품목 중 {pid} 페이지 ({15 * (pid - 1) + 1} - {15 * (pid - 1) + len(lsd)})",
            description="성공 - 물건 목록 보기",
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
        em.add_field(name="물건 번호", value=eos, inline=True)
        em.add_field(name="물건 이름", value=ens, inline=True)
        em.add_field(name="물건 가격", value=eps, inline=True)
        em.set_footer(text="Vending Bot v0.1.3")
        await ctx.send(embed=em)
    else:
        sjt = []
        try:
            sjt = jpgtb[str(ctx.guild.id)]
        except KeyError:
            sjt = [[]]
        sjtl = len(sjt)
        pid = 1
        if pid > sjtl:
            pid = sjtl
        lsd = sjt[pid - 1]
        em = discord.Embed(
            title=f"전체 품목 중 1 페이지 (1 - {15 * (pid - 1) + len(lsd)})",
            description="성공 - 물건 목록 보기",
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
        em.add_field(name="물건 번호", value=eos, inline=True)
        em.add_field(name="물건 이름", value=ens, inline=True)
        em.add_field(name="물건 가격", value=eps, inline=True)
        em.set_footer(text="Vending Bot v0.1.3")
        await ctx.send(embed=em)


@bot.command()
async def 도움(ctx):
    em = discord.Embed(
        title=f"자판기봇 도움말",
        description="",
        color=0x00FF00,
    )
    eos = """
    !자판기 물건보기 (페이지)
    !자판기 물건설명 번호
    !자판기 물건등록 이름 가격 설명
    !자판기 물건삭제 번호
    """
    ens = """
    (페이지)번째 페이지의 물건 목록을 봅니다.
    번호에 해당하는 물건의 설명을 봅니다.
    이름, 가격, 설명을 가진 물건을 등록합니다.
    번호에 해당하는 물건을 삭제합니다.
    """
    em.add_field(name="명령어", value=eos, inline=True)
    em.add_field(name="설명", value=ens, inline=True)
    em.add_field(name="개발자", value="! Tim23#9999, \nDeleted User 00000000#2214",
                 inline=False)
    em.set_footer(text="Vending Bot v0.1.3")
    await ctx.send(embed=em)


@bot.command()
async def 물건설명(ctx, n: int):
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
            "name": "등록된 물건 없음",
            "price": "2147483647",
            "description": "Wild MISSINGNO. appeared!",
        }]
    k = f[n - 1]
    em = discord.Embed(title=f"{n}번 물건의 설명", description="", color=0x00FF00)
    em.add_field(name=k["name"], value=k["description"], inline=True)
    em.set_footer(text="Vending Bot v0.1.3")
    await ctx.send(embed=em)


@bot.command()
@commands.has_permissions(administrator=True)
async def 물건등록(ctx, name, price, *, description):
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
    em = discord.Embed(title=f"{name}(이)가 생성됨", description="", color=0x00FF00)
    em.add_field(name="물건 번호", value=str(len(f) + 1), inline=True)
    em.add_field(name="물건 이름", value=name, inline=True)
    em.add_field(name="물건 가격", value=price, inline=True)
    em.set_footer(text="Vending Bot v0.1.3")
    await ctx.send(embed=em)


@bot.command()
@commands.has_permissions(administrator=True)
async def 물건삭제(ctx, v: int):
    sjt = jpgtb[str(ctx.guild.id)]
    var = sjt[int(v / 15)]
    print(str((v - int(v / 15) * 15)))
    print(str(var))
    del var[(v - (int(v / 15) * 15)) - 1]
    em = discord.Embed(title=f"{v}번 물건이 삭제됨", description="삭제가 완료되었습니다.", color=0xFF00)
    em.set_footer(text="Vending Bot v0.1.3")
    await ctx.send(embed=em)


@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.errors.MissingPermissions):
        em = discord.Embed(title="오류", description="당신은 이 커맨드를 사용할 권한이 없습니다!", color=0xFF0000)
        em.set_footer(text="Vending Bot v0.1.3")
        return await ctx.send(embed=em)

    raise err


# bot.run()
