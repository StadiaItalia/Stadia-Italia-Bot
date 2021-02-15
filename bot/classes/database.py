from boilerplate.mongodatabase import MongoDatabase
from classes.configuration import BotConfiguration
from pymongo import MongoClient


class BotDatabase(MongoDatabase):
    def __init__(self, host, user, password, database, configuration_repository, logger):
        self.logger = logger
        self.init_database(host=host, user=user, password=password, db_name=database)
        self.configuration_repository = self.get_collection(configuration_repository)

    def init_database(self, host, user, password, db_name):
        self.database = MongoClient(
            host.replace("<username>", user).replace("<password>", password).replace("<dbname>", db_name))[db_name]
        self.logger.debug(f"Connesso a {self.database}")

    def read_configuration(self, guild_id):
        configuration = self.configuration_repository.find_one({"guildId": guild_id})
        if configuration:
            self.logger.debug(f"Trovata configurazione: {str(configuration)}")
            return configuration
        else:
            self.logger.debug(f"Non ho trovato nessuna configurazione per il server {guild_id}")
            return None

    def remove_configuration(self, guild_id):
        deleted = self.configuration_repository.delete_many({"guildId": guild_id}).deleted_count
        if deleted.deleted_count > 0:
            self.logger.info(f"Cancellate {deleted} configurazioni per il server {guild_id}")
            return True
        else:
            self.logger.info(f"Impossibile cancellare la configurazione per il server {guild_id}")
            return False

    def update_configuration(self, guild_id, item, value):
        updated = self.configuration_repository.update_many({"guildId": guild_id}, {"$set": {item: value}})
        if updated.modified_count > 0:
            self.logger.info(f"Aggiornata la configurazione del server {guild_id}")
            self.logger.debug(f"==> aggiornato item {item} con valore {value}")
            return True
        else:
            self.logger.info(f"Impossibile aggiornare la configurazione del server {guild_id}")
            self.logger.debug(f"==> tentato aggiornamento item {item} con valore {value}")
            return False

    def create_configuration(self, guild_id):
        previous_configuration = self.read_configuration(guild_id=guild_id)
        if previous_configuration:
            self.logger.info(f"Configurazione per il server {guild_id} gia esistente")
            self.logger.debug(f"==> {str(previous_configuration)}")
            return BotConfiguration.from_dict(previous_configuration)
        else:
            bot_configuration = BotConfiguration(guildId=guild_id)
            self.logger.info(f"Creo la configurazione per il server {guild_id}")
            self.configuration_repository.insert_one(bot_configuration.to_dict())
            return bot_configuration
