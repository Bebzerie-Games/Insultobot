import discord
from discord.ext import tasks, commands
import random
import asyncio
import os
from dotenv import load_dotenv

# --- Charger les variables d'environnement ---
load_dotenv()

# --- Configuration ---
TOKEN = os.getenv('DISCORD_TOKEN')

# Liste des mots/phrases que le bot utilisera
LISTE_DE_MOTS_UNIQUE = [
    "baise", "baiseurs", "bamboula", "bamboulas", "bâtard", "bâtards", "bicot",
    "bouffeur de sperme", "bougnoul", "branlé", "branlo", "bridé", "chatte",
    "chattes", "chiant", "chibre", "chiennasse", "chienne", "chinetoque",
    "chinetoques", "clito", "connasses", "connerie", "crétin", "débile",
    "débile mental", "débiles", "ducon", "éjac", "éjacul", "emmerder",
    "enturbanné", "enturbannés", "espingouin", "espingouins", "fion",
    "foufounes", "gitan", "gitans", "gouine", "gouines", "gytan", "gytans",
    "merde", "jouir", "minou", "minous", "moules", "nègre", "nègres", "négro",
    "négros", "nique", "niqué", "niquer", "niqueur", "niqueurs", "pauvre crétin",
    "pauvre débile", "PD", "pédé", "pédés", "pédo", "pédophiles", "pédos",
    "pine", "pompe-moi", "putes", "rabbi", "raton", "ratons", "rital",
    "salope", "salopes", "sodomie", "sperme", "suce", "suce-bite", "suce-bites",
    "suce-moi", "tête de bite", "tête de noeud", "trou du cul", "trouduc",
    "trouducs", "trous du cul", "viol", "violée", "violer", "violeur", "viols",
    "youpin", "hippie", "luka", "https://media.discordapp.net/attachments/1021732643928297493/1210922190849966090/cm-chat-media-video-18542cf93-c4ad-4256-8e47-cfba9f80ef7b735500.gif", "nigga",
]

CANAL_ID_POUR_MESSAGES_AUTO = 1031638956762222662 

PROBABILITE_REPONSE_ALEATOIRE = 0.1

# --- Initialisation du bot ---
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- Événements du bot ---

@bot.event
async def on_ready():
    """Se déclenche lorsque le bot est connecté à Discord."""
    print(f'{bot.user.name} est connecté à Discord !')
    print(f'ID du bot : {bot.user.id}')
    if not envoyer_mot_aleatoire.is_running():
        envoyer_mot_aleatoire.start()

@bot.event
async def on_message(message):
    """Se déclenche à chaque fois qu'un message est envoyé."""
    if message.author == bot.user:
        return

    if message.author.bot: # Pour ignorer les messages des autres bots
        return

    if random.random() < PROBABILITE_REPONSE_ALEATOIRE:
        reponse = random.choice(LISTE_DE_MOTS_UNIQUE) + " de " + random.choice(LISTE_DE_MOTS_UNIQUE) + " de merde"
        await message.channel.send(reponse)

    await bot.process_commands(message)

# --- Tâches du bot (envoi de messages automatiques) ---

@tasks.loop(minutes=1)
async def envoyer_mot_aleatoire():
    """Envoie un mot/phrase aléatoire dans un salon défini à des intervalles aléatoires."""
    try:
        temps_attente_secondes = random.randint(60 * 10, 60 * 120)
        print(f"Prochain message automatique dans {temps_attente_secondes / 60:.1f} minutes...")
        await asyncio.sleep(temps_attente_secondes)

        channel = bot.get_channel(CANAL_ID_POUR_MESSAGES_AUTO)
        if channel:
            mot = random.choice(LISTE_DE_MOTS_UNIQUE) + " de " + random.choice(LISTE_DE_MOTS_UNIQUE) + " de merde"
            await channel.send(mot)
            print(f"Message automatique envoyé : '{mot}' dans #{channel.name}")
        else:
            print(f"Erreur : Canal avec l'ID {CANAL_ID_POUR_MESSAGES_AUTO} non trouvé.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du message aléatoire : {e}")

# --- Lancement du bot ---
if __name__ == "__main__":
    if TOKEN is None: 
        print("ATTENTION : Le token Discord n'a pas été trouvé. Assurez-vous que le fichier .env existe et contient 'DISCORD_TOKEN=VOTRE_TOKEN'.")
        print("Le bot ne démarrera pas sans un token valide.")
    else:
        bot.run(TOKEN)
