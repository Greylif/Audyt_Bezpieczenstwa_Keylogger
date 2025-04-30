# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
from supabase import *
import asyncio

#Supabase
url = "https://gurjbecyjphjhrhihnwv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1cmpiZWN5anBoamhyaGlobnd2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTA2NDI3NSwiZXhwIjoyMDYwNjQwMjc1fQ.ITRY-7aTl_M8eltm_MacrD_t3JeC2MBVBEzF8ae6J-g"
supabase: Client = create_client(url, key)

response = supabase.table("Keys").select("*").execute()

#Discordo
Token = ''
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')

@bot.command(name='MONSTEREK')
async def fetch_users(ctx):
    # Pobieranie danych z Supabase
    response = supabase.table("Mouse").select("*").execute()
    keys = response.data

    if not keys:
        await ctx.send("Brak paliwa ;-;")
        return

    # Przygotowanie wiadomości
    message = "**Jedyne monsterki jaki były:**\n"
    messages_to_send = []  # lista wiadomości do wysłania

    for key in keys:
        create = key.get("created_at", "Brak daty")
        click = key.get("data", "Brak przycisku")
        line = f"- {create}, {click}\n"

        # Jeśli nowa linijka spowoduje przekroczenie limitu
        if len(message) + len(line) > 2000:
            messages_to_send.append(message)
            message = ""  # zacznij nową wiadomość

        message += line

    # Dodaj ostatnią wiadomość (jeśli coś zostało)
    if message:
        messages_to_send.append(message)

    # Wysyłanie wszystkich wiadomości
    for msg in messages_to_send:
        await ctx.send(msg)

@bot.command(name='PIWO')
async def fetch_users(ctx):
    # Pobieranie danych z Supabase
    response = supabase.table("Keys").select("*").execute()
    keys = response.data

    if not keys:
        await ctx.send("Brak piwa ;-;")
        return

    # Przygotowanie wiadomości
    message = "**Jedyne piwo jakie było::**\n"
    messages_to_send = []  # lista wiadomości do wysłania

    for key in keys:
        create = key.get("created_at", "Brak daty")
        click = key.get("buttons", "Brak przycisku")
        line = f"- {create}, {click}\n"

        # Jeśli nowa linijka spowoduje przekroczenie limitu
        if len(message) + len(line) > 2000:
            messages_to_send.append(message)
            message = ""  # zacznij nową wiadomość

        message += line

    # Dodaj ostatnią wiadomość (jeśli coś zostało)
    if message:
        messages_to_send.append(message)

    # Wysyłanie wszystkich wiadomości
    for msg in messages_to_send:
        await ctx.send(msg)

bot.run(Token)
