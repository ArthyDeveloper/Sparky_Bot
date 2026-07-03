from discord.ext import commands
from mcstatus import JavaServer
import psutil, dotenv, os

class Server(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.env = dotenv.dotenv_values(".env")
  
  @commands.command(name="server", aliases=["sv", "usage", "uso", "cpu", "ram", "pc", "mundo", "world", "tamanho", "status", "stats"])
  async def server(self, ctx):
    message = ""
    # Tamanho do mundo
    def get_folder_size(folder_path):
      total_size = 0
      for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
          fp = os.path.join(dirpath, f)
          if not os.path.islink(fp):
            total_size += os.path.getsize(fp)
      return total_size

    size_bytes = get_folder_size(self.env["WORLD_PATH"])
    world_size = f"{((size_bytes//1024)//1024)/1024:.2f}GB"
    message += f">>> CPU: {int(psutil.cpu_percent(interval=1))}%\n"
    message += f"RAM: {int(psutil.virtual_memory().percent)}%\n\n"
    message += f"Servidor - {self.env['SERVER_MODPACK']}\n"
    #message += f"Versão: {env["SERVER_VERSION"]}\n"

    # Status do servidor
    try:
      server = JavaServer.lookup(f"{self.env["SERVER_IP"]}:{self.env["SERVER_PORT"]}").status()
      message += "Status: Online\n"
      message += f"Players: {server.players.online}/{self.env["SERVER_PLAYER_LIMIT"]}\n"
      message += f"Mundo: {world_size}\n"

      psutil.process_iter.cache_clear()
      processes = psutil.process_iter(["name", "pid", "username"])
      pids = []
      for process in processes:
        if process.name() == "java.exe":
          pids.append(process.pid)

      mem = []
      for pid in pids:
        mem.append(psutil.Process(pid).memory_info().rss/1024/1024/1024)

      server_ram_usage = f"{max(mem):.2f}"
      message += f"RAM: {server_ram_usage}GB | {float(server_ram_usage)*100//16}%\n"
    except(ConnectionRefusedError):
      message += "Status: Offline\n"
      message += f"Mundo: {world_size}\n"

    await ctx.send(message)

async def setup(bot):
  await bot.add_cog(Server(bot))