import requests
import json
from settings import currencys_designations


class APIException(Exception):
    pass


def construct_incorrect_currency_alarm(currency):
    return f'Введенное значение {currency} не является валютой из списка \
поддерживаемых валют: {list(currencys_designations.keys())}'


class ExchangeRateRequest:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_designation = currencys_designations[quote]
        except KeyError:
            raise APIException(construct_incorrect_currency_alarm(quote))
        try:
            base_designation = currencys_designations[base]
        except KeyError:
            raise APIException(construct_incorrect_currency_alarm(base))
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Введенное значение {amount} не является допустимым числом.')
        if base == quote:
            raise APIException(f'Введены одинаковые валюты {base} и {quote}. Конвертация не возможна.')
        api_address_string = f'https://api.exchangeratesapi.io/\
latest?symbols={quote_designation}&base={base_designation}'
        try:
            request_answer = requests.get(api_address_string)
        except ConnectionError:
            raise APIException("Не удается выполнить запрос к API:", api_address_string)
        answer_dict = json.loads(request_answer.content)
        return answer_dict['rates'][quote_designation] * amount
