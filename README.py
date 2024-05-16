import random

class Seed: 
    def __init__(self): 
        self.recharge = 0 
        self.recharge_index = 2

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

class Lane: 
    def __init__(self, name): 
        self.name = name 
        self.lane = ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] 
        self.mower_index = 1

    def print_lane(self):
        print(self.lane[0] , '|', self.lane[1] , '|', self.lane[2] , '|', self.lane[3] , '|', self.lane[4] , '|', self.lane[5] , '|', self.lane[6] , '|', self.lane[7] , '|', self.lane[8] , '|', self.lane[9] , '|')
    
    def summon_zombie(self):
        will_summon = random.randint(1, 25)
        if will_summon == 1:    
            self.lane[9] = "Z"
            
    def wave_zombie(self):
        will_summon = random.randint(1, 8)
        if will_summon == 1:    
            self.lane[9] = "Z"
    
    def move_zombie(self):
        for x in range(1,10):
            if self.lane[x] == "Z":
                if self.lane[x-1] == "M":
                    self.lane[x-1] = "Z"
                elif self.lane[x-1] == "W":
                    self.lane[x-1] = "w"
                elif self.lane[x-1] == "w":
                    self.lane[x-1] = "v"
                elif self.lane[x-1] == "Z":
                    pass
                elif self.lane[x-1] != " ":
                    self.lane[x-1] = " "
                else:
                    self.lane[x] = " "
                    self.lane[x-1] = "Z"
                    
    def check_nearest_zombie(self):
        for column in range(1,10):
            if self.lane[column] == "Z":
                return column
                break
        
    def check_peashooter_amount(self):
        amount = 0
        for column in range(1,10):
            if self.lane[column] == "P":
                amount = amount + 1
        return amount
    
    def use_mower(self):
        if self.mower_index == 1:
            if self.lane[0] == "Z":
                for x in range(0,10):
                    if self.lane[x] == "Z":
                        self.lane[x] = " "
                    
                self.mower_index = 0
        elif self.mower_index == 0:
            if self.lane[0] == "Z":
                game.check_loss = 1
                
class Game: 
    def __init__(self): 
        self.check_loss = 0 
        self.sun_count = 50 
        self.plant_this_turn = 2 
        self.lawn = [Lane(1), Lane(2), Lane(3), Lane(4), Lane(5)] 
        self.seeds = [Sunflower(), Peashooter(), Wallnut()]
    
    def print_lawn(self):
        for lane in self.lawn:
            print("---------------------------------------")
            lane.print_lane()
        print("---------------------------------------")
    
    def get_current_sun(self):
        for lane in self.lawn:
            for x in range(1,10):
                if lane.lane[x] == "S":
                    self.sun_count = self.sun_count + 25
        self.sun_count = self.sun_count + 25
        return self.sun_count
        
    def recharge_packets(self):
        for plant in self.seeds:
            if plant.recharge != plant.recharge_index:
                plant.recharge = plant.recharge + 1
    
    def peashooters_shoot(self):
        for lane in self.lawn:
            randomizer = random.randint(1, 5)
            if randomizer == 4:
                try:
                    if lane.check_peashooter_amount() > 0:
                        for i in range(1, lane.check_peashooter_amount() + 1):
                            lane.lane[lane.check_nearest_zombie()] = " "
                except:
                    pass
    
    def planting(self):
        try:
            self.plant_this_turn = int(input("Would you like to plant this turn? (1 = Yes, 2 = No): "))
            if self.plant_this_turn == 1:
                chosen_plant = int(input(f"What plant will you choose? (1 = Sunflower: {self.seeds[0].check_status()}, 2 = Peashooter: {self.seeds[1].check_status()}), 3 = Wall-nut: {self.seeds[2].check_status()}): "))
                if self.seeds[chosen_plant - 1].recharge == self.seeds[chosen_plant - 1].recharge_index:
                    chosen_lane = int(input("What lane do you want to plant in? (1 = Top Lane, 5 = Bottom Lane): "))
                    column = int(input("In what column? (1 = Backmost, 9 = Frontmost): "))
                    if self.lawn[chosen_lane - 1].lane[column] == " ":
                        self.lawn[chosen_lane - 1].lane[column] = self.seeds[chosen_plant - 1].look
                        if self.sun_count - self.seeds[chosen_plant - 1].sun_cost >= 0:
                            self.sun_count = self.sun_count - self.seeds[chosen_plant - 1].sun_cost
                            self.seeds[chosen_plant - 1].recharge = 0
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
        for i in range(20):
            for lane in self.lawn:
                lane.move_zombie()
                lane.summon_zombie()
                lane.use_mower()
            print(f"Current Sun = {self.get_current_sun()}")
            self.peashooters_shoot()
            self.print_lawn()
            self.recharge_packets()
            self.planting()
            if self.check_loss == 1:
                print("The Zombies ate your brains!")
                break
game = Game() 
game.play()
