import turtle
import random
import time
from functools import partial


# set up global variables
g_snake = None
g_monster = None
g_snake_sz = 5
g_intro = None
g_keypressed = None
g_motion = None
g_time = None
g_contact = None
g_game = None
g_key = []
g_food = []
scr = turtle.Screen()


COLOR_HEAD = "red"
COLOR_BODY = ("blue", "black")
COLOR_MONSTER = "purple"

SnacksPosition = []
FOOD = []
Food = []
TIME = 0
contact = 0
KEY_UP = "Up"
KEY_DOWN = "Down"
KEY_LEFT = "Left"
KEY_RIGHT = "Right"
KEY_SPACE = "space"
# the dircetion of snake movement
HEADING_BY_KEY = {KEY_UP: 90, KEY_DOWN: 270, KEY_LEFT: 180, KEY_RIGHT: 0}


# create a turtle at the given position
def Createturtle(x, y, color="red", border="black"):
    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x, y)
    return t


# create the game area, show the time, contact and motion
def CreateGamearea():
    scr.bgcolor('white')
    scr.title('Snake')
    scr.setup(560, 620)  # Set the game area size to 560x560
    m = Createturtle(-250, -250, "", "black")  # Set the start position of the game area
    m.shapesize(25, 25, 5)
    m.goto(0, -40)
    s = Createturtle(-250, -250, "", "black")  # Set the start position of the game area
    s.shapesize(4, 25, 5)
    s.goto(0, 250)

    intro = Createturtle(-200, 150)
    intro.hideturtle()
    intro.write("Click anywhere to start the game .....", font=("Arial", 16, "normal"))

    time = Createturtle(0, 0, "", "black")
    time.hideturtle()
    time.goto(-100, s.ycor()-10)
    time.write("Time:"+str(TIME), font=("Arial", 16, "normal"))

    contract = Createturtle(0, 0, "", "black")
    contract.hideturtle()
    contract.goto(-240, s.ycor()-10)
    contract.write("Contact:"+str(contact), font=("Arial", 16, "normal"))

    motion = Createturtle(0, 0, "", "black")
    motion.hideturtle()
    motion.goto(30, s.ycor()-10)
    motion.write("Motion:", font=("Arial", 16, "normal"))
    scr.update()

    return intro, contract, time, motion


# create the food
def CreateFood():
    global g_food
    # global FOOD
    for i in range(5):
        x = Createturtle(0, 0)
        x.hideturtle()
        g_food.append([x, str(i+1)])
    for food in g_food:
        FOOD.append(food[1])


# create the food, repalce the food that has not been eaten every 5 seconds
def OnTimerFood():
    global g_food
    global Food
    Food.clear()
    if g_food == []:
        scr.ontimer(OnTimerFood, 5000)
        return
    if g_game == False:
        return
    for food in g_food:
        food[0].clear()

    if len(g_food) == 0:
        scr.ontimer(OnTimerFood, 5000)
        return

    n = random.randint(1, len(g_food))
    random.shuffle(g_food)
    while n > 0:
        xdir = list(range(-240, 260, 20))
        ydir = list(range(-280, 220, 20))
        x = random.choice(xdir)
        y = random.choice(ydir)-10
        g_food[n-1][0].goto(x, y)
        g_food[n-1][0].write(str(g_food[n-1][1]), font=("Arial", 16, "normal"))
        Food.append(g_food[n-1])
        n -= 1

    scr.ontimer(OnTimerFood, 5000)
    scr.update()


# record time
def OnTimertime():
    global TIME
    TIME += 1
    g_time.clear()
    g_time.write("Time: "+str(TIME), font=("Arial", 16, "bold"))
    if g_game == False:
        return
    scr.update()
    scr.ontimer(OnTimertime, 1000)

# Create four monsters with random initial positions

# Control the movement of the monster
def OnTimerMonster():
    global contact
    if g_game == False:
        return
    for g_monster in g_monsters:
        g_monster.showturtle()
        
        if g_monster.xcor() < -220 and g_monster.heading() == 180:
            g_monster.setheading(0)
        elif g_monster.ycor() < -260 and g_monster.heading() == 270:
            g_monster.setheading(90)
        elif g_monster.xcor() > 220 and g_monster.heading() == 0:
            g_monster.setheading(180)
        elif g_monster.ycor() > 180 and g_monster.heading() == 90:
            g_monster.setheading(270)
        else:
            dir = []
            if g_monster.xcor() < g_snake.xcor():
                dir.append(0)        
            if g_monster.ycor() < g_snake.ycor():
                dir.append(90)
            if g_monster.xcor() > g_snake.xcor():
                dir.append(180)
            if g_monster.ycor() > g_snake.ycor():
                dir.append(270)

            random.shuffle(dir)
            g_monster.setheading(dir[0])
        g_monster.forward(20)

        for position in SnacksPosition:
            if g_monster.distance(position) <= 20:
                contact += 1
                g_contact.clear()
                g_contact.write("Contact: "+str(contact),
                                font=("Arial", 16, "bold"))
                break

    scr.update()
    scr.ontimer(OnTimerMonster, 1000)



# update the motion after the key is pressed
def UpdateMotion():
    g_motion.clear()
    g_motion.write('Motion:'+str(g_keypressed), font=('arial', 15, 'bold'))
    scr.update()


