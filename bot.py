import os
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
from flask import Flask
from threading import Thread

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Necesario para info de miembros

bot = commands.Bot(command_prefix=',', intents=intents)

# Color principal para los embeds
COLOR_PRINCIPAL = 0x5865F2  # Azul Discord

app = Flask(__name__)

def keep_alive():
    @app.route("/")
    def home():
        return "Bot activo."

    thread = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8080})
    thread.daemon = True
    thread.start()

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como: {bot.user.name}')
    print(f'🆔 ID: {bot.user.id}')
    print('---')

# ==================== COMANDOS DE MODERACIÓN ====================

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, cantidad: int):
    if cantidad < 1 or cantidad > 100:
        embed = discord.Embed(
            title="❌ Error",
            description="Debes especificar un número entre 1 y 100.",
            color=0xFF0000
        )
        embed.set_footer(text="Developed by @adinerar")
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()
        return
    
    mensajes_borrados = await ctx.channel.purge(limit=cantidad + 1)
    
    embed = discord.Embed(
        title="🗑️ Mensajes Borrados",
        description=f"Se borraron **{len(mensajes_borrados) - 1}** mensajes.",
        color=0x00FF00
    )
    embed.set_footer(text="Developed by @adinerar")
    confirmacion = await ctx.send(embed=embed)
    
    await asyncio.sleep(3)
    await confirmacion.delete()

@purge.error
async def purge_error(ctx, error):
    embed = discord.Embed(color=0xFF0000)
    embed.set_footer(text="Developed by @adinerar")
    
    if isinstance(error, commands.MissingPermissions):
        embed.title = "❌ Sin Permisos"
        embed.description = "No tienes permisos para borrar mensajes."
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.title = "❌ Uso Incorrecto"
        embed.description = "Uso: `,purge <cantidad>`"
    elif isinstance(error, commands.BadArgument):
        embed.title = "❌ Error"
        embed.description = "La cantidad debe ser un número."
    
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await msg.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    canal = ctx.channel
    
    embed = discord.Embed(
        title="💥 NUKE INCOMING",
        description="Borrando canal en 2 segundos...",
        color=0xFF0000
    )
    embed.set_footer(text="Developed by @adinerar")
    await ctx.send(embed=embed)
    
    await asyncio.sleep(2)
    
    nombre = canal.name
    categoria = canal.category
    posicion = canal.position
    topic = canal.topic
    
    await canal.delete()
    
    nuevo_canal = await ctx.guild.create_text_channel(
        name=nombre,
        category=categoria,
        position=posicion,
        topic=topic
    )
    
    embed = discord.Embed(
        title="💥 CANAL NUKED",
        description="Todos los mensajes han sido eliminados.",
        color=0x00FF00
    )
    embed.set_footer(text="Developed by @adinerar")
    msg = await nuevo_canal.send(embed=embed)
    
    await asyncio.sleep(5)
    await msg.delete()

@nuke.error
async def nuke_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Sin Permisos",
            description="Necesitas permisos de **Administrador** para usar este comando.",
            color=0xFF0000
        )
        embed.set_footer(text="Developed by @adinerar")
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()

# ==================== COMANDOS DE INFORMACIÓN ====================

