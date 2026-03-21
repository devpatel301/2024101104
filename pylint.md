Iteration 1:

* Removed MACOSX folder
* Removed extra space from cards.py

Iteration 2:

* Few extra space removed from cards.py
* Added all missing docstrings

Iteration 3:

* Fixed all unnecessary import and unnecessary keyword/paren errors
* Removed all unused variables

Iteration 4:

* Changed == to is for singleton comparison in board.py to check if a property is mortgaged

Iteration 5:

* Fixed all final new line missing errors

Iteration 6:

* Grouped all the jail related instances into one in player.py
* Removed mortgage_vale and houses instances from property.py. Calculating mortgage when needed and houses is not needed there.
* Added the chance and community decks to board.py from game.py

Iteration 7:

* Removed f-string when not needed.

Iteration 8:

* Combined the "birthday" and "collect_from_all" card actions within _apply_card(). Since both cards performed the exact same logic, they could be grouped together with an in statement.
* Removed a redundant "if prop:"" check since title=="property" already ensures that prop is valid

Iteration 9:

* Initialized doubles_streak = 0 inside init in dice.py
* Specified the ValueError type in try-except in ui.py

Iteration 10:

1. In property.py, init now accepts costs grouping price and base rent
2. Updated the initialization list in board.py to pass these two identical values grouped in a tuple
