import pygame, sys, random

pygame.init()

SW, SH = 1080, 800

BLOCK_SIZE = 20
FONT = pygame.font.Font("assets/fonts/Undertale-Battle-Font.ttf", 25)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        self.score = FONT.render("1", True, "black")
        self.score_rect = self.score.get_rect(center=(20, 20))

        self.snake = Snake()

        self.apple = Apple()

        direction = 'RIGHT'
        change_to = direction

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        change_to = 'RIGHT'
                
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'
        
            if direction == 'UP':
                self.snake.ydir = -1
                self.snake.xdir = 0
            if direction == 'DOWN':
                self.snake.ydir = 1
                self.snake.xdir = 0
            if direction == 'LEFT':
                self.snake.ydir = 0
                self.snake.xdir = -1
            if direction == 'RIGHT':
                self.snake.ydir = 0
                self.snake.xdir = 1

            # if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            #     self.snake.ydir -= 1
            #     self.snake.xdir -= 1
            
            self.update()

    def drawGrid(self, color):
        for x in range(0, SW, BLOCK_SIZE):
            for y in range(0, SH, BLOCK_SIZE):
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, f"{color}", rect, 1)

    def update(self):
        self.snake.update()
            
        screen.fill('white')

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.drawGrid("silver") 

        self.apple.update()

        score = FONT.render(f"Длинна {len(self.snake.body) + 1}", True, "black")

        pygame.draw.rect(screen, "#0AFF89", self.snake.head)

        for square in self.snake.body:
            pygame.draw.rect(screen, "#0AFF89", square)

        screen.blit(score, self.score_rect)

        if self.snake.head.x == self.apple.x and self.snake.head.y == self.apple.y:
            self.snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            self.apple = Apple()

        pygame.display.update()
        clock.tick(13)

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
    
    def update(self):
        global apple
        
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True 
            
            if self.head.x >= SW:
                self.head.x = 0
            elif self.head.x < 0:
                self.head.x += SW

            if self.head.y >= SH:
                self.head.y -= SH
            elif self.head.y < 0:
                self.head.y += SH

        if self.dead:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            self.apple = Apple()
        
        self.body.append(self.head)

        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y

        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE

        self.body.remove(self.head)

class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) * BLOCK_SIZE
        
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def update(self):
        pygame.draw.rect(screen, "red", self.rect)

if __name__ == "__main__":
	game = Game()
	game.update()