# Nathan Callon, CS302, 3/13/2024 Test Suite

import pytest
from unittest.mock import patch
import Event
import UserMenu
import RedBlackTree

@pytest.fixture
def BlackDragon():
    return Event.Boss("Black Dragon", 200) # Has the victory trophy by default

@pytest.fixture
def Goblin():
    return Event.Enemy("Goblin", 50, [], 10, 30)

@pytest.fixture
def Hero():
    return Event.Hero("Test Hero", 100, [])

@pytest.fixture
def Merchant():
    return Event.Merchant("Test Merchant", 150, [Event.Items.Long_Sword.name, Event.Items.Dragonslayer_Sword.name, Event.Items.Health_Potion.name], [50, 200, 10], 500)
# Merchant has mutable objects we use so we need to manually use the constructor in the fixture

@pytest.fixture
def Menu():
    with patch('builtins.input', side_effect=['hero','']):
        return UserMenu.UserMenu()

@pytest.fixture
def Tree():
    return RedBlackTree.RedBlackTree()

def test_lose_to_dragon(Hero, BlackDragon): # Test for if user fights the final boss without the necessary items
    assert BlackDragon.fight_hero(Hero) is False
    assert Hero.get_health() == 0

def test_win_to_dragon(Hero, BlackDragon): # Test for user beating game due to having the necessary items
    Hero.add_to_inventory(Event.Items.Black_Dragon_Eye.name)
    Hero.add_to_inventory(Event.Items.Dragonslayer_Sword.name)
    print(Hero.get_inventory())
    assert BlackDragon.fight_hero(Hero) is True
    assert Hero.get_inventory().count(Event.Items.Victory_Trophy.name) == 1

def test_hero_level_up(Hero): # Test for user leveling up and health incrementing by 10
    Hero.level_up()
    assert Hero.get_max_health() == 110

def test_enemy_drop_loot(Hero, Goblin): # Test for user getting gold from a a basic enemy
    Goblin.drop_loot(Hero)
    assert Hero.get_gold() == 10

def test_merchant_drop_loot(Hero, Merchant): # Test for user getting gold (and items) from defeating a merchant
    Merchant.drop_loot(Hero)
    assert Hero.get_gold() == 500
    assert Hero.get_inventory().count(Event.Items.Long_Sword.name) == 1
    assert Hero.get_inventory().count(Event.Items.Dragonslayer_Sword.name) == 1
    assert Hero.get_inventory().count(Event.Items.Health_Potion.name) == 1

def test_lose_to_goblin(Hero, Goblin): # Test for if user doesn't have enough health to defeat a goblin
    Hero.set_health(49)
    assert Goblin.fight_hero(Hero) is False
    assert Hero.get_health() == 19

def test_win_to_goblin(Hero, Goblin): # Test for if user does have enough health
    assert Goblin.fight_hero(Hero) is True
    assert Hero.get_gold() == 10
    assert Hero.get_health() == 70

def test_purchase_long_sword(Hero, Merchant): # Test for user buying a long sword
    with patch('builtins.input', side_effect=['0', '-1']): # Mock user input
        Hero.set_gold(50)
        Merchant.open_shop(Hero)
        assert Hero.get_gold() == 0

def test_purchase_and_drink_multiple_potions(Hero, Merchant): # Test for user buying multiple potions, and drinking them to increase health
    with patch('builtins.input', side_effect=['2', '2', '2', '2', '-1']): # Mock user input
        Hero.set_gold(40)
        Merchant.open_shop(Hero)
        assert Hero.get_gold() == 0
        assert Hero.get_inventory().count(Event.Items.Health_Potion.name) == 4
        assert Hero.drink_potion() == True
        assert Hero.drink_potion() == True
        assert Hero.drink_potion() == True
        Hero.set_health(90)
        assert Hero.get_health() == 90
        assert Hero.drink_potion() == True
        assert Hero.get_health() == 100

def test_level_up(Hero): # Test for user leveling up
    Hero.level_up()
    assert Hero.get_max_health() == 110

def test_insert_and_retrieve_event(Tree, Goblin): # Test for inserting events into the tree
    assert Tree.insert(Event.Event(0,'Enemy encounter (Goblin)', Goblin)) == True
    assert Tree.get_event(0).get_type() == Event.Enemy

def test_can_exit_menu(Menu): # Test for user exiting the menu
    with patch('builtins.input', side_effect=['0','2']): # Mock user input
        assert Menu.display_menu() == True

def test_can_play_event_(Menu, Hero): # Test for user playing an event
    with patch('builtins.input', side_effect=['1','1']): # Mock user input
        event = Event.Event(0,'Enemy encounter (Goblin)', Event.Enemy("Goblin", 50, [], 10, 30))
        assert Menu.play_event(event, Hero) == True # Hero should succeed with default stats
        Hero.set_health(0)
        assert Menu.play_event(event, Hero) == False # Hero should lose fight with 0 health