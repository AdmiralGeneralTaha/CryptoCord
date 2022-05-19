import os
from discord.ext import tasks
import discord
import random
from replit import db
import keep_alive
import itertools
from sub_routines import getCryptoPricesGBP, getCryptoPricesUSD, getCryptoPricesEUR
#from status import change_status

client = discord.Client()
client.current_status = 0
status = [
    "£bitcoin", "$bitcoin", "£ethereum", "$ethereum", "£dogecoin", "$dogecoin",
    "£cardano", "$cardano"
]

reply = ['daddy elon😍', '2DaMoon!', 'bitcoin!']


#prints confirmation message in console when logged in
@client.event
async def on_ready():
    change_status()
    print("we have logged in as {0.user}".format(client))
    change_status.start()


#cycles bot status every 15 seconds
@tasks.loop(seconds=15)
async def change_status():
    current = status[client.current_status]

    if current.startswith("£"):
        current = current.strip("£")
        getCryptoPricesGBP(current)
        text = f"{current}: £{str(db[current])}"
    else:
        current = current.strip("$")
        getCryptoPricesUSD(current)
        text = f"{current}: ${str(db[current])}"

    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Game(text))
    client.current_status += 1
    if client.current_status >= len(status):
        client.current_status = 0


#messages sent by the bot will be ignored
@client.event
async def on_message(message):
    if message.author == client.user:
        return

#if user message starts with "£" it uses the GBP api to return a message with the price of the crypto requested
    if message.content.startswith("£"):
        crypto = message.content.lower()
        crypto = crypto.replace("£", "")
        getCryptoPricesGBP(crypto)
        await message.channel.send("The current price of " + crypto +
                                   " is: £" + str((db[crypto])))

#same is done for "$", but uses the USD api
    if message.content.startswith("$"):
        crypto = message.content.lower()
        crypto = crypto.replace("$", "")
        getCryptoPricesUSD(crypto)
        await message.channel.send("The current price of " + crypto +
                                   " is: $" + str((db[crypto])))

    if message.content.startswith("€"):
        crypto = message.content.lower()
        crypto = crypto.replace("€", "")
        getCryptoPricesEUR(crypto)
        await message.channel.send("The current price of " + crypto +
                                   " is: €" + str((db[crypto])))

    if client.user.mentioned_in(message):
        await message.channel.send(random.choice(reply))

    if message.content == "-help":
        await message.channel.send(
            "do ${crypto name} for crypto price in dollars, or £{crypto name} for crypto price in pounds")

    if message.content == "-ping":
        await message.channel.send(f"{round(client.latency * 1000)}ms")


#keeps the bot running 24/7
keep_alive.keep_alive()

#connects to the discord bot account
client.run(os.getenv("token"))
