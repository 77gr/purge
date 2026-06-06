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
