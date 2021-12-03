from datetime import datetime
from backend.dragontigerproject import Round, Stats


async def get_create_game_round(game_id: str):
    # game_round = await Round.find_one(Round.game_id == game_id)
    # if game_round:
    #     return game_round
    game_round = Round(game_id=game_id, end_time=datetime.timestamp(datetime.now()) + 15)
    return await game_round.save()


async def get_create_stats(game_id):
    stats = await Stats.find_one(Stats.game_round_id == game_id)
    if stats:
        return stats
    stats = Stats(game_round_id=game_id)
    return await stats.save()

