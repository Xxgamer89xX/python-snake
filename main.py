import curses
import time
import random

columnas = 20
filas = 10
snake = [[4, 4], [4, 3], [4, 2]]  # Posición: [fila, columna]
direccion = 3   # Por defecto hacia la derecha



def beep():
    pass

def refresh(tablero, stdscr):
    stdscr.clear()
    for y, fila in enumerate(tablero):
        for x, celda in enumerate(fila):
            stdscr.addstr(y, x * 2, celda)
    stdscr.refresh()

def move():
    global direccion, snake
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = snake[i - 1].copy()
    if direccion == 0:
        snake[0][0] -= 1
    elif direccion == 1:
        snake[0][1] -= 1
    elif direccion == 2:
        snake[0][0] += 1
    elif direccion == 3:
        snake[0][1] += 1

def new_apple(tablero, cabeza):
    global apple
    y = random.randint(0, 19)
    x = random.randint(0, 9)
    if tablero[x][y] != "o" and tablero[x][y] != cabeza:
        apple = [x, y]

def grow(last_move):
    snake.insert(1, snake[0].copy())
    if time.time() - last_move >= 0.25:
        if direccion == 0:
            snake[0][0] -= 1
        elif direccion == 1:
            snake[0][1] -= 1
        elif direccion == 2:
            snake[0][0] += 1
        elif direccion == 3:
            snake[0][1] += 1

def lose(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    mensaje = [
        " __     ______  _    _   _      ____   _____ ______ ",
        " \\ \\   / / __ \\| |  | | | |    / __ \\ / ____|  ____|",
        "  \\ \\_/ / |  | | |  | | | |   | |  | | (___ | |__   ",
        "   \\   /| |  | | |  | | | |   | |  | |\\___ \\|  __|  ",
        "    | | | |__| | |__| | | |___| |__| |____) | |____ ",
        "    |_|  \\____/ \\____/  |______\\____/|_____/|______|",
        "                                                   ",
        "           Has perdido...                          ",
        "     Pulsa 'r' para reiniciar o 'q' para salir     "
    ]
    for i, linea in enumerate(mensaje):
        stdscr.addstr(i + 2, 2, linea)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            return "salir"
        elif key == ord('r'):
            return "reiniciar"

def main(stdscr):
    global direccion, snake, apple

    # Reiniciar snake y dirección cada vez que se entra a main
    snake[:] = [[4, 4], [4, 3], [4, 2]]
    direccion = 3

    apple = [9, 9]
    tablero = [["." for _ in range(columnas)] for _ in range(filas)]
    cabeza = ">"
    stdscr.timeout(250)
    last_move = time.time()
    aceptable_input = True
    curses.curs_set(0)

    while True:
        tablero = [["." for _ in range(columnas)] for _ in range(filas)]

        y2, x2 = snake[0]
        for i in range(1, len(snake)):
            y, x = snake[i]
            tablero[y][x] = "o"

        if snake[0] == apple:
            beep()
            new_apple(tablero, cabeza)
            grow(last_move)

        tablero[y2][x2] = cabeza
        tablero[apple[0]][apple[1]] = "X"
        refresh(tablero, stdscr)

        key = stdscr.getch()
        if key == ord('q'):
            break
        if aceptable_input:
            if key == ord('w') and direccion != 2:
                direccion = 0
                cabeza = "˄"
            elif key == ord('a') and direccion != 3:
                direccion = 1
                cabeza = "<"
            elif key == ord('s') and direccion != 0:
                direccion = 2
                cabeza = "v"
            elif key == ord('d') and direccion != 1:
                direccion = 3
                cabeza = ">"
            aceptable_input = False

        if time.time() - last_move >= 0.25:
            move()
            if snake[0] in snake[2:] or snake[0][0] > 9 or snake[0][1] > 19 or snake[0][0] < 0 or snake[0][1] < 0:
                resultado = lose(stdscr)
                if resultado == "salir":
                    break
                else:
                    snake1()  # Reinicio
                    return
            last_move = time.time()
            aceptable_input = True

def snake1():
    curses.wrapper(main)

snake1()

