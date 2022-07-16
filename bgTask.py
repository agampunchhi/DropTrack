import platform
from bs4.builder import TreeBuilder
from discord import channel, message
from discord.ext import tasks
import os
import discord
import Tracker
import classes
import psycopg2
import priceDropPNG

trackList = []
nlaDict = []

ownerID = os.environ.get("OWNER_ID") # Get the bot owner's ID from the environment variable

async def bgTask(client,dbURL):
        print("Background Task")
        conn = psycopg2.connect(dbURL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM item")
        rows = cur.fetchall()
        trackList = []
        for row in rows:
            newItem = classes.Item(row[1], row[2], row[3], row[4], row[5], row[6])
            newItem.id = row[0]
            trackList.append(newItem)
        for item in trackList:
            currentPrice = "0"
            channel = client.get_channel(item.channel)
            currentPrice = await Tracker.checkPrice(client ,item.url)
            if currentPrice == "":
                currentPrice = "0"
            if currentPrice != "0":
                print(currentPrice)
            if currentPrice.find('\n') != -1:
                currentPrice = currentPrice.replace('\n', '.')
            if currentPrice.find(",") != -1:
                currentPrice = currentPrice.replace(',','')
            if currentPrice.find("MRP:") != -1:
                currentPriceFloat = float(currentPrice[6:])
            elif currentPrice.find("₹") != -1:
                currentPriceFloat = float(currentPrice[1:])
            elif currentPrice.find("Rs.") != -1:
                currentPriceFloat = float(currentPrice[3:])
            else:
                currentPriceFloat = float(currentPrice)
            print(item.title.strip() + " CurrentPrice: " + str(currentPrice))
            itemPrice = item.price
            print(item.title.strip() + " ItemPrice: " + str(itemPrice))
            if itemPrice == "":
                itemPrice = "0"
            if itemPrice.find(",") != -1:
                itemPrice = itemPrice.replace(',','')
            if itemPrice.find("MRP:") != -1:
                itemPriceFloat = float(itemPrice[6:])
            elif itemPrice.find("₹") != -1:
                itemPriceFloat = float(itemPrice[1:])
            elif itemPrice.find("Rs.") != -1:
                itemPriceFloat = float(itemPrice[3:])
            else:
                itemPriceFloat = float(itemPrice)
            if currentPriceFloat == 0:
                if item.id in nlaDict:
                    continue
                try:
                    nlaDict.append(item.id)
                    print(nlaDict)
                    print("Item Ignored from TrackList")
                except Exception as error:
                    print(error)
                continue
            if(currentPriceFloat < itemPriceFloat):
                print("Item Price: {} & Current Price: {}".format(item.price, currentPrice))
                print(item.title.strip())
                difference = itemPriceFloat - currentPriceFloat
                if difference >= 60:
                    embed = discord.Embed(title="\u200b", color= discord.colour.Color.teal())
                    print(item.title.strip(), item.price, currentPrice, item.imgURL)
                    embedLink = priceDropPNG.getPriceDropPNG(item.title.strip(), item.price, currentPrice, item.imgURL)
                    outputPath = './tmp/'+ item.title.strip().split()[0]+'.jpeg'
                    if embedLink != "":
                        print(embedLink)
                        file = discord.File(embedLink, filename="priceDrop.jpeg")
                        embed.set_image(url="attachment://priceDrop.jpeg")
                        embed.add_field(name="\u200b", value="[**Price Dropped!**]({}) <@!{}>".format(item.url, item.user), inline=False)
                        await channel.send("**🚨{}🚨**".format(item.title.strip()), file=file, embed=embed)
                        if os.path.exists(outputPath):
                            os.remove(outputPath)
                            print('Removed image file')
                    else:
                        embed.set_thumbnail(url=item.imgURL)
                        embed.add_field(name="\u200b", value="[**Price Dropped!**]({}) <@!{}>".format(item.url, item.user), inline=False)
                        embed.add_field(name="\u200b", value="**[_{}_]({})**".format(item.title.strip(), item.url), inline=False)
                        embed.add_field(name="**Old Price:**", value="**{}**".format(item.price), inline=False)
                        embed.add_field(name="**New Price:**", value="**{}**".format(currentPrice), inline=True)
                        embed.add_field(name="**Difference:**", value="**₹{}**".format(difference), inline=False)
                        await channel.send(embed=embed)
            if(currentPriceFloat != itemPriceFloat):
                try:
                    if item.id in nlaDict:
                        nlaDict.remove(item.id)
                        print(nlaDict)
                    updateItem = """UPDATE item SET price = %s WHERE id = %s"""
                    data = (currentPrice, item.id)
                    cur.execute(updateItem, data)
                    conn.commit()
                    print("Item Price Updated")
                except psycopg2.DatabaseError as error:
                    print(error)
        print("Finished parsing through trackList")
