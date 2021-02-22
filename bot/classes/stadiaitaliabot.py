import traceback

from discord import channel, colour, errors
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
                    channel = get_channel(member,configuration.welcome_channel)
                    logger.info(channel)
                    if type(channel) is str:
                        channel = discord.utils.get(member.guild.channels, name=configuration.welcome_channel)
                    imageURL = "https://media.discordapp.net/attachments/805503312170451044/810886419425525840/Tavola_disegno_22-mostrilloo.png"
                    embed = discord.Embed(
                        colour=(discord.Colour.magenta()),
                        title='Benvenuto/a! 🎉',
                        description=(f'{configuration.welcome_message_list} {member.mention}!')
                    )
                    embed.set_thumbnail(url=imageURL)
                    await channel.send(embed=embed)
            #imageURL = "https://media.discordapp.net/attachments/711166475389501441/804298653950017536/Senzanome.png"
            embed = discord.Embed(
                colour=(discord.Colour.magenta()),
                title='Messaggio automatico di Benvenuto 🎉',
                description=(f'{configuration.welcome_direct_message}')
            )
            #embed.set_thumbnail(url=imageURL)
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
            imageURL = "https://media.discordapp.net/attachments/711166475389501441/793480475083538432/image0.jpg?width=575&height=639"
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
            channel = get_channel(message,configuration.command_channel)
            logger.info(channel)
            if configuration:
                embed = discord.Embed(
                    colour=(discord.Colour.purple()),
                    title='📔 Lista comandi 📔',
                    description='Qui troverete tutti i comandi disponibili con le rispettive configurazioni attuali'
                )
                if str(channel) == str(message.channel.name):
                    embed.add_field(name=f"{configuration.command_prefix} ruolo <valore>",
                        value=f"Corrente: {configuration.role}"+
                        "\nDescrizione: Comando per scegliere quale ruolo può usare i comandi del bot",
                        inline=False)
                    embed.add_field(name=f"{configuration.command_prefix} prefix <valore>",
                        value=f"Corrente: {configuration.command_prefix}"+
                        "\nDescrizione: Comando per cambiare il prefix per i comandi del bot",
                        inline=False)
                    embed.add_field(name=f"{configuration.command_prefix} canale_bot <valore>",
                        value=f"Corrente: {configuration.command_channel}"+
                        "\nDescrizione: Comando per cambiare il canale per i comandi del bot",
                        inline=False)
                    embed.add_field(name=f"{configuration.command_prefix} canale_benvenuto <valore>",
                        value=f"Corrente: {configuration.welcome_channel}"+
                        "\nDescrizione: Comando per cambiare il canale di benvenuto",
                        inline=False)
                    embed.add_field(name=f"{configuration.command_prefix} canale_regole <valore>",
                        value=f"Corrente: {configuration.rules_channel}"+
                        "\nDescrizione: Comando per cambiare il canale con le regole del server",
                        inline=False)
                    embed.add_field(name=f"{configuration.command_prefix} mod_benvenuto <valore>",
                        value=f"Corrente: {configuration.welcome_message_list}"+
                        "\nDescrizione: Comando per cambiare il messaggio di benvenuto in canale"+
                        "\n(la menzione per il nuovo arrivato è già integrata a fine messaggio)",
                        inline=False)
                    embed.add_field(name=f"{configuration.command_prefix} mod_DM <valore>",
                        value=f"Corrente: {configuration.welcome_direct_message}"+
                        "\nDescrizione: Comando per cambiare il messaggio di benvenuto privato (DM)",
                        inline=False)
                    embed.add_field(name=f"{configuration.command_prefix} pulisci",
                        value=f"Descrizione: Comando per cancellare gli ultimi 3 messaggi nella chat dei comandi bot"+
                        "\n(Ultimi due più il comando di pulizia)",
                        inline=False)
                else:
                    embed.add_field(name=f"{configuration.command_prefix} albi",
                        value=f"Descrizione: mostra una delle tante citazioni divertenti della community Stadia Italia ",
                        inline=False)
                    embed.add_field(name=f"{configuration.command_prefix} blu",
                        value=f"Descrizione: mostra una citazione divertente sulla macchina di Bluewine ",
                        inline=False)
                    embed.add_field(name=f"{configuration.command_prefix} regole",
                        value=f"Descrizione: mostra l'elenco delle regole del server ",
                        inline=False)
                await message.channel.send(embed=embed)

        # Comando regole, mostra la lista delle regole del server
        async def regole(message):
            configuration = database.read_configuration(guild_id=message.guild.id)
            if configuration:
                embed = discord.Embed(
                    colour=(discord.Colour.orange()),
                    title='Regole del server 🧐',
                )
                embed.add_field(name="1.",
                    value=f"Rispettare le diversità di opinione, di religione, di credo, elezione di genere e orientamento",
                        inline=False)
                embed.add_field(name="2.",
                    value=f"Sono vietati contenuti esplicitamente sessuali e in generale vietati a minori di 18 anni",
                        inline=False)
                embed.add_field(name="3.",
                    value=f"I contenuti politici e religiosi sono accettati laddove non diventino propaganda e non degenerino",
                        inline=False)
                embed.add_field(name="4.",
                    value=f"Ogni credo e ogni filosofia sono ben accetti e benvenuti",
                        inline=False)
                embed.add_field(name="5.",
                    value=f"Non sono accettate discussioni su software pirata, scambio password, condivisione account, piattaforme di streaming non legali ecc",
                        inline=False)
                embed.add_field(name="6.",
                    value=f"Il trolling non è tollerato",
                        inline=False)
                embed.add_field(name="7.",
                    value=f"È vietato condividere in pubblico informazioni personali",
                        inline=False)
                embed.add_field(name="Regole in dettaglio",
                    value=f"Per maggiori informazioni, consulta {configuration.rules_channel}",
                        inline=False)
                await message.channel.send(embed=embed)

        # Gestione dei comandi inseriti
        @stadia_italia_bot.event
        async def on_message(message):
            if message.author == stadia_italia_bot.user:
                return
    
            configuration = database.read_configuration(guild_id=message.guild.id)

            # Valido solo per prima configurazione on_guild_join (sicuramente esistono soluzioni più eleganti)
            if configuration.role == "Template":
                logger.info(configuration.role)
                ruolo = 1
            else:
                ruolo = check_role(message.author, configuration.role)
            
            # Comandi usabili da tutti, in qualsiasi canale
            if message.content.startswith(configuration.command_prefix):
                args = message.content.split()
                if args[0] == configuration.command_prefix:
                    args.pop(0)
                else:
                    args[0] = args[0].replace(configuration.command_prefix, "")
                if args[0] == "albi":
                    await albi(message)
                    return
                elif args[0] == "blu":
                    await blu(message)
                    return
                elif args[0] == "regole":
                    await regole(message)
                    return
                elif args[0] == "help":
                    await info(message)
                    return
            else:
                return
          
            # Controllo su prima configurazione on_guild_join/ controllo canale bot settato
            if configuration.command_channel != "Template":
                channel = get_channel(message,configuration.command_channel)
                if str(channel) != str(message.channel.name):
                    return

            # Comandi usabili solo dagli utenti con il ruolo specificato, nel canale bot scelto
            if message.content.startswith(configuration.command_prefix):
                args = message.content.split()
                if args[0] == configuration.command_prefix:
                    args.pop(0)
                else:
                    args[0] = args[0].replace(configuration.command_prefix, "")
                if args[0] == "canale_benvenuto":
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="welcome_channel", value=args[1] )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Canale di benvenuto aggiornato!'
                        )
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        await message.channel.send(embed=embed) 
                elif args[0] == "canale_bot":
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="command_channel", value=args[1] )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Canale per comandi bot aggiornato!'
                        )
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        await message.channel.send(embed=embed)
                elif args[0] == "canale_regole":
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="rules_channel", value=args[1] )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Canale delle regole aggiornato!'
                        )
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        await message.channel.send(embed=embed)       
                elif args[0] == "prefix":
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="command_prefix", value=args[1] )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Prefix per bot aggiornato!'
                        )
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        await message.channel.send(embed=embed) 
                elif args[0] == "ruolo":
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="role", value=args[1] )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Ruolo per gestire bot aggiornato!'
                        )
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        await message.channel.send(embed=embed) 
                elif args[0] == "mod_benvenuto":
                    if ruolo == 1:
                        args.pop(0)
                        frase = ' '.join(args)
                        database.update_configuration(guild_id=message.guild.id, item="welcome_message_list", value=frase )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Messaggio di benvenuto per canale, aggiornato!'
                        )
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        await message.channel.send(embed=embed) 
                elif args[0] == "mod_DM":
                    if ruolo == 1:
                        args.pop(0)
                        frase = ' '.join(args)
                        database.update_configuration(guild_id=message.guild.id, item="welcome_direct_message", value=frase )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Messaggio di benvenuto per DM, aggiornato!'
                        )
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        await message.channel.send(embed=embed)     
                elif args[0] == "reset":
                    reset(message)
                    embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Hai resettato i parametri principali!'
                        )
                    await message.channel.send(embed=embed)
                elif args[0] == "pulisci":
                    await message.channel.purge(limit=3)
                    embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Hai cancellato gli ultimi 3 messaggi!'
                        )
                    await message.channel.send(embed=embed)
                else:
                    imageURL = "https://4.bp.blogspot.com/-parios2iYXg/Vthg3WrhLlI/AAAAAAAAABk/F2mGSuC2zY8/s1600/Travolta1.jpg"
                    embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Errore, comando non trovato!'
                    )
                    embed.set_thumbnail(url=imageURL)
                    await message.channel.send(embed=embed) 
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

        # Fa la get del canale dedicato ai comandi del bot gestisce eccezioni su id o name
        def get_channel(member, id):
            try:
                channel = [x for x in member.guild.channels if x.id == int(id.replace("<#", "").replace(">", ""))]
                if (channel == None):
                    raise ValueError("type conflict")
            except ValueError:
                channel = id
                return channel
            else:
                if len(channel) > 0:
                    return channel[0]

        # Funzione reset (nascosta), "salvavita"
        def reset(message):
            database.update_configuration(guild_id=message.guild.id, item="role", value="Template" )
            database.update_configuration(guild_id=message.guild.id, item="command_prefix", value="s!" )
            database.update_configuration(guild_id=message.guild.id, item="command_channel", value="Template" )
            database.update_configuration(guild_id=message.guild.id, item="welcome_channel", value="Template" )
            return
        
        stadia_italia_bot.run(token)