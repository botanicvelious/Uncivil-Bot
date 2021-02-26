import chat_downloader 
import discord
import re

token = open("token","r").read()

async def get_messages(message):
    channel = discord.utils.get(message.guild.channels, name="bot-for-questions")
    url = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
    chat = chat_downloader.ChatDownloader().get_chat(url)       # create a generator
    emoji = '\N{WHITE HEAVY CHECK MARK}'
        
    await channel.send(url)
        
    async for text in chat:                        # iterate over messages
        if text["message"].lower().startswith("@uncivil law") or text["message"].lower().startswith("question"):
            string = chat.format(text)
            string = string.split('|', 1) 
            string = string[1].split(':', 1)
            message_id = await channel.send('''```'''+string[0]+''':```'''+ string[1])
            await message_id.add_reaction(emoji)
    
    await channel.send("Done getting all messages.")
    

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def report(server, name, *args, **kwargs):
        channel = discord.utils.get(server.channels, name=name, type=discord.ChannelType.text)
        await bot.send_message(channel, *args, **kwargs)

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
            
        if re.search("(?P<url>https?://[^\s]+)", message.content) and (message.channel.name == 'server-announcements' or message.channel.name == 'bot-for-questions'):
            client.loop.create_task(get_messages(message))

client = MyClient()
client.run(token)
