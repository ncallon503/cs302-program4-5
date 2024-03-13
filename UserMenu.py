import RedBlackTree
import Event
import random

class UserMenu:
    def __init__(self):
        self.__hero = None
        self.__event_tree = RedBlackTree.RedBlackTree()
        self.__initialize_events()
        self.__days_until_world_end = 30 # 30 days for user to complete the quest
        self.__max_progress=14

    def display_menu(self):
        print("Please enter one of the options:\n")
        print("1. Continue your journey (encounter)")
        print("2. View your inventory, gold, and health")
        print("3. Rest (heal) at expense of time")
        print("4. View days until world end")
        print("5. Drink a health potion (if you have one)")
        print("0. Quit")

    def __select__event(self):
        variation = random.randint(0,5) - 2 # Random number between -2 and 2
        eventChosen = self.__event_tree.get_event(self.max_progress + variation) 
        return eventChosen

    def __initialize_events(self):
        self.event_tree.insert(Event.Event(1,'Enemy encounter (Goblin)'))
        self.event_tree.insert(Event.Event(2,'Merchant encounter'))
        self.event_tree.insert(Event.Event(3,'Enemy encounter (Goblin)'))
        self.event_tree.insert(Event.Event(4,'Enemy encounter (Orc)'))
        self.event_tree.insert(Event.Event(5,'Merchant encounter'))
        self.event_tree.insert(Event.Event(6,'Enemy encounter (Goblin)'))
        self.event_tree.insert(Event.Event(7,'Enemy encounter (Orc)'))
        self.event_tree.insert(Event.Event(8,'Merchant encounter'))
        self.event_tree.insert(Event.Event(9,'Enemy encounter (Harpy)'))
        self.event_tree.insert(Event.Event(10,'Enemy encounter (Harpy)'))
        self.event_tree.insert(Event.Event(11,'Enemy encounter (Baby Dragon)'))
        self.event_tree.insert(Event.Event(12,'Merchant encounter'))
        self.event_tree.insert(Event.Event(13,'Enemy encounter (Harpy)'))
        self.event_tree.insert(Event.Event(14,'Merchant encounter'))
        self.event_tree.insert(Event.Event(15,'Enemy encounter (Baby Dragon)'))
        self.event_tree.insert(Event.Event(16,'Boss encounter (Dragon)'))

    def __initialize_hero(self):
        try:
            name = input("Please enter your name: ")
            self.__hero = Event.Hero(name)
            print(f"There is not much time, {self.__hero.get_name()}. There are 30 days before the Black Dragon completes his ritual and destroys the world.")
            print(f"You must prepare for the final battle. You have 100 health and 100 maximum health right now, and 0 gold.")
            print(f"You have an inventory and can acquire certain items to help you on your journey, but to find and slay the dragon,")
            print(f"you must have the Black Dragon Eye and Dragonslayer Sword. You can find these items from merchants or enemies.")
            print(f"Good luck, {self.__hero.get_name()}.")
        except:
            print("Invalid input. Please try again.")
            self.__initialize_hero()