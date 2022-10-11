import asyncio
import random
import time

import discord
import praw
import youtube_dl
from discord.ext import commands
from discord.utils import get

reddit = praw.Reddit(client_id='REDACTED',  # put your reddit API details here
                     client_secret='REDACTED',
                     user_agent='REDACTED')

token = open("token.txt", "r").read()  # store token inside a txt in the same dir
client = commands.Bot(command_prefix="?", intents=discord.Intents.all())
name = 'REDACTED'  # This is the "name" of the description or game that the bot is playing, or livestream
urltwitch = 'REDACTED'  # If you want the bot to show its streaming something, put that
# link here
client.remove_command('help')
ROLE = "REDACTED"  # If you want autorole, put the role you want them to automatically be upon joining here
voice_clients = {}
yt_dl_opts = {"format": "bestaudio/best"}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {"options": "-vn -ab 128k -ac 2 -ar 44100 -acodec libmp3lame"}  # These options provide HQ audio


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name=name, url=urltwitch))
    print("Bot is ready.")


@client.event
async def on_member_join(member, server):
    print(f'{member} has joined {server}.')
    role = get(member.guild.roles, name=ROLE)
    await member.add_roles(role)
    print(f"{member} was given {role}")


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


@client.command(aliases=['help'])
async def _help(ctx):
    helpembed = discord.Embed(title='Help', description="""Commands are as follows

Note: For the mute command, you must have a "muted" role 

?8ball: Ask the mystical 8 ball a question
?play: Plays a song, accepts youtube links only
?pause: Pauses song
?resume: Resumes song
?stop: Stops playing song
?kick: Kicks a user
?ban: Bans a user
?unban: Unbans a user
?mute: Mutes user
?unmute: Unmutes user
?links: Check out my links!
?meme: Pulls a fresh reddit meme
?nsfw: Have some nsfw fun with gifs
?clear: Clears messaged (dont abuse or it will be rate limited)
?ping: Bot's ping
""",
                              colour=discord.Colour.dark_gold())
    helpembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    helpembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    await ctx.send(embed=helpembed)


@client.command()
async def ping(ctx):
    ping = discord.Embed(title='Ping', description=f'pong! {round(client.latency * 1000)}ms',
                         colour=discord.Colour.dark_gold())
    ping.set_author(name=client.user.name, icon_url=client.user.avatar)
    ping.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    await ctx.send(embed=ping)


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes - definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 '''Don't count on it.''',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    eightball = discord.Embed(title='8ball', description=f'Question: {question}\nAnswer: {random.choice(responses)}',
                              colour=discord.Colour.dark_gold())
    eightball.set_author(name=client.user.name, icon_url=client.user.avatar)
    eightball.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    await ctx.send(embed=eightball)


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)
    clearembed = discord.Embed(title='clear', description=f'Cleared {amount}',
                               colour=discord.Colour.dark_gold())
    clearembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    clearembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    await ctx.send(embed=clearembed)
    time.sleep(5.0)
    await ctx.channel.purge(limit=1)


@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    kickembed = discord.Embed(title='KICKED!', description=f'{member} has been kicked for {reason}',
                              colour=discord.Colour.dark_gold())
    kickembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    kickembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    await ctx.send(embed=kickembed)


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    banembed = discord.Embed(title='BANNED!', description=f'{member} has been banned for {reason}',
                             colour=discord.Colour.dark_gold())
    banembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    banembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    await ctx.send(embed=banembed)
    await ctx.send(f'{member} has been banned for {reason}')


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_descriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_descriminator):
            await ctx.guild.unban(user)
            unbanembed = discord.Embed(title='Unbanned', description=f'Unbanned {user.mention}',
                                       colour=discord.Colour.dark_gold())
            unbanembed.set_author(name=client.user.name, icon_url=client.user.avatar)
            unbanembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=unbanembed)


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None):
    if not member:
        muteerror3 = discord.Embed(title='ERROR', description='Member not specified!',
                                   colour=discord.Colour.dark_gold())
        muteerror3.set_author(name=client.user.name, icon_url=client.user.avatar)
        muteerror3.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=muteerror3)
        return
    role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.add_roles(role)


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        muteerror2 = discord.Embed(title='ERROR', description='You are not allowed to mute people',
                                   colour=discord.Colour.dark_gold())
        muteerror2.set_author(name=client.user.name, icon_url=client.user.avatar)
        muteerror2.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=muteerror2)


