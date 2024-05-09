from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from webscraper import WebScraper
from globals import Globals

router = Router()


@router.message(Command('help', 'start'))
async def cmd_help(message: Message):
    if Globals.language == 'rus':
        info = (
            '*Данный бот собирает актуальную информацию о курсе криптовалют со страницы сайта Forbes.*\n\n'
            'Команды:\n'
            '/rates – вывести информацию о криптовалютах\n'
            '/info + {_название/символ_} – узнать больше о криптовалюте\n'
            '/russian или /rus – переключение на русский язык\n'
            '/english или /eng – переключение на английский язык\n')
        await message.answer(info, parse_mode="Markdown")
    else:
        info = (
            '*This bot gathers the latest cryptocurrency exchange rate information from the Forbes website.*\n\n'
            'Commands:\n'
            '/rates – display information about cryptocurrencies\n'
            '/info + {_name/symbol_} – learn more about a cryptocurrency\n'
            '/russian or /rus – set the language to Russian\n'
            '/english or /eng – set the language to English\n')
        await message.answer(info, parse_mode="Markdown")


@router.message(Command('english', 'eng'))
async def cmd_switch_to_eng(message: Message):
    Globals.language = 'eng'
    await message.answer('You have switched to English, '
                         'enter /help to get the list of commands.')


@router.message(Command('russian', 'rus'))
async def cmd_switch_to_rus(message: Message):
    Globals.language = 'rus'
    await message.answer('Вы переключились на русский язык, '
                         'введите /help, чтобы получить список комманд.')


@router.message(Command('rates'))
async def cmd_rates(message: Message):
    scraper = WebScraper()
    data = scraper.scrape()
    info = ''
    for currency in data:
        info += f"*{currency['name']}/{currency['symbol']}:* {currency['price']}\n"
    await message.answer(info, parse_mode="Markdown")


def convert_value(value_str):
    if 'K' in value_str:
        return float(value_str.replace('$', '').replace('K', '')) * 1000
    elif 'M' in value_str:
        return float(value_str.replace('$', '').replace('M', '')) * 1000000
    elif 'B' in value_str:
        return float(value_str.replace('$', '').replace('B', '')) * 1000000000
    elif 'T' in value_str:
        return float(
            value_str.replace(
                '$',
                '').replace(
                'T',
                '')) * 1000000000000
    else:
        return float(value_str.replace('$', '').replace(',', ''))


@router.message(Command('info'))
async def cmd_info(message: Message, command: CommandObject):
    currency_name = command.args
    scraper = WebScraper()
    data = scraper.scrape()
    info = ''
    for currency in data:
        if currency['name'] == currency_name or currency['symbol'] == currency_name:
            hour_dynamics_value = float(
                currency['hour_dynamics'].strip('%').replace(
                    ',', '.'))
            day_dynamics_value = float(
                currency['day_dynamics'].strip('%').replace(
                    ',', '.'))
            week_dynamics_value = float(
                currency['week_dynamics'].strip('%').replace(
                    ',', '.'))

            hour_emoji = "📈" if hour_dynamics_value > 0 else "📉" if hour_dynamics_value < 0 else ""
            day_emoji = "📈" if day_dynamics_value > 0 else "📉" if day_dynamics_value < 0 else ""
            week_emoji = "📈" if week_dynamics_value > 0 else "📉" if week_dynamics_value < 0 else ""
            price_value = convert_value(currency['price'])
            price_emoji = "💵" if price_value < 10 else "💰" if price_value < 1000 else "💰💰" if price_value < 10000 else "💰💰💰"

            market_cap_value = convert_value(currency['market_cap'])
            market_cap_emoji = "💰" if market_cap_value < 1e9 else "💰💰" if market_cap_value < 1e12 else "💰💰💰"

            day_volume_value = convert_value(currency['day_volume'])
            day_volume_emoji = "💰" if day_volume_value < 1e7 else "💰💰" if day_volume_value < 1e9 else "💰💰💰"

            if Globals.language == 'rus':
                info += (f"{'=' * 25}\n"
                         f"*Название:* {currency['name']}\n"
                         f"{'-' * 44}\n"
                         f"*Символ:* {currency['symbol']}\n"
                         f"{'-' * 44}\n"
                         f"*Цена:* {currency['price']} {price_emoji}\n"
                         f"{'-' * 44}\n"
                         f"*За 1 час:* {currency['hour_dynamics']} {hour_emoji}\n"
                         f"{'-' * 44}\n"
                         f"*За 24 часа:* {currency['day_dynamics']} {day_emoji}\n"
                         f"{'-' * 44}\n"
                         f"*За 7 дней:* {currency['week_dynamics']} {week_emoji}\n"
                         f"{'-' * 44}\n"
                         f"*Капитализация:* {currency['market_cap']} {market_cap_emoji}\n"
                         f"{'-' * 44}\n"
                         f"*Объем за день:* {currency['day_volume']} {day_volume_emoji}\n"
                         f"{'=' * 25}\n")
            else:
                info += (f"{'=' * 25}\n"
                         f"*Name:* {currency['name']}\n"
                         f"{'-' * 44}\n"
                         f"*Symbol:* {currency['symbol']}\n"
                         f"{'-' * 44}\n"
                         f"*Price:* {currency['price']} {price_emoji}\n"
                         f"{'-' * 44}\n"
                         f"*1H:* {currency['hour_dynamics']} {hour_emoji}\n"
                         f"{'-' * 44}\n"
                         f"*24H:* {currency['day_dynamics']} {day_emoji}\n"
                         f"{'-' * 44}\n"
                         f"*7D:* {currency['week_dynamics']} {week_emoji}\n"
                         f"{'-' * 44}\n"
                         f"*Market Cap:* {currency['market_cap']} {market_cap_emoji}\n"
                         f"{'-' * 44}\n"
                         f"*Day Volume:* {currency['day_volume']} {day_volume_emoji}\n"
                         f"{'=' * 25}\n")

    if info == '':
        if Globals.language == 'rus':
            info += 'Валюта не найдена. Пожалуйста, убедитесь, что название введено правильно.'
        else:
            info += 'Currency not found. Please make sure the typed-in name is correct.'
    await message.answer(info, parse_mode="Markdown")
