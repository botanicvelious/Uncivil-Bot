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
            print('*****')
            chat = chat_downloader.ChatDownloader().get_chat(url)       # create a generator
            print('*****')
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
client.run('NzIwMDQ0MzM4MDk2MzczNzYz.XuAPiw.9Uz_lAAkyjSWKDWUZXQ1gACvSww')

"""
{
   "time_in_seconds":4995.866,
   "action_type":"add_chat_item",
   "message":"Thanks Kurt!!! 😁",
   "message_id":"CjoKGkNLcklxZHoyNWU0Q0ZZeUxnZ29kSmE4UDJREhxDSmlQblpIbTVlNENGV0hIRmdrZDdPUU04QTU5",
   "timestamp":1613187225658185,
   "time_text":"1:23:15",
   "author":{
      "name":"Betty Boop",
      "images":[
         {
            "url":"https://yt3.ggpht.com/ytc/AAUvwnimk_UGDezC7n6fr33-ij5Rwpybsc8bpxHvjA",
            "id":"source"
         },
         {
            "url":"https://yt3.ggpht.com/ytc/AAUvwnimk_UGDezC7n6fr33-ij5Rwpybsc8bpxHvjA=s32-c-k-c0x00ffffff-no-rj",
            "width":32,
            "height":32,
            "id":"32x32"
         },
         {
            "url":"https://yt3.ggpht.com/ytc/AAUvwnimk_UGDezC7n6fr33-ij5Rwpybsc8bpxHvjA=s64-c-k-c0x00ffffff-no-rj",
            "width":64,
            "height":64,
            "id":"64x64"
         }
      ],
      "badges":[
         {
            "title":"Moderator",
            "icon_name":"moderator"
         },
         {
            "title":"New member",
            "icons":[
               {
                  "url":"https://yt3.ggpht.com/qwZj1KPvLGNjaal7fWIWkw_W3flkDocxxhZGT7nbrMjIRII0TyrgxsfHvh6dJg21UlG7Hbx0ARY",
                  "id":"source"
               },
               {
                  "url":"https://yt3.ggpht.com/qwZj1KPvLGNjaal7fWIWkw_W3flkDocxxhZGT7nbrMjIRII0TyrgxsfHvh6dJg21UlG7Hbx0ARY=s16-c-k",
                  "width":16,
                  "height":16,
                  "id":"16x16"
               },
               {
                  "url":"https://yt3.ggpht.com/qwZj1KPvLGNjaal7fWIWkw_W3flkDocxxhZGT7nbrMjIRII0TyrgxsfHvh6dJg21UlG7Hbx0ARY=s32-c-k",
                  "width":32,
                  "height":32,
                  "id":"32x32"
               }
            ]
         }
      ],
      "id":"UC-DfmVdVan5TEfoqnEbAqag"
   },
   "message_type":"text_message"
}    
"""