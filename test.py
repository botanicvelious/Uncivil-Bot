import chat_downloader 
import discord
import re

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

        if re.search("(?P<url>https?://[^\s]+)", message.content) and message.channel.name == 'server-announcements':
            channel = discord.utils.get(message.guild.channels, name="test123")
            url = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
            await message.reply("getting chat from " +url)
            chat = chat_downloader.ChatDownloader().get_chat(url)       # create a generator
            emoji = '\N{WHITE HEAVY CHECK MARK}'
            await channel.send("test")
            for text in chat:                        # iterate over messages
                if text["message"].lower().startswith("@uncivil law") or text["message"].lower().startswith("question"):
                    try :
                        if "Moderator" in text["author"]["badges"][0]["title"]:
                            message_id = await channel.send('''```'''+text["author"]["name"]+''' (Moderator) :```'''+ text["message"])
                        elif "member" in text["author"]["badges"][0]["title"]:
                            message_id = await channel.send('''```'''+text["author"]["name"]+''' (Member) :```'''+ text["message"])
                        else:
                            message_id = await channel.send('''```'''+text["author"]["name"]+''':```'''+ text["message"])
                    except KeyError:
                        message_id = await channel.send('''```'''+text["author"]["name"]+''':```'''+ text["message"])
                        pass
                    await message_id.add_reaction(emoji)
            

client = MyClient()
client.run('token')
