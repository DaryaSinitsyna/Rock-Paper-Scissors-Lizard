from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile
from keyboards.keyboards import game_kb, yes_no_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_bot_choice, get_winner

router = Router()
users: dict = {}


@router.message(CommandStart())
async def process_start_command(message: Message):
    photo = FSInputFile('media/sheldon.jpg')
    await message.answer_photo(photo=photo,
                               caption=LEXICON_RU['/start'],
                               reply_markup=yes_no_kb
                               )
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'wins': 0,
                                       'bot_wins': 0}


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    photo = FSInputFile('media/big_bang_theory.jpg')
    await message.answer_photo(photo=photo,
                               caption=LEXICON_RU['/help'],
                               reply_markup=yes_no_kb
                               )


@router.message(F.text == LEXICON_RU['yes_button'])
async def process_yes_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
    await message.answer(text=LEXICON_RU['yes'],
                         reply_markup=game_kb)


@router.message(F.text == LEXICON_RU['no_button'])
async def process_no_answer(message: Message):
    users[message.from_user.id] = {'in_game': False,
                                   'wins': 0,
                                   'bot_wins': 0}

    await message.answer(text=LEXICON_RU['no'])


@router.message(F.text.in_([LEXICON_RU['rock'],
                            LEXICON_RU['paper'],
                            LEXICON_RU['scissors'],
                            LEXICON_RU['lizard'],
                            LEXICON_RU['Spock']
                            ]))
async def process_game_button(message: Message):
    bot_choice = get_bot_choice()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} '
                              f'- {LEXICON_RU[bot_choice]}')
    winner = get_winner(message.text, bot_choice, users, message.from_user.id)
    await message.answer(text=LEXICON_RU[winner].format(users[message.from_user.id]['wins'],
                                                        users[message.from_user.id]['bot_wins']),
                         reply_markup=yes_no_kb)
