# Standardowe biblioteki
from dataclasses import dataclass

# Zewnętrzne biblioteki
import discord

@dataclass(frozen=True)
class Constants:
    """
    Przydatne stałe o wartościach wykorzystywanych w różnych częściach oprogramowania.

    Attributes:
        KOLOR (discord.Color): discord.Color(0xFFFFFF)
        KRÓTSZA_STOPKA (str): Krótka stopka w embedach bez informacji licencyjnych.
        DŁUŻSZA_STOPKA (str): Pełna stopka w embedach z informacjami licencyjnymi.
    """

    # 0xFFFFFF to kolor biały w zapisie szesnastkowym
    KOLOR: discord.Color = discord.Color(0xFFFFFF)
    KRÓTSZA_STOPKA: str = "femboybot the goat"
    DŁUŻSZA_STOPKA: str = ""