# if press the space key, the snack will stop
def OnArrowKeyPressed(key):
    global g_keypressed
    global g_key
    if key == 'space':
        if g_key[-1] != 'Pause':
            g_keypressed = 'Pause'
        else:
            g_keypressed = g_key[-2]
    else:
        g_keypressed = key
    g_key.append(g_keypressed)

    SetSnakeHeading(key)
    UpdateMotion()


# set the snack heading
def SetSnakeHeading(key):
    if key in HEADING_BY_KEY.keys():
        g_snake.setheading(HEADING_BY_KEY[key])



# create a function that monitor if the snack eaten the food and displace it
def EatFood():
    global g_snake_sz
    global FOOD
    global g_food
    global Food
    if g_food == []:
        scr.ontimer(EatFood, 100)
        return
    for food in Food:
        if int(g_snake.ycor()+0.5) == int(food[0].ycor()+10.5) and int(g_snake.xcor()+0.5) == int(food[0].xcor()+0.5) :
            g_snake_sz += int(food[1])
            food[0].clear()
            Food.remove(food)
            FOOD.remove(food[1])
            g_food.remove(food)
            break
    scr.update()


# the motion of the snack depends on the key preesed
def OnTimerSnake():
    global SnacksPosition
    if g_keypressed == 'Pause':
        scr.ontimer(OnTimerSnake, 200)
        return
    elif g_keypressed == None:
        scr.ontimer(OnTimerSnake, 200)
        return
    elif g_game == False:
        return

    EatFood()

    # move the snake
    for position in SnacksPosition[0:-1:1]:
        if (int(g_snake.xcor()+20.5) == int(position[0]+0.5) and int(g_snake.ycor()+0.5) == int(position[1]+0.5) and g_snake.heading() == 0) \
                or (int(g_snake.xcor()-20+0.5) == int(position[0]+0.5) and int(g_snake.ycor()+0.5) == int(position[1]+0.5) and g_snake.heading() == 180) \
                or (int(g_snake.xcor()+0.5) == int(position[0]+0.5) and int(g_snake.ycor()+20.5) == int(position[1]+0.5) and g_snake.heading() == 90) \
                or (int(g_snake.xcor()+0.5) == int(position[0]+0.5) and int(g_snake.ycor()-20+0.5) == int(position[1]+0.5) and g_snake.heading() == 270):
            scr.ontimer(OnTimerSnake, 200)
            return

    if (int(g_snake.xcor()+0.5) < -220 and g_snake.heading() == 180) \
            or (int(g_snake.xcor()+0.5) > 220 and g_snake.heading() == 0) \
            or (int(g_snake.ycor()+0.5) > 180 and g_snake.heading() == 90) \
            or (int(g_snake.ycor()+0.5) < -260 and g_snake.heading() == 270):
        scr.ontimer(OnTimerSnake, 200)
        return

    else:
        # Clone the head as body
        g_snake.color(*COLOR_BODY)
        g_snake.stamp()
        g_snake.color(COLOR_HEAD)
        g_snake.forward(20)
        SnacksPosition.append(g_snake.pos())
    # Shifting or extending the tail.
    # Remove the last square on Shifting.
    if len(g_snake.stampItems) > g_snake_sz:
        g_snake.clearstamps(1)
        del SnacksPosition[0]
    # Check if snake is eating itself

    scr.update()

    scr.ontimer(OnTimerSnake, 200)


# start the game
def StartGame(x, y):
    scr.onscreenclick(None)
    g_intro.clear()

    scr.onkey(partial(OnArrowKeyPressed, KEY_UP), KEY_UP)
    scr.onkey(partial(OnArrowKeyPressed, KEY_DOWN), KEY_DOWN)
    scr.onkey(partial(OnArrowKeyPressed, KEY_LEFT), KEY_LEFT)
    scr.onkey(partial(OnArrowKeyPressed, KEY_RIGHT), KEY_RIGHT)
    scr.onkey(partial(OnArrowKeyPressed, KEY_SPACE), KEY_SPACE)

    scr.ontimer(OnTimerSnake, 10)
    scr.ontimer(OnTimerFood, 100)
    scr.ontimer(OnTimerMonster, 1000)
    scr.ontimer(OnTimertime, 1000)


# check if the game is win or lost
def GameOverOrWin():
    for g_monster in g_monsters:
        if g_snake.distance(g_monster) < 20:
            g_snake.write("Game Over !!", font=("Arial", 30, "normal"))
            scr.update()
            return False
        elif g_snake_sz == 20 and len(g_snake.stampItems) == 20:
            g_snake.write("Winner !!", font=("Arial", 30, "normal"))
            scr.update()
            return False


def OnTimerGame():
    global g_game
    g_game = GameOverOrWin()
    if g_game == False:
        return
    scr.update()
    scr.ontimer(OnTimerGame, 10)


# main part
if __name__ == '__main__':
    scr.cv._rootwindow.resizable(False, False)
    scr.tracer(0)
    scr.title("Snake Game")
    scr.bgcolor("black")
    scr.tracer(0)
    CreateFood()
    g_intro, g_contact, g_time, g_motion = CreateGamearea()
    UpdateMotion()
    g_monsters = [Createturtle(random.randint(-11, 11) * 20, random.randint(-11, 11) * 20, "purple", "black") for _ in range(4)]
    g_snake = Createturtle(0, 0, "red", "black")
    scr.onscreenclick(StartGame)
    scr.ontimer(OnTimerGame, 100)
    scr.update()
    scr.listen()
    turtle.mainloop()
