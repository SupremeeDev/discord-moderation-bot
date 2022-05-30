#                                      #
#     Bot created by $upreme#1337      #
#      Discord.py Moderation Bot       #
#                                      #

import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="!")               # Bot Prefix
bot.remove_command("help")                           # Da vam ne prikazuje default help / Not to show you the default help

# Config
AdminID = 873962910970441738                         # ID Admin Rola          / Admin Role ID
MuteID = 924635552244965446                          # ID Muted Rola          / Muted Role ID
LogChannel = 933866614699483156                      # ID Channela za logove  / Log Channel ID


# Start
@bot.event
async def on_ready():
    print("Bot Developer: $upreme#1337\nBot status: Online")


# Error Log
@bot.event
async def on_command_error(ctx,error):
	if not isinstance(error, CommandNotFound):
		print(f"[ERROR] - {error}")


# Mute Komanda

@bot.command()
@commands.has_role(AdminID)
async def mute(ctx, member: discord.Member = None, vreme:int = None, *, razlog = "Nema"):

    # !mute @tag/id hours reason

    MutedRole = discord.utils.get(ctx.guild.roles, id=MuteID)

    if member == None:
        await ctx.reply("Nisi upisao/la membera!")
        return

    if vreme == None:
        await ctx.reply("Nisi upisao/la vreme!")
        return

    if MutedRole in member.roles:
        await ctx.reply(f"Member **{member}** je već mutiran/a!")

    else:
        Cooldown = int(vreme*3600)
        print(Cooldown)
        MuteLog = bot.get_channel(LogChannel)
        await member.add_roles(MutedRole)
        await ctx.reply(f'**{member.name}** je mutiran/a na **{vreme}**h, Razlog: `{razlog}`')
        await MuteLog.send(f'**{ctx.author}** je mutirao/la Membera **{member}** na **{vreme}**h | Razlog: `{razlog}`')
        await asyncio.sleep(Cooldown)
        await member.remove_roles(MutedRole)
        return



# Unmute Komanda

@bot.command()
@commands.has_role(AdminID)
async def unmute(ctx, member: discord.Member = None):

    if member == None:
        await ctx.reply("Nisi upisao/la Membera!")
        return

    MutedRole = discord.utils.get(ctx.guild.roles, id=MuteID)
    if MutedRole not in member.roles:
        await ctx.reply(f"Member **{member.name}** nije mutiran/a")
        return

    else:
        UnmuteLog = bot.get_channel(LogChannel)
        await member.remove_roles(MutedRole)
        await ctx.reply(f"**{member.name}** je unmutiran/a od strane **{ctx.author.name}**")
        await UnmuteLog.send(f"**{ctx.author}** je unmutiran//la Membera {member.mention}")


# Kick Komanda

@bot.command()
@commands.has_role(AdminID)
async def kick(ctx, member : discord.Member=None, *, reason="Nema"):
    if member == None:
        await ctx.reply("Nisi upisao/la Membera")
        return

    else:
        await member.kick(reason=reason)
        KicklogChannel = bot.get_channel(LogChannel)
        await KicklogChannel.send(f'**{ctx.author}** je kickovao/la <@{member.id}> ・ Razlog: `{reason}`')
        return

@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.CheckFailure):
    await ctx.reply("Ne mozete koristiti `KICK` komandu, niste Admin!")


# Ban Komanda

@bot.command()
@commands.has_role(AdminID)
async def ban(ctx, member: discord.Member=None, *, razlog="Nema"):
    if member == None:
        await ctx.reply("Nisi upisao/la Membera")
        return


    if member == ctx.author:
        await ctx.reply("Ne mozeš Banovati sam/a sebe")
        return

    else:
        await member.ban(reason=razlog)
        await ctx.reply(f"**{member.name}** je banovan/a! Razlog: `{razlog}`")
        BanLogChannel = bot.get_channel(LogChannel)
        await BanLogChannel.send(f'**{ctx.author.name}** je banovao/la <@{member.id}>! Razlog: `{razlog}`')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error,commands.CheckFailure):
        await ctx.reply(f'Ne mozete koristiti `BAN` komandu, niste Admin!')



# Unban All Komanda

@bot.command()
@commands.has_permissions(administrator=True) # Potrebna vam je Administrator permisija za ovu komandu
async def unbanall(ctx):
    BanovaniMemberi = await ctx.guild.bans()

    for x in BanovaniMemberi:
        member = x.user
        await ctx.guild.unban(member)
        await ctx.reply(f"> Svi Memberi su Unbanovani by {ctx.author.name}")


bot.run("ODQ3NzkyOTE4ODAyNTk1ODYw.YLDOrw.4wC6oITNz9fOnhH9KaIn21pkGIA") # Token
