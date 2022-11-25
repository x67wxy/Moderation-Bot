import discord
import os
import urllib
import sys
import json
import requests
import asyncio
import jishaku
from discord.utils import find
from discord.ext import commands, tasks

async def get_prefix(client, message):
    if message.author.id in []:
        return ""
    else:
        return "-"

token = "OTE3NzAzMjAyNTQ2MjYyMDI4.GtfrQS.qjJcHNk7AbIJ-BGIQ28-U0J1fMciiGxEHPZAwQ"
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
client = commands.AutoShardedBot(shard_count=1,command_prefix=get_prefix, case_insensitive=True, intents=intents , help_command=None)
client.owner_ids = [979967089542569994]
headers = {"Authorization": f"{token}"}

os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

client.load_extension("jishaku")

async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(f"-help | {len(client.guilds)} servers"))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game(f"Protection"))
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print(f"Sucessfully logged in {client.user}")
    client.loop.create_task(status_task())

def restart_client(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@client.command()
@commands.is_owner()
async def restart(ctx):
  await ctx.send(f"`Restarting All Servers Of {client.user}`")
  restart_client()

######## ERROR ###########

@client.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)
    await ctx.send(embed=discord.Embed(color=0x2f3136,description=f'<:error:992024170785427537> {error}'))


################ HELP ##################

@client.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(
        title=
        f'Protection',
        description=
        f'>>> **Hey i am [Protection](https://discord.com/api/oauth2/authorize?client_id=1004465906375741560&permissions=8&scope=bot) A Moderation & Utility Bot With Few Fun Commands!**\n\n**<:fenix_dash:1007475039731466320> General Commands\n<:rep:992046915170619414> `ping` | `mc` | `botinfo` | `stats` | `invite`\n\n<:fenix_dash:1007475039731466320> Moderation Commands\n<:rep:992046915170619414> `hide` | `unhide` | `kick` | `ban` | `purge` | `lock` | `unlock` | `setnick` \n\n<:fenix_dash:1007475039731466320> Utility Commands\n<:rep:992046915170619414> `av` | `banner` | `servericon` | `serverbanner`\n\n<:fenix_dash:1007475039731466320> Fun Commands\n<:rep:992046915170619414> `qr` | `meme` | `truth` | `dare`**',
        color=0x2f3136)

    embed.set_thumbnail(
        url=
        ""
    )
    await ctx.send(embed=embed)

@client.command(aliases=["latency"])
async def ping(ctx):
    embed = discord.Embed(color=0x2f3136,
        description=
        f"**`{int(client.latency * 1000)}ms`**")
    embed.set_thumbnail(
        url=
        ''
    )
    await ctx.send(embed=embed)

@client.command(aliases=["bi", "stats", "stat"])
async def botinfo(ctx):
    embed = discord.Embed(
        title=
        f'Protection | BotInfo',
        description=
        f'**<:fenix_dash:1007475039731466320> Guilds\n<:rep:992046915170619414>{len(client.guilds)}\n\n<:fenix_dash:1007475039731466320> Users\n\n<:rep:992046915170619414>{len(client.users)}\n\n<:fenix_dash:1007475039731466320> Ping\n<:rep:992046915170619414>{int(client.latency * 1000)}\n\n<:fenix_dash:1007475039731466320> Dev\n<:rep:992046915170619414>[NotYourFenix](https://discord.com/users/979967089542569994)\n\n<:fenix_dash:1007475039731466320> Owners\n<:rep:992046915170619414>[Phantom.#7777](https://discord.com/users/990572902535553095)**',
        color=0x2f3136)

    embed.set_thumbnail(
        url=
        ""
    )
    await ctx.send(embed=embed)

@client.command(aliases=["mc"])
async def membercount(ctx):
  scembed = discord.Embed(colour=discord.Colour(0x2f3136))
  scembed.add_field(name='**__Members__**', value=f"{ctx.guild.member_count}")
  await ctx.send(embed=scembed, mention_author=False)

@client.command(aliases=["inv", "i"])
async def invite(ctx):
    embed = discord.Embed(color=0x2f3136,
        description=
        f"**[Click Here To Invite Protection](https://discord.com/api/oauth2/authorize?client_id=1010772863743172618&permissions=8&scope=bot)**")
    embed.set_thumbnail(
        url=
        ''
    )
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def unhide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,view_channel=True)
    await ctx.send('> **<:success:992024105975037992> | Channel is Now Visible!**')

 
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason==None:
      reason=" no reason provided"
    await ctx.guild.kick(member)
    await ctx.send(f'**> <:success:992024105975037992> | Kicked {member.mention} For Reason: `{reason}`**') 


@client.command("purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send((f"> **<:success:992024105975037992> | Deleted `{amount}` Messages/Chats!**"), delete_after=10)

@client.command(aliases=["av"])
async def avatar(ctx, member : discord.Member = None):
    member = ctx.author if not member else member

    embed = discord.Embed(
    title = f"**Avatar/PFP of {member.name}**",
    color = 0x2f3136
    )
    embed.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=embed)


