import chat_downloader 
import discord
import re

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if re.search("(?P<url>https?://[^\s]+)", message.content) and message.channel.name == 'test':
            print(message.guild.id)
            url = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
            await message.reply("getting chat from " +url)
            chat = chat_downloader.ChatDownloader().get_chat(url)       # create a generator
            emoji = '\N{WHITE HEAVY CHECK MARK}'
            for text in chat:                        # iterate over messages
                if text["message"].lower().startswith("@uncivil law") or text["message"].lower().startswith("question"):
                    try :
                        if "Moderator" in text["author"]["badges"][0]["title"]:
                            message_id = await message.channel.send('''```'''+text["author"]["name"]+''' (Moderator) :```'''+ text["message"])
                        elif "member" in text["author"]["badges"][0]["title"]:
                            message_id = await message.channel.send('''```'''+text["author"]["name"]+''' (Member) :```'''+ text["message"])
                        else:
                            message_id = await message.channel.send('''```'''+text["author"]["name"]+''':```'''+ text["message"])
                    except KeyError:
                        message_id = await message.channel.send('''```'''+text["author"]["name"]+''':```'''+ text["message"])
                        pass
                    await message_id.add_reaction(emoji)
            

client = MyClient()
client.run('NzIwMDQ0MzM4MDk2MzczNzYz.XuAPiw.DxUTycQ5aB7txErc24cgYd3cvA8')
