import os
import time
import discord
from discord.ext import tasks
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

# Set up aliases for the environment variables.
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL')
PLAYING = os.getenv('PLAYING')

# Format activity from .env file for use in the init.
activity = (discord.Game(name=str(PLAYING)))

# Discord Init
intents = discord.Intents.default()
client = discord.Client(intents=intents, activity=activity, status=discord.Status.idle)

# Google Init
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = Credentials.from_service_account_file(GOOGLE_SHEETS_CREDENTIALS, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Global variable to store spreadsheet data and sent messages
spreadsheet_data = []
sent_messages = set()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    load_sent_messages()
    load_spreadsheet_data()
    send_scheduled_messages.start()
    reload_spreadsheet_data.start()

def load_spreadsheet_data():
    global spreadsheet_data
    sheet = service.spreadsheets()
    try:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Formatted-For-Bot!A5:C').execute()
        spreadsheet_data = result.get('values', [])
        #print(spreadsheet_data)
    except Exception as e:
        print(f"Error loading spreadsheet data: {e}")
        restart_program()

def load_sent_messages():
    global sent_messages
    if os.path.exists('sent_messages.txt'):
        with open('sent_messages.txt', 'r') as file:
            sent_messages = set(file.read().splitlines())

def save_sent_message(message_content):
    with open('sent_messages.txt', 'a') as file:
        file.write(message_content + '\n')

def restart_program():
    print("Restarting program...")
    os._exit(1)

@tasks.loop(minutes=1)
async def send_scheduled_messages():
    global spreadsheet_data, sent_messages
    try:
        for row in spreadsheet_data:
            if not row or len(row) < 3 or not all(row):
                continue
            message_content, scheduled_time, time_zone = row
            scheduled_time = datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')
            tz = pytz.timezone(time_zone)
            scheduled_time = tz.localize(scheduled_time)
            now = datetime.now(pytz.utc)
            ten_minutes_ago = now - timedelta(minutes=10)
            #print(spreadsheet_data)
            if ten_minutes_ago <= scheduled_time <= now and message_content not in sent_messages:
                channel = client.get_channel(int(CHANNEL_ID))
                await channel.send(message_content)
                print(f"{datetime.now()} - Message Sent: {message_content}")
                sent_messages.add(message_content)
                save_sent_message(message_content)
    except Exception as e:
        print(f"Error in send_scheduled_messages: {e}")
        restart_program()

@tasks.loop(minutes=1)
async def reload_spreadsheet_data():
    try:
        load_spreadsheet_data()
        print(f"{datetime.now()} - Spreadsheet data reloaded")
    except Exception as e:
        print(f"Error in reload_spreadsheet_data: {e}")
        restart_program()

client.run(DISCORD_TOKEN)
