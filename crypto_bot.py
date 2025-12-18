import telebot
from config import TOKEN
from extension import Converter, APIException

bot = telebot.TeleBot(TOKEN)

keys = {
    'Доллар': 'USD',
    'Евро': 'EUR',
    'Рубль': 'RUB',
    'Биткоин': 'BTC'
}


@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    bot.reply_to(
        message,
        'Чтобы начать работу,введите команду в формате:\n'
        'USD EUR 100\n\n'
        'Показать все доступные валюты:/values'
    )

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:\n'
    for name,code in keys.items():
        text += f'- {name} ({code})\n'
    bot.reply_to(message, text)

@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def convert(message: telebot.types.Message):
    try:
        quote, base, amount = message.text.upper().split()
        amount = float(amount)

        if base not in keys.values() or quote not in keys.values():
            raise APIException('Неизвестная валюта. Используй /values')

        result = Converter.get_price(quote,base,amount)
        bot.send_message(message.chat.id,f'{amount} {base}={result} {quote}')

    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат.\n'
                                          'Пример: USD EUR 100')
    except APIException as e:
        bot.send_message(message.chat.id, str(e))


@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def unknown(message):
    bot.send_message(message.chat.id,'Неизвестная команда')
bot.polling(none_stop=True)
