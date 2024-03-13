import enum

class Items(enum.Enum):
    Long_Sword = 1
    Dragonslayer_Sword = 2
    Health_Potion = 3
    Black_Dragon_Eye = 4
    Victory_Trophy = 5

class Event: # The event will be stored inside of the nodes of the red black tree
    def __init__(self, chronological="0", name="", character=None):
        self.__chronological = chronological
        self.__name = name
        self.__character = character
        self.__type = type(character)

    def __str__(self): # String method for displaying event
        return f"{self.__name}\n"
    
    def get_chronological(self): # Retrieves the order the event should be encountered
        return self.__chronological
    
    def get_character(self):
        return self.__character
    
    def get_type(self):
        return self.__type


class Character:
    def __init__(self, name, health=50, inventory=[], gold=10): # Default health is 100, default inventory is empty, default gold is 10
        self._name = name
        self._health = health
        self._inventory = inventory
        self._gold = gold

    def __str__(self): # String method for displaying character
        return f"Name: {self._name}, Health: {self._health}, Inventory: {self._inventory}, Gold: {self._gold}\n"
    
    def get_name(self):
        return self._name
    
    def get_health(self):
        return self._health
    
    def get_inventory(self):
        return self._inventory
    
    def get_gold(self):
        return self._gold
    
    def set_name(self, name):
        self._name = name
        return True
    
    def set_health(self, health):
        self._health = health
        if(health <= 0):
            self._health = 0 # Can't go negative
        return True
    
    def set_gold(self, gold):
        self._gold = gold
        return True
    
    def remove_from_inventory(self, item):
        self._inventory.remove(item)
        return True
    
    def add_to_inventory(self, item):
        self._inventory.append(item)
        return True

    def greeting_msg(self):
        print(f"Hello, my name is {self._name}.")

    def drop_loot(self, other_character):
        other_character += self._gold
        print(f"{other_character.get_name()} has acquired {self._gold} gold from {self._name}.")
        return self._drop_loot_recursive(other_character, 0)

    def _drop_loot_recursive(self, other_character, index): # Recursive helper for dropping inventory to other character
        if index == len(self._inventory) or len(self._inventory) == 0: # Base cases
            return True
        item = self._inventory.pop(0) # Pops for no duplicates
        other_character.add_to_inventory(item) # Appends to other inventory
        print(f"{other_character.get_name()} has acquired {item} from {self._name}.")
        return self._drop_loot_recursive(other_character, index + 1) # Recursively calls

    def __iadd__(self, gold): # The overloaded increment and decrement decrease and increase gold by an integer
        if isinstance(gold, int):
            self._gold += gold
        else:
            raise TypeError("Can only increment by an integer.")
        return self
    
    def __isub__(self, gold):
        if isinstance(gold, int):
            self._gold -= gold
        else:
            raise TypeError("Can only decrement by an integer.")
        return self

class Hero(Character):
    def __init__(self, name, health=100, inventory=[], gold=0, max_health=100):
        super().__init__(name, health, inventory, gold)
        self._max_health = max_health # Hero starts out with 100 max_health which grows as they level up by defeating foes (We don't keep track of level, just health)

    def get_max_health(self): # Only need getter, hero increases by leveling up
        return self._max_health

    def encounter_msg(self):
        print(f"Hello, my name is {self._name}.")

    def level_up(self):
        self._max_health += 10
        print(f"{self._name} has won the battle and leveled up! Max health increased by 10.")

    def drink_potion(self):
        if self._inventory.count(Items.Health_Potion.name) > 0:
            print(f"{self._name} has drunk a health potion and restored to max health of {self._max_health}.")
            self._health = self._max_health
            self._inventory.remove(Items.Health_Potion.name)
            return True
        else:
            print(f"\n You do not have any health potions.")
            return False

    def rest(self):
        print(f"\n{self._name} has rested and restored to max health of {self._max_health}.")
        self._health = self._max_health

    def open_inventory(self):
        if(len(self._inventory) == 0):
            print(f"\nYou have no items in your inventory.")
        else:
            print(f"You have the followiing items in your inventory:")
            self.__rec__print_inventory(self._inventory, 0)
        print(f"You have {self._gold} gold.")
        print(f"You have {self._health} health currently, and {self._max_health} max health.")
        return True

    def __rec__print_inventory(self, inventory, index):
        if len(inventory) == 0:
            return False
        if index == len(inventory):
            return True
        print(f"{index}. {inventory[index]}")
        return self.__rec__print_inventory(inventory, index + 1)

class Enemy(Character):
    def __init__(self, name, health=50, inventory=[], gold=0, health_taken = 30):
        super().__init__(name, health, inventory, gold)
        self._gold = gold
        self._health_taken = health_taken

    def fight_hero(self, hero): # For the fights with the hero, the other character calls this function passing the hero in
        print(f"{self._name} is fighting {hero.get_name()}.")
        if hero.get_health() <= self._health:
            print(f"{self._name} has defeated {hero.get_name()}.")
            print(f"{hero.get_name()} has taken {self._health_taken} damage.")            
            if hero.get_inventory().count(Items.Long_Sword.name) > 0:
                print ("Hero has taken half damage with long sword.")
                hero.set_health(hero.get_health() - self._health_taken / 2)
            else:
                hero.set_health(hero.get_health() - self._health_taken)
            print(f"{hero.get_name()} has {hero.get_health()} health remaining.")
            return False
        else:
            print(f"{self._name} has been defeated by {hero.get_name()}.")
            if hero.get_inventory().count(Items.Long_Sword.name) > 0:
                print ("Hero has taken half damage with long sword.")
                hero.set_health(hero.get_health() - self._health_taken / 2)
            else:
                hero.set_health(hero.get_health() - self._health_taken)
            self.drop_loot(hero)
            print(f"{hero.get_name()} has taken {self._health_taken} damage.")
            print(f"{hero.get_name()} has {hero.get_health()} health remaining.")
            hero.level_up()
            return True

