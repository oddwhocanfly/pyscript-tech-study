from js import document #type: ignore

def main():
    display([
        'T', 'O', 'E', 
        'T', 'A', 'C', 
        'T', 'I', 'C', 
    ])

def display(field):
    display = document.getElementById("display")
    display.innerHTML =\
        field[6] + ' ' + field[7] + ' ' + field[8] + '<br>' +\
        field[3] + ' ' + field[4] + ' ' + field[5] + '<br>' +\
        field[0] + ' ' + field[1] + ' ' + field[2] + '<br>'

if __name__ == '__main__':
    main()