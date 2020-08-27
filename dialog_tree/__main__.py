import sys

import game

print("Starting application...")

args = sys.argv[1:]

dialog_filename = args[0] if args else None
game.start(dialog_filename)
