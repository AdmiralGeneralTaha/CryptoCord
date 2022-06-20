import os
from discord.ext import tasks
import discord
import random
from replit import db
import keep_alive
from sub_routines import getCryptoPrices, stdform_convert, tf_hChange, ath
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
      await message.channel.send("`The current price of " + crypto +
                                 " is: " + message.content[0] + price +"`")

    if message.content.startswith("%"):
      currency_change = message.content[1:]
      tf_hChange()
      if currency_change in currencies:
        currency_change = currencies[currency_change]
      change = str(db[currency_change])
      if change[0] == "-":
        await message.channel.send("`" + currency_change[1:] + " is down " + change + "% in the past 24 hours`")
      else:
        await message.channel.send("`" + currency_change + " is up " + change + "% in the past 24 hours`")

    if client.user.mentioned_in(message):
        await message.channel.send(random.choice(reply))

    if message.content == "-help":
        await message.channel.send(
            "`do ${crypto name} for crypto price in dollars, or £{crypto name} for crypto price in pounds`")

    if any([message.content[4] in clientCurrencies]) and message.content[0:3] == "ath":
      symbol, crypto = message.content[4], message.content[5:]

      ath(symbol)
      if crypto in currencies:
        crypto = currencies[crypto]
        thing = str(db[crypto])
        if "e" in thing:
           thing = stdform_convert(thing)
        crptcurr = message.content[5:]
        crptcurr = crptcurr.upper()
        await message.channel.send("`The all time high for " + crptcurr + " was $" + thing + "`")
        
    if message.content == "-ping":
        await message.channel.send(f"`{round(client.latency * 1000)}ms`")

keep_alive.keep_alive()

client.run(os.getenv("token"))
