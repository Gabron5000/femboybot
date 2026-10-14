# Standardowe biblioteki
import asyncio

# Zewnętrzne biblioteki
import discord

# Wewnętrzne importy
from src.classes.constants import Constants
from src.handlers.logging import logiKonsoli
from src.helpers.helpers import (
    ograniczReagowanie,
    ograniczUsuwanie,
    ograniczWysyłanie
)

async def wyślijAktualizacje(
    kanał: discord.TextChannel,
    identyfikatorSerwera: int,
    informacjeDodatkowe: str,
    aktualneWpisyZastępstw: list[tuple[str, list[str]]]
) -> None:
    """
    Wysyła aktualizacje zastępstw do konkretnego kanału tekstowego Discord.
    """

    # Customowe opisy nagłówka
    opisTylkoDlaInformacjiDodatkowych = (
        "**Informacje dodatkowe zastępstw:**"
        f"\n{informacjeDodatkowe}"
        "\n\n**Informacja o tej wiadomości:**"
        "\nSłuchaj stary, wszyscy przyszli Brak nowych zastępstw pasujących do Twoich filtrów."
    )
    
    opisDlaInformacjiDodatkowych = (
        "**Informacje dodatkowe:**"
        f"\n{informacjeDodatkowe}"
        "\n\n**Informacja o tej wiadomości:**"
        "\nWszystkie zastępstwa dla Twojej klasy znajdują się poniżej."
    )

    try:
        ostatniaWiadomość = None
        tytuł = ""

        # 1. BRAK ZASTĘPSTW DLA CAŁEJ SZKOŁY I BRAK INFO DODATKOWYCH
        if not informacjeDodatkowe and not aktualneWpisyZastępstw:
            embed = discord.Embed(
                title="i got some bad news...",
                description="Słuchaj stary, wszyscy przyszli,  Brak jakichkolwiek zastępstw.",
                color=Constants.KOLOR
            )
            embed.set_footer(text=Constants.KRÓTSZA_STOPKA)
            await ograniczWysyłanie(kanał, embed=embed)

        # 2. SĄ TYLKO INFORMACJE DODATKOWE (Brak zastępstw dla wybranej klasy)
        elif informacjeDodatkowe and not aktualneWpisyZastępstw:
            embed = discord.Embed(
                title="**Zastępstwa:**",
                description=opisTylkoDlaInformacjiDodatkowych,
                color=Constants.KOLOR
            )
            embed.set_footer(text=Constants.KRÓTSZA_STOPKA)
            await ograniczWysyłanie(kanał, embed=embed)

        # 3. SĄ ZASTĘPSTWA DLA KLASY
        elif (informacjeDodatkowe and aktualneWpisyZastępstw) or (aktualneWpisyZastępstw):
            # Wysyłanie i automatyczne kasowanie powiadomienia @everyone
            if kanał.permissions_for(kanał.guild.me).mention_everyone:
                wzmianka = await ograniczWysyłanie(kanał, "@everyone Zastępstwa zostały zaktualizowane!", allowed_mentions=discord.AllowedMentions(everyone=True))
                await asyncio.sleep(5)
                try:
                    await ograniczUsuwanie(wzmianka)
                except Exception:
                    pass
            else:
                logiKonsoli.warning(
                    f"Brak uprawnień do używania @everyone dla serwera o ID {identyfikatorSerwera}. Wzmianka została pominięta."
                )

            # Główna wiadomość nagłówkowa
            embed = discord.Embed(
                title="**Zastępstwa zostały zaktualizowane**",
                description=opisDlaInformacjiDodatkowych if informacjeDodatkowe else "**Wszystkie zastępstwa znajdują się pod tą wiadomością.**",
                color=Constants.KOLOR
            )
            embed.set_footer(text=Constants.DŁUŻSZA_STOPKA)
            await ograniczWysyłanie(kanał, embed=embed)

            # Wysyłanie poszczególnych kart nauczycieli
            for tytuł, wpisyZastępstw in aktualneWpisyZastępstw:
                # Pomijaj całkowicie nieprzypisane klasy
                if "Zastępstwa z nieprzypisanymi klasami" in tytuł:
                    continue

                tekstZastępstw = "\n\n".join(wpisyZastępstw)

                embed = discord.Embed(
                    title=f"**{tytuł}**",
                    description=tekstZastępstw,
                    color=Constants.KOLOR
                )
                embed.set_footer(text=Constants.KRÓTSZA_STOPKA)

                ostatniaWiadomość = await ograniczWysyłanie(kanał, embed=embed)

        # Dodanie reakcji serduszka pod ostatnią kartą
        if ostatniaWiadomość:
            await ograniczReagowanie(ostatniaWiadomość, "❤️")

    except discord.DiscordException as e:
        logiKonsoli.exception(
            f"Wystąpił błąd podczas wysyłania wiadomości do serwera o ID {identyfikatorSerwera}. Więcej informacji: {e}"
        )
    except Exception as e:
        logiKonsoli.exception(
            f"Wystąpił nieoczekiwany błąd podczas wysyłania wiadomości do serwera o ID {identyfikatorSerwera}. Więcej informacji: {e}"
        )