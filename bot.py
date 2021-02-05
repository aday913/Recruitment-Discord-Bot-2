import os
import random
import json

with open("zoomLinks.json", "r") as f:
    links = json.load(f)
interviewNames = []
for key in links['interviews']:
    interviewNames.append(key)

from discord import errors
from discord.ext import commands
from discord import utils
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='commands', help='Returns the list of possible bot commands')
async def getCommands(ctx):
    commands = (
            '!socials: returns the social media links for the department!\n'
            '!github: returns the github link for the bot! \n'
            '!interviewLinks [insert name]: grab the zoom link for admissions interviews\n'
            '!tourLink: grab the zoom link for the lab tours\n'
            'ADMIN ONLY:\n'
            '!createTextChannel [insert name]: create a discord text channel with a given name\n'
            '!createVoiceChannel [insert name]: create a discord voice channel with a given name\n'
        )
    await ctx.send(commands)

@bot.command(name='socials', help='Responds with links to the various BME social media sites')
async def socialLinks(ctx):
    socialMediaLinks = (
            'Follow the UA BME department at the following social media links!\n'
            'Insta: https://www.instagram.com/uarizonabme/?hl=en \n'
            'Twitter: https://twitter.com/uarizonabme?lang=en'
        )
    
    await ctx.send(socialMediaLinks)

@bot.command(name='github', help='Provides a link to the Discord server bot source code')
async def github(ctx):
    githubLink = (
            'Interested in how this bot functions? Head over to the github repository containing the source code below: \n'
            'Github: https://github.com/aday913/Recruitment-Discord-Bot-2'
        )

    await ctx.send(githubLink)

@bot.command(name='interviewLinks', help="Provides the zoom links for the admissions interviews")
async def getInterviewLinks(ctx, name=None):
    # print(ctx.author)
    name = str(name)
    name = name.lower()
    if name in interviewNames:
        responseText = links['interviews'][name]
    else:
        responseText = links['interviews']['generic']
    response = ''
    await ctx.send(response.join(responseText))

@bot.command(name='tourLink', help="Provides the zoom links for the lab tours")
async def getTourLinks(ctx):
    # print(ctx.author)
    response = 'Zoom link for lab tours: https://arizona.zoom.us/j/85976710181'
    await ctx.send(response)

@bot.command(name='createTextChannel', help='Will create a text channel if a user with admin privileges wants to')
@commands.has_role('admin')
async def createTextChannel(ctx, channelName):
    guild = ctx.guild
    existing_channel = utils.get(guild.channels, name=channelName)
    if not existing_channel:
        await guild.create_text_channel(channelName)

@bot.command(name='createVoiceChannel', help='Will create a voice channel if a user with admin privileges wants to')
@commands.has_role('admin')
async def createVoiceChannel(ctx, channelName):
    guild = ctx.guild
    existing_channel = utils.get(guild.channels, name=channelName)
    if not existing_channel:
        await guild.create_voice_channel(channelName)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

print('Attempting to log in the bot...')
try:
    bot.run(TOKEN)
except errors.LoginFailure:
    print('The bot could not log in, check the token!')