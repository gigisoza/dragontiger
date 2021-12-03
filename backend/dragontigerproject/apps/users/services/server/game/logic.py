async def betting(card_type, stats, load):
    if card_type == "dragon":
        stats.bet_on_dragon += load
        stats.player_deposit -= load
    elif card_type == "tiger":
        stats.bet_on_tiger += load
        stats.player_deposit -= load
    else:
        stats.bet_on_tie += load
        stats.player_deposit -= load

    stats.full_bet += load
    return await stats.save()


async def winner(dragon, tiger, game_round):
    try:
        if dragon[:-1] > tiger[:-1]:
            game_round.finished = True
            return "dragon"
        elif dragon[:-1] < tiger[:-1]:
            game_round.finished = True
            return "tiger"
    except TypeError:
        print("waiting for cards...")


async def payout(round_id, game_round, stats):
    fullstats = await stats.find_all().to_list()
    for player in fullstats:
        if player.game_round_id == round_id:
            if game_round.winner == 'dragon' and player.bet_on_dragon > 0:
                player.player_deposit += player.bet_on_dragon * 2
                return await player.save()
            elif game_round.winner == 'tiger' and player.bet_on_tiger > 0:
                player.player_deposit += player.bet_on_tiger * 2
                return await player.save()
            elif game_round.winner == 'tie' and player.bet_on_tie > 0:
                player.player_deposit += player.bet_on_tie * 11
                return await player.save()
