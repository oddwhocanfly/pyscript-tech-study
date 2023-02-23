import js # type: ignore
import pyodide # type: ignore
from asyncio import sleep, ensure_future
from random import randint, choice

async def main():
    init()
    try: await game()
    except Exception as e: 
        panic(str(e))

async def game():
    while True:
        draw([
            'T', 'I', 'C',
            'T', 'A', 'C', 
            'T', 'O', 'E', 
        ])
        player_letter, computer_letter = await input_player_letter()
        turn = who_goes_first()
        show('The ' + turn + ' will go first.')
        await sleep(2)
        # draw([
        #     'q', 'w', 'e',
        #     'a', 's', 'd', 
        #     'z', 'x', 'c', 
        # ])
        board = [
            ' ', ' ', ' ',
            ' ', ' ', ' ', 
            ' ', ' ', ' ', 
        ]
        game_is_playing = True
        while game_is_playing:
            if turn == 'player':
                draw(board)
                move = await get_player_move(board, player_letter)
                make_move(board, player_letter, move)

                if is_winner(board, player_letter):
                    draw(board)
                    show('Hooray! You\'ve won the game!')
                    await sleep(4)
                    game_is_playing = False
                else:
                    if is_board_full(board):
                        draw(board)
                        show('The game is a tie!')
                        await sleep(4)
                        break
                    else:
                        turn = 'computer'
            else:
                move = get_computer_move(board, computer_letter)
                make_move(board, computer_letter, move)

                if is_winner(board, computer_letter):
                    draw(board)
                    show('The computer has beaten you! You lose.')
                    await sleep(4)
                    game_is_playing = False
                else:
                    if is_board_full(board):
                        draw(board)
                        show('The game is a tie!')
                        await sleep(4)
                        break
                    else:
                        turn = 'player'
        if not await play_again():
            break

def make_move(board, letter, position):
    board[position] = letter

def get_computer_move(board, computer_letter):
    if computer_letter == 'X':
        player_letter = 'O'
    else:
        player_letter = 'X'
    
    # Check if Computer can win in the next move.
    for i in range(0, 9):
        copy = board.copy()
        if is_position_free(copy, i):
            make_move(copy, computer_letter, i)
            if is_winner(copy, computer_letter):
                return i
    
    # Check  if PLayer could win on their next move, and block them.
    for i in range(0, 9):
        copy = board.copy()
        if is_position_free(copy, i):
            make_move(copy, player_letter, i)
            if is_winner(copy, player_letter):
                return i
    
    # Try to take one of the corners, if they are free.
    move = choose_random_move_from_list(board, [0, 2, 6, 8])
    if move != None:
        return move
    
    # Try to take the center, if it is free.
    if is_position_free(board, 4):
        return 4
    
    # Move on one of the sides.
    return choose_random_move_from_list(board, [1, 3, 5, 7])        

def choose_random_move_from_list(board, moves_list):
    possible_moves = []
    for i in moves_list:
        if is_position_free(board, i):
            possible_moves.append(i)

    if len(possible_moves) != 0:
        return choice(possible_moves)
    else:
        return None

def is_winner(board, letter):
    b = board
    l = letter
    return ((b[0] == l and b[1] == l and b[2] == l) or # across the top
        (b[3] == l and b[4] == l and b[5] == l) or # across the middle
        (b[6] == l and b[7] == l and b[8] == l) or # across the bottom
        (b[0] == l and b[3] == l and b[6] == l) or # down the left side
        (b[1] == l and b[4] == l and b[7] == l) or # down the middle
        (b[2] == l and b[5] == l and b[8] == l) or # down the right side
        (b[0] == l and b[4] == l and b[8] == l) or # diagonal
        (b[2] == l and b[4] == l and b[6] == l)) # diagonal

def is_board_full(board):
    return not ' ' in board

async def play_again():
    show('Do you want to play again? (yes or no)')
    choice = await get_key()
    return choice == 'KeyY'

async def input_player_letter():
    letter = ''
    show('Welcome to Tic Tac Toe!\n' +
         'Do you want to be X or O?')
    while not (letter == 'KeyX' or letter == 'KeyO'):
        letter = await get_key()

    if letter == 'KeyX':
        return ['X', 'O']
    else:
        return ['O', 'X']

def who_goes_first():
    if randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

async def get_player_move(board, player_letter):
    move = ' '
    positions = [
        'KeyQ', 'KeyW', 'KeyE',
        'KeyA', 'KeyS', 'KeyD', 
        'KeyZ', 'KeyX', 'KeyC',
    ]
    while move not in positions or \
        not is_position_free(board, positions.index(move)):
        show('You play as ' + player_letter + '\n'
            'What is your next move?')
        move = await get_key()
    return positions.index(move)

def is_position_free(board, position):
    return board[position] == ' '

def draw(board):
    assert len(board) == 9, '9 board elements expected'
    html_board = js.document\
        .getElementById('board')\
        .getElementsByTagName('*')
    for i in range(0, 9):
        html_board[i].innerText = board[i]

def show(message):
    status = js.document.getElementById('status')
    status.innerText = message

def init():
    on_key_down_proxy = pyodide.ffi.create_proxy(on_key_down)
    js.document.addEventListener('keydown', on_key_down_proxy)

def panic(message): show('Error: ' + message)

async def get_key():
    global get_key_key
    get_key_key = None
    while get_key_key == None:
        await sleep(0)
    return get_key_key

def on_key_down(event):
    global get_key_key
    get_key_key = event.code

if __name__ == '__main__':
    ensure_future(main())