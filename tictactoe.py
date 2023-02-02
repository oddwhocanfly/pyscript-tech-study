from js import document #type: ignore

def main():
    display([
        'T', 'O', 'E', 
        'T', 'A', 'C', 
        'T', 'I', 'C',
    ])

def display(board):
    assert len(board) == 9, '9 board elements expected'
    display = document.getElementById("display")
    display.innerHTML =\
        board[6] + ' ' + board[7] + ' ' + board[8] + '<br>' +\
        board[3] + ' ' + board[4] + ' ' + board[5] + '<br>' +\
        board[0] + ' ' + board[1] + ' ' + board[2] + '<br>'

if __name__ == '__main__':
    main()