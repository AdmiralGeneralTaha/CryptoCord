import os
from discord.ext import tasks
import discord
import random
from replit import db
import keep_alive
from sub_routines import getCryptoPrices, stdform_convert, tf_hChange, ath, marketcaprank
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
      await message.channel.send("`xd The current price of " + crypto +
                                 " is: " + message.content[0] + price +"`")

    if message.content.startswith("%"):
      currency_change = message.content[1:]
      tf_hChange()
      if currency_change in currencies:
        currency_change = currencies[currency_change]
      change = str(db[currency_change])
      if change[0] == "-":
        await message.channel.send("`" + currency_change + " is down " + change + "% in the past 24 hours`")
      else:
        await message.channel.send("`" + currency_change + " is up " + change + "% in the past 24 hours`")

    if client.user.mentioned_in(message):
        await message.channel.send(random.choice(reply))
    
    if message.content.startswith("ath") and message.content[4] in clientCurrencies:
      symbol, crypto = message.content[4], message.content[5:]

      ath(symbol)
      if crypto in currencies:
        crypto = currencies[crypto]
        thing = str(db[crypto])
        if "e" in thing:
           thing = stdform_convert(thing)
        crptcurr = message.content[5:]
        crptcurr = crptcurr.upper()
        await message.channel.send("`The all time high for " + crptcurr + " was "+ message.content[4] + thing + "`")

    if message.content.startswith("mcr"):
      crypto = message.content[4:]

      marketcaprank()
      if crypto in currencies:
        crypto = currencies[crypto]
        rank = str(db[crypto])
        rankedcurr = message.content[4:]
        rankedcurr = rankedcurr.upper()
        await message.channel.send("`The market cap rank for " + rankedcurr + " is " + rank +"`")

    if message.content == "-ping":
        await message.channel.send(f"`{round(client.latency * 1000)}ms`")

    if message.content == "-commence spam-tag":
      while True:
       await message.channel.send("<@311602664985067520>")
        
    if message.content == "-help":
        await message.channel.send(
            "`CryptoCord is a simple bot that will bring you real time Crypto Currency prices, and relevant information upon request\n\n$/£/€{crypto name} for real time crypto price. - $btc \n%{crypto name} for 24hour cyrpto percentage change - %btc \nath $/£/€{crypto name} for All time high of requested currency - ath $btc\nmcr {crypto name] for the Market cap rank of requested currency - mcr btc`")

keep_alive.keep_alive()

client.run(os.getenv("token"))
