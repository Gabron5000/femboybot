import random
import discord
from src.handlers.logging import logiKonsoli, logujPolecenia

# Lista Twoich ulubionych linków do GIF-ów
ULUBIONE_GIFY = [
    "https://cdn.discordapp.com/attachments/1055391927740137552/1516169779562676315/israel_IMG_3387.gif?ex=6ac74ce4&is=6ac5fb64&hm=a72fb81c66881434efc1c3995855a7822e86ec9330239024b683a2e209c10dc8&",
    "https://cdn.discordapp.com/attachments/1217928649727148032/1279446703791144981/attachment.gif?ex=6ac7a799&is=6ac65619&hm=6619b2ff874bc8d7fd1c26ca4e8b15ee08dad11c89038196101b264ddbab8891&",
    "https://cdn.discordapp.com/attachments/1093525673060081754/1428445268159758519/mozesz_dac_jakas_nazwe.gif?ex=6ac73413&is=6ac5e293&hm=f7f1a2758596451dc0d98454ef085db3ef1ed0ec9297cec5655ac990598ea46e&",
    "https://cdn.discordapp.com/attachments/879640979076964412/1343263767458349228/attachment.gif?ex=6ac7211e&is=6ac5cf9e&hm=6cdf2be10ccb110e5bc28f60bd71ad1676ae5661f430a27fb6f7b779b94175df&",
    "https://cdn.discordapp.com/attachments/1099822350465253391/1489608461300928622/attachment.gif?ex=6ac791fc&is=6ac6407c&hm=4913564e77d9452ebf3588c6512ec85167309e0f48d2440e47ce023f975b428f&",
    "https://cdn.discordapp.com/attachments/1252970530727002212/1313501608281243721/Femboygif.gif?ex=6ac79eb3&is=6ac64d33&hm=e05d0af9c6bb3683e2f0776f302f45bc9d8c1386364cf14ed8ef505bce36e780&",
    "https://media.discordapp.net/attachments/1070865073230319677/1179484046468841603/1689981933309283.gif?ex=6ac7335e&is=6ac5e1de&hm=1e9d3b24335237a3534646ff9396b37e65ee3a7773ff7c8ff538dd068eefbedb&",
    "https://cdn.discordapp.com/attachments/1433581888735543306/1459718923803951144/worse_than_hitler.gif?ex=6ac798ef&is=6ac6476f&hm=7dd08968faa8c1a9744009fd794fbaddbaf68823f6eae1ffc432f07897407a86&",
    "https://cdn.discordapp.com/attachments/1255430717135912981/1409521857031311450/togif.gif?ex=6ac79306&is=6ac64186&hm=19163a17995b877924cdaee0bd059062805f702293ece48f98aaa405decd119a&",
    "https://cdn.discordapp.com/attachments/1255903627328098374/1396815609525829703/attachment.gif?ex=6ac77de8&is=6ac62c68&hm=8e309760f1cf4753402a0ef0bb9d4a30736f15aa9057e37f3b206da56f151322&",
    "https://cdn.discordapp.com/attachments/1450616153658359890/1455662859479683273/17313552171839433.gif?ex=6ac757ee&is=6ac6066e&hm=68deb9c6fa54aded3c5485b496959811ecdedd62de9b24ffb27cf9dcaab216bd&",
    "https://cdn.discordapp.com/attachments/919335494473621564/1502043468531241100/attachment.gif?ex=6ac7533d&is=6ac601bd&hm=a4b363cc84a222bf2a80f1473c7f6cd7b5d34bb7ecc77c5f1313e831b8f0e22c&"
    # Dodaj tutaj tyle linków, ile chcesz
]

def ustaw(bot: discord.Client) -> None:
    """
    Rejestruje polecenie `/response` w drzewie bota.
    """

    @bot.tree.command(
        name="response",
        description="Wysyła losowego GIF-a z listy ulubionych"
    )
    async def response(interaction: discord.Interaction) -> None:
        try:
            if not ULUBIONE_GIFY:
                await interaction.response.send_message(
                    "Lista GIF-ów jest pusta!", ephemeral=True
                )
                return

            # Losujemy jeden link z listy
            wybrany_gif = random.choice(ULUBIONE_GIFY)

            # Wysyłamy sam link (Discord automatycznie wyświetli z niego GIF)
            await interaction.response.send_message(wybrany_gif)
            logujPolecenia(interaction, sukces=True)

        except Exception as e:
            logujPolecenia(interaction, sukces=False, wiadomośćBłędu=str(e))
            logiKonsoli.exception(f"Błąd podczas wykonywania /response: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "Wystąpił błąd podczas wysyłania GIF-a.", ephemeral=True
                )