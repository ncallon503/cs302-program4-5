# Nathan Callon, CS302, 3/10/2024 Test Suite Draft

import pytest
import Event
import UserMenu

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
    return Event.Merchant("Test Merchant")

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

def test_lose_to_goblin(Hero, Goblin): # Test for if user doesn't have enough health to defeat a goblin
    Hero.set_health(49)
    assert Goblin.fight_hero(Hero) is False
    assert Hero.get_health() == 19

def test_win_to_goblin(Hero, Goblin): # Test for if user does have enough health
    assert Goblin.fight_hero(Hero) is True
    assert Hero.get_gold() == 10
    assert Hero.get_health() == 70