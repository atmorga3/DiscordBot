import discord
import os
import requests
import json
import random
from replit import db
from discord.ext import commands


client = discord.Client()

sad_words=["sad", "depressed", "unhappy", "angry", "cry", "tired", "depressing", "unworthy", "stupid", "myself"]

starter_encouragements=[
"Hang in there!", 
"Keep going",
"Love you <3", 
"You were born to be real, not perfect",
"Love conquers all things; let us too surrender to love",
"You are capble of amazing things",
"You are enough",
"You are loved",
"Say it with me - I deserve love and happiness",
"Say it with me - I am doing my best and am proud of myself",
"UWU"
]
def get_quote():
  response= requests.get("http://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote=json_data[0]['q'] +" -"+ json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db ["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db ["encouragements"] = encouragements

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.idle, activity=discord.Game('a Game'))
  print('ONLINE: {0.user}'.format(client))



  @client.event
  async def on_message(message):
    if message.author ==client.user:
      return

    msg = message.content

    if message.content.startswith('$hi'):
      await message.channel.send('Sup, how u like ur eggs')

    if message.content.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)

    options = starter_encouragements

    if "encouragements" in db.keys():
      options = options+db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
      encouraging_message = msg.split("$new ", 1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New nice message added")

    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split("$del",1)[1])
        delete_encouragement(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)
    
    if message.content.startswith('$commands'):
      await message.channel.send('$hi - bot says hi \n $inspire - random inspirational quote \n $new <quote>- adds <quote> to encouraging words list \n $del <index> -delete an entered phrase at <index>\n more to come soon...')

client.run(os.getenv('TOKEN'))
