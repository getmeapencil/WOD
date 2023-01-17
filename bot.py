import keys
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import tasks
import datetime

channel = None

client = discord.Client(intents=discord.Intents.default())

def get_content():
    """
    Get the word and its definition from the website
    """
    try:
        word_site = "https://www.shabdkosh.com/word-of-the-day/english-hindi"
        res = requests.get(word_site)
        soup = BeautifulSoup(res.text, 'html.parser')
        content = soup.select(".my-2 p")
        return content
    except:
        print("error while fetching word")
        return None

def get_word(words):
    """
    Get the word from the string
    """
    word=""
    for c in words:
        if c == "|":
            break;
        word+=c
    return word

@tasks.loop(hours=24)
async def send_word_daily():
    await send_word()

async def send_word():
    """
    Send the word to the discord channel
    """
    content = get_content()
    if content:
        word=get_word(content[0].text)
        embed = discord.Embed(title=f"{content[0].text}", description=f"-> {content[1].text}\n-> {content[2].text}\n", color=0x00ff00)
        embed.add_field(name="", value=f"[Google it!](https://www.google.com/search?q={word})")
        await channel.send(embed=embed)

@client.event
async def on_ready():
    global channel
    channel = client.get_channel(keys.CHANNEL)
    send_word_daily.start()
    #send_word_daily.start(next_todo=datetime.time(10,0,0), unit='seconds')

if __name__ == "__main__":
    client.run(keys.TOKEN)
