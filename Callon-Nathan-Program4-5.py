# Callon, Nathan, Program #5 Finished, Karla Fant, CS302, 3/18/2024
# For this program I made a game where the user's end goal is to slay a dragon, before the 40 day time limit is up and he destroys the world.
# The user rolls a number and encounters an event, which can be a merchant, enemy, or boss. This is how the user progresses, by successfully
# completing these events. The final boss requires both a Black Dragon Eye and Dragonslayer Sword to defeat, of which the Black Dragon Eye
# are dropped from baby dragons, and the Dragonslayer Sword is sold by the shopkeeper. The user's health increases ("leveling up") after
# defeating enemies. Resting takes energy and time which brings the world closer to an end but health potions can restore the user
# without taking any time. A recommended strategy would be to use health potions as much as possible rather than resting to conserve time,
# but also make sure to save up for the Dragonslayer Sword so you have it when the time comes.

import UserMenu

def main():

    menu = UserMenu.UserMenu()
    menu.display_menu()

    return 0

if __name__ == '__main__':
    main()