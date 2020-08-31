import sys

import dialog_app

print("Starting application...")

args = sys.argv[1:]

dialog_filepath = args[0] if args else None
dialog_app.start(dialog_filepath)
