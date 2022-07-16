![Header](https://i.imgur.com/vh2Cjlq.png | width=150 "Header")

# DropTrack Discord Bot
 DropTrack tracks prices from various ecommerce sites and notifies the user of any price drops on items they want to track.
# Supported Websites
 DropTrack currently supports the following websites - `Flipkart | Amazon India | Myntra | TataCliq | H&M India`

# How to run DropTrack

- Clone this repository.
- Install the required packages for Python3 using this command in terminal - `pip3 install -r requirements.txt`
- Set up the environment and add the following environment variables -
  -`DATABASE_URL` - The URL for your PostgreSQL Database
  -`BOT_TOKEN` - Token for your discord bot application obtained from Discord Developer Portal
  -`OWNER_ID` - The Discord User ID for the bot owner
- Run the bot using the following command - `python3 main.py`

# DropTrack Bot Commands

- `.track <Product Link>` - Adds the product to the users tracking list and checks frequently for price drops.
- `.stop` - Shows the list of products being tracked by the bot for the user.
- `.stop <ID>` - Deletes the corresponding product from the tracking list for the user.
- `.invite` - Sends an invite link to invite the bot into another server.
