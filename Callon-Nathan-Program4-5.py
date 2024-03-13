import Event
import RedBlackTree

def main():

    tree = RedBlackTree.RedBlackTree()

    # tree.insert(Event.Event(1,'Enemy encounter (Goblin)'))
    # tree.insert(Event.Event(2,'Merchant encounter'))
    # tree.insert(Event.Event(3,'Enemy encounter (Goblin)'))
    # tree.insert(Event.Event(4,'Enemy encounter (Orc)'))
    # tree.insert(Event.Event(5,'Merchant encounter'))
    # tree.insert(Event.Event(6,'Enemy encounter (Goblin)'))
    # tree.insert(Event.Event(7,'Enemy encounter (Orc)'))
    # tree.insert(Event.Event(8,'Merchant encounter'))
    # tree.insert(Event.Event(9,'Enemy encounter (Harpy)'))
    # tree.insert(Event.Event(10,'Enemy encounter (Harpy)'))
    # tree.insert(Event.Event(11,'Enemy encounter (Baby Dragon)'))
    # tree.insert(Event.Event(12,'Merchant encounter'))
    # tree.insert(Event.Event(13,'Enemy encounter (Harpy)'))
    # tree.insert(Event.Event(14,'Merchant encounter'))
    # tree.insert(Event.Event(15,'Enemy encounter (Baby Dragon)'))
    # tree.insert(Event.Event(16,'Boss encounter (Dragon)'))

    # print(tree.get_event(1))
    # print(tree.get_event(13))
    # print(tree.get_event(6))
    # print(tree.get_event(1))

    merchant = Event.Merchant("Test Merchant")
    hero = Event.Hero("Test Hero")

    merchant.open_shop(hero)

    return 0

if __name__ == '__main__':
    main()

