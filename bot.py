import sys,os
import numpy as np
from PIL import Image
import wikipedia
from wordcloud import WordCloud,STOPWORDS
from pyrogram import Client,Filters
import time

app = Client(
    "wordart_bot",
    api_id= "api id here",
    api_hash="api hash here",
    bot_token="bot token here"
)


@app.on_message(Filters.command(["start"]))
def start(client, message):
    client.send_message(
        chat_id=message.chat.id,
        text=f"Hi {message.from_user.first_name}"
      )
    client.send_message(
           chat_id=message.chat.id,
           text="Enter the Word to make wordcloud"
      )

@app.on_message(Filters.text)
def echo(client, message):
    img_path = f"./downloads/{message.chat.id}/"
    if not os.path.isdir(img_path):   
        os.makedirs(img_path)
    image = img_path + "image.png"
    pro = client.send_message(
       chat_id = message.chat.id,
       text = "Processing...",
       reply_to_message_id=message.message_id
    )
    msg=message.text
    title=wikipedia.search(msg)[0]
    page=wikipedia.page(title)
    texxt=page.content
    background=np.array(Image.open("cloud.png"))
    stopwords=set(STOPWORDS)
    wc=WordCloud(background_color="white",
                max_words=200,
                mask=background,
                stopwords=stopwords)
    wc.generate(texxt)
    wc.to_file(image)
    pro.edit("Uploading to telegram")
    client.send_photo(
          chat_id=message.chat.id,
          photo=image,
          caption = f"wordcloud for __{msg}__",         
          reply_to_message_id=message.message_id          
    )
    pro.delete()
app.run()
