from tkinter import *
from tkinter import font
import random
import pygame


#add snake texture
#rankings
#make it look like a real game

class Food:
    #try to implement this in OOP way
    #each time u ate the food, you should delete the food entity and create a new one
    #The new one position should be generated randomly
    #random google it
    def __init__(self,width, height):

        self.x = random.randrange(width)
        self.y = random.randrange(height)
        self.color = "#%03x" % random.randint(0, 0xFFF)


    def render(self, canvas, size):
        #self.position = something random

            x = self.x
            y = self.y

            #print("generate is running")


            canvas.create_rectangle(x * size, y * size, (x + 1) * size, (y + 1) * size, fill=self.color)


class Snake:

    def __init__(self):
        self.body = [[0,15],[1,15]]
        self.direction = "Right"
        self.tail= "none"

        self.col = "#e00b27"

    def turn(self, keysym):
        if keysym == "Right" and self.direction != "Left":

            self.direction = keysym
        if keysym == "Left" and self.direction != "Right":
            self.direction = keysym
        if keysym == "Up" and self.direction != "Down":
            self.direction = keysym
        if keysym == "Down" and self.direction != "Up":
            self.direction = keysym

    def move(self):
        (x,y) = self.body[-1]
        self.tail = self.body[0]
        if self.direction == "Right":
            self.body += [[x+1,y]]
            del self.body[0]
        if self.direction == "Left":
            self.body += [[x-1,y]]
            del self.body[0]
        if self.direction == "Up":
            self.body += [[x,y-1]]
            del self.body[0]
        if self.direction == "Down":
            self.body += [[x,y+1]]
            del self.body[0]

    def grow(self):

        self.body.insert(0, self.tail)

    def render(self, canvas, size):

        for(x,y) in self.body:

            canvas.create_rectangle(x * size, y * size, (x+1)*size, (y+1)*size, fill = self.col)





class SnakeGame:

    class State:
        TITLE = 0
        RUNNING = 1
        GAMEOVER =2
        RANK = 3

    def __init__(self):
        self.frame = Tk()
        self.width = 40
        self.height = 30
        self.size = 20
        self.canvas = Canvas(self.frame, width = self.width * self.size, height = self.height * self.size, bg="#EBF4F7")
        self.frame.bind("<KeyPress>", self.keyboard_event_handler)
        self.frame.bind("<Button-1>", self.mouse_event_handler)
        self.canvas.pack()
        self.score = 0
        #Game entities
        self.food = Food(self.width, self.height)
        self.snake = Snake()
        #Game status
        self.state = 0
        #Game effects
        pygame.mixer.init()
        self.sound_eat = pygame.mixer.Sound("eat.wav")
        self.sound_over = pygame.mixer.Sound("over.wav")
        self.sound_click = pygame.mixer.Sound("Click.wav")

    def mouse_event_handler(self, event):
        if self.state == self.State.TITLE:
            if (event.x in range(300,551)) and (event.y in range(200,301)):
                self.sound_click.play()
                self.state = 1
            if (event.x in range(300, 551) and (event.y in range(300,401))):
                self.sound_click.play()
                self.state = 3
            if (event.x in range(300,551)) and (event.y in range(400,501)):
                self.sound_click.play()
                quit(0)


        if self.state == self.State.GAMEOVER:
            if (event.x in range(300,501))and (event.y in range(470,531)):
                self.sound_click.play()
                self.snake = Snake()
                self.food = Food(self.width, self.height)
                self.state = 0
        if self.state == self.State.RANK:
            if (event.x in range(10, 91)) and (event.y in range(10, 51)):
                self.sound_click.play()
                self.snake = Snake()
                self.food = Food(self.width, self.height)
                self.state = 0



    def keyboard_event_handler(self, event):
        if self.state == self.State.RUNNING:
            if event.keysym in ["Up", "Down", "Left","Right"]:
                self.snake.turn(event.keysym)
            elif event.keysym == "g" or event.keysym == "G":
                self.snake.grow()
            else:
                print("Invalid input")
        if self.state == self.State.GAMEOVER:
            if event.keysym == "Return":
                self.score = 0
                self.snake = Snake()
                self.food= Food(self.width, self.height)
                self.state = self.State.RUNNING

    #Main loop and data graphic layer
    def gameLoop(self):
            self.update() #data layer
            self.render()  # graphic layer
            self.frame.after(100, self.gameLoop)

    def update(self):
        #print("update is running")
        if self.state == self.State.RUNNING:
            self.snake.move()
            if self.snake.body[-1][0] == self.food.x and self.snake.body[-1][1] == self.food.y: #eat a food
                self.sound_eat.play()
                self.score+=1
                self.snake.grow()
                del self.food
                self.food = Food(self.width, self.height)
            if self.isOver(self.snake.body):
                self.sound_over.play()
                del self.food
                del self.snake

                self.state = self.State.GAMEOVER


    def render(self):


        if self.state == self.State.TITLE:
            self.canvas.delete(ALL)
            self.score = 0
            self.canvas.create_text(400, 100, text="Pai Qu's Snake Game", fill="#e00b27", font=font.Font(size=50))
            #start game
            self.canvas.create_rectangle(300, 200, 550, 300, fill="#e00b27")
            self.canvas.create_text(425, 240, text="Start Game", fill="#f2f2f2", font=font.Font(size=50))
            #rank list
            self.canvas.create_rectangle(300, 300, 550, 400, fill="#e00b27")
            self.canvas.create_text(425, 340, text="Rankings", fill="#f2f2f2", font=font.Font(size=50))
            #quit game
            self.canvas.create_rectangle(300, 400, 550, 500, fill="#e00b27")
            self.canvas.create_text(425, 450, text="Quit Game", fill="#f2f2f2", font=font.Font(size=50))
        if self.state == self.State.RUNNING:
            self.canvas.delete(ALL)

            self.canvas.create_text(700,50, text = "Score = " + str(self.score),fill="#e00b27", font=font.Font(size=24))
            self.snake.render(self.canvas, self.size)
            self.food.render(self.canvas, self.size)

        if self.state == self.State.GAMEOVER:
            self.canvas.delete(ALL)
            self.canvas.create_text(400, 200, text = "Your score is " + str(self.score), fill="#e00b27", font=font.Font(size=24))
            self.canvas.create_text(400, 300, text = "GAMEOVER",fill="#e00b27", font=font.Font(size=36))
            self.canvas.create_text(400, 350, text = "Press Return to Restart the Game", fill="#e00b27", font=font.Font(size=24))
            self.canvas.create_text(200, 400, text = "What's your name?", fill ="#e00b27", font=font.Font(size=24))
            self.canvas.create_rectangle(300,470,500,530,fill = "#e00b27")
            self.canvas.create_text(400, 500, text="Back to title", fill="#EBF4F7", font=font.Font(size=24))

        if self.state == self.State.RANK:
            self.canvas.delete(ALL)
            self.canvas.create_rectangle(10, 10, 90, 50, fill="#e00b27")
            self.canvas.create_text(50, 30, text="Back", fill="#EBF4F7", font=font.Font(size=24))

    # for checking game status
    def isOver(self, body):

        if body[-1][0] > self.width:
            print("true")
            return True

        if body[-1][1] > self.height:
            print("true")
            return True
        if body[-1][0] < 0:
            return True
        if body[-1][1] < 0:
            return True

        if body[-1] in body[:-1]:

            return True




g = SnakeGame()

g.gameLoop()

g.frame.mainloop()
