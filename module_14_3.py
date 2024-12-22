from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton( text = 'Рассчитать')
button2 = KeyboardButton( text = 'Информация')
button3 = KeyboardButton( text = 'Купить')
kb.row(button1, button2, button3)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
in_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.row(in_button1, in_button2)

kb3 = InlineKeyboardMarkup(resize_keyboard=True)
button_1 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button_2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button_3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button_4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb3.row(button_1, button_2, button_3, button_4)

@dp.message_handler(commands=['start'])
async def start(message):
    print('start')
    await message.answer('Привет! Я бот помогающий твоему здоровью.',
                         reply_markup = kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)

@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(ag=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(grow=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weig=message.text)
    data = await state.get_data()
    norma = int(10 * int(data['weig']) + 6.25 * int(data['grow']) - 5 * int(data['ag']) + 5)
    await message.answer(f"Ваша норма в сутки {norma} ккал")
    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(4):
        number = i + 1
        await message.answer(f'Название: Product{number} | Описание: описание{number} | Цена: {number*100}')
        with open (f'{str(number) + ".png"}', 'rb') as img:
            await message.answer_photo(img)

    await message.answer(text='Выберите продукт для покупки: ', reply_markup=kb3)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler()
async def all_message(message):
    print(message)
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
