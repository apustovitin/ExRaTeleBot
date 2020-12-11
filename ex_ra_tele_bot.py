import telebot
from extensions import APIException, ExchangeRateRequest
from settings import TOKEN, currencys_designations


bot = telebot.TeleBot(TOKEN)


def help_message():
    return """Введите через пробел:
<имя валюты, в деньги которой надо конвертировать деньги исходной валюты>
<имя исходной валюты>
<количество денег в исходной валюте>
Список поддерживаемых валют: """ + str(list(currencys_designations.keys()))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    bot.reply_to(message, help_message())


@bot.message_handler(commands=['values', ])
def send_welcome(message: telebot.types.Message):
    bot.reply_to(message, 'Список поддерживаемых валют: ' + str(list(currencys_designations.keys())))


@bot.message_handler(content_types=['text', ])
def convert_currency(message: telebot.types.Message):
    try:
        words_from_user_message = message.text.split(' ')
        if len(words_from_user_message) != 3:
            raise APIException('Введено неверное количество параметров', help_message())
        quote, base, amount = words_from_user_message
        total_quote = ExchangeRateRequest.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Случилась предвиденная ошибка.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Случилась непредвиденная ошибка.\n{e}')
    else:
        result_text = f'Цена {amount} {base} в {quote} = {round(total_quote, 2)}'
        bot.send_message(message.chat.id, result_text)


bot.polling()
