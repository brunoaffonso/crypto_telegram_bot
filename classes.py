import requests
import telegram


class CoinGeckoAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def ping(self) -> bool:
        print('Checking API...')
        url = f'{self.base_url}/ping'
        return requests.get(url).status_code == 200

    def price_search(self, coin_id_list: list[str]) -> tuple:
        price_list = []
        updated_at_list = []
        coin = []

        for coin_id in coin_id_list:
            print(f'Searching {coin_id} price...')
            url = f'{self.base_url}/simple/price?ids={coin_id}&vs_currencies=BRL&include_last_updated_at=true'

            response = requests.get(url)

            if response.status_code == 200:
                coin_data = response.json().get(coin_id, None)
                price = coin_data.get('brl', None)
                updated_at = coin_data.get('last_updated_at', None)

                price_list.append(price)
                updated_at_list.append(updated_at)
                coin.append(coin_id)

            else:
                raise ValueError('Código de Requisição diferente de 200')

        return price_list, updated_at_list, coin


class TelegramBot:
    def __init__(self, token: str):
        self.bot = telegram.Bot(token=token)
        self.chats = set()
        updates = self.bot.get_updates()
        for i in updates:
            self.chats.add(i.effective_chat.id)

    def send_message(self, markdown_text: str):
        for chat in self.chats:
            self.bot.send_message(text=markdown_text,
                                  chat_id=chat,
                                  parse_mode=telegram.ParseMode.MARKDOWN)
        print('Message sent successfully!')


