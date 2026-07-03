from discord.ext import commands, tasks
from pygtail import Pygtail
import dotenv, asyncio

class Chat(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.env = dotenv.dotenv_values(".env")
    self.chat.start()

  def cog_unload(self):
    self.chat.cancel()

  @tasks.loop(seconds=1)
  async def chat(self):
    canal = self.bot.get_channel(int(self.env["DISCORD_SERVER_CHAT_ID"]))
    messages = []

    def format_msg(msg):
      return msg.replace("\n", "").rsplit("]: ", 1)[-1]

    def msg_queue_add(msg):
      messages.append(msg)

    player_info = "[Server thread/INFO] [minecraft/MinecraftServer]"
    player_info2 = "[Server thread/INFO] [net.minecraft.server.MinecraftServer/]"
    msg_not_perms = ["[minecraft/RconClient]", "[net.minecraft.server.rcon.thread.GenericThread/]", "Invalid component key: pattern<ingredient> - Component", "Notice: Jupiter cannot resolve", "<NONE>", "[<NONE>]", "CAKE BLOCK CONSTRUCTOR LOADED", "at TRANSFORMER/kubejs", "[KubeJS Server/]:", "<init>", "ThreadedAnvilChunkStorage", "No leak was found so far..."]

    for line in Pygtail(self.env["LOGS_PATH"], encoding="utf-8"):
      is_player_log = (player_info in line or player_info2 in line)

      # Conquista
      if is_player_log and "has made the advancement" in line:
        player = format_msg(line).split(" ")[0]
        msg_queue_add(f":trophy: {player} conquistou {format_msg(line).rsplit("advancement ")[-1]}")

      # Objetivo
      elif is_player_log and "has reached the goal" in line:
        player = format_msg(line).split(" ")[0]
        msg_queue_add(f":scroll: {player} alcançou o objetivo {format_msg(line).rsplit("goal ")[-1]}")

      # Desafio
      elif is_player_log and "has completed the challenge" in line:
        player = format_msg(line).split(" ")[0]
        msg_queue_add(f":crossed_swords: {player} cumpriu o desafio {format_msg(line).rsplit("challenge ")[-1]}")

      # Morte
      elif "[tombstone/]:" in line or is_player_log and "has successfully been saved" in line:
        player = format_msg(line).rsplit("The player ")[-1].rsplit(" has successfully been saved")[0]
        msg_queue_add(f":skull_crossbones: {player} morreu!")

      # Entrando no jogo
      elif is_player_log and "joined the game" in line:
        player = format_msg(line).split(" ")[0]
        msg_queue_add(f":signal_strength: {player} entrou no servidor!")

      # Saiu do jogo
      elif is_player_log and "left the game" in line:
        player = format_msg(line).split(" ")[0]
        msg_queue_add(f":signal_strength: {player} saiu do servidor!")

      # Schematics
      elif is_player_log and ("[com.simibubi.create.Create/]" in line or "New Schematic Uploaded: " in line):
        player, schem = line.rstrip().rsplit(": ")[-1].split("/")
        msg_queue_add(f":tools: {player} criou a schematic {schem}.")

      # Mensagens
      elif is_player_log or "[Server]" in line:
        message = True

        if message:
          for item in msg_not_perms:
            if item in line:
              message = False

        if message:
          player = format_msg(line).split(" ")[0]
          msg_queue_add(f":speech_balloon: {player} {line.replace(f"{player} ", "").rsplit("]: ")[-1]}")

    for message in messages:
      await canal.send(message)
    await asyncio.sleep(1)
  
  @chat.before_loop
  async def before_chat(self):
    await self.bot.wait_until_ready()

async def setup(bot):
  await bot.add_cog(Chat(bot))