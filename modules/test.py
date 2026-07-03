from discord.ext import commands

class Test(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="test", aliases=["t", "teste"])
  async def test(self, ctx, t1: str, t2: str):
    message = ">>> Isso é um teste\n"
    message += "Testando concatenação"
    await ctx.send(f"{t1} {t2}")
  
async def setup(bot):
  await bot.add_cog(Test(bot))