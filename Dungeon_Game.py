from random import randint, choice
import subprocess
import platform
import time
import hashlib


class MapGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.dragon = []
        self.treasure = []
        self.start = (0, 0)
        self.goal = (width-1, height-1)
        self.player = (0, 0)

    def move_player(self, d):
        x = self.player[0]
        y = self.player[1]
        pos = None

        if d[0] == 'd':
            pos = (x + 1, y)
        if d[0] == 'a':
            pos = (x - 1, y)
        if d[0] == 'w':
            pos = (x, y - 1)
        if d[0] == 's':
            pos = (x, y + 1)

        if pos not in self.walls:
            self.player = pos     

        if pos == self.goal:
            print("You made it to the end!")
        
        return pos



def draw_grid(g, width=2):
    for y in range(g.height):
        for x in range(g.width):
            if (x, y) in g.walls:
                symbol = '#'
            elif (x, y) in g.dragon:
                symbol = '@'  
            elif (x, y) in g.treasure:
                symbol = '*'      
            elif (x, y) == g.player:
                symbol = '$'
            elif (x, y) == g.start:
                symbol = '<'
            elif (x, y) == g.goal:
                symbol = '>'
            else:
                symbol = '.'
            print("%%-%ds" % width % symbol, end="")
        print()


def get_walls(g: MapGrid) -> list:
        out = []
        for i in range(4,10):
            for j in range(6):
                if i == 4 or i == 9 or j == 0 or j == 5:
                    if j !=3:
                        out.append((i, j))

        for i in range(6,12):
            for j in range(12,18):
                if i == 6 or i == 11 or j == 12 or j == 17:
                    if j !=15:
                        out.append((i, j))                
        return out

def get_dragon(g: MapGrid) -> list:
        out = []
        out.append((7, 2))
        out.append((8, 4)) 
        out.append((9, 15))
        out.append((8, 13))         
        return out

def get_treasure(g: MapGrid) -> list:
        out = []
        out.append((7, 3))
        out.append((9, 16))
        return out


def clear():
    subprocess.Popen("cls" if platform.system() == "Windows" else "clear", shell=True)
    time.sleep(.01)


def main():
    g = MapGrid(20, 20)
    g.walls = get_walls(g)
    g.dragon = get_dragon(g.walls)
    g.treasure = get_treasure(g.dragon)


    while g.player != g.goal:
        draw_grid(g)
        d = input("Which way? (d, a, w, s)")
        g.move_player(d)
        clear()
    print("You made it!")@app.on_event('shutdown')
    async def on_shutdown():
        pass


if __name__ == '__main__':
    # users
    user_list = ["Ibrahiim43", "Fahad", "yourgenericchan" ]

    # a dict of customers with passwords
    authentication = {"Ibrahiim43": hashlib.sha256("IamIbrahiim43".encode()).hexdigest(), 
                    "Fahad": hashlib.sha256("IamFahad123".encode()).hexdigest(),
                    "yourgenericchan": hashlib.sha256("Iamyourgenericchan32".encode()).hexdigest()}

    # User_Authentication
    username = input("Enter a username:\n")
    password = input("Enter password:\n")

    if username in user_list:
        if hashlib.sha256(password.encode()).hexdigest() == authentication[username]:
            main()
        else:
            print("\nInvalid Password\n")
    else:
        print("\nInvalid Username\n")