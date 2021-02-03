import discord
from discord.ext import commands
import discord.utils
from discord.utils import get
from discord.ext.commands import CommandNotFound
TOKEN = ("ODA2NTUyNDgzNjY0MzYzNTMx.YBrGiQ.SrVoAC1XIAYC-LrAA9uF_9J_8rA")
GUILD = 804827461644189726
MODMAIL_CATEGORY = "KM_TK"
prefix="."
game = "DM to contact KINGAMNTEAM!"
MODMAIL_REPLY = "Thank you for your message! Your message has been sent to our KINGAMNTEAM team, and we will contact you as soon as possible."
intents = discord.Intents(guilds=True, members=True, presences=True, messages=True, reactions=True)
bot = commands.Bot(command_prefix=prefix, intents=intents)
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=game))
    print(
        f"\n"
        f'Username: {bot.user}\n'
        f'ID: {bot.user.id}\n'
    )
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    errorsend = f"```{error}```"
    await ctx.channel.send(errorsend)
@bot.event
async def on_message(message=None):
    await bot.process_commands(message)
    guild = bot.get_guild(GUILD)
    channel = discord.utils.get(guild.channels, name=(f"ticket-{message.author.id}"))
    if message.guild:
        category = discord.utils.get(guild.categories, name=MODMAIL_CATEGORY)
        if message.channel.category != category:
            return
        if message.author == bot.user:
            return
        else:
            if message.content.startswith(prefix)==True:
                return
            else:
                embed=discord.Embed(description=f"{message.author.mention}",color=0x00eaff)
                embed.set_thumbnail(url=message.author.avatar_url)
                if message.content != "":
                    embed.add_field(name="─────────────", value=f"{message.content}", inline=False)
                if len(message.attachments) > 0:
                    attachment = message.attachments[0]
                    embed.set_image(url=attachment.url)
                userid = message.channel.name.replace("ticket-","")
                userid = int(userid)
                user = bot.get_user(id=userid)
                await user.send(embed=embed)
                await message.delete()
                await message.channel.send(embed=embed)

    elif message.author == bot.user:
        return
    else:
        category = discord.utils.get(guild.categories, name=MODMAIL_CATEGORY)
        if category == None:
            await guild.create_category(MODMAIL_CATEGORY)
        if len(message.attachments) > 0:
            attachment = message.attachments[0]
        embed=discord.Embed(description=f"{bot.user.mention}", color=0xff0090)
        embed.set_thumbnail(url=bot.user.avatar_url)
        embed.add_field(name="─────────────", value=MODMAIL_REPLY, inline=False)
        await message.author.send(embed=embed)
        guild = bot.get_guild(GUILD)
        category = discord.utils.get(guild.categories, name=MODMAIL_CATEGORY)
        channel = discord.utils.get(guild.channels, name=(f"ticket-{message.author.id}"))
        if channel == None:
            await guild.create_text_channel(f"ticket-{message.author.id}", category=category)
            channel = discord.utils.get(guild.channels, name=(f"ticket-{message.author.id}"))
        embed=discord.Embed(description=f"{message.author.mention}",color=0xff0090)
        embed.set_thumbnail(url=message.author.avatar_url)
        if message.content != "":
            embed.add_field(name="─────────────", value=f"{message.content}", inline=False)
        if len(message.attachments) > 0:
            attachment = message.attachments[0]
            embed.set_image(url=attachment.url)
        await channel.send(embed=embed)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def close(ctx):
    guild = bot.get_guild(GUILD)
    modmailcategory = discord.utils.get(guild.categories, name=MODMAIL_CATEGORY)
    if ctx.message.channel.category == modmailcategory:
        await ctx.channel.delete()
@bot.command()
@commands.has_permissions(manage_messages=True)
async def open(ctx, user: discord.User):
    await ctx.message.delete()
    guild = bot.get_guild(GUILD)
    category = discord.utils.get(guild.categories, name=MODMAIL_CATEGORY)
    if category == None:
        await guild.create_category(MODMAIL_CATEGORY)
        category = discord.utils.get(guild.categories, name=MODMAIL_CATEGORY)
    channel = discord.utils.get(guild.channels, name=(f"ticket-{user.id}"))
    if channel == None:
        await guild.create_text_channel(f"ticket-{user.id}", category=category)
bot.run(TOKEN)
