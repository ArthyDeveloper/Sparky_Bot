import discord, dotenv, os
from discord.ext import commands
from datetime import datetime, timezone
from mcrcon import MCRcon

def main():
  env = dotenv.dotenv_values(".env")

  intents = discord.Intents.default()
  intents.message_content = True

  bot = commands.Bot(
    command_prefix=env["BOT_PREFIX"],
    intents=intents,
    help_command=None,
    case_insensitive=True
  )

  """
  async def test_loop():
    runs = 0
    while True:
      runs += 1
      print(runs)
      await asyncio.sleep(1)
  """

  @bot.event
  async def on_ready():
    # Carregando Cogs
    total_load_time = 0
    for filename in os.listdir("./modules"):
      if filename.endswith(".py"):
        now = datetime.now(timezone.utc)
        await bot.load_extension(f"modules.{filename[:-3]}")
        end = datetime.now(timezone.utc)
        cog_load_time = round((end - now).total_seconds() * 1000) *1
        total_load_time += cog_load_time
        print(f"- {filename.replace(".py", "").title()} [{cog_load_time}ms]")

    print(f"{bot.user} online! [{total_load_time}ms]")

  @bot.event
  async def on_message(message):
    if message.author == bot.user:
      return

    # Mensagens Discord --> Servidor (RCON)
    canal = str(message.channel.id)
    canal_logs = env["DISCORD_SERVER_CHAT_ID"]
    if canal == canal_logs:
      mensagem = f"<{message.author.display_name}> {message.content}"
      with MCRcon(host=env["SERVER_IP"], password=env["SERVER_RCON_PASSWORD"], port=int(env["SERVER_RCON_PORT"])) as mcr:
        mcr.command(f'say {mensagem}')

    await bot.process_commands(message)

  bot.run(env["DISCORD_TOKEN"])

if __name__ == "__main__":
  main()