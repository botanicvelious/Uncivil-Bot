from chat_downloader import ChatDownloader

url = 'https://www.youtube.com/watch?v=frVrQ6NthAs'
chat = ChatDownloader().get_chat(url)       # create a generator
for message in chat:                        # iterate over messages
    print(chat.format(message))             # print the formatted message