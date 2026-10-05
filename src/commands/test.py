# Standardowe biblioteki
import discord
from discord import app_commands

# Wewnętrzne importy
from src.handlers.configuration import konfiguracja
from src.handlers.data import zarządzajPlikiemDanych
from src.handlers.scraper import pobierzZawartośćStrony
from src.handlers.parser import wyodrębnijDane
from src.handlers.notifications import wyślijAktualizacje

@app_commands.command(
    name="test",
    description="[ADMIN] Testowe wywołanie wysyłania dzisiejszych zastępstw."
)
@app_commands.default_permissions(administrator=True)
async def test(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=True)

    identyfikatorSerwera = str(interaction.guild_id)
    konfiguracjaSerwera = await zarządzajPlikiemDanych(identyfikatorSerwera)

    if not konfiguracjaSerwera:
        konfiguracjaSerwera = konfiguracja.get("serwery", {}).get(identyfikatorSerwera, {})

    if not konfiguracjaSerwera:
        await interaction.followup.send(
            "Ten serwer nie został jeszcze skonfigurowany!",
            ephemeral=True
        )
        return

    kodSzkoły = konfiguracjaSerwera.get("szkoła")
    słownikSzkoły = konfiguracja.get("szkoły", {}).get(kodSzkoły)

    if not kodSzkoły or not słownikSzkoły:
        await interaction.followup.send(
            "Nie skonfigurowano prawidłowo szkoły dla tego serwera w pliku config.json.",
            ephemeral=True
        )
        return

    url = słownikSzkoły.get("url")
    kodowanie = słownikSzkoły.get("kodowanie", "utf-8")

    try:
        zawartośćStrony = await pobierzZawartośćStrony(
            bot=interaction.client,
            url=url,
            kodowanie=kodowanie
        )

        if not zawartośćStrony:
            await interaction.followup.send(
                "Nie udało się pobrać strony z zastępstwami dla Twojej szkoły.",
                ephemeral=True
            )
            return

        wybraneKlasy = konfiguracjaSerwera.get("klasy", [])
        wybraniNauczyciele = konfiguracjaSerwera.get("nauczyciele", [])
        
        wszystkieKlasy = []
        for lista in słownikSzkoły.get("lista-klas", {}).values():
            wszystkieKlasy.extend(lista)

        informacjeDodatkowe, wpisyZastępstw = wyodrębnijDane(
            zawartośćStrony=zawartośćStrony,
            wybraneKlasy=wybraneKlasy,
            wybraniNauczyciele=wybraniNauczyciele,
            listaKlas=wszystkieKlasy
        )

        await wyślijAktualizacje(
            kanał=interaction.channel,
            identyfikatorSerwera=interaction.guild_id,
            informacjeDodatkowe=informacjeDodatkowe,
            aktualneWpisyZastępstw=wpisyZastępstw
        )

        await interaction.followup.send(
            "Pomyślnie wysłano testową wiadomość z zastępstwami na ten kanał!",
            ephemeral=True
        )

    except Exception as e:
        await interaction.followup.send(
            f"Wystąpił błąd podczas generowania testowych zastępstw: {e}",
            ephemeral=True
        )

def ustaw(bot: discord.Client) -> None:
    """
    Dodaje polecenie test do drzewa komend bota.
    """
    bot.tree.add_command(test)