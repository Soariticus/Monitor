# The actual discord bot to handle the input, everything will be parsed and forwarded to MonitorAPI.py for further processing

import discord
from discord.ext import commands
from MonitorAPI import monitor as m
from datetime import datetime

staff = [199576000844136448, 395066428409118720, 659226316679413793, 413955398387630080, 269511972393844736,
         132739019007197185, 142088223345213440, 638494850861367296, 429083450322976768, 297061136048848898]
# Dennis, Golden, Grim, Bio, Darkness, SavuBTW, Sav, rev, Safari

support = [320006306486550528, 472444075342037030, 191137771455250432, 521196999073202182, 270655412662042626,
           242389105864998913]
# Array, Berry, Rowin, Stormi, Troop, Sansgay
class MyClient(discord.Client):
    async def on_ready(self):
        print("Monitoring...")
        print("____________________________________________")
        activity = discord.Activity(name='you...', type=discord.ActivityType.watching)
        await m.startTimer(self=m)
        await client.change_presence(activity=activity)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("mon.utctime"):
            await message.channel.send(m.parseTime(self=m))

#        if message.author.id in staff or message.author.id in support:
#            if message.author.id == 142088223345213440:
#                userID = 132739019007197185
#            else:
#                userID = message.author.id
#            try:
#                print(f"Checking user: {message.author}")
#                m.checkUser(self=m, uid=userID, name=message.author.name)
#            except () as e:
#                print(e)

        if message.author.id == 638494850861367296:
            if message.content.startswith("mon.output"):
                try:
                    m.excWrite(self=m)
                    await message.channel.send("Writing complete, check server files for output.", delete_after=10)
                except PermissionError:
                    await message.channel.send("Cannot output whilst file is open on client. Close it and try again.", delete_after=10)
#
#            if message.content.startswith("mon.time"):
#                timeLeft = m.getHour(self=m)
#                await message.channel.send(timeLeft[0])




client = MyClient()
client.run("NzA2MTM1NjQxMTI1MDI3ODgw.XrMFmA.yTg2ULDakirKhK0_NnKtajGD_wM")
