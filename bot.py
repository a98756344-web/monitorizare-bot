import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Server Web Secundar pentru menținerea activității 24/7 pe hosting
app = Flask('')

@app.route('/')
def home():
    return "Sistemul de monitorizare este online 24/7!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()

# Intențiile complete pentru citirea statusului utilizatorilor
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True  

bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)

# Noul tău token configurat direct în execuție
TOKEN = "MTUxOTYwMjM1MjYzMjYyNzIzMA.GjzjjQ.oLgUv6SBFPCNZ7wEc9Z71Kfi19-aqWuUtlATOw"
SERVER_TAG = "https://discord.gg"  
ROLE_ID = 1517233325083726014  

@bot.event
async def on_ready():
    print(f"[-] SCRIPT 24/7 REPARAT: Sistem de monitorizare activ.")
    print(f"[-] Conectat ca: {bot.user.name} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="Prefix: + | Tag & Status Monitor"))

def check_user_eligibility(member):
    # Criteriul 1: Verificare link server în Nume sau Nickname
    has_tag = (SERVER_TAG.lower() in member.name.lower()) or \
              (member.nick and SERVER_TAG.lower() in member.nick.lower())
    
    # Criteriul 2: Verificare text "/kkk" în Custom Status (Stare personală)
    has_status = False
    if member.activities:
        for activity in member.activities:
            if isinstance(activity, discord.CustomActivity):
                status_text = ""
                if hasattr(activity, 'text') and activity.text:
                    status_text = activity.text.lower()
                elif activity.name:
                    status_text = activity.name.lower()
                
                if "/kkk" in status_text:
                    has_status = True
                    break
                    
    return has_tag or has_status

@bot.event
async def on_presence_update(before, after):
    if after.bot: return
    guild = after.guild
    role = guild.get_role(ROLE_ID)
    if not role: return

    if check_user_eligibility(after):
        if role not in after.roles:
            try: 
                await after.add_roles(role)
                print(f"[+] Rol oferit automat lui {after.name} (Status/Tag detectat)")
            except Exception: pass
    else:
        if role in after.roles:
            try: 
                await after.remove_roles(role)
                print(f"[-] Rol scos automat de la {after.name} (A șters statusul/tag-ul)")
            except Exception: pass

@bot.event
async def on_member_update(before, after):
    if after.bot: return
    guild = after.guild
    role = guild.get_role(ROLE_ID)
    if not role: return

    if check_user_eligibility(after):
        if role not in after.roles:
            try: 
                await after.add_roles(role)
                print(f"[+] Rol oferit automat lui {after.name} (Nume/Nick modificat)")
            except Exception: pass
    else:
        if role in after.roles:
            try: 
                await after.remove_roles(role)
                print(f"[-] Rol scos automat de la {after.name} (A șters tag-ul din nume)")
            except Exception: pass

keep_alive()
bot.run(TOKEN)
