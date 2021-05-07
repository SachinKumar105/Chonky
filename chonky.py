# bot.py
import os
import random
from discord import client
import discord
from discord.activity import CustomActivity
from discord.errors import LoginFailure
import json
from discord.ext import commands
# from dotenv import load_dotenv

# load_dotenv()
# TOKEN = 'ODM5OTc3NTg2Mzg4ODkzNzM2.YJRgFg.h2iAcbK66DyZ0pEs0O6sAk6Bs-E'


# print("lol", loginFlag)
bot = commands.Bot(command_prefix='ch ')

@bot.command(name='login')
async def login(ctx):
    fpr = open('auth.json', 'r')
    data = json.load(fpr)
    lf = data['flag']
    # loginStr.strip()
    # if loginStr == '1':
    #     lf = 1
    # else:
    #     lf = 0

    if lf == 0:
        lf = 1
        fpw = open('auth.json','w')
        user = ctx.author
        data['flag'] = lf
        data['user'] = user.name
        json.dump(data,fpw)
        await ctx.send(user.name + " logged in!")
        await bot.change_presence(activity=discord.Activity(name=user.name, type=discord.ActivityType.watching))
        
        # await bot.change_presence(activity=CustomActivity('bonking ' + user.name))
    else:
        name = data['user']
        await ctx.send(name + " already logged in, you mofo!")

@bot.command(name='logout')
async def logout(ctx):
    fpr = open('auth.json', 'r')
    data = json.load(fpr)
    lf = data['flag']

    if lf == 1:
        lf = 0
        loginStr = str(lf)
        fpw = open('auth.json','w')
        user = ctx.author
        data['flag'] = lf
        data['user'] = None
        json.dump(data,fpw)
        await bot.change_presence(activity=None)
        await ctx.send(user.name + " logged out!")
    else:
        await ctx.send("It is logged out mofo!")

@bot.command(name='creds')
async def show_creds(ctx):
    fp = open('creds.json', 'r')
    d = json.load(fp)
    await ctx.send('Username: ' + d['username'])
    await ctx.send('Password: ' + d['password'])

@bot.command(name='credchange')
async def change_creds(ctx):
    fp = open('creds.json', 'w')
    # d = json.load(fp)
    d = {}
    await ctx.send('Username: ')
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    username = await bot.wait_for('message', check=check)
    d['username'] = str(username.content)
    await ctx.send('Password: ')
    password = await bot.wait_for('message', check=check)
    d['password'] = str(password.content)
    json.dump(d,fp)
    await ctx.send("creds changed successfully")


@bot.event
async def on_ready():
    # global loginFlag
    print('We have logged in as {0.user}'.format(bot))

bot.run(os.environ['BOT_TOKEN'])
