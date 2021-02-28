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
            embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
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
            embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
            await message.channel.send(embed=embed)

        # Comando info, mostra la lista dei comandi utilizzabili e le configurazioni attuali corrispondenti
        async def info(message,conf):
            channel = get_channel(message,conf.command_channel)
            logger.info(channel)
            if conf:
                embed = discord.Embed(
                    colour=(discord.Colour.purple()),
                    title='📔 Lista comandi 📔',
                    description='Qui troverete tutti i comandi disponibili'
                )
                if str(message.channel.type) == "private":
                    embed.add_field(name=f"{conf.command_prefix} registra <nick Stadia> <url profilo Stadia>",
                        value=f"Descrizione: comando per registrare il proprio account Discord/Stadia ",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} aggiorna <nick Stadia> <url profilo Stadia>",
                        value=f"Descrizione: comando per aggiornare il nickname Stadia di un account Discord già registrato ",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} lista_user",
                        value=f"Descrizione: mostra l'elenco degli utenti discord registrati, ed il loro nickname Stadia ",
                        inline=False)
                elif (str(channel) == str(message.channel.name)) or (str(channel) == "Template"):
                    embed.add_field(name=f"{conf.command_prefix} ruolo <valore>",
                        value=f"Corrente: {conf.role}"+
                        "\nDescrizione: Comando per scegliere quale ruolo può usare i comandi del bot",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} prefix <valore>",
                        value=f"Corrente: {conf.command_prefix}"+
                        "\nDescrizione: Comando per cambiare il prefix per i comandi del bot",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} canale_bot <valore>",
                        value=f"Corrente: {conf.command_channel}"+
                        "\nDescrizione: Comando per cambiare il canale per i comandi del bot",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} canale_benvenuto <valore>",
                        value=f"Corrente: {conf.welcome_channel}"+
                        "\nDescrizione: Comando per cambiare il canale di benvenuto",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} canale_regole <valore>",
                        value=f"Corrente: {conf.rules_channel}"+
                        "\nDescrizione: Comando per cambiare il canale con le regole del server",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} mod_benvenuto <valore>",
                        value=f"Corrente: {conf.welcome_message_list}"+
                        "\nDescrizione: Comando per cambiare il messaggio di benvenuto in canale"+
                        "\n(la menzione per il nuovo arrivato è già integrata a fine messaggio)",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} mod_DM <valore>",
                        value=f"Corrente: {conf.welcome_direct_message}"+
                        "\nDescrizione: Comando per cambiare il messaggio di benvenuto privato (DM)",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} pulisci <valore>",
                        value=f"Descrizione: Comando per cancellare gli ultimi n messaggi nella chat dei comandi bot",
                        inline=False)
                    embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                else:
                    embed.add_field(name=f"{conf.command_prefix} albi",
                        value=f"Descrizione: mostra una delle tante citazioni divertenti della community Stadia Italia ",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} blu",
                        value=f"Descrizione: mostra una citazione divertente sulla macchina di Bluewine ",
                        inline=False)
                    embed.add_field(name=f"{conf.command_prefix} regole",
                        value=f"Descrizione: mostra l'elenco delle regole del server ",
                        inline=False)
                    embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                    #embed.add_field(name=f"{conf.command_prefix} slap <@utente>",
                    #    value=f"Descrizione: slappa qualcuno (consigliamo Kalamajo) ",
                    #    inline=False)
                
                await message.channel.send(embed=embed)

        # Comando regole, mostra la lista delle regole del server
        async def regole(message,conf):
            if conf:
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
                embed.add_field(name="8.",
                    value=f"È vietato spammare",
                        inline=False)
                embed.add_field(name="Regole in dettaglio",
                    value=f"Per maggiori informazioni, consulta {conf.rules_channel}",
                        inline=False)
                embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                await message.channel.send(embed=embed)

        # Gestione dei comandi inseriti
        @stadia_italia_bot.event
        async def on_message(message):
            if message.author == stadia_italia_bot.user:
                return
    
            #Sezione comandi del bot in dm
            if str(message.channel.type) == "private":
                # Workaround temporaneo - da rivedere
                server = 737561180855336962
                config_dm = database.read_configuration(guild_id=int(server))
                trovato = 0
                if config_dm:
                    if message.content.startswith(config_dm.command_prefix):
                        args = message.content.split()
                        if args[0] == config_dm.command_prefix:
                            args.pop(0)
                        else:
                            args[0] = args[0].replace(config_dm.command_prefix, "")
                        if args[0] == "registra":
                            args.pop(0)
                            if len(args) == 0:
                                embed = discord.Embed(
                                        colour=(discord.Colour.red()),
                                        title='Errore! ⚠️',
                                        description='Non hai digitato il tuo nickname!'
                                    )
                                await message.channel.send(embed=embed)
                                return
                            elif len(args) == 1:
                                embed = discord.Embed(
                                        colour=(discord.Colour.red()),
                                        title='Errore! ⚠️',
                                        description="Non hai riportato l'url del tuo profilo stadia!"
                                    )
                                await message.channel.send(embed=embed)
                                return
                            else:
                                utente = await check_user_list(message,config_dm.user,message.author)
                                if utente != True:
                                    database.update_configuration_append(guild_id=server, item="user", value=f"{message.author} | {args[0]} | {args[1]}")
                                    embed = discord.Embed(
                                        colour=(discord.Colour.green()),
                                        title='Fatto! 👍',
                                        description='Registrazione completata!'
                                    )
                                    await message.channel.send(embed=embed)
                        elif args[0] == "lista_user":
                            await read_user_list(message,config_dm.user)
                            return
                        elif args[0] == "aggiorna":
                            args.pop(0)
                            if len(args) == 0:
                                embed = discord.Embed(
                                        colour=(discord.Colour.red()),
                                        title='Errore! ⚠️',
                                        description='Non hai digitato il tuo nickname!'
                                    )
                                await message.channel.send(embed=embed)
                                return
                            elif len(args) == 1:
                                embed = discord.Embed(
                                        colour=(discord.Colour.red()),
                                        title='Errore! ⚠️',
                                        description="Non hai riportato l'url del tuo profilo stadia!"
                                    )
                                await message.channel.send(embed=embed)
                                return
                            else:
                                for x in range(len(config_dm.user)):
                                    if str(message.author) in config_dm.user[x]:
                                        database.update_configuration(guild_id=server, item=f"user.{x}", value=f"{message.author} | {args[0]} | {args[1]}")
                                        embed = discord.Embed(
                                            colour=(discord.Colour.green()),
                                            title='Fatto! 👍',
                                            description='Aggiornamento completato!'
                                        )
                                        trovato = 1
                                        await message.channel.send(embed=embed)
                                if trovato == 0:
                                    embed = discord.Embed(
                                        colour=(discord.Colour.red()),
                                        title='Errore! ⚠️',
                                        description='Utente non trovato!'
                                    )
                                    await message.channel.send(embed=embed)
                        elif args[0] == "help":
                            await info(message,config_dm)
                            return

        
                    else:
                        return
            else:
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
                    await message.channel.purge(limit=1)
                    await albi(message)
                    return
                elif args[0] == "blu":
                    await message.channel.purge(limit=1)
                    await blu(message)
                    return
                elif args[0] == "regole":
                    await message.channel.purge(limit=1)
                    await regole(message,configuration)
                    return
                elif args[0] == "help":
                    await message.channel.purge(limit=1)
                    await info(message,configuration)
                    return
                #elif args[0] == "slap":
                #    await message.channel.purge(limit=1)
                #    slap_user = get_user(message,args[1])
                #    logger.info(slap_user)
                #    imageURL = "https://i.imgflip.com/1ntnht.jpg"
                #    embed = discord.Embed(
                #            colour=(discord.Colour.green()),
                #            title='Get Slapped N00b! 👋',
                #            description=f'{message.author} ha schiaffeggiato {slap_user} !'
                #        )
                #    embed.set_thumbnail(url=imageURL)
                #    await message.channel.send(embed=embed)
                #    for x in range(0, 5):
                #        await slap_user.send("👋 *Paccheri sound intesifies*"+
                #                             "\n *Paccheri sound intesifies* 👋"
                #        )
                #    return
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
                    await message.channel.purge(limit=1)
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="welcome_channel", value=args[1] )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Canale di benvenuto aggiornato!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed) 
                elif args[0] == "canale_bot":
                    await message.channel.purge(limit=1)
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="command_channel", value=args[1] )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Canale per comandi bot aggiornato!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed)
                elif args[0] == "canale_regole":
                    await message.channel.purge(limit=1)
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="rules_channel", value=args[1] )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Canale delle regole aggiornato!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed)       
                elif args[0] == "prefix":
                    await message.channel.purge(limit=1)
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="command_prefix", value=args[1] )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Prefix per bot aggiornato!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed) 
                elif args[0] == "ruolo":
                    await message.channel.purge(limit=1)
                    if ruolo == 1:
                        database.update_configuration(guild_id=message.guild.id, item="role", value=args[1] )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Ruolo per gestire bot aggiornato!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed) 
                elif args[0] == "mod_benvenuto":
                    await message.channel.purge(limit=1)
                    if ruolo == 1:
                        args.pop(0)
                        frase = ' '.join(args)
                        database.update_configuration(guild_id=message.guild.id, item="welcome_message_list", value=frase )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Messaggio di benvenuto per canale, aggiornato!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed) 
                elif args[0] == "mod_DM":
                    await message.channel.purge(limit=1)
                    if ruolo == 1:
                        args.pop(0)
                        frase = ' '.join(args)
                        database.update_configuration(guild_id=message.guild.id, item="welcome_direct_message", value=frase )
                        embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Messaggio di benvenuto per DM, aggiornato!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed)
                    else: 
                        embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Non hai i permessi per questo comando!'
                        )
                        embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                        await message.channel.send(embed=embed)     
                elif args[0] == "reset":
                    await message.channel.purge(limit=1)
                    reset(message)
                    embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description='Hai resettato i parametri principali!'
                        )
                    embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                    await message.channel.send(embed=embed)
                elif args[0] == "pulisci":
                    await message.channel.purge(limit=int(args[1]))
                    embed = discord.Embed(
                            colour=(discord.Colour.green()),
                            title='Fatto! 👍',
                            description=f'Hai cancellato gli ultimi {args[1]} messaggi!'
                    )
                    embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
                    await message.channel.send(embed=embed)
                else:
                    imageURL = "https://4.bp.blogspot.com/-parios2iYXg/Vthg3WrhLlI/AAAAAAAAABk/F2mGSuC2zY8/s1600/Travolta1.jpg"
                    embed = discord.Embed(
                            colour=(discord.Colour.red()),
                            title='Errore! ⚠️',
                            description='Errore, comando non trovato!'
                    )
                    embed.set_footer(icon_url=message.author.avatar_url, text=f"Richiesto da: {message.author}")
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
                    raise AttributeError("type conflict")
            except ValueError:
                channel = id
                return channel
            except AttributeError:
                return
            else:
                if len(channel) > 0:
                    return channel[0]

        # Fa la get dell'utente specificato nel comando
        def get_user(member, id):
            try:
                user = [x for x in member.guild.members if x.id == int(id.replace("<@!", "").replace(">", ""))]
                if (user == None):
                    raise AttributeError("type conflict")
            except ValueError:
                user = id
                return user
            else:
                if len(user) > 0:
                    return user[0]
        
        # Funzione reset (nascosta), "salvavita"
        def reset(message):
            database.update_configuration(guild_id=message.guild.id, item="role", value="Template" )
            database.update_configuration(guild_id=message.guild.id, item="command_prefix", value="s!" )
            database.update_configuration(guild_id=message.guild.id, item="command_channel", value="Template" )
            database.update_configuration(guild_id=message.guild.id, item="welcome_channel", value="Template" )
            return

        # Funzione leggi lista user
        async def read_user_list(message,lista):
            embed = discord.Embed(
                colour=(discord.Colour.magenta()),
                title='Lista utenti! 👍',
                description='Ecco la lista degli utenti Discord ed il loro corrispondente nickname Stadia!'
            )
            embed.add_field(name="Discord",
                        value="--------------------",
                        inline=True)
            embed.add_field(name="Stadia",
                        value="--------------------",
                        inline=True)
            embed.add_field(name="Profili",
                        value="--------------------",
                        inline=True)
            for x in range(len(lista)):
                frase = lista[x].rsplit(' | ',2)
                logger.info(frase)
                embed.add_field(name="\u200b",
                        value=f"{frase[0]}",
                        inline=True)
                embed.add_field(name="\u200b",
                        value=f"{frase[1]}",
                        inline=True)
                embed.add_field(name="\u200b",
                        value=f"[Link al profilo Stadia]({frase[2]})",
                        inline=True)
            await message.channel.send(embed=embed)

        # Funzione controllo su registra 
        async def check_user_list(message,lista,user):
            embed = discord.Embed(
                        colour=(discord.Colour.red()),
                        title='Errore! ⚠️',
                        description='Sei già registrato/a!'
            )
            logger.info(user)
            for x in range(len(lista)):
                if str(user) in lista[x]:
                    await message.channel.send(embed=embed)
                    return True

                

                    
                
                


        stadia_italia_bot.run(token)