@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("Please specify a member")
        return
    role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(role)


@mute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        muteerror = discord.Embed(title='ERROR', description='You are not allowed to unmute people',
                                  colour=discord.Colour.dark_gold())
        muteerror.set_author(name=client.user.name, icon_url=client.user.avatar)
        muteerror.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=muteerror)


@client.command()
async def meme(ctx):
    global submission
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    memeembed = discord.Embed(title='Here is a meme for ya!', description='meme inbound!',
                              colour=discord.Colour.dark_gold(), url=submission.url)
    memeembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    memeembed.set_image(url=submission.url)
    memeembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    await ctx.send(embed=memeembed)


@client.command()
async def nsfw(ctx):
    global submission
    nsfw_sub = reddit.subreddit('NSFW_GIF').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in nsfw_sub if not x.stickied)
    nsfwembed = discord.Embed(title='Here is a meme for ya!', description='meme inbound!',
                              colour=discord.Colour.dark_gold(), url=submission.url)
    nsfwembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    nsfwembed.set_image(url=submission.url)
    nsfwembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    await ctx.send(embed=nsfwembed)


@client.command()
async def links(ctx):
    linksembed = discord.Embed(title='Here are my links!', description='''looking for my links? here you are! 

My discord ----> http://q.gs/EvrQG 
subscribe here: ----> http://q.gs/EvrQ6 
I stream all the time, check it here ----> http://j.gs/D1mt 
my personal website ----> http://j.gs/D1mv 
my twitter ----> http://j.gs/D1mw 
my buddy hengu ----> http://j.gs/D1mx
and his twitter too ----> http://j.gs/D1n0''',
                               # Left my own links here as an example, you can change this to your stuff
                               colour=discord.Colour.red())
    linksembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    linksembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    await ctx.send(embed=linksembed)


@client.command()
async def play(ctx, url: str):
    global voice_client
    playerembed = discord.Embed(title="Now playing", description=f"Now playing: {url}", colour=discord.Colour.red())
    playerembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    playerembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    try:
        voice_client = await ctx.author.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client
    except AttributeError:
        print("error")
    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        song = data["url"]
        player = discord.FFmpegPCMAudio(song, **ffmpeg_options)  # Designed for linux hosts, apt-get install ffmpeg, you
        # won't need to specify executable. windows hosts, specify after options separated by comma, executable="Path
        # to ffmpeg executable folder"
        voice_client.play(player)
        await ctx.send(embed=playerembed)
    except AttributeError:
        print("error")


@client.command()
async def pause(ctx):
    pausembed = discord.Embed(title="Paused", description="Song is paused", colour=discord.Colour.red())
    pausembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    pausembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    voice_clients[ctx.guild.id].pause()
    await ctx.send(embed=pausembed)


@client.command()
async def resume(ctx):
    resumembed = discord.Embed(title="Resuming", description="Song is resuming", colour=discord.Colour.red())
    resumembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    resumembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    voice_clients[ctx.guild.id].resume()
    await ctx.send(embed=resumembed)


@client.command()
async def stop(ctx):
    stopembed = discord.Embed(title="Stopping", description="Song is stopping", colour=discord.Colour.red())
    stopembed.set_author(name=client.user.name, icon_url=client.user.avatar)
    stopembed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    voice_clients[ctx.guild.id].stop()
    await voice_clients[ctx.guild.id].disconnect()
    await ctx.send(embed=stopembed)


client.run(token)
