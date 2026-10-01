# main.py — EXCALIBUR BOT (discord.py)
import discord
from discord.ext import commands
import os, asyncio, datetime
from dotenv import load_dotenv

import api
import nuke as nk

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")

if not TOKEN:
    raise SystemExit("[X] Falta DISCORD_TOKEN en las variables de entorno.")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"[OK] Conectado como {bot.user} (ID: {bot.user.id})")
    print(f"[OK] En {len(bot.guilds)} servidor(es)")
    try:
        await bot.change_presence(activity=discord.Game(name=".help | EXCALIBUR"))
    except Exception:
        pass


@bot.command(name="help")
async def cmd_help(ctx):
    embed = discord.Embed(
        title="EXCALIBUR BOT",
        description="Comandos disponibles (prefijo `.`)",
        color=0xFF0000,
    )
    embed.add_field(name="`.ping`", value="Latencia del bot", inline=False)
    embed.add_field(name="`.serverinfo`", value="Info del servidor", inline=False)
    embed.add_field(name="`.userinfo <@user|id>`", value="Info del usuario", inline=False)
    embed.add_field(name="`.ban <@user|id> [razon]`", value="Banea", inline=False)
    embed.add_field(name="`.kick <@user|id> [razon]`", value="Expulsa", inline=False)
    embed.add_field(name="`.unban <id>`", value="Desbanea", inline=False)
    embed.add_field(name="`.mute <@user|id> <min>`", value="Timeout", inline=False)
    embed.add_field(name="`.purge <n>`", value="Borra n mensajes", inline=False)
    embed.add_field(name="`.send <canal_id> <msg>`", value="Envia mensaje", inline=False)
    embed.add_field(name="`.embed <canal_id> <titulo> | <desc>`", value="Embed", inline=False)
    embed.add_field(name="`.massroles <nombre> <qty>`", value="Crea N roles", inline=False)
    embed.add_field(name="`.delroles`", value="Borra TODOS los roles", inline=False)
    embed.add_field(name="`.delchannels`", value="Borra TODOS los canales", inline=False)
    embed.add_field(name="`.createchannels <nombre> <qty>`", value="Crea N canales", inline=False)
    embed.add_field(name="`.massban`", value="Banea a TODOS los miembros", inline=False)
    embed.add_field(name="`.nuke <n_canales> <msgs> <mensaje>`", value="NUKE TOTAL RAPIDO", inline=False)
    embed.set_footer(text="Made By Coldwix & Exagonal")
    await ctx.send(embed=embed)


@bot.command(name="ping")
async def cmd_ping(ctx):
    lat = round(bot.latency * 1000)
    await ctx.send(f"Pong `{lat}ms`")


@bot.command(name="serverinfo")
async def cmd_serverinfo(ctx):
    g = ctx.guild
    embed = discord.Embed(title=g.name, color=0xFF0000)
    embed.add_field(name="ID", value=str(g.id))
    embed.add_field(name="Miembros", value=str(g.member_count))
    embed.add_field(name="Owner", value=str(g.owner))
    embed.add_field(name="Canales", value=str(len(g.channels)))
    embed.add_field(name="Roles", value=str(len(g.roles)))
    embed.add_field(name="Boosts", value=f"{g.premium_subscription_count} (Nivel {g.premium_tier})")
    if g.icon:
        embed.set_thumbnail(url=g.icon.url)
    await ctx.send(embed=embed)


@bot.command(name="userinfo")
async def cmd_userinfo(ctx, *, target: str = None):
    if target is None:
        member = ctx.author
    else:
        member = await api.resolve_member(ctx.guild, target)
        if member is None:
            return await ctx.send("[X] Usuario no encontrado.")
    embed = discord.Embed(title=str(member), color=0xFF0000)
    embed.add_field(name="ID", value=str(member.id))
    embed.add_field(name="Bot", value="Si" if member.bot else "No")
    embed.add_field(name="Nick", value=member.nick or "Ninguno")
    embed.add_field(name="Creado", value=member.created_at.strftime("%Y-%m-%d"))
    if member.joined_at:
        embed.add_field(name="Se unio", value=member.joined_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)


@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def cmd_ban(ctx, target: str, *, razon: str = "Sin razon"):
    member = await api.resolve_member(ctx.guild, target)
    if member is None:
        return await ctx.send("[X] Usuario no encontrado.")
    try:
        await member.ban(reason=razon, delete_message_days=0)
        await ctx.send(f"[OK] {member} baneado. Razon: {razon}")
    except discord.Forbidden:
        await ctx.send("[X] Sin permisos.")


@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def cmd_kick(ctx, target: str, *, razon: str = "Sin razon"):
    member = await api.resolve_member(ctx.guild, target)
    if member is None:
        return await ctx.send("[X] Usuario no encontrado.")
    try:
        await member.kick(reason=razon)
        await ctx.send(f"[OK] {member} expulsado. Razon: {razon}")
    except discord.Forbidden:
        await ctx.send("[X] Sin permisos.")


