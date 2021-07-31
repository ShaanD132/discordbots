import discord
from discord.ext import commands, tasks
import os
import asyncio
import time
import datetime
import requests
import json
import requests
import asyncio
import random
from discord.utils import get
from mcstatus import MinecraftServer 
from keepalive import keep_alive

member_info = []
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents = intents)

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    global member_info
    f = open("times.txt")
    content = f.readlines()
    for i in range (0, len(content)):
        content[i] = content[i].split(", ")
        content[i][0] = int(content[i][0])
        content[i][1] = int(content[i][1].strip())
        member_info.append(content[i])
    print(member_info)
    track_user_time.start()
    update_file.start()

@bot.command()
async def myTime(ctx):
    author = ctx.author.id
    global member_info
    for b in range (0, len(member_info)):
        if (member_info[b][0] == author):
            time_spent = member_info[b][1]
            user_days = time_spent // 3600
            user_hours = (time_spent - (user_days*3600)) // 60
            user_minutes = time_spent - (user_days*3600) - (user_hours *60) 
            time_msg = f"""
            Time Spent by: {ctx.author.name}
            Days Spent Studying: {user_days} day(s)
            Hours Spent Studying: {user_hours} hour(s)
            Minutes Spent Studying: {user_minutes} minutes
            """
            await ctx.send(time_msg)

@tasks.loop(seconds=60)
async def track_user_time():
    global member_info 
    active_members = []
    await bot.wait_until_ready()
    channel = bot.get_channel(868830478705233993)
    members = channel.members
    for k in range (0, len(members)):
        if (members[k].id not in active_members):
            active_members.append(members[k].id)
    #find their id for each work channel
    #look for corresponding id in member_info
    #add 1 minute to their time spent studying
    channel = bot.get_channel(868835241958182984)
    members = channel.members
    for p in range (0, len(members)):
        if (members[p].id not in active_members):
            active_members.append(members[p].id)

    channel = bot.get_channel(868835476147146752)
    members = channel.members
    for o in range (0, len(members)):
        if (members[o].id not in active_members):
            active_members.append(members[o].id)

    print(active_members)
    for f in range (0, len(member_info)):
        for y in range(0, len(active_members)):
            if (member_info[f][0] == active_members[y]):
                member_info[f][1] = member_info[f][1] + 1
    print("working")

@tasks.loop(seconds = 90)
async def update_file():
    await bot.wait_until_ready()
    f = open('times.txt', 'w')
    for q in range(0, len(member_info)): 
        file_info = str(member_info[q][0]) + ", " + str(member_info[q][1]) + "\n"
        f.write(file_info)
    print("updated")

keep_alive()
bot.run(os.getenv("TOKEN"))