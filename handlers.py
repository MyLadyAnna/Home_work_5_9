from aiogram import types
from loader import dp
import random

total = 0
max_count = 150 
new_game = False
max_candy = 28
first_move = 0

@dp.message_handler(commands=['start', 'старт'])
async def mes_start(message: types.Message):
    print(message)
    await message.answer(f'Привет, {message.from_user.first_name}. Добро пожаловать в игру с конфетами! \nНа столе лежит {max_count} конфет. '
                          f'Первый ход определяется жеребьёвкой.\nЗа один ход можно забрать не более чем {max_candy} конфет. \n'
                          'Все конфеты достаются сделавшему последний ход.\n'
                          'Чтобы узнать все доступные команды нажми /help')

@dp.message_handler(commands=['new_game'])
async def mes_NG(message: types.Message):
    global new_game
    global first_move
    global total
    global max_count
    new_game = True
    total = max_count
    first_move = random.randint(0,1)
    await message.answer('Игра началась!')
    if first_move == 1:
        await message.answer(f'По жребию первый ход твой, {message.from_user.first_name}! Возьми конфеты.') 
    else:
        await message.answer('По жребию первым ходит бот.')
        await bot_move(message)

@dp.message_handler(commands=['help'])
async def mes_help(message: types.Message):
    await message.answer(f'Команды: \n \t /new_game - начать новую игру \n \t /stop_game - принудительно закончить игру\n'
                          f'\t /set и нужное количество конфет (например, /set 200) - изменить первоначальное количество конфет. Данную команду необходимо вводить до начала игры!')    

@dp.message_handler(commands=['stop_game'])
async def mes_SG(message: types.Message):
    global new_game
    new_game = False
    await message.answer('Игра закончена!')

# /set 200
@dp.message_handler(commands=['set'])       # Установить кол-во конфет
async def mes_set(message: types.Message):
    global max_count
    global new_game
    count = message.text.split()[1]
    if not new_game:
        if count.isdigit() and int(count) >= 100:
            max_count = int(count)
            await message.answer(f'Конфет теперь будет {count}')
            # чтобы игра не заканчивалась за 1-3 хода 
        elif count.isdigit() and int(count) < 100:
            await message.answer(f'{message.from_user.first_name}, введи, пожалуйста, число больше 100, чтобы игра была интереснее :)')
        else:
            await message.answer(f'{message.from_user.first_name}, напиши количество конфет цифрами!')
    else:
        await message.answer(f'{message.from_user.first_name}, нельзя менять правила во время игры!')

@dp.message_handler() 
# Пусто в скобках означает, что бот будет реагировать так как описали ниже на ВСЕ команды, кроме тех, что описаны выше
async def mes_take_candy(message: types.Message):
    global total
    global new_game
    global max_candy
    if new_game:     
        if message.text.isdigit() and 0 < int(message.text) <= max_candy:
            total -= int(message.text)
            if total <= 0:
                await message.answer(f'{message.from_user.first_name}, ты победил(а)!. ')
                new_game = False
            else:
                await message.answer(f'{message.from_user.first_name} взял(а) {message.text} конфет. '
                                 f'На столе осталось {total} конфет')
                await bot_move(message)
        elif message.text.isdigit() and (int(message.text) <= 0 or int(message.text) > max_candy):
             await message.answer(f'{message.from_user.first_name}, необходимо указать число от 1 до 28.')
        else:
            await message.answer(f'{message.from_user.first_name}, напиши количество конфет цифрами.')
            
#Фун хода бота
async def bot_move(message: types.Message):
    global total
    global max_candy
    global new_game
    bot_take = 0
    if 0 < total <= max_candy:
        bot_take = total
        total -= bot_take
        await message.answer(f'Бот взял последние {bot_take} конфет(ы) и одержал победу')
        new_game = False
    else:
        remainder = total%29 
        bot_take = remainder if remainder != 0 else 28
        total -= bot_take
        await message.answer(f'Бот взял {bot_take} конфет. '
                             f'На столе осталось {total}')