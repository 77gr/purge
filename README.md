# Purge Discord Bot

Bot de moderación para Discord.

## Preparar antes de ejecutar

1. Instala dependencias:
   ```powershell
   pip install discord.py flask
   ```
2. Define el token de Discord como variable de entorno:
   ```powershell
   $env:DISCORD_TOKEN = "tu_token_aqui"
   ```
3. Ejecuta el bot:
   ```powershell
   python bot.py
   ```

## GitHub

- No subas tu token a GitHub.
- Usa `.gitignore` para ignorar `__pycache__` y archivos sensibles.
- Crea un repositorio en GitHub y añade el remoto:
  ```powershell
  git remote add origin https://github.com/usuario/repositorio.git
  git branch -M main
  git push -u origin main
  ```

## Railway

1. Asegúrate de que `bot.py`, `requirements.txt`, `Procfile` y `.env.example` estén en la raíz del repositorio.
2. En Railway, abre tu proyecto y ve a **Variables** o **Settings → Environment Variables**.
3. Agrega la variable:
   - `DISCORD_TOKEN`
   - valor: el token de tu bot de Discord
4. Si Railway no detecta el `Procfile`, usa el comando de inicio manual en **Settings → Start Command**:
   ```bash
   python bot.py
   ```
5. Luego haz click en **Redeploy**.

> Si Railway lanza el error `La variable de entorno DISCORD_TOKEN no está definida.`, significa que la variable no está configurada en el panel de Railway.
