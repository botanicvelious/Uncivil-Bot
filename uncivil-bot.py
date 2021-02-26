import chat_downloader 
import discord
import re
from pytchat import LiveChatAsync
import asyncio
import json

token = open("token","r").read()

class MyClient(discord.Client):

    async def func(self, chatdata):
        channel = discord.utils.get(data.guild.channels, name="bot-for-questions")
        emoji = '\N{WHITE HEAVY CHECK MARK}'
                    
        for c in chatdata.items:
            print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString} ")
            if c.message.lower().startswith("@uncivil law") or c.message.lower().startswith("question"):
                message_id = await channel.send('''```'''+c.author.name+''':```'''+ c.message)
                await message_id.add_reaction(emoji)
            await chatdata.tick_async()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def report(server, name, *args, **kwargs):
        channel = discord.utils.get(server.channels, name=name, type=discord.ChannelType.text)
        await bot.send_message(channel, *args, **kwargs)

    async def background_task(self, message):
        try: 
            channel = discord.utils.get(message.guild.channels, name="bot-for-questions")
            url = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
            urlstr = url.split("=",1)
                    
            await channel.send(url)
            
            livechat = LiveChatAsync(urlstr[1], callback = self.func, interruptable=False, force_replay=True)
            while livechat.is_alive():
                await asyncio.sleep(.1)               
                
        except Exception as e:
            await channel.send(e)
            

    async def on_message(self, message):
    
        global data 
        data = message
        
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
            
        if re.search("(?P<url>https?://[^\s]+)", message.content) and (message.channel.name == 'bot-for-questions' or message.channel.name == 'server-announcements'):
            self.bg_task = self.loop.create_task(self.background_task(message))

client = MyClient()
client.run(token)
