import js #type: ignore
import pyodide #type: ignore
import asyncio
from random import randint

async def main():
    init()
    while True:
        draw([
            'T', 'I', 'C',
            'T', 'A', 'C', 
            'T', 'O', 'E', 
        ])
        player_letter, computer_letter = await input_player_letter()
        turn = who_goes_first()
        print('The ' + turn + ' will go first.')
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
                move = await get_player_move(board)
                make_move(board, player_letter, move)

                if is_winner(board, player_letter):
                    draw(board)
                    print('Hooray! You\'ve won the game!')
                    game_is_playing = False
                else:
                    if is_board_full(board):
                        draw(board)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'computer'
            else:
                move = get_computer_move(board, computer_letter)
                make_move(board, computer_letter, move)

                if is_winner(board, computer_letter):
                    draw(board)
                    print('The computer has beaten you! You lose.')
                    game_is_playing = False
                else:
                    if is_board_full(board):
                        draw(board)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'player'
        if not await play_again():
            break

def make_move(board, letter, position):
    board[position] = letter

def get_computer_move(board, computer_letter):
    return board.index(' ')

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
    print('Do you want to play again? (yes or no)')
    choice = await get_key()
    return choice == 'KeyY'

async def input_player_letter():
    letter = ''
    print('Do you want to be X or O?')
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

async def get_player_move(board):
    move = ' '
    positions = [
        'KeyQ', 'KeyW', 'KeyE',
        'KeyA', 'KeyS', 'KeyD', 
        'KeyZ', 'KeyX', 'KeyC',
    ]
    while move not in positions or \
        not is_position_free(board, positions.index(move)):
        print('What is your next move?')
        move = await get_key()
    return positions.index(move)

def is_position_free(board, position):
    return board[position] == ' '

def init():
    on_key_down_proxy = pyodide.ffi.create_proxy(on_key_down)
    js.document.addEventListener('keydown', on_key_down_proxy)

def draw(board):
    assert len(board) == 9, '9 board elements expected'
    display = js.document.getElementById('display')
    display.innerHTML =\
        board[0] + ' ' + board[1] + ' ' + board[2] + '<br>' +\
        board[3] + ' ' + board[4] + ' ' + board[5] + '<br>' +\
        board[6] + ' ' + board[7] + ' ' + board[8] + '<br>'

async def get_key():
    global get_key_key
    get_key_key = None
    while get_key_key == None:
        await asyncio.sleep(0)
    return get_key_key

def on_key_down(event):
    global get_key_key
    get_key_key = event.code

if __name__ == '__main__':
    asyncio.ensure_future(main())