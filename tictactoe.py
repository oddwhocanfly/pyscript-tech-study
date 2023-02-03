import js #type: ignore
import pyodide #type: ignore
import asyncio

async def main():
    init()
    draw([
        'T', 'O', 'E', 
        'T', 'A', 'C', 
        'T', 'I', 'C',
    ])
    while True:
        key = await get_key()
        print(key)

def init():
    on_key_down_proxy = pyodide.ffi.create_proxy(on_key_down)
    js.document.addEventListener('keydown', on_key_down_proxy)

def draw(board):
    assert len(board) == 9, '9 board elements expected'
    display = js.document.getElementById('display')
    display.innerHTML =\
        board[6] + ' ' + board[7] + ' ' + board[8] + '<br>' +\
        board[3] + ' ' + board[4] + ' ' + board[5] + '<br>' +\
        board[0] + ' ' + board[1] + ' ' + board[2] + '<br>'

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