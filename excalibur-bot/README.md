[README.md](https://github.com/user-attachments/files/32884006/README.md)
# EXCALIBUR BOT

Bot de administración con comandos de nuke/backup/mass-actions.

## Comandos
Prefijo: `.`

- `.help`
- `.ping`
- `.serverinfo`
- `.userinfo <@user|id>`
- `.ban <@user|id> [razon]`
- `.kick <@user|id> [razon]`
- `.unban <id>`
- `.mute <@user|id> <min>`
- `.purge <n>`
- `.send <canal_id> <msg>`
- `.embed <canal_id> <titulo> | <desc>`
- `.massroles <nombre> <qty>`
- `.delroles`
- `.delchannels`
- `.createchannels <nombre> <qty>`
- `.massban`
- `.nuke <qty> <msgs> <msg>`

## Deploy en Railway

1. Sube el repo a GitHub.
2. Entra a https://railway.app → New Project → Deploy from GitHub repo.
3. Selecciona tu repo.
4. En la pestaña **Variables**, agrega:
   - `DISCORD_TOKEN` = tu token del bot
5. Railway detecta `Procfile` y `requirements.txt` automaticamente.
6. Deploy se inicia solo. El bot queda corriendo 24/7.
