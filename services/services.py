import random
from lexicon.lexicon_ru import LEXICON_RU


def get_bot_choice() -> str:
    return random.choice([
        'rock', 'paper', 'scissors',
        'lizard', 'Spock'
    ])


def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            break
    return key


def get_winner(user_choice: str, bot_choice: str, users: dict, id_user: int) -> str:
    user_choice = _normalize_user_answer(user_choice)
    rules = {'scissors': {'paper', 'lizard'},
             'paper': {'rock', 'Spock'},
             'rock': {'lizard', 'scissors'},
             'lizard': {'Spock', 'paper'},
             'Spock': {'scissors', 'rock'}
             }
    if user_choice == bot_choice:
        return 'nobody_won'
    elif bot_choice in rules[user_choice]:
        users[id_user]['wins'] += 1
        return 'user_won'
    users[id_user]['bot_wins'] += 1
    return 'bot_won'
