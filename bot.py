import asyncio
import random
import time

import discord
import praw
import youtube_dl
from discord.ext import commands
from discord.utils import get

reddit = praw.Reddit(client_id='m3CPMso5Cifasg',
                     client_secret='vc-sLJaSGq1dfxFsNPD2MKbTHjY',
                     user_agent='DR3AMCH3AT')

token = open("token.txt", "r").read()
client = commands.Bot(command_prefix="?", intents=discord.Intents.all())
name = 'Destiny Creates Entertainment'
urltwitch = 'https://www.twitch.tv/destiny_creates'
client.remove_command('help')
ROLE = "member"
voice_clients = {}
yt_dl_opts = {"format": "bestaudio/best"}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {"options": "-vn -ab 128k -ac 2 -ar 44100 -acodec libmp3lame"}


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
    await ctx.send("""Commands are as follows

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
?bumper: Auto-Bump ;)
""")


@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')


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
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.send('Clearing...')
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Cleared {amount}')
    time.sleep(2.0)
    await ctx.channel.purge(limit=1)


@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked for {reason}')


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned for {reason}')


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx: commands.Context, *, member):
    banned_users = ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    async for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None):
    if not member:
        await ctx.send('Member not specified!')
        return
    role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.add_roles(role)
    await ctx.send(f"Muted: {member}")


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You are not allowed to mute people')


@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("Please specify a member")
        return
    role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(role)
    await ctx.send("")


@mute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You are not allowed to unmute people')


@client.command()
async def meme(ctx):
    global submission
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    await ctx.send(submission.url)
    await ctx.send('\nEnjoy the meme ;)')


@client.command()
async def nsfw(ctx):
    global submission
    nsfw_sub = reddit.subreddit('NSFW_GIF').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in nsfw_sub if not x.stickied)
    await ctx.send(submission.url)
    await ctx.send('\nEnjoy ;)')


@client.command()
async def nsfwlink(ctx):
    global submission
    nsfwlink_sub = reddit.subreddit('nsfw_Videos').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in nsfwlink_sub if not x.stickied)
    await ctx.send(submission.url)
    await ctx.send('\nEnjoy ;)')


@client.command()
async def links(ctx):
    await ctx.send('''looking for my links? here you are! 

My discord ----> http://q.gs/EvrQG 
subscribe here: ----> http://q.gs/EvrQ6 
I stream all the time, check it here ----> http://j.gs/D1mt 
my personal website ----> http://j.gs/D1mv 
my twitter ----> http://j.gs/D1mw 
my buddy hengu ----> http://j.gs/D1mx
and his twitter too ----> http://j.gs/D1n0''')


@client.command()
async def play(ctx, url: str):
    global voice_client
    try:
        voice_client = await ctx.author.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client
    except AttributeError:
        print("error")
        await ctx.send("Error! Contact destiny_creates@outlook.com")
    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        song = data["url"]
        player = discord.FFmpegPCMAudio(song, **ffmpeg_options,
                                        executable="""C:\\Users\\desti\\Documents\\GitHub\\discord-bot\\ffmpeg""")  # add to path and remove
        # executable portion, or put the ffmpeg folder inside the bot folder, and it will work.
        voice_client.play(player)
        await ctx.send(f"Now playing: {url}")
    except AttributeError:
        await ctx.send("Error! Contact destiny_creates@outlook.com")


@client.command()
async def pause(ctx):
    voice_clients[ctx.guild.id].pause()
    await ctx.send("Song is paused")


@client.command()
async def resume(ctx):
    voice_clients[ctx.guild.id].resume()
    await ctx.send("Song is resuming")


@client.command()
async def stop(ctx):
    voice_clients[ctx.guild.id].stop()
    await voice_clients[ctx.guild.id].disconnect()
    await ctx.send("Song is stopping")


client.run(token)
