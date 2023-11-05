from js import document  # type: ignore
from pyodide import ffi  # type: ignore
from asyncio import sleep, ensure_future
from random import choice, shuffle

last_clicked_element = None

async def main():
    on_click_proxy = ffi.create_proxy(on_click)
    document.addEventListener('click', on_click_proxy)

    field = [
        'T', 'I', 'C',
        'T', 'A', 'C',
        'T', 'O', 'E',
    ]
    render(field, 0, 'Click anywhere to start')
    await next_clicked_element()

    while True:
        field = [
            ' ', ' ', ' ',
            ' ', ' ', ' ',
            ' ', ' ', ' ',
        ]
        pieces = ['X', 'O']
        shuffle(pieces)
        player_piece, bot_piece = pieces
        next_turn = choice(pieces)
        num_turns = 0

        while True:
            if next_turn == player_piece:
                render(field, 0, f'Player turn ({player_piece})')
                place = await next_player_move(field)
                field[place] = player_piece

                line = line_of_three(field, player_piece)
                if line is not None:
                    render(field, line, 'Player wins, click to restart')
                    await next_clicked_element()
                    break
                else:
                    if is_full_field(field):
                        render(field, 0, 'Tie, click to restart')
                        await next_clicked_element()
                        break
                    else:
                        next_turn = bot_piece
            else:
                if num_turns > 0:
                    render(field, 0, f'PyScript turn ({bot_piece})')
                await sleep(0.7)
                place = choose_best_move(field, bot_piece, player_piece)
                field[place] = bot_piece

                line = line_of_three(field, bot_piece)
                if line is not None:
                    render(field, line, 'PyScript wins, click to restart')
                    await next_clicked_element()
                    break
                else:
                    if is_full_field(field):
                        render(field, 0, 'Tie, click to restart')
                        await next_clicked_element()
                        break
                    else:
                        next_turn = player_piece

            num_turns += 1

async def next_player_move(field):
    place = None
    while place is None or not is_free_place(field, place):
        element = await next_clicked_element()
        place = getattr(element, '__place_idx', None)
    return place

def choose_best_move(field, own_piece, opponent_piece):
    # Try make winning move
    for i in range(0, 9):
        temp_field = field.copy()
        if is_free_place(temp_field, i):
            temp_field[i] = own_piece
            if line_of_three(temp_field, own_piece) is not None:
                return i

    # Block player's winning move
    for i in range(0, 9):
        temp_field = field.copy()
        if is_free_place(temp_field, i):
            temp_field[i] = opponent_piece
            if line_of_three(temp_field, opponent_piece) is not None:
                return i

    # Try to take one of the corners
    move = choose_valid_move(field, [0, 2, 6, 8])
    if move is not None:
        return move

    # Try to take the center
    if is_free_place(field, 4):
        return 4

    # Move on one of the sides
    return choose_valid_move(field, [1, 3, 5, 7])

def choose_valid_move(field, moves):
    valid_moves = []
    for move in moves:
        if is_free_place(field, move):
            valid_moves.append(move)
    if len(valid_moves) != 0:
        return choice(valid_moves)
    else:
        return None

def line_of_three(field, piece):
    if   field[0] == piece and field[1] == piece and field[2] == piece: return 1  # noqa
    elif field[3] == piece and field[4] == piece and field[5] == piece: return 2  # noqa
    elif field[6] == piece and field[7] == piece and field[8] == piece: return 3  # noqa
    elif field[0] == piece and field[3] == piece and field[6] == piece: return 4  # noqa
    elif field[1] == piece and field[4] == piece and field[7] == piece: return 5  # noqa
    elif field[2] == piece and field[5] == piece and field[8] == piece: return 6  # noqa
    elif field[0] == piece and field[4] == piece and field[8] == piece: return 7  # noqa
    elif field[2] == piece and field[4] == piece and field[6] == piece: return 8  # noqa
    return None

def is_free_place(field, place):
    return field[place] == ' '

def is_full_field(field):
    return ' ' not in field

def render(field, strike_line, message):
    field_elem = document.createElement('div')
    field_elem.classList.add('field')
    if strike_line is not None:
        field_elem.classList.add(f'strike-{strike_line}')
    for i in range(0, 9):
        place = document.createElement('div')
        place.classList.add('place')
        place.innerText = field[i]
        setattr(place, '__place_idx', i)
        field_elem.appendChild(place)

    message_elem = document.createElement('div')
    message_elem.classList.add('message')
    message_elem.innerText = message

    game_elem = document.getElementById('tictactoe')
    game_elem.replaceChildren(field_elem, message_elem)

async def next_clicked_element():
    global last_clicked_element
    last_clicked_element = None
    while last_clicked_element is None:
        await sleep(0)
    return last_clicked_element

def on_click(event):
    global last_clicked_element
    last_clicked_element = event.srcElement

if __name__ == '__main__':
    ensure_future(main())

