import chat_downloader 
import discord
import re
from pytchat import LiveChatAsync
import asyncio
import json
from functools import partial 
import os
import string
import random

token = open("token","r").read()

class MyClient(discord.Client):

    async def checkmessagesfunc(self, chatdata, message):
        channel = discord.utils.get(message.guild.channels, name="bot-for-questions")
        emoji = '\N{WHITE HEAVY CHECK MARK}'
                            
        for c in chatdata.items:
            #print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString} ")
            if c.message.lower().startswith("@uncivil law") or c.message.lower().startswith("question"):
                message_id = await channel.send('''```'''+c.author.name+''':```'''+ c.message)
                await message_id.add_reaction(emoji)
                await chatdata.tick_async()
            else:
                await chatdata.tick_async()

    async def dumpchat(self, message):
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) 
        try: 
            channel = message.channel
            url = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
                    
            await channel.send(f'Getting chat for <{url}>')
            chat = chat_downloader.ChatDownloader().get_chat(url)       # create a generator
            
            if os.path.exists(res):
                os.remove(res)
            stringprint= []
            for message in chat:                        # iterate over messages
                stringprint.append(chat.format(message)+"\n")
            with open(res, "w", encoding = "UTF-8") as file:
                file.writelines(stringprint) 
                file.close()
            embed = discord.Embed()
            with open(res, "rb") as file:
                await channel.send("Chatlog file:", file=discord.File(file, "result.txt"))
                file.close()
            if os.path.exists(res):
                os.remove(res)
                
        except Exception as e:
            if os.path.exists(res):
                os.remove(res)            
            await channel.send(e)

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
            urlstr = urlstr[1].split("&",1)
                    
            await channel.send(f'Parsing chat for <{url}>')
            
            livechat = LiveChatAsync(urlstr[0], callback=(lambda chatdata:self.checkmessagesfunc(chatdata, message)), interruptable=False)
            while livechat.is_alive():
                await asyncio.sleep(1)               
                
            await channel.send("!clear 100000")
        except Exception as e:
            await channel.send(e)
            

    async def on_message(self, message):
        
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        
        #check for !getchat
        if re.search("(?P<url>https?://[^\s]+)", message.content) and message.content.lower().startswith("!getchat"):
            self.bg_task = self.loop.create_task(self.dumpchat(message))
            
        #get questions
        elif re.search("(?P<url>https?://[^\s]+)", message.content) and (message.channel.name == 'bot-for-questions' or message.channel.name == 'server-announcements'):
            self.bg_task = self.loop.create_task(self.background_task(message))

client = MyClient()
client.run(token)
