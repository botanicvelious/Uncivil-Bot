import chat_downloader 
import discord

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

        if message.content.startswith('https://www.youtube.com'):
            await message.reply("getting chat from " +message.content+ " from user "+message.author.id, mention_author=True)
            url = message.content
            chat = chat_downloader.ChatDownloader().get_chat(url)       # create a generator
            for text in chat:                        # iterate over messages
                if text["message"].lower().startswith("@uncivil law") or text["message"].lower().startswith("question"):
                    try :
                        if "Moderator" in text["author"]["badges"][0]["title"]:
                            await message.channel.send('''```'''+text["author"]["name"]+''' (Moderator) :```'''+ text["message"])
                        elif "member" in text["author"]["badges"][0]["title"]:
                            await message.channel.send('''```'''+text["author"]["name"]+''' (Member) :```'''+ text["message"])
                        else:
                            await message.channel.send('''```'''+text["author"]["name"]+''':```'''+ text["message"])
                    except KeyError:
                        await message.channel.send('''```'''+text["author"]["name"]+''':```'''+ text["message"])
                        pass
                    #await message.channel.send(text["message"])
            

client = MyClient()
client.run('token')
