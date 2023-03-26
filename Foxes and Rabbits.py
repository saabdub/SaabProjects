import tkinter as tk
import random
import math
import time

WIDTH = 500
HEIGHT = 500
RABBIT_COLOR = 'red'
FOX_COLOR = 'blue'

class Animal:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.age = 0
        self.boy = False #random.choice([True, False])

    def get_older(self):
        self.age += 1
    
    def move(self,speed):
        self.x += self.vx * speed
        self.y += self.vy * speed
        if self.x < 0:
            self.vx = abs(self.vx)
        elif self.x > WIDTH:
            self.vx = -abs(self.vx)
        if self.y < 0:
            self.vy = abs(self.vy)
        elif self.y > HEIGHT:
            self.vy = -abs(self.vy)

class Rabbit(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, RABBIT_COLOR)
        self.speed = 1

    def mate(self):
        return Rabbit(self.x+ random.randint(-20,20), self.y+ random.randint(-20,20))
            

class Fox(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, FOX_COLOR)
        self.speed = 2
        self.hunger = 0
        self.mating_timer = 0
        

    def mate(self):
        return Fox(self.x + random.randint(-25,25), self.y + random.randint(-25,25))
            

class Simulation:
    def __init__(self, num_rabbits, num_foxes):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.animals = []
        for i in range(num_rabbits):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            rabbit = Rabbit(x, y)
            self.animals.append(rabbit)

        for i in range(num_foxes):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            fox = Fox(x, y)
            self.animals.append(fox)


    def run(self):
        
        while True:
            self.canvas.delete('all')

            for animal in self.animals:
                animal.move(animal.speed)
                animal.get_older()
                

                if isinstance(animal, Rabbit):
                    self.canvas.create_oval(animal.x-5, animal.y-5, animal.x+5, animal.y+5, fill=RABBIT_COLOR)
                elif isinstance(animal, Fox):
                    self.canvas.create_oval(animal.x-5, animal.y-5, animal.x+5, animal.y+5, fill=FOX_COLOR)

                # mate if possible
                if isinstance(animal, Rabbit) and animal.age >= 20 and animal.age <= 25 and animal.boy == False:
                    self.animals.append(animal.mate())

                elif isinstance(animal, Fox)  and animal.age >= 50 and animal.boy == False and animal.mating_timer >= 5 and animal.mating_timer <= 55:
                    self.animals.append(animal.mate())

                if isinstance(animal, Fox) and animal.hunger < 80:
                    animal.mating_timer += 1
                
                if isinstance(animal, Fox):
                    nearby_rabbits = [animal1 for animal1 in self.animals if isinstance(animal1, Rabbit) and math.sqrt((animal1.x-animal.x)**2 + (animal1.y-animal.y)**2) < 25]
                    if nearby_rabbits:
                            animal.hunger = 0
                            prey = random.choice(nearby_rabbits)
                            self.animals.remove(prey)
                            del prey
                    else:
                        animal.hunger += 5
                
                
                if isinstance(animal, Fox) and (animal.hunger >= 200 or animal.age >= 50):
                    self.animals.remove(animal)
                    del animal
                elif isinstance(animal, Rabbit)and animal.age >= 30:
                    self.animals.remove(animal)
                    del animal
                
                if len(self.animals) <= 0 or len(self.animals) >= 20000:
                    print(len(self.animals))
                    exit()
                


                
                


                

                #print(len(self.animals), animal.age,animal.x)

                """
                # increment mating timer
                if isinstance(animal, Rabbit) and animal.mating_timer < 200:
                    animal.mating_timer += 1
                elif isinstance(animal, Fox) and animal.mating_timer < 200:
                    animal.mating_timer += 1

            for fox in [animal for animal in self.animals if isinstance(animal, Fox)]:
                nearby_rabbits = [animal for animal in self.animals if isinstance(animal, Rabbit) and math.sqrt((animal.x-fox.x)**2 + (animal.y-fox.y)**2) < 10]
                if nearby_rabbits:
                    fox.hunger = 0
                    prey = random.choice(nearby_rabbits)
                    self.animals.remove(prey)
                    del prey
                else:
                    fox.hunger += 1
                    if fox.hunger >= 100:
                        self.animals.remove(fox)
                        del fox
                    else:
                        rabbit = random.choice([animal for animal in self.animals if isinstance(animal, Rabbit)])
                        dx = rabbit.x - fox.x
                        dy = rabbit.y - fox.y
                        distance = math.sqrt(dx**2 + dy**2)
                        fox.vx = fox.speed * dx / distance
                        fox.vy = fox.speed * dy / distance

            for rabbit in [animal for animal in self.animals if isinstance(animal, Rabbit)]:
                nearby_foxes = [animal for animal in self.animals if isinstance(animal, Fox) and math.sqrt((animal.x-rabbit.x)**2 + (animal.y-rabbit.y)**2) < 10]
                if nearby_foxes:
                    self.animals.remove(rabbit)
                    del rabbit
                else:
                    rabbit.vx = random.uniform(-rabbit.speed, rabbit.speed)
                    rabbit.vy = random.uniform(-rabbit.speed, rabbit.speed)

            # spawn new rabbits periodically
            self.rabbit_spawn_timer += 1
            if self.rabbit_spawn_timer >= 100:
                for i in range(random.randint(1, 3)):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    rabbit = Rabbit(x, y)
                    self.animals.append(rabbit)
                self.rabbit_spawn_timer = 0

            # spawn new foxes periodically
            self.fox_spawn_timer += 1
            if self.fox_spawn_timer >= 200:
                for i in range(random.randint(1, 2)):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    fox = Fox(x, y)
                    self.animals.append(fox)
                self.fox_spawn_timer = 0"""

            self.canvas.update()
            self.canvas.after(50)

if __name__ == '__main__':
    sim = Simulation(20, 30)
    sim.run()


