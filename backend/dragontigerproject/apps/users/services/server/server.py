import socketio

from urllib.parse import parse_qs
from beanie import PydanticObjectId
from backend.dragontigerproject.apps.users.services.docs.documents import Game, Round, Stats
from backend.dragontigerproject.apps.users.services.server.game.logic import winner, payout, betting
from backend.dragontigerproject.apps.users.services.server.queries import get_create_game_round, get_create_stats

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
sio_app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    game_id = parse_qs(environ['QUERY_STRING']).get("game_id")[0]
    game = await Game.get(PydanticObjectId(game_id))
    game_round = await get_create_game_round(game_id)
    send_data = {
        "min_limit_bet": game.min_limit_bet,
        "max_limit_bet": game.max_limit_bet,
        "name": game.name,
        "game_round_id": str(game_round.id),
        "start_timestamp": 15
    }
    sio.enter_room(sid, game_id)
    await sio.emit("on_connect_data", send_data, to=sid)
    print("...connected")


@sio.event
async def scanning(sid, data):
    game_round_id = data.get('game_round_id')
    game_round = await Round.get(PydanticObjectId(game_round_id))

    card = data['card']

    if game_round.count_cards == 0:
        game_round.card_of_dragon = card
        game_round.count_cards += 1
        await game_round.save()
        await sio.emit("send_card_of_dragon", {"card": card}, room=game_round.game_id)
    else:
        game_round.card_of_tiger = card
        game_round.count_cards += 1
        await game_round.save()
        await sio.emit("send_card_of_tiger", {"card": card}, room=game_round.game_id)

    game_round.winner = await winner(game_round.card_of_dragon, game_round.card_of_tiger, game_round)
    await game_round.save()
    await sio.emit('winner', {'winner': game_round.winner}, room=game_round.game_id)

    if game_round.finished:
        print(game_round)
        await payout(Stats, game_round_id, game_round)


@sio.event
async def place_bet(sid, data):
    load = int(data.get('load'))
    card_type = data.get('card_type')
    round_id = data.get('game_round_id')

    stats = await get_create_stats(round_id)
    await betting(card_type, stats, load)


@sio.event
async def disconnect(sid):
    print("...disconnected!")
