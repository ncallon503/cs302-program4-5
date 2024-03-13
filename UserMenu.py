import RedBlackTree
import Event
import random

class InputException(Exception):
    def __init__(self, message="Invalid data type for input. Please enter a valid input."):
        super().__init__(message)

class OutOfRangeException(Exception):
    def __init__(self, min, max):
        message = f"Please enter a number between {min} and {max}."
        super().__init__(message)

class UserMenu:
    def __init__(self):
        self.__days_until_world_end = 30 # 30 days for user to complete the quest
        self.__progress = 0 # Progress of the hero
        self.__max_progress = 14 # There will be 16 events total, so due to the variation being 2 we do 16-2 so the tree doesn't go out of bounds when __select__event is called 
        self.__hero = None
        self.__event_tree = RedBlackTree.RedBlackTree()
        self.__initialize_events()
        self.__initialize_hero()

    def display_menu(self):
        try:
            print("\nPlease enter one of the options:\n")
            print("1. Continue your journey (encounter)")
            print("2. View your inventory, gold, and health")
            print("3. Rest (heal) at expense of time")
            print("4. View days until world end")
            print("5. Drink a health potion (if you have one)")
            print("0. Quit\n")
            choice = self.__prompt__int__range(0,5)
            match choice:
                case 0:
                    print("Are you sure you want to give up on your journey? The world needs you.")
                    print("1. No, I will save the world.")
                    print("2. Yes, I give up.")
                    choice = self.__prompt__int__range(1,2)
                    if choice == 1:
                        print(f"Thank you, {self.__hero.get_name()}. The world is counting on you.")
                        return self.display_menu()
                    else:
                        print(f"You gave up on your journey, {self.__hero.get_name()}. You made it to day {30 - self.__days_until_world_end}.")
                    return 0
                case 1:
                    event = self.__select__event()
                    success = self.play_event(event, self.__hero)
                    if(success):
                        if(self.__progress != self.__max_progress): # Don't want to progress past limit
                            self.__progress += 1 # If succeed in event, proceed
                    self.__days_until_world_end -= 1 # World ends sooner no matter what
                    self.__prompt_continue()
                    return self.display_menu()
                case 2:
                    print(f"\nInventory: {self.__hero.get_inventory()}")
                    print(f"Gold: {self.__hero.get_gold()}")
                    print(f"Health: {self.__hero.get_health()}/{self.__hero.get_max_health()}")
                    self.__prompt_continue()
                    return self.display_menu()
                case 3:
                    self.__hero.rest()
                    self.__days_until_world_end -= 1
                    print(f"There are now {self.__days_until_world_end} days until the world ends.")
                    self.__prompt_continue()
                    return self.display_menu()
                case 4:
                    print(f"\nDays until world end: {self.__days_until_world_end}\n")
                    self.__prompt_continue()
                    return self.display_menu()
                case 5:
                    self.__hero.drink_potion() # Does not take up any time
                    self.__prompt_continue()
                    return self.display_menu()
        except OutOfRangeException as e:
            print(e)
            return self.display_menu()
        except InputException as e:
            print(e)
            return self.display_menu()
        except ... as e:
            print(e)
            return False
        
    def play_event(self, event, hero):
        try:
            print(f"Encountering event: {event}")
            match event.get_type():
                case Event.Enemy:
                    print("You have encountered an enemy.\n")
                    print(f"You have the following items in your inventory: {self.__hero.get_inventory()}")
                    print(f"and you have {self.__hero.get_health()} health remaining.")
                    print(f"The enemy requires {event.get_character().get_health()} health to defeat.")
                    print("Do you wish to fight (1) or flee (2)?\n")
                    choice = self.__prompt__int__range(1,2)
                    match choice:
                        case 1:
                            return event.get_character().fight_hero(hero)
                        case 2:
                            print("You have fled from the enemy.")
                            return False
                case Event.Merchant:
                    print("You have encountered a merchant.\n")
                    return event.get_character().open_shop(hero)
                case Event.Boss:
                    print("You have encountered the final boss, the evil Black Dragon.\n")
                    return event.get_character().fight_hero(hero)
            return True
        except ... as e:
            print(e)
            return False
    
    def __prompt__int__range(self, low, high):
        try:
            choice = int(input("Please enter a number: "))
            if choice < low or choice > high:
                raise OutOfRangeException(low, high)
            return choice
        except OutOfRangeException as e:
            print(e)
            return self.__prompt__int__range(low, high)
        except ... as e:
            print("Invalid input. Please try again.")
            return self.__prompt__int__range(low, high)

    def __select__event(self):
        variation = random.randint(1,4) - 2 # Random number between -1 and 2
        eventNumber = self.__progress + variation
        if(eventNumber < 0): # Cannot choose less than 0
            eventNumber = 0
        eventChosen = self.__event_tree.get_event(eventNumber) 
        return eventChosen

    def __initialize_events(self):
        self.__event_tree.insert(Event.Event(0,'Enemy encounter (Goblin)', Event.Enemy("Goblin", 50, [], 10, 30)))
        self.__event_tree.insert(Event.Event(1,'Merchant encounter', Event.Merchant("Merchant")))
        self.__event_tree.insert(Event.Event(2,'Enemy encounter (Goblin)', Event.Enemy("Goblin", 50, [], 10, 30)))
        self.__event_tree.insert(Event.Event(3,'Enemy encounter (Orc)', Event.Enemy("Orc", 100, [], 20, 40)))
        self.__event_tree.insert(Event.Event(4,'Merchant encounter', Event.Merchant("Merchant")))
        self.__event_tree.insert(Event.Event(5,'Enemy encounter (Goblin)', Event.Enemy("Goblin", 50, [], 10, 30)))
        self.__event_tree.insert(Event.Event(6,'Enemy encounter (Harpy)', Event.Enemy("Harpy", 75, [], 15, 45)))
        self.__event_tree.insert(Event.Event(7,'Merchant encounter', Event.Merchant("Merchant")))
        self.__event_tree.insert(Event.Event(8,'Enemy encounter (Orc)', Event.Enemy("Orc", 100, [], 20, 40)))
        self.__event_tree.insert(Event.Event(9,'Enemy encounter (Harpy)', Event.Enemy("Harpy", 75, [], 15, 45)))
        self.__event_tree.insert(Event.Event(10,'Enemy encounter (Baby Dragon)', Event.Enemy("Baby Dragon", 150, ["Black_Dragon_Eye"], 30, 50)))
        self.__event_tree.insert(Event.Event(11,'Merchant encounter', Event.Merchant("Merchant")))
        self.__event_tree.insert(Event.Event(12,'Enemy encounter (Heavy Orc)', Event.Enemy("Heavy Orc", 150, [], 30, 60)))
        self.__event_tree.insert(Event.Event(13,'Merchant encounter', Event.Merchant("Merchant")))
        self.__event_tree.insert(Event.Event(14,'Enemy encounter (Baby Dragon)', Event.Enemy("Baby Dragon", 150, ["Black_Dragon_Eye"], 30, 50)))
        self.__event_tree.insert(Event.Event(15,'Boss encounter (Dragon)', Event.Boss("Black Dragon", 200)))

    def __initialize_hero(self):
        try:
            name = input("Please enter your name: ")
            self.__hero = Event.Hero(name)
            print(f"\nThere is not much time, {self.__hero.get_name()}. There are {self.__days_until_world_end} days before the Black Dragon completes his ritual and destroys the world.")
            print(f"You must prepare for the final battle. You have {self.__hero.get_health()} health and {self.__hero.get_max_health()} maximum health right now, and {self.__hero.get_gold()} gold.")
            print(f"You have an inventory and can acquire certain items to help you on your journey, but to find and slay the dragon,")
            print(f"To defeat, the Black Dragon, you must have the Black Dragon Eye and Dragonslayer Sword. You can find these items from merchants or enemies.")
            print(f"Good luck, {self.__hero.get_name()}.")
            print()
            self.__prompt_continue() # Simple for pressing enter to read
        except:
            print("Invalid input. Please try again.")
            self.__initialize_hero()

    def __prompt_continue(self): # Simple function for readability for menu
        print("Press enter to continue...")
        input()
