# Stadia-Italia-Bot

## Bot ufficiale del server discord Stadia Italia

src="(https://i.imgur.com/z6bGB2N.png" width="100" height="100" />

Le funzionalità principali del bot consistono nel dare il benvenuto ai nuovi utenti, tramite chat di server e messaggio privato(DM).

## Comandi

Il bot risponderà ai seguenti comandi:

Comando | Descrizione
--------|------------
s! ruolo <valore> | Comando per scegliere quale ruolo può usare i comandi del bot
s! prefix <valore> | Comando per cambiare il prefix per i comandi del bot
s! canale_bot <valore> | Comando per cambiare il canale per i comandi del bot
s! canale_benvenuto <valore> | Comando per cambiare il canale di benvenuto
s! canale_regole <valore> | Comando per cambiare il canale con le regole del server
s! mod_benvenuto <valore> | Comando per cambiare il messaggio di benvenuto in canale
s! mod_DM <valore> | Comando per cambiare il messaggio di benvenuto privato (DM)
s! pulisci <valore> | Comando per cancellare gli ultimi n messaggi nella chat dei comandi bot
s! albi | mostra una delle tante citazioni divertenti della community Stadia Italia
s! blu | mostra una citazione divertente sulla macchina di Bluewine
s! regole | mostra l'elenco delle regole del server
  
  
## Configurazione

Puoi personalizzare queste configurazioni per il tuo server discord:

Prefix | Descrizione
--------|------------
role <@role> | Specifica quale ruolo può usare i comandi del bot (default Template)
command_prefix <value> | Specifica il prefix per comandi (default s!)
command_channel <#channel> | Specifica il canale dedicato ai comandi del bot (default Template)
welcome_channel <#channel> | Specifica il canale di benvenuto selezionato (default Template)
rules_channel <#channel> | Specifica il canale delle regole del server selezionato (default Template)
welcome_message_list <value> | Specifica il messaggio di benvenuto da inviare in canale (default Template)
welcome_direct_message <value> | Specifica il messaggio di benvenuto da inviare in privato(DM) (default Template)
  

## FAQ

**Come invitare il bot sul server**

clicca [qui](https://discord.com/api/oauth2/authorize?client_id=808751622293291039&permissions=126032&scope=bot) e
segui gli step successivi.

**Ho bisogno di qualche variabile d'ambiente per far funzionare il bot?**

Si, ecco le variabili d'ambiente da usare (o da salvare in un `.env` file):

Variable | Descrizione
---------|------------
STADIA_ITALIA_DISCORD_TOKEN | Discord token 
STADIA_ITALIA_LOGGING_LEVEL | Logging level `[WARN, ERROR, INFO, DEBUG]`
STADIA_ITALIA_DATABASE_USER | user
STADIA_ITALIA_DATABASE_PASSWORD | psw
STADIA_ITALIA_DATABASE | Nome database MongoDB
STADIA_ITALIA_DATABASE_HOST | Stringa di connessione MongoDB (es. `mongodb://\[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]` )
STADIA_ITALIA_CONFIGURATION_COLLECTION | Nome istanza
  

  
  
  
