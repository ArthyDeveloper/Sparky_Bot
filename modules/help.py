from discord.ext import commands
from discord.ext.commands.errors import BadArgument

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.HELP_PAGES = [
    # Pag 1
    ";help [Num].\n"
    "> Alt: ajuda, comandos, cmd.\n"
    ";ping | Testar conexão do Bot.\n"
    "> Alt: pong.\n"
    ";server | Status do servidor e uso de Hardware.\n"
    "> Alt: sv, usage, uso, cpu, ram, pc, mundo, tamanho, status, stats.\n"
    ";radmin | Rede Radmin\n"
    "> Alt: ip, rede.",
    # Pag 2
    ";scheme [Num] | [Scheme / Num]"
    "> Alt: schema, schemes, schemas, schematic, schematics"
    ]
    self.HELP_NUM_PAGES = len(self.HELP_PAGES)
  
  @commands.command(name="help", aliases=["ajuda", "comandos", "cmd"])
  async def help(self, ctx, page:int=1):
    if 0 < int(page) < self.HELP_NUM_PAGES + 1:
      await ctx.send(f">>> Comandos Pág {page}\n\n{self.HELP_PAGES[page-1]}")
    else:
      await ctx.send(f"Use uma página válida! [1 - {self.HELP_NUM_PAGES}]\n"
                     f"Exemplo: {ctx.prefix}help 1")

  @help.error
  async def help_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send(
        f"Faltou a página!\n"
        f"Exemplo: {ctx.prefix}help 1")
    elif isinstance(error, BadArgument):
      await ctx.send(f"Use um `número` válido! [1 - {self.HELP_NUM_PAGES}]\n"
                     f"Exemplo: {ctx.prefix}help 1")

async def setup(bot):
  await bot.add_cog(Help(bot))