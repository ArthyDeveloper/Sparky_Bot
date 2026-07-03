from discord.ext import commands
from datetime import datetime, timezone

class Ping(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="ping", aliases=["pingue", "pong", "pongue"])
  async def pint(self, ctx):
    msg_time = ctx.message.created_at
    now = datetime.now(timezone.utc)
    ping = round((now - msg_time).total_seconds() * 1000) *-1

    answer = "Ping!" if ctx.invoked_with in ["pong", "pongue"] else "Pong!"

    await ctx.send(f"{answer} {ping}ms")

async def setup(bot):
  await bot.add_cog(Ping(bot))