@bot.command()
async def server(ctx):
    """Muestra información del servidor"""
    guild = ctx.guild
    
    # Contadores
    total_miembros = guild.member_count
    bots = len([m for m in guild.members if m.bot])
    humanos = total_miembros - bots
    
    # Canales
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categorias = len(guild.categories)
    
    # Roles
    total_roles = len(guild.roles) - 1  # -1 para excluir @everyone
    
    # Emojis
    total_emojis = len(guild.emojis)
    
    # Crear embed
    embed = discord.Embed(
        title=f"📊 Información de {guild.name}",
        color=COLOR_PRINCIPAL,
        timestamp=datetime.now()
    )
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="🆔 ID", value=f"`{guild.id}`", inline=True)
    embed.add_field(name="👑 Dueño", value=guild.owner.mention if guild.owner else "Desconocido", inline=True)
    embed.add_field(name="📅 Creado", value=f"<t:{int(guild.created_at.timestamp())}:R>", inline=True)
    
    embed.add_field(name="👥 Miembros", value=f"Total: **{total_miembros}**\nHumanos: **{humanos}**\nBots: **{bots}**", inline=True)
    embed.add_field(name="📁 Canales", value=f"Texto: **{text_channels}**\nVoz: **{voice_channels}**\nCategorías: **{categorias}**", inline=True)
    embed.add_field(name="🏷️ Roles", value=f"**{total_roles}** roles", inline=True)
    
    embed.add_field(name="😀 Emojis", value=f"**{total_emojis}** emojis", inline=True)
    embed.add_field(name="🚀 Boosts", value=f"Nivel **{guild.premium_tier}**\n**{guild.premium_subscription_count}** boosts", inline=True)
    embed.add_field(name="🔒 Verificación", value=f"Nivel **{guild.verification_level.name}**", inline=True)
    
    if guild.description:
        embed.add_field(name="📝 Descripción", value=guild.description, inline=False)
    
    embed.set_footer(text="Developed by @adinerar")
    
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx, miembro: discord.Member = None):
    """Muestra información de un usuario"""
    user = miembro or ctx.author
    
    # Fechas
    cuenta_creada = f"<t:{int(user.created_at.timestamp())}:R>"
    union_servidor = f"<t:{int(user.joined_at.timestamp())}:R>" if user.joined_at else "Desconocido"
    
    # Roles (excluyendo @everyone)
    roles = [role.mention for role in user.roles[1:]]
    roles_str = ", ".join(roles) if roles else "Ninguno"
    
    # Crear embed
    embed = discord.Embed(
        title=f"👤 Información de {user}",
        color=user.color if user.color.value != 0 else COLOR_PRINCIPAL,
        timestamp=datetime.now()
    )
    
    embed.set_thumbnail(url=user.display_avatar.url)
    
    embed.add_field(name="🆔 ID", value=f"`{user.id}`", inline=True)
    embed.add_field(name="🏷️ Apodo", value=user.display_name, inline=True)
    embed.add_field(name="🤖 Bot", value="Sí" if user.bot else "No", inline=True)
    
    embed.add_field(name="📅 Cuenta Creada", value=cuenta_creada, inline=True)
    embed.add_field(name="📥 Se Unió", value=union_servidor, inline=True)
    embed.add_field(name="🎨 Color", value=str(user.color), inline=True)
    
    embed.add_field(name=f"🏷️ Roles [{len(user.roles) - 1}]", value=roles_str[:1024] or "Ninguno", inline=False)
    
    # Estado personalizado
    if user.activity:
        embed.add_field(name="🎮 Actividad", value=f"{user.activity.type.name}: {user.activity.name}", inline=False)
    
    embed.set_footer(text="Developed by @adinerar")
    
    await ctx.send(embed=embed)

@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(
            title="❌ Usuario no encontrado",
            description="No se encontró ese usuario en el servidor.",
            color=0xFF0000
        )
        embed.set_footer(text="Developed by @adinerar")
        await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, user: discord.User = None):
    """Muestra el avatar de un usuario (propio o por ID)"""
    user = user or ctx.author
    
    embed = discord.Embed(
        title=f"🖼️ Avatar de {user.name}",
        color=COLOR_PRINCIPAL
    )
    
    # Avatar principal (siempre el más grande)
    avatar_url = user.display_avatar.url
    
    embed.set_image(url=avatar_url)
    embed.add_field(name="🔗 Links", value=f"[Descargar PNG]({user.display_avatar.replace(format='png').url}) | [Descargar JPG]({user.display_avatar.replace(format='jpg').url}) | [Descargar WEBP]({user.display_avatar.replace(format='webp').url})")
    embed.set_footer(text="Developed by @adinerar")
    
    await ctx.send(embed=embed)

@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.UserNotFound):
        embed = discord.Embed(
            title="❌ Usuario no encontrado",
            description="No se encontró un usuario con esa ID.",
            color=0xFF0000
        )
        embed.set_footer(text="Developed by @adinerar")
        await ctx.send(embed=embed)

@bot.command()
async def banner(ctx, user: discord.User = None):
    """Muestra el banner de un usuario"""
    user = user or ctx.author
    
    # Obtener el banner (necesita fetch_user para banner)
    user_fetch = await bot.fetch_user(user.id)
    
    if user_fetch.banner:
        embed = discord.Embed(
            title=f"🎨 Banner de {user.name}",
            color=COLOR_PRINCIPAL
        )
        
        banner_url = user_fetch.banner.url
        embed.set_image(url=banner_url)
        embed.add_field(name="🔗 Link", value=f"[Descargar]({banner_url})")
        embed.set_footer(text="Developed by @adinerar")
        
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Sin Banner",
            description=f"**{user.name}** no tiene un banner personalizado.",
            color=0xFF0000
        )
        embed.set_footer(text="Developed by @adinerar")
        await ctx.send(embed=embed)

@banner.error
async def banner_error(ctx, error):
    if isinstance(error, commands.UserNotFound):
        embed = discord.Embed(
            title="❌ Usuario no encontrado",
            description="No se encontró un usuario con esa ID.",
            color=0xFF0000
        )
        embed.set_footer(text="Developed by @adinerar")
        await ctx.send(embed=embed)

keep_alive()

token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("La variable de entorno DISCORD_TOKEN no está definida.")

bot.run(token)