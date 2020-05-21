import discord
import random
import time

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
         'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
         'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
delay = 0.8
default = "https://discord.gift/"

class MyClient(discord.Client):
    async def on_ready(self):
        print("Ready to go")
        print("____________________________________________")
        activity = discord.Activity(name='[help', type=discord.ActivityType.watching)
        await client.change_presence(activity=activity)


    async def on_message(self,message):
        global num, stop, delay, default

        if message.content.startswith("[help"):
            embed = discord.Embed(title="NitroMiner", description="Commands", color=0x00ff00)
            embed.add_field(name="Start", value="[start (int) {Starts mining}", inline=False)
            embed.add_field(name="Stop", value="[stop {Stops the bot}", inline=False)
            embed.add_field(name="Delay", value="[delay (float) {Sets the delay, default 0.8}", inline=False)
            await message.channel.send(embed=embed)

        if message.content.startswith("[delay"):
            split = message.content.split()
            try:
                setDelay = float(split[1])
                await message.channel.send(f"Delay set to {setDelay}s (default 0.8) | Will be reset on next restart.")
                delay = setDelay
            except IndexError:
                await message.channel.send(f"Delay is currently {delay}s (default 0.8)")
            except ValueError:
                setDelay = split[1]
                await message.channel.send(f"Value must be float or int, not `{setDelay}` (default 0.8)")

        if message.content.startswith("[stop"):
            await message.channel.send("Preparing to stop...")
            stop = True

        if message.content.startswith("[start"):
            stop = False
            split = message.content.split()
            try:
                num = int(split[1])
                print(f"Outputting to {message.channel} at {delay}s delay | {num} times.")
                for x in range(num):
                    key = "".join(random.sample(chars, 16))
                    await message.channel.send(default + key)
                    time.sleep(delay)
                    if stop:
                        break

            except IndexError as e:
                print(f"outputting to {message.channel} at {delay}s delay")
                while not stop:
                    key = "".join(random.sample(chars, 16))
                    await message.channel.send(default + key)
                    time.sleep(delay)
                    print('yeet')

            except ValueError:
                num = " ".join(split[1:])
                await message.channel.send(f"`{num}` is not a valid number, please either use an int, or leave it empty"
                                           f" to go on infinitely.")


client = MyClient()
client.run("NzEwMDcyMjg0MjE5NTcyMjg1.XrvIXQ.4kMwsgZpOioTbLdP6LoOvRlAedc")
