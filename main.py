import os
from discord.ext import tasks
import discord
import random
from replit import db
import keep_alive
from sub_routines import getCryptoPrices, stdform_convert
from lists import currencies, status, reply, clientCurrencies

client = discord.Client()
client.current_status = 0

@client.event
async def on_ready():
    await change_status()
    print("we have logged in as {0.user}".format(client))
    change_status.start()

@tasks.loop(seconds=10)
async def change_status():
    current = status[client.current_status]
    print (current)
    if current[0] in clientCurrencies:
      symbol = current[0]
      getCryptoPrices(symbol)
      text = f"{current[1:]}: {current[0]}{str(db[current[1:]])}"

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(text)))
    client.current_status += 1
    if client.current_status >= len(status):
      client.current_status = 0

@client.event
async def on_message(message):
    if message.author == client.user:
        return
      
    if any([message.content[0] in clientCurrencies]):
      symbol, crypto = message.content[0], message.content[1:]

      getCryptoPrices(symbol)
      if crypto in currencies:
        crypto = currencies[crypto]
        price = str(db[crypto])
        if "e" in price:
          price = stdform_convert(price)
      await message.channel.send("The current price of " + crypto +
                                 " is: " + message.content[0] + price)

    if client.user.mentioned_in(message):
        await message.channel.send(random.choice(reply))

    if message.content == "-help":
        await message.channel.send(
            "do ${crypto name} for crypto price in dollars, or £{crypto name} for crypto price in pounds")

    if message.content == "-ping":
        await message.channel.send(f"{round(client.latency * 1000)}ms")

keep_alive.keep_alive()

client.run(os.getenv("token"))
