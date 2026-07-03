from discord.ext import commands
from nbt import nbt
import dotenv, os

class Scheme(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(name="scheme", aliases=["schema", "schemes", "schemas", "schematic", "schematics"])
  async def scheme(self, ctx, player="", scheme=""):
    env = dotenv.dotenv_values(".env")
    
    #player, scheme = 1, "casa"
    message = ""

    schemes = env["SCHEMATICS_PATH"]
    players = os.listdir(f"{schemes}")

    def getMaterials(path: str):
      nbtf = nbt.NBTFile(path)

      count = {}
      palette = [block["Name"].value for block in nbtf["palette"]]
      states = [state["state"].value for state in nbtf["blocks"]]
      sizes = nbtf["size"]
      largura, altura, comprimento = sizes[0].value, sizes[1].value, sizes[2].value

      for state in states:
        try:
          count[palette[state]] += 1
        except(KeyError):
          count[palette[state]] = 1

      materiais = []
      for block, qtd in sorted(count.items(), key=lambda item: item[1], reverse=True):
        materiais.append({"block":block, "quantity":qtd})
      
      dados = {"tamanho": {"x":largura, "y":altura, "z":comprimento}, "materiais": materiais}

      return (dados)

    if not player and not scheme:
      message = "Escolha um jogador:\n""> ;scheme Num\n""\n""Ou escolha diretamente:\n""> ;scheme Num NomeEsquema\n\n""Jogadores:\n"
      for idx, p in enumerate(players):
        message += f"[{idx+1}] - {p}\n"
      
      await ctx.send(message)

    elif player and not scheme:
      try:
        player = int(player)
        if player - 1 < 0 or player - 1 > len(players) - 1:
          message += "Index Error | Escolha inválida."
          await ctx.send(message)
      except(TypeError):
        await ctx.send("Digite um número de jogador válido.")

      message = f"Schemes de {players[player-1]}:\n"
      scheme_path = f"{schemes}/{players[player-1]}"
      scheme_files = os.listdir(scheme_path)
      for idx, s in enumerate(scheme_files):
        message += f"[{idx+1}] - {s.removesuffix(".nbt")}\n"
        await ctx.send(message)
      
      print(message)

    elif player and scheme:
      try:
        player = int(player)
        player_schemes_path = f"{schemes}/{players[player-1]}"
        scheme_files = os.listdir(player_schemes_path)
        print(scheme_files)
        
        try:
          scheme = int(scheme)
          if scheme <= 0 or scheme > len(scheme_files)+1:
            await ctx.send("Seleção de Schematic inválida - IndexError.")
            return
        except(ValueError):
          pass

        scheme_name = scheme if type(scheme) == str else str(scheme_files[scheme-1]).replace(".nbt", "")
        scheme_path = f"{schemes}/{players[player-1]}/{scheme_name}.nbt" if type(scheme) == str else f"{schemes}/{players[player-1]}/{scheme_files[scheme-1]}"
        print(scheme_path)

        data = getMaterials(scheme_path)
        sizes = data["tamanho"]
        materiais = data["materiais"]
        message += f"- Schematic {scheme_name.title()}\n"f"Largura: {sizes["x"]}\nAltura: {sizes["y"]}\nComprimento: {sizes["z"]}\n\n""- Lista de materiais:\n"f""
        for material in materiais:
          qtd = material["quantity"]
          message += f"{material["block"]} - {qtd} {f'({qtd // 64} {"Packs" if qtd // 64 > 1 else "Pack"}' if qtd >= 64 else ""}{f' + {qtd % 64})' if qtd > 64 and qtd % 64 != 0 else ""}\n"
        
        print(message)
        await ctx.send(message.rstrip())

      except(FileNotFoundError):
        message += "Schematic não encontrada."
        print(message)
        await ctx.send(message)

      except(TypeError):
        message += "Erro de parâmetro."
        print(message)
        await ctx.send(message)

async def setup(bot):
  await bot.add_cog(Scheme(bot))
#print(getMaterials(scheme_path))
