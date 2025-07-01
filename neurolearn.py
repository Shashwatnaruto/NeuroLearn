
import random
import pygame
class Snake:
    def __init__(self):
        self.body= [(100, 100), (90,100), (80,100)]
        self.direction= "RIGHT"
        self.color(0, 0, 255)
    def move(self):
        head_x, head_y= self.body[0]
        if self.direction== "UP":
            head_y-= 10
        elif self.direction== "DOWN":
            head_y+= 10
        elif self.direction()== "RIGHT":
            head_x+=10
        elif self.direction=="LEFT":
            head_y-=10
        head_x= head_x % 800
        head_y= head_y % 600
        new_head= (head_x, head_y)
        self.body= [new_head] + self.body[:-1]
    def grow(self):
        self.body.append(self.body[-1])  
    def draw(self, screen):
        for block in self.body:
            pygame.draw.rect(screen, self.color, pygame.Rect(block[0, block[1], 10, 10]))
class Apple():
    def __init__(self):
        self.size= 10
        self.color= (255, 0, 0)
        self.position= self.spawn()
    def spawn(self):
        x= random.randint(0, 79)* self.size
        y= random.randint(0, 59) * self.size
        return (x,y)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.size, self.size))
    def Main():
        pygame.init()
        screen= pygame.display.set_mode((800, 600))
        clock= pygame.time.Clock()
        snake= Snake()
        apple= Apple()
        running= True
        while running:
            screen.fill(0, 255, 0)
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    running= False
                elif event.type== pygame.KEYDOWN:
                   if event.key== 'K_UP' and snake.direction != "DOWN":
                       snake.direction= "UP"
                   elif event.key== 'K_DOWN'and snake.direction != "UP":
                       snake.direction= "DOWN"
                   elif event.key== "K-LEFT" and snake.direction != "RIGHT":
                       snake.direction= "LEFT"
                   elif event.key== "K_RIGHT" and snake.direction != "LEFT":
                       snake.direction= "RIGHT"
                       snake.move()
                       if snake.body[0]== apple.position:
                           snake.grow()
                           apple= Apple()
                apple.draw(screen)
                snake.draw(screen)
                pygame.display.update()
                clock.tick(10)
                pygame.quit()
                if __name__== "__Main__":
                        print("snake game started")
                        main()
                        