class Merchant(Character):
    def __init__(self, name="Merchant", health=150, inventory=[Items.Long_Sword.name, Items.Dragonslayer_Sword.name, Items.Health_Potion.name], prices = [50, 200, 10], gold = 500):
        super().__init__(name, health, inventory, gold)
        self.__prices = prices # Shopkeeper has prices for menu items

    def open_shop(self, user):
        print(f"Welcome to my shop, {user.get_name()}.")
        print("I have the following items for sale:")
        print("Would you like to buy anything?")
        return self.__prompt_to_buy(user)

    def __rec__print_inventory(self, inventory, index):
        if index == len(inventory):
            return True
        print(f"{index}. {inventory[index]} - {self.__prices[index]} gold.")
        return self.__rec__print_inventory(inventory, index + 1)

    def __prompt_to_buy(self, user):
        self.__rec__print_inventory(self._inventory, 0)
        print(f"\nYou have {user.get_gold()} gold.")
        choice = int(input("\nPlease enter the number of the item you would like to buy, \n-1 to leave the merchant, or...\n-2 to try to fight the merchant.\nPlease enter one of the following options.\n"))
        if choice == -1:
            print("Thank you for visiting my shop. Goodbye.")
            return True
        if choice == -2:
            print(f"You have chosen to fight the merchant, {user.get_name()}.")
            return self.__fight_hero(user)
        if choice < 0 or choice >= len(self._inventory):
            print(f"choice is {choice}, len is {len(self._inventory)}, choice < 0 is {choice < 0}, choice >= len is {choice >= len(self._inventory)}")
            print("this")
            print("Invalid choice. Please try again.")
            return self.__prompt_to_buy(user)
        else:
            return self.__sell_item(user, choice)
    
    def __fight_hero(self, hero): # The merchant has a private function because the user must choose through the menu to fight him
        health_taken = 100 # Merchant will always deal 100 damage (or half with long sword)
        print(f"{self._name} is fighting {hero.get_name()}.")
        if hero.get_health() <= self._health:
            print(f"{self._name} has defeated {hero.get_name()}.")
            hero.set_health(0)
            print(f"{hero.get_name()} has taken {hero.get_max_health()} damage.")
            print(f"{hero.get_name()} has {hero.get_health()} health remaining.")
            return False
        else:
            print(f"{self._name} has been defeated by {hero.get_name()}.")
            if hero.get_inventory().count(Items.Long_Sword.name) > 0:
                print ("Hero has taken half damage with long sword.")
                hero.set_health(hero.get_health() - health_taken / 2)
                print(f"{hero.get_name()} has taken {health_taken / 2} damage.")
            else:
                hero.set_health(hero.get_health() - health_taken)
                print(f"{hero.get_name()} has taken {health_taken} damage.")
            self.drop_loot(hero)
            hero.level_up()
            return True

    def __sell_item(self, user, choice):
        try:
            if user.get_gold() < self.__prices[choice]:
                print("\nYou do not have enough gold to purchase this item.")
                return self.__prompt_to_buy(user)
            else:
                print(f"You have purchased {self._inventory[choice]} for {self.__prices[choice]} gold.\n")
                if self._inventory[choice] == Items.Health_Potion.name:
                    user.add_to_inventory(self._inventory[choice]) # We don't pop health potions, merchant has infinite
                    user -= self.__prices[choice] # Overloaded operator decreases user gold
                else:
                    user.add_to_inventory(self._inventory.pop(choice))
                    user -= self.__prices[choice] # Overloaded operator decreases user gold
                    self.__prices.pop(choice) # We the price and item off the menu
                return self.__prompt_to_buy(user)
        except ValueError:
            print("Value")
            print("Invalid choice. Please try again.")
            return self.__prompt_to_buy(user)
        except Exception as e:
            print(e)
            return False


class Boss(Character):
    def __init__(self, name, health=200, inventory=[Items.Victory_Trophy.name], gold = 1000):
        super().__init__(name, health, inventory, gold)

    def fight_hero(self, hero):
        print(f"{self._name} is fighting {hero.get_name()}.")
        if hero.get_inventory().count(Items.Black_Dragon_Eye.name) > 0 and hero.get_inventory().count(Items.Dragonslayer_Sword.name) > 0: # Can only defeat when both items acquired
            print(f"{hero.get_name()} has defeated {self._name}.")
            print(f"Congratulations, {hero.get_name()}! You have defeated the Black Dragon and saved the world.")
            self.drop_loot(hero)
            return True
        else:
            print(f"{self._name} has defeated {hero.get_name()}.")
            print(f"You must have the Black Dragon Eye and Dragonslayer Sword to defeat the Black Dragon.")
            print("The shopkeeper will sell the Dragonslayer Sword and Baby Dragons have a chance of dropping on the Black Dragon Eye.")
            hero.set_health(0)
            print(f"\nAfter a brutal loss, {hero.get_name()} health has dropped to 0. You must rest.")
            return False
