import pygame

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x,y, 0) for x in range(width)] for y in range(height)]
        self.generation = 0
    
    def set_cell_alive(self, x, y):
        self.grid[x][y].state = 1
    def evolve_cell_alive(self, x, y):
        self.grid[x][y].next_state = 1
    def evolve_cell_dead(self, x, y):
        self.grid[x][y].next_state = 0
    
    def set_cell_dead(self, x, y):
        self.grid[x][y].state = 0

    def get_cell_state(self, x, y):
        return self.grid[x][y].state

    def get_cell_next_state(self, x, y):
        return self.grid[x][y].next_state
    
    def count_neighbors(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if i == 0 and j == 0:
                        continue
                    if self.get_cell_state(x + i, y + j) == 1:
                        count += 1
                except:
                    continue
        return count

    def evolve(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].state = self.grid[x][y].next_state
class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.next_state = state

class Rules:
    def __init__(self):
        self.rules = []
    def add_rule(self, rule):
        self.rules.append(rule)

    def sutisfy_rules(self, environment, x, y):
        for rule in self.rules:
            rule(environment, x, y)
        return True

    def _rule1(self, environment, x, y):
        completed = False
        if environment.get_cell_state(x, y) == 0 and environment.count_neighbors(x, y) == 3:
            environment.evolve_cell_alive(x, y)
            completed = True
        return completed


    def _rule2(self, environment, x, y):
        completed = False
        if environment.get_cell_state(x, y) == 1 and (environment.count_neighbors(x, y) <= 2 or environment.count_neighbors(x, y) >= 3):
            environment.evolve_cell_dead(x, y)
            completed = True
        return completed

    def _rule3(self, environment, x, y):
        completed = False
        if environment.get_cell_state(x, y) == 1 and 2<=environment.count_neighbors(x, y)<=3:
            environment.evolve_cell_alive(x, y)
            completed = True
        return completed


class Game:
    def __init__(self) -> None:
        self.environment = Environment(50, 50)
        self.rules = Rules()
        self.rules.add_rule(self.rules._rule1)
        self.rules.add_rule(self.rules._rule2)
        self.rules.add_rule(self.rules._rule3)
        pygame.init()
        self.screen = pygame.display.set_mode((self.environment.width * 20, self.environment.height * 20)) # gives 1000*1000
        self.dead_color = (0, 0, 0)
        self.alive_color = (255, 255, 255)
    def run_evolution(self):
        CLOCK = pygame.time.Clock()
        evolutioning = True
        while evolutioning:
            CLOCK.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    evolutioning = False
            for x in range(self.environment.width):
                for y in range(self.environment.height):
                    self.rules.sutisfy_rules(self.environment, x, y)
            for x in range(self.environment.width):
                for y in range(self.environment.height):
                    if self.environment.get_cell_next_state(x, y) == 1:
                        rect = pygame.Rect(x*20, y*20, 20, 20) # maximizes to 1000*1000 and each rect  is 20*20
                        pygame.draw.rect(self.screen, self.alive_color,rect)
                    else:
                        rect = pygame.Rect(x*20, y*20, 20, 20)
                        pygame.draw.rect(self.screen, self.dead_color,rect)
            self.environment.generation += 1
            print("Generation: " + str(self.environment.generation))
            self.environment.evolve()
            pygame.display.update()
        
    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.run_evolution()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = pos[0] // 20
                    y = pos[1] // 20
                    print("Clicked at: " + str(x) + " " + str(y))
                    if self.environment.get_cell_state(x, y) == 0:
                        self.environment.set_cell_alive(x, y)
                        rect = pygame.Rect(x*20, y*20, 20, 20)
                        pygame.draw.rect(self.screen, self.alive_color,rect)
                    else:
                        self.environment.set_cell_dead(x, y)
                        rect = pygame.Rect(x*20, y*20, 20, 20)
                        pygame.draw.rect(self.screen, self.dead_color,rect)
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()