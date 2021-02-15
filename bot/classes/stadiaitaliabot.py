import traceback
import modules.configuration as configuration
import random
import discord as discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True


class StadiaItaliaBot(discord.ext.commands.Bot):
    def __init__(self, database, logger):
        super(StadiaItaliaBot, self).__init__(command_prefix=".", intents=intents)
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
                                                activity=discord.Game("Pronto all'azione! .help per info"))
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

    @stadia_italia_bot.event
    async def on_member_join(member):
        logger.info(f"Utente {member.name} entrato in {member.guild.name}")
        configuration = database.read_configuration(guild_id=member.guild.id)
        if configuration:
            if configuration.welcome_channel and len(configuration.welcome_message_list) > 0:
                channel = discord.utils.get(member.guild.channels, id=configuration.welcome_channel)
                await channel.send(f"{random.choice(configuration.welcome_message_list)}")

        embed = discord.Embed(
            colour=(discord.Colour.magenta()),
            title='Messaggio di Benvenuto',
            description=f'Ciao e benvenuto sul server discord di Stadia Italia {member.mention}.'
        )
        await member.send(embed=embed)
        await channel.send(f'Diamo tutti il benvenuto a {member.mention} !')

    # Comando albicocco, per display frasi divertenti di Stadia Italia
    # @stadia_italia_bot.command()
    # async def albi(ctx):
    #     imageURL = "http://www.wetoo.viandanza.it/wp-content/uploads/2017/07/ALBICOCCA.jpg"
    #     embed = discord.Embed(
    #         colour=(discord.Colour.green()),
    #         title='Albicocco dice 🥭',
    #         description=(random.choice(albicocco_string))
    #     )
    #     embed.set_thumbnail(url=imageURL)
    #     await ctx.message.channel.send(embed=embed)

    # Comando blu, per display frasi divertenti sulla macchina di Bluewine
    # @stadia_italia_bot.command()
    # async def blu(ctx):
    #     imageURL = "https://cdn.images.express.co.uk/img/dynamic/24/590x/Dirty-car-596260.jpg"
    #     embed = discord.Embed(
    #         colour=(discord.Colour.blue()),
    #         title='Brum Brum 🚗',
    #         description=(random.choice(macchina_blu))
    #     )
    #     embed.set_thumbnail(url=imageURL)
    #     await ctx.message.channel.send(embed=embed)

    stadia_italia_bot.run(token)

