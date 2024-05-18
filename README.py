import random

class Seed: 
    def check_status(self):
        if self.recharge != self.recharge_index:
            return "Recharging"
        else:
            return "Active"
            
class Sunflower(Seed): 
    def __init__(self): 
        self.recharge = 2 
        self.recharge_index = 2
        self.sun_cost = 50 
        self.look = "S"

class Peashooter(Seed): 
    def __init__(self):
        self.recharge = 0
        self.recharge_index = 3
        self.sun_cost = 100 
        self.look = "P"

class Wallnut(Seed): 
    def __init__(self):
        self.recharge = 0
        self.recharge_index = 4
        self.sun_cost = 50 
        self.look = "W"

class Potatomine(Seed): 
    def __init__(self): 
        self.recharge = 0
        self.recharge_index = 5
        self.sun_cost = 25
        self.look = "."

class Jalapeno(Seed):
    def __init__(self):
        self.recharge = 0
        self.recharge_index = 8 
        self.sun_cost = 125 
        self.look = "J"

class Iceshroom(Seed):
    def __init__(self):
        self.recharge = 0
        self.recharge_index = 8 
        self.sun_cost = 150 
        self.look = "I"

class Lane: 
    def __init__(self, name): 
        self.name = name 
        self.lane = ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] 
        self.mower_index = 1

    def print_lane(self):
        print(self.lane[0] , '|', self.lane[1] , '|', self.lane[2] , '|', self.lane[3] , '|', self.lane[4] , '|', self.lane[5] , '|', self.lane[6] , '|', self.lane[7] , '|', self.lane[8] , '|', self.lane[9] , '|')
    
    def summon_zombie(self):
        if game.tick in range(5, 21):
            will_summon = random.randint(1, 16)
            if will_summon == 1:    
                self.lane[9] = "Z"
        if game.tick in range(20,27):
            will_summon = random.randint(1, 3)
            if will_summon == 1:    
                self.lane[9] = "Z"

    def move_zombie(self):
        for x in range(1,10):
            if self.lane[x] == "Z" or self.lane[x] == "z":
                if self.lane[x-1] == "M":
                    self.use_mower()
                elif self.lane[x-1] == "W":
                    self.lane[x-1] = "w"
                elif self.lane[x-1] == "w":
                    self.lane[x-1] = "v"
                elif self.lane[x-1] == "i":
                    self.lane[x-1] = " "
                    self.lane[x] = " "
                    print("SPUDOW!")
                elif self.lane[x-1] == "Z" or self.lane[x-1] == "z":
                    pass
                elif self.lane[x-1] != " ":
                    self.lane[x-1] = " "
                else:
                    self.lane[x-1] = self.lane[x]
                    self.lane[x] = " "

    def check_nearest_peashooter(self):
        for column in range(1,10):
            if self.lane[column] == "P":
                return column
                break

    def check_nearest_zombie(self):
        for column in range(1,10):
            if self.lane[column] == "Z" or self.lane[column] == "z":
                if column > self.check_nearest_peashooter():
                    return column
                    break
        
    def check_peashooter_amount(self):
        amount = 0
        for column in range(1,10):
            if self.lane[column] == "P":
                amount = amount + 1
        return amount
    
    def use_mower(self):
        if game.jalapeno_index == 1:
            for x in range(0,10):
                if self.lane[x] == "Z" or self.lane[x] == "z":
                    self.lane[x] = " "
            game.jalapeno_index = 0
        elif self.mower_index == 1:
            for x in range(0,10):
                if self.lane[x] == "Z" or self.lane[x] == "z":
                    self.lane[x] = " "
                    self.lane[0] = " "
            self.mower_index = 0
        elif self.mower_index == 0:
            if self.lane[0] == "Z":
                game.check_loss = 1

    def check_zombie_amount(self):
        amount = 0
        for column in range(1,10):
            if self.lane[column] == "Z" or self.lane[column] == "z":
                amount = amount + 1
        return amount
    
    def potatos_grow(self):
        for column in range(1,10):
            if self.lane[column] == ".":
                self.lane[column] = "i"

