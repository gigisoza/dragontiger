from typing import List, Optional
from beanie import Document
from datetime import datetime


class User(Document):
    email: str
    password: str


class Game(Document):
    name: str
    max_limit_bet: Optional[int] = 10000
    min_limit_bet: Optional[int] = 5


class Round(Document):
    game_id: str
    card_of_dragon: str = None
    card_of_tiger: str = None
    count_cards: int = 0
    winner: str = None
    round_ending_time: float = datetime.timestamp(datetime.now()) + 15
    finished: bool = False


class Stats(Document):
    bet_on_dragon: int
    bet_on_tiger: int
    bet_on_tie: int
    full_bet: int
    player_deposit: int
    game_round_id: int
