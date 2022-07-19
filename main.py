# # chat_id = 742393719
# {"id":"ethereum","symbol":"eth","name":"Ethereum"}
# {"id":"bitcoin","symbol":"btc","name":"Bitcoin"}
from time import sleep
import locale
from datetime import datetime
from classes import CoinGeckoAPI, TelegramBot
from decouple import config

coin_id_list = []
coin_id = True
while coin_id != '':
    coin_id = input('Type a coin ID to track ou live blank: ')
    coin_id_list.append(coin_id) if coin_id != '' else coin_id

# min_value = int(input('What is the minimum value to track? '))
# max_value = int(input('What is the maximum value to track? '))

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

api = CoinGeckoAPI(base_url='https://api.coingecko.com/api/v3')
bot = TelegramBot(token=config('TOKEN'))

while True:
    if api.ping():
        print('API Online!')
        price, updated_at, coin = api.price_search(coin_id_list=coin_id_list)
        print('Successful price search!')

        for i in range(len(coin_id_list)):
            date_time = datetime.fromtimestamp(updated_at[i]).strftime('%x %X')
            message = f'*Cotação do {coin[i].capitalize()}*: \n' \
                      f'\t*Preço*: R$ {price[i]} \n' \
                      f'\t*Última Atualização*: {date_time} \n' \

            if message:
                bot.send_message(markdown_text=message)

    else:
        print('API Offline.')

    sleep(60)
