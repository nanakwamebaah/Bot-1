import os
import discord
import requests
import json
import random
from replit import db



client = discord.Client()
my_secret = os.environ['TOKEN']

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", 
            "not fine", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "Don't everything will be fine.",
  "You are an amazing person!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def get_bible_quote(verse):
  response = requests.get('https://bible-api.com/' + verse)
  json_data = json.loads(response.text)
  return(json_data['text'])

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def del_encouragement(index):    
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
      
  
#event as the bot is ready
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#event when message is recieved
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send('Hello!')

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith('$bible'):
    verse = msg.split("$bible ",1)[1]
    bible = get_bible_quote(verse)
    await message.channel.send(bible)  

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])
  
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      del_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)  
#if you want the bot to respond to sad message
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")     
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")  

client.run(my_secret)

    

