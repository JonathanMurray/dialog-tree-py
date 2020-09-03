#!/usr/bin/env bash

directory=$(dirname $0)

python3 dialog_tree/runners/dialog_app.py "$directory/dragonball.json" \
--sound_dir "$directory/data" \
--image_dir "$directory/data"