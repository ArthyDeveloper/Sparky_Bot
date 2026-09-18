from discord.ext import commands
import dotenv

class Ip(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="ip", aliases=["vpn", "rede", "radmin"])
  async def ip(self, ctx):
    env = dotenv.dotenv_values(".env")
    network_name, network_password = eval(env["VPN_NETWORK"])
    answer = (
      ">>> > Rede Radmin:\n"
      f"Nome: {network_name}\n"
      f"Senha: {network_password}\n\n"
      "> Ip do servidor:\n"
      f"{env["SERVER_IP"]}:{env["SERVER_PORT"]}"
    )

    await ctx.send(answer)

async def setup(bot):
  await bot.add_cog(Ip(bot))
