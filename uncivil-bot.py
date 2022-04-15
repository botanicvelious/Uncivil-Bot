import chat_downloader
import discord
import re
import asyncio
import json
from functools import partial
import os
import string
import random
from pytchat import LiveChatAsync
import pytchat
import traceback
from urllib.parse import urlparse, parse_qs

token = open("token", "r").read()


class MyClient(discord.Client):
    def get_yt_video_id(self, url):
        """Returns Video_ID extracting from the given url of Youtube
        
        Examples of URLs:
          Valid:
            'http://youtu.be/_lOT2p_FCvA',
            'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
            'http://www.youtube.com/embed/_lOT2p_FCvA',
            'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
            'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
            'youtube.com/watch?v=_lOT2p_FCvA',
          
          Invalid:
            'youtu.be/watch?v=_lOT2p_FCvA',
        """
        
        if url.startswith(('youtu', 'www')):
            url = 'http://' + url
            
        query = urlparse(url)
        
        if 'youtube' in query.hostname:
            if query.path == '/watch':
                doreturn = parse_qs(query.query)['v'][0]
            elif query.path.startswith(('/embed/', '/v/')):
                doreturn = query.path.split('/')[2]
        elif 'youtu.be' in query.hostname:
            doreturn = query.path[1:]
        if doreturn.find("?") != -1:
            urlstr = doreturn.split("?", 1)
            return urlstr[0]
        else:
            return doreturn

    async def checkmessagesfunc(self, chatdata, message):
        channel = discord.utils.get(
            message.guild.channels, name="bot-for-questions")
        superchatchannel = discord.utils.get(
            message.guild.channels, name="bot-for-superchats")
        emoji = '\N{WHITE HEAVY CHECK MARK}'

        for c in chatdata.items:
            #print(f"{c.datetime} [{c.author.name}]-{c.message} {c.type} {c.amountString} {c.type}")
            if c.type == "superChat":
                embedVar = discord.Embed(
                    title="SUPERCHAT "+c.amountString, description="-"+c.author.name, color=0x00ff00)
                embedVar.add_field(
                    name="Message", value="-"+c.message, inline=False)
                await superchatchannel.send(embed=embedVar)
            elif c.message.lower().startswith("@uncivil law") or c.message.lower().startswith("question"):
                message_id = await channel.send('''```'''+c.author.name+''':```''' + c.message)
                await message_id.add_reaction(emoji)
            #else:
            #    await channel.send('''```'''+c.author.name+''':```''' + c.message)
            await chatdata.tick_async()

    async def dumpchat(self, message):
        res = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))
        try:
            channel = message.channel
            url = re.search(
                "(?P<url>https?://[^\s]+)", message.content).group("url")

            await channel.send(f'Getting chat for <{url}>')
            chat = chat_downloader.ChatDownloader().get_chat(url)       # create a generator

            if os.path.exists(res):
                os.remove(res)
            stringprint = []
            for message in chat:                        # iterate over messages
                stringprint.append(chat.format(message)+"\n")
            with open(res, "w", encoding="UTF-8") as file:
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
        channel = discord.utils.get(
            server.channels, name=name, type=discord.ChannelType.text)
        await bot.send_message(channel, *args, **kwargs)

    async def background_task(self, message):
        try:
            channel = discord.utils.get(
                message.guild.channels, name="bot-for-questions")
            superchatchannel = discord.utils.get(
                message.guild.channels, name="bot-for-superchats")

            url = re.search(
                "(?P<url>https?://[^\s]+)", message.content).group("url")
            urlstr = self.get_yt_video_id(url)

            await channel.send(f'Parsing chat for <{url}>')

            livechat = LiveChatAsync(str(urlstr), callback=(
                lambda chatdata: self.checkmessagesfunc(chatdata, message)))
            while livechat.is_alive():
                await asyncio.sleep(3)
            try:
                livechat.raise_for_status()
            except pytchat.ChatDataFinished:
                await channel.send(f'Chat data finished.')
            except Exception as e:
                print(type(e), str(e))
                await channel.send(str(e))

            #await channel.purge(limit=9000, bulk=False)
            await channel.send(f'Done parsing chat for <{url}> so channel cleared!')
            #await superchatchannel.purge(limit=9000, bulk=False)
            await superchatchannel.send(f'Done parsing chat for <{url}> so channel cleared!')

        except Exception as e:
            traceback.print_exc()
            await channel.send(e)

    async def on_message(self, message):

        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        # check for !getchat
        if re.search(r"\byoutube|youtu\b", message.content) and message.content.lower().startswith("!getchat"):
            self.bg_task = self.loop.create_task(self.dumpchat(message))

        # get questions
        if re.search(r"\byoutube|youtu\b", message.content) and (message.channel.name == 'bot-for-questions' or message.channel.name == 'server-announcements'):
            self.bg_task = self.loop.create_task(self.background_task(message))


client = MyClient()
client.run(token)
