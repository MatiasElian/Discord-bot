import discord
from discord.ext import tasks, commands
import os
import random
import time  # Para manejar el tiempo
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
ROLE_ID = int(os.getenv('ROLE_ID'))

# Configuración de intents
intents = discord.Intents.default()
intents.members = True  # Necesario para acceder a los miembros
intents.message_content = True  # Necesario para recibir comandos

# Crear el bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de posibles apodos
nicknames = ["Momolico","Me duele el qlo","Niigru","MUUUY gei","Puuuto Puuuutoo","Hugo","HUGUITO","Huguisanfer","Juano","Falnermu","mufalner","mulanfer","tota","star Kgando","p1pardium","boludo gordo","ROGELIO FUNES MORI","Iknoshia?","Tony tony choppa","Tony","mat11","matonse","NabO","MediaPiZZa","PERMATRAGO","PADALUSTRO","CROTOFROTO","UXIONO","SOBO","TRUJO","MAINCROF","Me cago con hambre","SHALALA","Pacubet","Nabuu","Necho","Qchame una cosha Piibe","Melomano","Yogurcito de Yogur","Me comi un trava","PUTO GORDO","El one piece es ADO","Pendejo Femboy","CULO sucio","Space Potat0","pakitoamoroso","TONTA PELADA","tizi","QUIQUE QUISPE OE","ENRIQUE","Un palo y una tela","tengo frio y estoy mojado","Renshi","Ignacio Nacho Nax","EL RATAS","Fan de las ventanas","autopista","ENRIQUE DOS SANTOS AVEIRO","QUIQUE QUISPE MAMANI QUISPE"]

# Diccionario para llevar registro de los nombres usados
used_nicknames = {}

# Variables para manejar el tiempo
last_change_time = time.time()  # Guarda el momento del último cambio
change_interval = 8 * 3600  # 8 horas en segundos (ajusta a 24 * 3600 para 24h)

@bot.event
async def on_ready():
    print(f'✅ Conectado como {bot.user}')
    cambiar_nicknames.start()

@tasks.loop(hours=8)  # Para pruebas rápidas, cambia a hours=24 después
async def cambiar_nicknames():
    global last_change_time
    last_change_time = time.time()  # Guarda el tiempo del último cambio
    print("🔄 Ejecutando cambio de nicknames...")

    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("❌ Servidor no encontrado.")
        return

    role = discord.utils.get(guild.roles, id=ROLE_ID)
    if role is None:
        print("❌ Rol no encontrado con esa ID.")
        return

    if not role.members:
        print("⚠️ No hay usuarios con este rol.")
        return

    available_nicknames = nicknames.copy()  # Copia la lista de nombres disponibles

    for member in role.members:
        # Si ya se han asignado todos los nombres, se reinicia la lista
        if len(available_nicknames) == 0:
            available_nicknames = nicknames.copy()
            used_nicknames.clear()

        # Seleccionamos un nuevo nombre que no haya sido usado
        nuevo_nick = random.choice(available_nicknames)
        available_nicknames.remove(nuevo_nick)  # Quitamos el nombre de la lista
        used_nicknames[member.id] = nuevo_nick  # Registramos el cambio

        try:
            await member.edit(nick=nuevo_nick)
            print(f"✅ Cambiado nickname de {member.name} a {nuevo_nick}")
        except discord.Forbidden:
            print(f"❌ No tengo permisos para cambiar el nick de {member.name}.")
        except discord.HTTPException as e:
            print(f"⚠️ Error al cambiar nickname de {member.name}: {e}")

# Comando para ver el tiempo restante
@bot.command(name="TimeP")
async def tiempo_restante(ctx):
    global last_change_time
    time_elapsed = time.time() - last_change_time
    time_remaining = max(change_interval - time_elapsed, 0)  # Evita números negativos

    hours = int(time_remaining // 3600)
    minutes = int((time_remaining % 3600) // 60)
    seconds = int(time_remaining % 60)

    await ctx.send(f"⏳ **Tiempo restante para el próximo cambio de nombres:** {hours} horas, {minutes} minutos y {seconds} segundos.")

bot.run(TOKEN)

