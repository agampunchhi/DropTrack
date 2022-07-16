import platform
from bs4.builder import TreeBuilder
from discord import channel, message
from discord.ext import tasks
import os
from datetime import datetime
import pytz
import discord
import Tracker
from bgTask import bgTask
import classes
import psycopg2
import priceDropPNG


ownerID = os.environ.get("OWNER_ID")
dbURL = os.environ.get('DATABASE_URL')
token = os.environ.get('BOT_TOKEN')

conn = psycopg2.connect(dbURL)
cur = conn.cursor()
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            
            print("Connected to database")
            createTable = """CREATE TABLE IF NOT EXISTS item (
                            id SERIAL PRIMARY KEY,
                            userid BIGINT NOT NULL, 
                            channel BIGINT NOT NULL,
                            title VARCHAR(500) NOT NULL,
                            price VARCHAR(255) NOT NULL,
                            url VARCHAR(1000) NOT NULL,
                            imgURL VARCHAR(1000))"""
            cur.execute(createTable)
            conn.commit()
        except psycopg2.DatabaseError as error:
            print(error)
        # start the task to run in the background
        self.my_background_task.start()
        self.priceDropChecker.start()


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="prices go down."))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('.track'):
            extractedURL = message.content.split()
            print("ExtractedURL: {}".format(extractedURL))
            for index in extractedURL[1:]:
                if (index.find('amazon.in') != -1) or (index.find('flipkart') != -1) or (index.find('myntra') != -1) or (index.find('tatacliq') != -1) or (index.find('127.0.0.1') != -1) or (index.find('hm') != -1):
                    user = message.author.id
                    channelID = message.channel.id
                    item = await Tracker.createItem(user, channelID, index, client)
                    addItem = """INSERT INTO item (userid, channel, title, price, url, imgURL) VALUES (%s, %s, %s, %s, %s, %s)"""
                    data = (user, channelID, item.title.strip(), item.price, item.url, item.imgURL)
                    try:
                        print("Connected to database on item add")
                        cur.execute(addItem, data)
                        print("Item added to database")
                        conn.commit()
                        if len(extractedURL) == 2:
                            await message.delete()
                            embed = discord.Embed(color= discord.Color.teal())
                            embed.add_field(name="**Item added**", value='[_{}_]({}) is now being tracked ✅ <@!{}>'.format(item.title.strip(), item.url, user), inline=False)
                            embed.set_thumbnail(url=item.imgURL)
                            await message.channel.send(embed=embed)
                        if index == extractedURL[-1] and len(extractedURL) > 2:
                            await message.delete()
                            await message.channel.send('Items are now being tracked ✅ <@!{}>'.format(user))
                    except psycopg2.DatabaseError as error:
                        print(error)
                else:
                    await message.delete()
                    await message.channel.send('Please enter a valid link ❌ <@!{}>'.format(message.author.id))
                
        if message.content.startswith('.stop'):
            cmd = message.content.split()
            if len(cmd) == 1:
                if(message.author.id != ownerID):
                    cur.execute("SELECT * FROM item WHERE userid = %s", (message.author.id,))
                else:
                    cur.execute("SELECT * FROM item")
                rows = cur.fetchall()
                if len(rows) != 0:
                    embed = discord.Embed(title="List of Items being tracked", description="To delete item, send .stop <id>", color= discord.colour.Color.teal())
                    embed.set_thumbnail(url="https://i.imgur.com/vh2Cjlq.png")
                    embed.add_field(name="ID        Title       Price", value="\u200b", inline=True)
                else:
                    await message.delete()
                    await message.channel.send('You have no items being tracked ❌ <@!{}>'.format(message.author.id))
                    return
                for row in rows:
                    if message.author.id == ownerID:
                        embed.add_field(name="\u200b", value="**{}**        [_{}_]({})        **{}**    **<@{}>**".format(row[0],row[3],row[5], row[4], row[1]), inline=False)
                    else:
                        embed.add_field(name="\u200b", value="**{}**        [_{}_]({})        **{}**".format(row[0],row[3],row[5], row[4]), inline=False)
                await message.channel.send(embed=embed)
            elif len(cmd) == 2:
                if(str(cmd[1]).lower() == "all" ):
                    cur.execute("SELECT * FROM item WHERE userid = %s", (message.author.id,))
                    rows = cur.fetchall()
                    if len(rows) != 0:
                        for row in rows:
                            cur.execute("DELETE FROM item WHERE id = %s", (row[0],))
                            conn.commit()
                            await message.delete()
                        await message.channel.send('All items have been deleted ✅ <@!{}>'.format(message.author.id))
                    else:
                        await message.delete()
                        await message.channel.send('You have no items being tracked ❌ <@!{}>'.format(message.author.id))
                else:
                    try:
                        if(message.author.id != ownerID):
                            cur.execute("SELECT * FROM item WHERE id = %s AND userid = %s", (cmd[1],message.author.id,))
                        else:
                            cur.execute("SELECT * FROM item WHERE id = %s", (cmd[1],))
                        rows = cur.fetchall()
                        if len(rows) == 0:
                            await message.delete()
                            await message.channel.send('Please enter a valid ID ❌ <@!{}>'.format(message.author.id))
                        else:
                            if(message.author.id != ownerID):
                                cur.execute("DELETE FROM item WHERE id = %s AND userid = %s", (cmd[1],message.author.id,))
                            else:
                                cur.execute("DELETE FROM item WHERE id = %s", (cmd[1],))
                            conn.commit()
                            await message.delete()
                            await message.channel.send('Item deleted ✅ <@!{}>'.format(message.author.id))
                    except psycopg2.DatabaseError as error:
                        print(error)

        if message.content.startswith('.invite'):
            invURl = 'https://discord.com/api/oauth2/authorize?client_id=890461132429594634&permissions=515396589632&scope=bot'
            embed = discord.Embed(title="Invite Link", description="**Click [here]({}) to invite me to your server**".format(invURl), color= discord.colour.Color.teal())
            embed.set_thumbnail(url="https://i.imgur.com/vh2Cjlq.png")
            await message.delete()
            await message.channel.send(embed=embed)

    @tasks.loop(seconds=60)
    async def priceDropChecker(self):
        timeZone = pytz.timezone('Asia/Kolkata')
        now = datetime.now(timeZone)
        currentTime = now.strftime("%H:%M:%S")
        timeComponents = currentTime.split(':')
        if(int(timeComponents[0])%12 == 0 and timeComponents[1] == '00'):
            print("BGTask called from time")
            await bgTask(client, dbURL)
            
                
    @tasks.loop(seconds=900) # task runs every 6 hours
    async def my_background_task(self):
        await bgTask(client, dbURL)
        

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

client = MyClient()
client.run(token)
