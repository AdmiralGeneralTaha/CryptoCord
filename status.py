from sub_routines import getCryptoPricesGBP, getCryptoPricesUSD
from replit import db
from discord.ext import tasks
import discord
#from main import client

status = ["£bitcoin", "$bitcoin", "£ethereum", "$ethereum", "£dogecoin", "$dogecoin", "£cardano", "$cardano"]

@tasks.loop(seconds=15)
async def change_status():

  current = status[discord.Client.current_status]
    
  if current.startswith("£"):
      current = current.strip("£")
      getCryptoPricesGBP(current)
      text = f"{current}: £{str(db[current])}"
  else:
      current = current.strip("$")
      getCryptoPricesUSD(current)
      text = f"{current}: ${str(db[current])}"
   
  await discord.Client.change_presence(
      status=discord.Status.idle,
      activity=discord.Game(text)
  )
  discord.Client.current_status += 1
  if discord.Client.current_status >= len(status):
    discord.Client.current_status = 0