@client.command()
async def banner(ctx, user:discord.Member = None):
    if user == None:
       user = ctx.author
    bid = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = bid["banner"]
    
    if banner_id:
       embed = discord.Embed(color= 0x2f3136)
       embed.set_author(name=f"Banner of {user.name}")
       embed.set_image(url=f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024")
       await ctx.send(embed = embed)
    else:
       embed = discord.Embed(color=0x2f3136, description=f"**The Selected User Dont Have A Banner! xD**")
       await ctx.send(embed = embed)

@client.command(aliases=['icon', 'sicon'])
async def servericon(ctx):
    embed = discord.Embed(title=ctx.guild.name, color=0x2f3136)
    embed.set_image(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Protection")
    await ctx.send(embed=embed)

@client.command()
async def serverbanner(ctx):
    embed = discord.Embed(title=ctx.guild.name, color=0x2f3136)
    embed.set_image(url=ctx.guild.banner_url)
    embed.set_footer(text=f"Protection")
    await ctx.send(embed=embed)

@client.command()
async def qr(ctx, input):
    if input == None:
        await ctx.send("Enter A Link!")
    else:
        embed = discord.Embed(title="Protection | QR Generated")
        embed.set_image(
            url=
            f"https://api.qrserver.com/v1/create-qr-code/?size=450x450&data={input}"
        )
        await ctx.send(embed=embed)

@client.command()
async def nitro(ctx):
  em = discord.Embed(color=discord.Colour(0x2f3136), title="Protection", description="**You Have Been Rick-Rolled xD! 🤣**")
  em.set_image(url="https://media.discordapp.net/attachments/990444922899402752/1006234384757690481/6a0104ba30c01bff32b9e19c49fec1b5.gif")
  em.set_thumbnail(url="https://cdn.discordapp.com/attachments/983055525568733254/1007478109387358218/unknown.png")
  txt = "**<:boost_:1007478937963745370> __Boost & Nitro Reward!__ <:boost_:1007478937963745370>**"
  await ctx.send(txt, embed=em)

@client.command()
async def meme(ctx):
    memeAPI = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme")

    memeData = json.load(memeAPI)

    memeUrl = memeData["url"]
    memeName = memeData["title"]
    memePoster = memeData["author"]
    memeSub = memeData["subreddit"]
    memeLink = memeData["postLink"]

    embed = discord.Embed(title=memeName, color=0x2f3136)
    embed.set_image(url=memeUrl)
    embed.set_footer(text=f"Memes | Protection", icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
  channel = channel or ctx.channel
  overwrite = channel.overwrites_for(ctx.guild.default_role)
  overwrite.view_channel = False
  await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
  description=f'> **<:success:992024105975037992> | {ctx.channel.mention} Has Been Locked!**'
  await ctx.reply(embed=discord.Embed(color=discord.Colour(0x2f3136), description=description))

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
  channel = channel or ctx.channel
  overwrite = channel.overwrites_for(ctx.guild.default_role)
  overwrite.send_messages = True
  await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
  description=f'> **<:success:992024105975037992> | {ctx.channel.mention} Has Been Unlocked!**'
  await ctx.reply(embed=discord.Embed(color=discord.Colour(0x2f3136), description=description))

@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def truth(ctx):
    content = requests.get("https://api.truthordarebot.xyz/v1/truth").text
    data = json.loads(content)
    text = data["question"]
    idk = discord.Embed(color = discord.Colour(0x2f3136), description=text)
    await ctx.reply(embed=idk, mention_author=False)

@client.command(aliases=["nick", "setnick"])
@commands.has_permissions(manage_nicknames=True)
async def nickname(ctx, member: discord.Member, *, nick):
    old_name = member.name
    await member.edit(nick=nick)
    description = f"**🧋| Changed Nick of `{old_name}` To `{nick}`**"
    await ctx.reply(embed=discord.Embed(color=discord.Colour(0x2f3136), description=description))

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
  if ctx.author.top_role.position < member.top_role.position or ctx.author.top_role.position == member.top_role.position:
    await ctx.reply(embed=discord.Embed(color=discord.Colour(0x2f3136), description=f"**You Can't Ban Member Above You!**"))
  else:
    await member.ban(reason=f"Banned by {ctx.author}, reason: {reason}")
    await ctx.reply(embed=discord.Embed(color=discord.Colour(0x2f3136), description=f"**<:success:992024105975037992> | Banned {member}**"))
    try:
      await member.send(embed=discord.Embed(color=discord.Colour(0x2f3136), description=f"**You Have Been Banned From `{ctx.guild.name}` By `{ctx.auhtor}` For `{reason}`**"))
    except:
      pass
#################################################################################################################

client.run(token)
