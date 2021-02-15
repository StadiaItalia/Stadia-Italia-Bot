from asyncio.exceptions import SendfileNotAvailableError
import discord
from discord import message # Per discord
from discord.ext import commands # Per discord
import random # Per funzioni randomiche
import logging 
from pathlib import Path # Per gestire i path
import datetime
import asyncio
import os
import json # Per file json
from discord.utils import get
import pymongo # Per DB
from pymongo import MongoClient # Per DB

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

# Definizione variabili
intents = discord.Intents.default()
intents.members = True

secret_file = json.load(open(cwd+'\\bot_config\\secrets.json'))
bot = commands.Bot(command_prefix=".", intents=intents)
bot.config_token = secret_file['token']
bot.connection_url = secret_file['mongo']
#logging.basicConfig(level=logging.INFO)

albicocco_string = [
                 "Stadia chiude?",
                 "Che motore grafico usa Fifa?",
                 "Kalamaygiò...KALAMAHO! Invited to the gaaaame!",
                 "Che chioma fluente!",
                 "Vacca Boia!",
                 "Chro è un lui o una lei?",
                 "Ci sono donne su sto server?",
                 "Regola n°1 di Stadia Italia? Non toccatemi Facchinetti",
                 "Salutate tutti, sua maestà MikkaVez!",
                 "Oh ma i ruoli nuovi? Vogliamo i colori !1!111!!",
                 "Albicocche..albicocche ovunque!",
                 "Ce nge na ma scì sciamanìnne, ce non ge na ma scì non ge ne sime scènne!",
                 "Mei murė sufegá dala brügna che dal biönc",
                 "Mi sono appena fermato a un supermercato svizzero a prendere un panino. Ho chiesto un francese con il prosciutto cotto. Mi hanno risposto che il francese in Svizzera non esiste, si chiama birichino…Buon dio.",               
                 "Il problema non sono le 3 ragazze su 180.... è l'1 Mikkaels su 180!",
                 "Secondo voi Google me lo fa cambiare il Nick di Stadia in albicocco giusto per la partita di sta sera e poi tornare kalamajo oppure mi sputa in faccia?",
                 "3 chiavi dorate, il codice scade domani!",
                 "Se un designer è anche coder diventa un decoder?",
                 "https://tenor.com/view/shrek-princess-fiona-when-the-caffeine-hits-when-the-dick-too-good-dick-too-good-gif-5611089"
                ]

macchina_blu = [
                 "La macchina di Bluewine è talmente sporca che se passa a Cervinia con tutta quella neve dopo pare Detroit degli anni '60",               
                 "La macchina di bluewine è cosi sporca che quando la fermano i carabinieri al posto di patente e libretto chiedono spugna e sapone",
                 "La macchina di bluewine è così sporca che quando parte lascia la polvere come Beep beep",
                 "La macchina di bluewine è così sporca che è la controfigura della Batmobile in Batman Arkham lavaggio a mano",
                 "La macchina di Blue è così sporca che è riuscita ad incrostare pure il sistema predittivo della mia tastiera",
                 "La macchina di Blue è così sporca che al semaforo i lavavetri le chiedono pagamento con bonifico",
                 "La macchina di Blue è così sporca che anche Walter White quando ti vede arrivare chiude il bandone (breaking bad who dis?)",
                 "La macchina di Blue è così sporca che per azionare il tergicristallo ci vuole il porto d'armi",
                 "La macchina di Blue è così sporca che per mettere la freccia a sinistra deve abbassare il finestrino e fare cenno con la mano",
                 "La macchina di Blue è così sporca che quando va a fare benzina non trovano il buco per la pompa",
                 "La macchina di Blue è talmente sporca che sono i Fixer a pagarti per portarla via #🌃｜night_city",
                 "La macchina di Blue è così sporca che hanno provato a lavarla nel Gange ed è risultato più pulito il fiume",
                 "La macchina di Blue è così sporca che d'estate non ha bisogno di mettere il parasole sul parabrezza",
                 "La macchina di Blue è così sporca che quando passa è la strada ad essere più nera di prima"
                ]

# Inizializzo il bot
@bot.event
async def on_ready() :
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game("Pronto all'azione! .help per info"))
    print("Sono online! :)")

# Invio DM di benvenuto e messaggio su canale
@bot.event
async def on_member_join(member):
    print("è entrato l'utente :" + member.name)
    channel = discord.utils.get(member.guild.channels, name="generale") #da modificare in salotto
    embed = discord.Embed(
        colour = (discord.Colour.magenta()),
        title = 'Messaggio di Benvenuto',
        description = f'Ciao e benvenuto sul server discord di Stadia Italia {member.mention}.'
    )
    await member.send(embed=embed)
    await channel.send(f'Diamo tutti il benvenuto a {member.mention} !')
    
# Comando albicocco, per display frasi divertenti di Stadia Italia
@bot.command()
async def albi(ctx) :
    imageURL = "http://www.wetoo.viandanza.it/wp-content/uploads/2017/07/ALBICOCCA.jpg"
    embed = discord.Embed(
        colour = (discord.Colour.green()),
        title = 'Albicocco dice 🥭',
        description = (random.choice(albicocco_string))
    )
    embed.set_thumbnail(url=imageURL)
    await ctx.message.channel.send(embed=embed)

# Comando blu, per display frasi divertenti sulla macchina di Bluewine
@bot.command()
async def blu(ctx) :
    imageURL = "https://cdn.images.express.co.uk/img/dynamic/24/590x/Dirty-car-596260.jpg"
    embed = discord.Embed(
        colour = (discord.Colour.blue()),
        title = 'Brum Brum 🚗',
        description = (random.choice(macchina_blu))
    )
    embed.set_thumbnail(url=imageURL)
    await ctx.message.channel.send(embed=embed)

# Prova connessione al db - da rifare
@bot.command()   
async def db(ctx) :
    cluster = MongoClient(bot.connection_url)
    db = cluster["database"]
    collection = db["new"]

    
    ping_cm = {"Messaggio_benvenuto": "ciao"}
    collection.insert_one(ping_cm)

    await ctx.channel.send("Messaggio di benvenuto aggiornato ")


bot.run(bot.config_token)
