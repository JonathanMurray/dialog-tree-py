import time

from graph import DialogGraph, DialogNode, DialogChoice
from text_util import layout_text_in_area


def main():
    dialog_graph = DialogGraph(
        root_node_id="START",
        nodes=[
            DialogNode(
                node_id="START",
                text="You are in a dimly lit room. There are two doors leading out of the room, one to the west and "
                     "another one to the east.",
                choices=[DialogChoice("Exit west", "WEST"),
                         DialogChoice("Exit east", "EAST")]),
            DialogNode(
                node_id="WEST",
                text="You are in a library. There seems to be nothing here of interest.",
                choices=[DialogChoice("Leave the library", "START")]),
            DialogNode(
                node_id="EAST",
                text="You are in a narrow and straight corridor. On the east end of it, there's a hole in the floor!",
                choices=[DialogChoice("Leave corridor to the west", "START"),
                         DialogChoice("Jump down in the hole", "BASEMENT")]),
            DialogNode(
                node_id="BASEMENT",
                text="You hurt yourself quite badly in the fall, and find yourself in a dark cellar. You can't see "
                     "anything.",
                choices=[DialogChoice("Sit down and wait for better days", "SUNLIGHT"),
                         DialogChoice("Feel your way through the room", "SPEAR")]),
            DialogNode(
                node_id="SUNLIGHT",
                text="Eventually the room gets brighter. The sun is shining in through a window and you can see a "
                     "door at the other end of the cellar leading to the outside. The walls are full of mounted spears "
                     "and other nasty things, and you think to yourself that it was a good thing you didn't try to "
                     "navigate here in the dark.",
                choices=[DialogChoice("Leave through the door", "VICTORY")]),
            DialogNode(
                node_id="SPEAR",
                text="You accidentally walk into spear that's mounted to the wall. You are dead.",
                choices=[DialogChoice("Retry", "START"),
                         DialogChoice("Exit game", "EXIT")]),
            DialogNode(
                node_id="VICTORY",
                text="Hooray, you escaped!",
                choices=[DialogChoice("Start from beginning", "START"),
                         DialogChoice("Exit game", "EXIT")]),
            DialogNode(
                node_id="EXIT",
                text="",
                choices=[]),
        ],
    )

    while True:
        node = dialog_graph.current_node()

        if node.node_id == "EXIT":
            break

        print("")
        print_in_box(node.text, 50)
        print("")

        time.sleep(0.5)

        print("Select one of these choices:")
        for i, choice in enumerate(node.choices):
            time.sleep(0.15)
            print(f"{i} : {choice.text}")

        choice = -1
        valid_choices = range(len(node.choices))
        while choice not in valid_choices:
            text_input = input("> ")
            try:
                choice = int(text_input)
                if choice not in valid_choices:
                    print("Invalid choice. Select one of the listed numbers!")
            except ValueError:
                print("Invalid input. Type a number!")

        print(f"\"{node.choices[choice].text.upper()}\"")
        time.sleep(0.5)

        dialog_graph.make_choice(choice)


def print_in_box(text: str, line_width):
    lines = layout_text_in_area(text, len, line_width)
    print("+" + "-" * (line_width + 2) + "+")
    for line in lines:
        time.sleep(0.03)
        print("| " + line.ljust(line_width + 1, " ") + "|")
    time.sleep(0.03)
    print("+" + "-" * (line_width + 2) + "+")


if __name__ == '__main__':
    main()
