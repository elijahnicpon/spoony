import discord
import pygsheets
import pandas as pd
from datetime import datetime

'''INIT GOOGLE SHEETS'''
#authorization
gc = pygsheets.authorize(service_file= ${{ secrets.googleSheetsAuthServiceFile }})
# Create empty dataframe
df = pd.DataFrame()
# Create a column

#open the google spreadsheet (where 'Spoon Assasins!' is the name of my sheet)
sheets = gc.open('Spoon Assassins!')
#select the first sheet 
# wks = sh[0]
# #update the first sheet with df, starting at cell B2. 
# wks.set_dataframe(df,(1,1))

'''INIT DISCORD'''
TOKEN = ${{ secrets.discordToken }}
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("logged in!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$register') and message.channel.name == 'kill-feed':

        registered_name = message.content.split(" ", 1)[1]
        discord_id = message.author.id

        newrow = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), discord_id, registered_name]
        worksheet = sheets[0]
        cells = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
        last_row = len(cells)
        worksheet = worksheet.insert_rows(last_row, number=1, values= newrow)

        await message.channel.send(f'<@{message.author.id}>, you have been registered as "{registered_name}"')

    if message.content.startswith('$pooned') and message.channel.name == 'kill-feed':
        
        assassin = message.author.id
        assassinated = message.content.split('@')[1].split(' ')[0]

        newrow = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), assassin, assassinated]
        worksheet = sheets[1]
        cells = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
        last_row = len(cells)
        worksheet = worksheet.insert_rows(last_row, number=1, values= newrow)

        await message.channel.send(f'🥄🥄🥄<@{assassin}> has assassinated <@{assassinated}🥄🥄🥄')

    if message.content.startswith('$challenge') and message.channel.name == 'kill-feed':

        challenger = message.author.id
        challenged = message.content.split('@')[1].split(' ')[0]

        newrow = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), challenger, challenged]
        worksheet = sheets[2]
        cells = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
        last_row = len(cells)
        worksheet = worksheet.insert_rows(last_row, number=1, values= newrow)

        await message.channel.send(f'🥄🥄🥄<@{challenger}> has challenged <@{challenged}🥄🥄🥄\n<@{challenger}>, state your case in a reply to this messasge. <@{challenged}, make your defense in a reply to this message.')


client.run(TOKEN)


    