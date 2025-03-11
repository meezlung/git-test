# pyright: strict

from lab05e import MenuPlanning

def test_MenuPlanning():
    menu_planning = MenuPlanning(["Trio of Shiny Pearls", "Frozen Evergreen"])

    menu_planning.use_with_new(0, "Melted Essence")  # month 1
    menu_planning.use_with_new(0, "Jet Black Queen") # month 2
    menu_planning.use_with_new(2, "Twilight Ocean")  # month 3

    assert menu_planning.last_menu_item(0) == "Frozen Evergreen"

    menu_planning.use_without_last(3)                # month 4

    assert menu_planning.last_menu_item(4) == "Jet Black Queen"

    # TODO add more tests here
