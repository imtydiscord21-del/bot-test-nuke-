# api.py — utilidades de servidor (crear/borrar masivo)
import asyncio
import discord


async def resolve_member(guild: discord.Guild, target: str):
    """Acepta mencion, ID, o username."""
    target = target.strip().lstrip("<@!").rstrip(">")
    if target.isdigit():
        m = guild.get_member(int(target))
        if m: return m
        try:
            return await guild.fetch_member(int(target))
        except discord.NotFound:
            return None
    # buscar por nombre
    low = target.lower()
    for m in guild.members:
        if m.name.lower() == low or (m.nick and m.nick.lower() == low):
            return m
    for m in guild.members:
        if low in m.name.lower():
            return m
    return None


async def create_mass_roles(guild, base_name, qty):
    created = 0
    for i in range(1, qty + 1):
        try:
            await guild.create_role(name=f"{base_name}-{i}", reason="Mass roles")
            created += 1
            await asyncio.sleep(0.2)
        except discord.HTTPException:
            pass
    return created


async def delete_all_roles(guild):
    deleted = 0
    tasks = []
    for r in guild.roles:
        if r.name == "@everyone" or r.managed:
            continue
        tasks.append(r.delete(reason="Mass delete"))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for r in results:
        if not isinstance(r, Exception):
            deleted += 1
    return deleted


async def delete_all_channels(guild):
    deleted = 0
    tasks = [ch.delete(reason="Mass delete") for ch in guild.channels]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for r in results:
        if not isinstance(r, Exception):
            deleted += 1
    return deleted


async def create_mass_channels(guild, base_name, qty):
    created = 0
    tasks = []
    for i in range(1, qty + 1):
        tasks.append(guild.create_text_channel(name=f"{base_name}-{i}", reason="Mass create"))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for r in results:
        if not isinstance(r, Exception):
            created += 1
    return created


async def mass_ban(guild, razon="Mass ban"):
    banned = 0
    tasks = []
    for m in guild.members:
        if m.id == guild.owner_id or m == guild.me:
            continue
        tasks.append(guild.ban(m, reason=razon, delete_message_days=0))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for r in results:
        if not isinstance(r, Exception):
            banned += 1
    return banned