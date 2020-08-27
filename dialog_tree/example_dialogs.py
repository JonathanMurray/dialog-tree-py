from dialog_graph import DialogGraph, DialogNode, DialogChoice

DRAGON_BALL_DIALOG = DialogGraph(
    "START",
    [DialogNode("START", "Hey you! I have a task for you!", "son_goku",
                [DialogChoice("Ok.", "BRIEFING_1"), DialogChoice("No way!", "REJECTED_ONCE")]),
     DialogNode("REJECTED_ONCE", "What!? You dare stand up to me?", "son_goku_surprised",
                [DialogChoice("Well... ok then!", "BRIEFING_1"),
                 DialogChoice("I said no way!", "REJECTED_TWICE")]),
     DialogNode("REJECTED_TWICE", "As you wish! You will feel the consequences of my wrath!", "son_goku_mad",
                [DialogChoice("START OVER", "START")]),
     DialogNode("BRIEFING_1", "You know what? Nevermind.", "son_goku",
                [DialogChoice("START OVER", "START")]),
     DialogNode("BRIEFING_2", "We'll enter the room on my count.", "son_goku",
                [DialogChoice("Finish game.", "END")]),
     DialogNode("END", "[GAME OVER]", "son_goku", [])
     ])
