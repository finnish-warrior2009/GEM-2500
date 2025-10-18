import discord
from discord.ext import commands 
import os

#DATOS ACTUALIZADOS DE MIGRANTES EN CHILE:

migrantes_años = {
    "2025": 1920000,
    "2024": 1608650,
    "2023": 1918583,
    "2022": 1625074


}

migrantes_origenes = {
    "venezolanos": 728586,
    "peruanos": 260785,
    "haitianos": 188131,
    "colombianos": 209946,
    "bolivianos": 180226,
    "ecuatorianos": 50460,
    "argentinos": 83265,
    "dominicanos": 22836,
    "cubanos": 21305,
    "brasileños": 21272,
    "españoles": 19854,
    "chinos": 15143,
    "estadounidenses": 14783,
    "mexicanos": 8466,
    "alemanes": 7084,
    "franceses": 7051,
    "paraguayos": 6747,
    "uruguayos": 6340,
    "britanicos": 6668,
    "rusos": 1300,
    "croatas": 900,
    "japoneses": 3000,
    "coreanos": 2725,
    "georgianos": 13589,
    "palestinos": 5620,
    "suizos": 6097,
    "hungaros": 1306,
    "total": 1920000
    

}

#CONFIGURACIÓN DEL BOT

#COMANDO PARA EL NÚMERO DE MIGRANTES ENTRE 2022 Y 2025

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name="ayuda")
async def mostrar_ayuda(ctx):
    ayuda_embed = discord.Embed(
        title=" Comandos disponibles",
        description="Lista de comandos para consultar datos sobre la migración en Chile",
        color=discord.Color.green()
    )

    ayuda_embed.add_field(name="!migrantes_chile_años", value="Muestra el número de migrantes en Chile por año (2022-2025).", inline=False)
    ayuda_embed.add_field(name="!migrantes <nacionalidad>", value="Muestra el número de migrantes en Chile de una nacionalidad específica. Ejemplo: \"!migrantes venezolanos.\"", inline=False)
    ayuda_embed.add_field(name="!top10", value="Muestra el top 10 de nacionalidades con más migrantes en Chile.", inline=False)
    ayuda_embed.add_field(name="!less10", value="Muestra el top 10 de nacionalidades con menos migrantes en Chile.", inline=False)
    ayuda_embed.add_field(name="!mayor_migrantes", value="Muestra la nacionalidad con más migrantes en Chile.", inline=False)
    ayuda_embed.add_field(name="!menor_migrantes", value="Muestra la nacionalidad con menos migrantes en Chile.", inline=False)
    ayuda_embed.set_footer(text="Datos de Instituto Nacional de Estadísticas (INE), Servicio Nacional de Migraciones (SERMIG) y Departamento de Extranjería y Migración (DEM) - Actualizado 2024") 
    await ctx.send(embed=ayuda_embed)
                          



@bot.command(name="migrantes_chile_años")
async def cmd_migrantes(ctx):
    response = "Datos de Migrantes en Chile por año: \n"
    for year, count in sorted(migrantes_años.items(), key=lambda x: int(x[0])):
        response += f"**{year}**: {count:,}\n"
    await ctx.send(response)

@bot.command(name="migrantes")
async def cmd_migrantes_pais(ctx, *, pais: str):
    pais = pais.lower().strip()  # normaliza el texto
    if pais in migrantes_origenes:
        cantidad = migrantes_origenes[pais]
        await ctx.send(f"🌎 En Chile hay aproximadamente **{cantidad:,}** migrantes **{pais.capitalize()}**.")
    else:
        await ctx.send(f"⚠️ No tengo datos sobre migrantes **{pais.capitalize()}**.")

@cmd_migrantes_pais.error
async def migrantes_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Debes indicar una nacionalidad. Ejemplo: `!migrantes peruanos`.")

@bot.command(name="top10")
async def cmd_top10(ctx):
    # Ordena el diccionario sin incluir la clave "total"
    top10 = sorted(
        ((pais, cant) for pais, cant in migrantes_origenes.items() if pais != "total"),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    response = "🏆 **Top 10 grupos de migrantes en Chile:**\n"
    for i, (pais, cantidad) in enumerate(top10, start=1):
        response += f"{i}. **{pais.capitalize()}** — {cantidad:,}\n"

    await ctx.send(response)

@bot.command(name="less10")
async def cmd_less10(ctx):
    less10 = sorted(
        ((pais, cant) for pais, cant in migrantes_origenes.items() if pais != "total"),
        key=lambda x: x[1]
    )[:10]
    response = "🔻 **Top 10 grupos de migrantes menos numerosos en Chile:**\n"
    for i, (pais, cantidad) in enumerate(less10, start=1):
        response += f"{i}. **{pais.capitalize()}** — {cantidad:,}\n"

    await ctx.send(response)

@bot.command(name="mayor_migrantes")
async def cmd_mayor_migrantes(ctx):
    mayor = max(
        ((pais, cant) for pais, cant in migrantes_origenes.items() if pais != "total"),
        key=lambda x: x[1]
    )
    pais, cantidad = mayor
    await ctx.send(f"🏅 El grupo de migrantes más numeroso en Chile son los **{pais.capitalize()}**, con aproximadamente **{cantidad:,}** personas.")

@bot.command(name="menor_migrantes")
async def cmd_menor_migrantes(ctx):
    menor = min(
        ((pais, cant) for pais, cant in migrantes_origenes.items() if pais != "total"),
        key=lambda x: x[1]
    )
    pais, cantidad = menor
    await ctx.send(f"📉 El grupo de migrantes menos numeroso en Chile son los **{pais.capitalize()}**, con aproximadamente **{cantidad:,}** personas.")

#EJECUTAR EL BOT

bot.run(os.getenv("DISCORD_TOKEN"))
