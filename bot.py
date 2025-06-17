import discord
from discord.ext import tasks, commands
import random
import asyncio
import os
from dotenv import


TOKEN = os.getenv('DISCORD_TOKEN')


LISTE_DE_MOTS_UNIQUE = [
"baise",
"baiseurs",
"bamboula",
"bamboulas",
"bâtard",
"bâtards",
"bicot",
"bouffeur de sperme",
"bougnoul",
"branlé",
"branlo",
"bridé",
"chatte",
"chattes",
"chiant",
"chibre",
"chiennasse",
"chienne",
"chinetoque",
"chinetoques",
"clito",
"connasses",
"connerie",
"crétin",
"débile",
"débile mental",
"débiles",
"ducon",
"éjac",
"éjacul",
"emmerder",
"enturbanné",
"enturbannés",
"espingouin",
"espingouins",
"fion",
"foufounes",
"gitan",
"gitans",
"gouine",
"gouines",
"gytan",
"gytans",
"merde",
"jouir",
"minou",
"minous",
"moules",
"nègre",
"nègres",
"négro",
"négros",
"nique",
"niqué",
"niquer",
"niqueur",
"niqueurs",
"pauvre crétin",
"pauvre débile",
"PD",
"pédé",
"pédés",
"pédo",
"pédophiles",
"pédos",
"pine",
"pompe-moi",
"putes",
"rabbi",
"raton",
"ratons",
"rital",
"salope",
"salopes",
"sodomie",
"sperme",
"suce",
"suce-bite",
"suce-bites",
"suce-moi",
"tête de bite",
"tête de noeud",
"trou du cul",
"trouduc",
"trouducs",
"trous du cul",
"viol",
"violée",
"violer",
"violeur",
"viols",
"youpin",
]

# L'ID du salon où le bot enverra les messages automatiques
# Pour trouver l'ID d'un salon : active le mode développeur dans Discord (Paramètres utilisateur > Avancé),
# puis fais un clic droit sur le salon et clique sur "Copier l'ID".
CANAL_ID_POUR_MESSAGES_AUTO = 123456789012345678 # REMPLACE CECI PAR L'ID DE TON SALON !

# --- Initialisation du bot ---
intents = discord.Intents.default()
intents.message_content = True # Permet au bot de lire le contenu des messages
intents.messages = True # Permet au bot de recevoir les événements de message
intents.guilds = True # Permet au bot de connaître les serveurs où il se trouve

bot = commands.Bot(command_prefix='!', intents=intents)

# --- Événements du bot ---

@bot.event
async def on_ready():
    """Se déclenche lorsque le bot est connecté à Discord."""
    print(f'{bot.user.name} est connecté à Discord !')
    print(f'ID du bot : {bot.user.id}')
    # Lance la tâche d'envoi de messages aléatoires
    if not envoyer_mot_aleatoire.is_running():
        envoyer_mot_aleatoire.start()

@bot.event
async def on_message(message):
    """Se déclenche à chaque fois qu'un message est envoyé."""
    # Ne réponds pas à tes propres messages pour éviter les boucles infinies
    if message.author == bot.user:
        return

    # Si le bot est mentionné, il répond avec un mot/phrase aléatoire de la liste unique
    if bot.user.mentioned_in(message):
        reponse = random.choice(LISTE_DE_MOTS_UNIQUE)
        await message.channel.send(reponse)

    # Important : cette ligne permet de traiter les commandes du bot (celles qui commencent par '!')
    await bot.process_commands(message)

# --- Tâches du bot (envoi de messages automatiques) ---

@tasks.loop(minutes=1) # Par défaut, vérifie toutes les minutes
async def envoyer_mot_aleatoire():
    """Envoie un mot/phrase aléatoire dans un salon défini à des intervalles aléatoires."""
    try:
        # Sélectionne un temps d'attente aléatoire (par exemple entre 10 minutes et 2 heures)
        # Tu peux ajuster ces valeurs, Théo !
        temps_attente_secondes = random.randint(60 * 10, 60 * 120) # Entre 10 minutes et 2 heures
        print(f"Prochain message automatique dans {temps_attente_secondes / 60:.1f} minutes...")
        await asyncio.sleep(temps_attente_secondes)

        channel = bot.get_channel(CANAL_ID_POUR_MESSAGES_AUTO)
        if channel:
            mot = random.choice(LISTE_DE_MOTS_UNIQUE)
            await channel.send(mot)
            print(f"Message automatique envoyé : '{mot}' dans #{channel.name}")
        else:
            print(f"Erreur : Canal avec l'ID {CANAL_ID_POUR_MESSAGES_AUTO} non trouvé.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du message aléatoire : {e}")


# --- Lancement du bot ---
if __name__ == "__main__":
    if TOKEN == 'TON_TOKEN':
        print("ATTENTION : Veuillez remplacer 'TON_TOKEN' par le vrai token de votre bot Discord.")
        print("Le bot ne démarrera pas sans un token valide.")
    elif CANAL_ID_POUR_MESSAGES_AUTO == 123456789012345678:
        print("ATTENTION : Veuillez remplacer 'CANAL_ID_POUR_MESSAGES_AUTO' par l'ID de votre salon Discord.")
        print("Le bot ne pourra pas envoyer de messages automatiques sans un ID de canal valide.")
    else:
        bot.run(TOKEN)