@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def cmd_unban(ctx, user_id: int, *, razon: str = "Desban"):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=razon)
        await ctx.send(f"[OK] {user} desbaneado.")
    except discord.NotFound:
        await ctx.send("[X] Ese usuario no esta baneado.")
    except discord.Forbidden:
        await ctx.send("[X] Sin permisos.")


@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def cmd_mute(ctx, target: str, minutos: int = 10):
    member = await api.resolve_member(ctx.guild, target)
    if member is None:
        return await ctx.send("[X] Usuario no encontrado.")
    until = discord.utils.utcnow() + datetime.timedelta(minutes=minutos)
    try:
        await member.timeout(until, reason="Mute")
        await ctx.send(f"[OK] {member} muteado {minutos} min.")
    except discord.Forbidden:
        await ctx.send("[X] Sin permisos.")


@bot.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def cmd_purge(ctx, cantidad: int = 10):
    cantidad = max(1, min(100, cantidad))
    deleted = await ctx.channel.purge(limit=cantidad + 1)
    await ctx.send(f"[OK] {len(deleted)-1} mensajes borrados.", delete_after=3)


@bot.command(name="send")
@commands.has_permissions(administrator=True)
async def cmd_send(ctx, canal_id: int, *, mensaje: str):
    ch = bot.get_channel(canal_id)
    if ch is None:
        return await ctx.send("[X] Canal no encontrado.")
    try:
        await ch.send(mensaje)
        await ctx.send("[OK] Enviado.")
    except discord.Forbidden:
        await ctx.send("[X] Sin permisos en ese canal.")


@bot.command(name="embed")
@commands.has_permissions(administrator=True)
async def cmd_embed(ctx, canal_id: int, *, contenido: str):
    if "|" not in contenido:
        return await ctx.send("Uso: `.embed <canal_id> <titulo> | <descripcion>`")
    titulo, desc = contenido.split("|", 1)
    ch = bot.get_channel(canal_id)
    if ch is None:
        return await ctx.send("[X] Canal no encontrado.")
    embed = discord.Embed(
        title=titulo.strip(),
        description=desc.strip(),
        color=0xFF0000,
    )
    await ch.send(embed=embed)
    await ctx.send("[OK] Embed enviado.")


@bot.command(name="massroles")
@commands.has_permissions(administrator=True)
async def cmd_massroles(ctx, nombre: str = "Rol", cantidad: int = 10):
    cantidad = max(1, min(100, cantidad))
    await ctx.send(f"[..] Creando {cantidad} roles...")
    created = await api.create_mass_roles(ctx.guild, nombre, cantidad)
    await ctx.send(f"[OK] {created} roles creados.")


@bot.command(name="delroles")
@commands.has_permissions(administrator=True)
async def cmd_delroles(ctx):
    await ctx.send("[..] Borrando roles...")
    n = await api.delete_all_roles(ctx.guild)
    await ctx.send(f"[OK] {n} roles borrados.")


@bot.command(name="delchannels")
@commands.has_permissions(administrator=True)
async def cmd_delchannels(ctx):
    await ctx.send("[..] Borrando canales...")
    n = await api.delete_all_channels(ctx.guild)
    await ctx.send(f"[OK] {n} canales borrados.")


@bot.command(name="createchannels")
@commands.has_permissions(administrator=True)
async def cmd_createchannels(ctx, nombre: str = "canal", cantidad: int = 10):
    cantidad = max(1, min(150, cantidad))
    await ctx.send(f"[..] Creando {cantidad} canales...")
    n = await api.create_mass_channels(ctx.guild, nombre, cantidad)
    await ctx.send(f"[OK] {n} canales creados.")


@bot.command(name="massban")
@commands.has_permissions(administrator=True)
async def cmd_massban(ctx, *, razon: str = "Mass ban"):
    await ctx.send(f"[..] Baneando a TODOS los miembros...")
    n = await api.mass_ban(ctx.guild, razon)
    await ctx.send(f"[OK] {n} baneados.")


@bot.command(name="nuke")
@commands.has_permissions(administrator=True)
async def cmd_nuke(ctx, qty: int = 30, nm: int = 3, *, msg: str = "@everyone NUKED"):
    if qty > 150: qty = 150
    if nm > 15:  nm = 15
    await ctx.send(f"[!!] NUKE INICIADO -> {qty} canales x {nm} msgs")
    await nk.do_nuke(ctx.guild, qty=qty, nm=nm, msg=msg)
    try:
        await ctx.send("[OK] Nuke completado.")
    except Exception:
        pass


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("[X] No tienes permisos para ese comando.")
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(f"[X] Falta argumento: `{error.param.name}`")
    if isinstance(error, commands.CommandNotFound):
        return
    try:
        await ctx.send(f"[X] Error: {error}")
    except Exception:
        pass


if __name__ == "__main__":
    bot.run(TOKEN)