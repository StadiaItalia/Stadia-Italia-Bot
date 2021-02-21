import traceback

from discord import colour
import modules.configuration as configuration
import random
import discord as discord
from discord.ext import commands

from modules.albicocco import albicocco_string
from modules.blue import macchina_blu

intents = discord.Intents.default()
intents.members = True


class StadiaItaliaBot(discord.ext.commands.Bot):
    def __init__(self, database, logger):
        super(StadiaItaliaBot, self).__init__(command_prefix="s!", intents=intents)
        self.database = database
        self.logger = logger

    async def on_error(self, event_method, *args, **kwargs):
        self.logger.error(f"Something went wrong: {event_method}")
        traceback.print_exc()

    @staticmethod
    def run_bot(database, logger, token):
        stadia_italia_bot = StadiaItaliaBot(database=database, logger=logger)

        @stadia_italia_bot.event
        async def on_ready():
            await stadia_italia_bot.change_presence(status=discord.Status.idle,
                                                activity=discord.Game("Pronto all'azione! s! help per la lista comandi"))
            logger.info(f"{stadia_italia_bot.user} è connesso a Discord!")

        @stadia_italia_bot.event
        async def on_guild_join(guild):
         logger.info(f"Stadia Italia Bot è stato aggiunto nel server {guild.name}")
         logger.debug(f"Creo una configurazione di default per {guild.name} - {guild.id}")
         database.create_configuration(guild_id=guild.id)

        @stadia_italia_bot.event
        async def on_guild_remove(guild):
         logger.info(f"Stadia Italia Bot è stato rimosso dal server {guild.name}")
         logger.info(f"Cancello la configurazione per  {guild.name} - {guild.id}")
         database.remove_configuration(guild_id=guild.id)

        # Evento membro join su server : invia un messaggio di benvenuto privato e nel canale specificato di benvenuto
        @stadia_italia_bot.event
        async def on_member_join(member):
            logger.info(f"Utente {member.name} entrato in {member.guild.name}")
            configuration = database.read_configuration(guild_id=member.guild.id)
            if configuration:
                if configuration.welcome_channel and len(configuration.welcome_message_list) > 0:
                    channel = discord.utils.get(member.guild.channels, name=configuration.welcome_channel)
                    await channel.send(f'{configuration.welcome_message_list} {member.mention}!')

            embed = discord.Embed(
                colour=(discord.Colour.magenta()),
                title='Messaggio di Benvenuto',
                description=(f'{configuration.welcome_direct_message}')
            )
            await member.send(embed=embed) 

        # Comando albicocco, per display frasi divertenti di Stadia Italia
        async def albi(message):
            imageURL = "http://www.wetoo.viandanza.it/wp-content/uploads/2017/07/ALBICOCCA.jpg"
            embed = discord.Embed(
             colour=(discord.Colour.green()),
             title='Albicocco dice 🥭',
             description=(random.choice(albicocco_string))
            )
            embed.set_thumbnail(url=imageURL)
            await message.channel.send(embed=embed)

        # Comando blu, per display frasi divertenti sulla macchina di Bluewine
        async def blu(message):
            imageURL = "https://cdn.images.express.co.uk/img/dynamic/24/590x/Dirty-car-596260.jpg"
            embed = discord.Embed(
                colour=(discord.Colour.blue()),
                title='Brum Brum 🚗',
                description=(random.choice(macchina_blu))
            )
            embed.set_thumbnail(url=imageURL)
            await message.channel.send(embed=embed)

        # Comando info, mostra la lista dei comandi utilizzabili e le configurazioni attuali corrispondenti
        async def info(message):
            configuration = database.read_configuration(guild_id=message.guild.id)
            if configuration:
                embed = discord.Embed(
                    colour=(discord.Colour.purple()),
                    title='📔 Lista comandi 📔',
                    description='Qui troverete tutti i comandi disponibili con le rispettive configurazioni attuali'
                )
                embed.add_field(name=f"{configuration.command_prefix} ruolo",
                        value=f"Corrente: {configuration.role}"+
                        "\nDescrizione: Comando per scegliere quale ruolo può usare i comandi del bot",
                        inline=False)
                embed.add_field(name=f"{configuration.command_prefix} prefix",
                        value=f"Corrente: {configuration.command_prefix}"+
                        "\nDescrizione: Comando per cambiare il prefix per i comandi del bot",
                        inline=False)
                embed.add_field(name=f"{configuration.command_prefix} canale_bot",
                        value=f"Corrente: {configuration.command_channel}"+
                        "\nDescrizione: Comando per cambiare il canale per i comandi del bot",
                        inline=False)
                embed.add_field(name=f"{configuration.command_prefix} canale_benvenuto",
                        value=f"Corrente: {configuration.welcome_channel}"+
                        "\nDescrizione: Comando per cambiare il canale di benvenuto",
                        inline=False)
                embed.add_field(name=f"{configuration.command_prefix} mod_benvenuto",
                        value=f"Corrente: {configuration.welcome_message_list}"+
                        "\nDescrizione: Comando per cambiare il messaggio di benvenuto in canale"+
                        "\n(la menzione per il nuovo arrivato è già integrata a fine messaggio)",
                        inline=False)
                embed.add_field(name=f"{configuration.command_prefix} mod_DM",
                        value=f"Corrente: {configuration.welcome_direct_message}"+
                        "\nDescrizione: Comando per cambiare il messaggio di benvenuto privato (DM)",
                        inline=False)
                embed.add_field(name=f"{configuration.command_prefix} albi",
                        value=f"Descrizione: mostra una delle tante citazioni divertenti della community Stadia Italia ",
                        inline=False)
                embed.add_field(name=f"{configuration.command_prefix} blu",
                        value=f"Descrizione: mostra una citazione divertente sulla macchina di Bluewine ",
                        inline=False)
                await message.channel.send(embed=embed)

        # Gestione dei comandi inseriti
        @stadia_italia_bot.event
        async def on_message(message):
            if message.author == stadia_italia_bot.user:
                return
    
            configuration = database.read_configuration(guild_id=message.guild.id)
            ruolo = check_role(message.author, configuration.role)

            if configuration.command_channel:
                if configuration.command_channel != message.channel.name:
                    return

            if message.content.startswith(configuration.command_prefix):
                args = message.content.split()
                if args[0] == configuration.command_prefix:
                    args.pop(0)
                else:
                    args[0] = args[0].replace(configuration.command_prefix, "")
                if args[0] == "help":
                    await info(message)
                elif args[0] == "canale_benvenuto":
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="welcome_channel", value=args[1] )
                        await message.channel.send("Canale di benvenuto aggiornato!")
                    else: 
                        await message.channel.send("Non hai i permessi per questo comando!")
                elif args[0] == "canale_bot":
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="command_channel", value=args[1] )
                        await message.channel.send("Canale per comandi bot aggiornato!")
                    else: 
                        await message.channel.send("Non hai i permessi per questo comando!")    
                elif args[0] == "prefix":
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="command_prefix", value=args[1] )
                        await message.channel.send("Prefix per bot aggiornato!")
                    else: 
                        await message.channel.send("Non hai i permessi per questo comando!")
                elif args[0] == "ruolo":
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="role", value=args[1] )
                        await message.channel.send("Ruolo per gestire bot aggiornato!")
                    else: 
                        await message.channel.send("Non hai i permessi per questo comando!")
                elif args[0] == "mod_benvenuto":
                    if ruolo == 1:
                        args.pop(0)
                        frase = ' '.join(args)
                        database.update_configuration(guild_id=message.guild.id, item="welcome_message_list", value=frase )
                        await message.channel.send("Messaggio di benvenuto per canale, aggiornato!")
                    else: 
                        await message.channel.send("Non hai i permessi per questo comando!")
                elif args[0] == "mod_DM":
                    if ruolo == 1:
                        args.pop(0)
                        frase = ' '.join(args)
                        database.update_configuration(guild_id=message.guild.id, item="welcome_direct_message", value=frase )
                        await message.channel.send("Messaggio di benvenuto per DM, aggiornato!")
                    else: 
                        await message.channel.send("Non hai i permessi per questo comando!")    
                elif args[0] == "albi":
                    await albi(message)
                elif args[0] == "blu":
                    await blu(message)
                else:
                    await message.channel.send("Errore, comando non trovato!")
                return
            else:
                return

        # Controlla se il ruolo della configurazione è assegnato all'autore del messaggio (serve per i permessi sui comandi)
        def check_role(author, roleId):
            ruolo = int(roleId.replace("<@&", "").replace(">", ""))
            if ruolo in [y.id for y in author.roles]:
                return 1 
            else:
                return None

      


        stadia_italia_bot.run(token)