class Game: 
    def __init__(self): 
        self.check_loss = 0 
        self.sun_count = 50 
        self.plant_this_turn = 2 
        self.lawn = [Lane(1), Lane(2), Lane(3), Lane(4), Lane(5)] 
        self.seeds = [Sunflower(), Peashooter(), Wallnut(), Potatomine(), Jalapeno(), Iceshroom()]
        self.tick = 1
        self.jalapeno_index = 0
    
    def print_lawn(self):
        for lane in self.lawn:
            print("---------------------------------------")
            lane.print_lane()
        print("---------------------------------------")
    
    def get_current_sun(self):
        for lane in self.lawn:
            for x in range(1,10):
                if lane.lane[x] == "S":
                    self.sun_count = self.sun_count + 10
        self.sun_count = self.sun_count + 10
        return self.sun_count
        
    def recharge_packets(self):
        for plant in self.seeds:
            if plant.recharge < plant.recharge_index:
                plant.recharge = plant.recharge + 1
    
    def plants_deal_damage(self):
        for lane in self.lawn:
            for column in range(1,10):
                if lane.lane[column] == "J":
                    self.jalapeno_index = 1
                    lane.use_mower()
                    lane.lane[column] = " "
            try:
                if lane.check_peashooter_amount() > 0:
                    if self.tick % 2 == 0:
                        for i in range(1, lane.check_peashooter_amount() + 1):
                            if lane.lane[lane.check_nearest_zombie()] == "z":
                                lane.lane[lane.check_nearest_zombie()] = " "
                            if lane.lane[lane.check_nearest_zombie()] == "Z":
                                lane.lane[lane.check_nearest_zombie()] = "z"
            except:
                pass

    def check_iceshroom(self):
        if self.seeds[5].recharge in range(0, 3):
            return True
        else:
            for lane in self.lawn:
                for column in range(1,10):
                    if lane.lane[column] == "I":
                        lane.lane[column] = " "
            return False

    def planting(self):
        try:
            self.plant_this_turn = int(input("Would you like to plant this turn? (1 = Yes, 2 = No): "))
            if self.plant_this_turn == 1:
                chosen_plant = int(input(f"What plant will you choose? (1 = Sunflower/50: {self.seeds[0].check_status()}, 2 = Peashooter/100: {self.seeds[1].check_status()}, 3 = Wall-nut/50: {self.seeds[2].check_status()}, 4 = Potato Mine/25: {self.seeds[3].check_status()}, 5 = Jalapeño/125: {self.seeds[4].check_status()}, 6 = Ice-Shroom/150: {self.seeds[5].check_status()}): "))
                if self.seeds[chosen_plant - 1].recharge == self.seeds[chosen_plant - 1].recharge_index:
                    chosen_lane = int(input("What lane do you want to plant in? (1 = Top Lane, 5 = Bottom Lane): "))
                    column = int(input("In what column? (1 = Backmost, 9 = Frontmost): "))
                    if self.lawn[chosen_lane - 1].lane[column] == " ":
                        if self.sun_count - self.seeds[chosen_plant - 1].sun_cost >= 0:
                            self.sun_count = self.sun_count - self.seeds[chosen_plant - 1].sun_cost
                            self.seeds[chosen_plant - 1].recharge = 0
                            self.lawn[chosen_lane - 1].lane[column] = self.seeds[chosen_plant - 1].look
                        else:
                            print("You don't have enough sun to plant that!")
                            self.planting()
                    else:
                        print("You can't plant in that slot!")
                        self.planting()
                else:
                    print("The plant is still recharging!")
                    self.planting()
        except:
            print("Can't compute your answer, try again.")
            self.planting()

    def play(self):
        while True:
            self.plants_deal_damage()
            for lane in self.lawn:
                if self.check_iceshroom() == False:
                    lane.move_zombie()
                lane.summon_zombie()
                if self.seeds[3].recharge == self.seeds[3].recharge_index:
                    lane.potatos_grow()
            self.print_lawn()
            self.recharge_packets()
            if self.tick > 22:
                total_zombies = 0
                for lane in self.lawn:
                    total_zombies = total_zombies + lane.check_zombie_amount()
                if total_zombies == 0:
                    print("You won!")
                    self.tick = 0
                    break
            print(f"Current Sun = {self.get_current_sun()}")
            self.planting()
            if self.check_loss == 1:
                print("The Zombies ate your brains!")
                break
            if self.tick == 19:
                print("A huge wave of Zombies is Approaching")
            self.tick = self.tick + 1

game = Game() 
game.play()