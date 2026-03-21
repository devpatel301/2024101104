# Test Cases report

### `test_player_initialization`

**Why it is needed:** Validates that the Player initialization functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_player_dd_deduct_money`

**Why it is needed:** Validates that the Player add deduct money functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_player_move_passes_go`

**Why it is needed:** Validates that the Player move passes go functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** AssertionError: Player should receive GO_SALARY when passing Go

**Fix:** Changed condition from `self.position == 0` to `old_position + steps >= BOARD_SIZE` so Go salary is awarded when passing Go, not just landing on it

### `test_player_net_worth`

**Why it is needed:** Validates that the Player net worth functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** AssertionError: Net worth should include property values

**Fix:** Changed `return self.balance` to `return self.balance + sum(p.price for p in self.properties)` to include property values in net worth

### `test_player_go_to_jail`

**Why it is needed:** Verifies accurate deduction and turn-handling when jailed.

**Result:** `Passed`

### `test_dice_roll_values`

**Why it is needed:** Validates that the Dice roll values functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_dice_max_roll`

**Why it is needed:** Validates that the Dice max roll functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** AssertionError: Dice should be able to roll a 6 (faces 1-6)

**Fix:** Changed `random.randint(1, 5)` to `random.randint(1, 6)` for both dice to allow rolling a 6

### `test_dice_doubles`

**Why it is needed:** Validates that the Dice doubles functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_property_group_all_owned_by`

**Why it is needed:** Validates that the Property group all owned by functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** AssertionError: Should only be true if ALL properties are owned by player

**Fix:** Changed `any()` to `all()` in `all_owned_by` so group ownership requires owning every property, not just one

### `test_property_mortgage`

**Why it is needed:** Checks mortgage multipliers and nested active boolean state transitions.

**Result:** `Passed (Fixed)`

**Bug/Error:** assert mortgage_value == 100

**Fix:** Changed `return self.mortgage_value` to `return self.mortgage_value()` in `mortgage()` to call the method instead of returning the method object

### `test_property_rent`

**Why it is needed:** Validates that the Property rent functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** AssertionError: assert 20 == 10

**Fix:** Fixed by the `any()` to `all()` change in `all_owned_by`, which was incorrectly doubling rent when only one property in the group was owned

### `test_bank_transactions`

**Why it is needed:** Validates that the Bank transactions functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_bank_loans`

**Why it is needed:** Validates that the Bank loans functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** Assertion failure testing exact bank funds decrease, since Bank.give_loan failed to deduct the given loan amount from the bank's funds.

**Fix:** Added `self.pay_out(amount)` before `player.add_money()` in `give_loan` to ensure the bank's reserves correctly decrease by the loan amount constraint.

### `test_game_find_winner`

**Why it is needed:** Validates that the Game find winner functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** AssertionError: find_winner should return the player with the highest net worth

**Fix:** Changed `min()` to `max()` in `find_winner` so the player with the highest net worth is returned

### `test_game_buy_property_exact_balance`

**Why it is needed:** Validates that the Game buy property exact balance functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** AssertionError: Player should be able to buy property with exact balance

**Fix:** Changed `player.balance <= prop.price` to `player.balance < prop.price` so a player can buy when balance equals price exactly

### `test_game_pay_rent_transfers_money`

**Why it is needed:** Validates that the Game pay rent transfers money functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** AssertionError: Owner should receive the rent payment

**Fix:** Added `prop.owner.add_money(rent)` in `pay_rent` so the owner actually receives the rent amount

### `test_game_jail_fine`

**Why it is needed:** Verifies accurate deduction and turn-handling when jailed.

**Result:** `Passed (Fixed)`

**Bug/Error:** AttributeError: 'Player' object has no attribute 'jail_turns'

**Fix:** Changed `player.jail_turns` to `player.jail["turns"]` to access jail turns from the jail dict

### `test_game_bankruptcy`

**Why it is needed:** Ensures bankruptcy processing correctly handles nested player elimination paths and properties are released gracefully.

**Result:** `Passed`

### `test_game_apply_card`

**Why it is needed:** Validates that the Game apply card functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** AttributeError: 'Player' object has no attribute 'get_out_of_jail_cards'

**Fix:** Changed `player.get_out_of_jail_cards += 1` to `player.jail["cards"] += 1` to use the jail dict

### `test_get_player_names`

**Why it is needed:** Validates that the Get player names functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_main_success`

**Why it is needed:** Validates that the Main success functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_main_value_error`

**Why it is needed:** Validates that the Main value error functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_main_keyboard_interrupt`

**Why it is needed:** Validates that the Main keyboard interrupt functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_bank_methods`

**Why it is needed:** Validates that the Bank methods functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_bank_insufficient_funds`

**Why it is needed:** Validates that the Bank insufficient funds functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_board_repr`

**Why it is needed:** Validates that the Board repr functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_board_tile_types`

**Why it is needed:** Validates that the Board tile types functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_board_is_purchasable`

**Why it is needed:** Validates that the Board is purchasable functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_board_owned_and_unowned`

**Why it is needed:** Validates that the Board owned and unowned functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_card_deck_empty`

**Why it is needed:** Validates that the Card deck empty functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_card_deck_repr`

**Why it is needed:** Validates that the Card deck repr functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** ZeroDivisionError: integer division or modulo by zero when `CardDeck` runs `__repr__` with an empty deck.

**Fix:** Added an explicit return statement `if not self.cards: return "CardDeck(0 cards, next=0)"` into `CardDeck.__repr__` to handle the empty case without hitting modulo zero exception.

### `test_player_remove_property`

**Why it is needed:** Validates that the Player remove property functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_player_count_properties`

**Why it is needed:** Validates that the Player count properties functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_player_repr_and_status`

**Why it is needed:** Validates that the Player repr and status functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_player_bankrupt`

**Why it is needed:** Ensures bankruptcy processing correctly handles nested player elimination paths and properties are released gracefully.

**Result:** `Passed`

### `test_property_repr`

**Why it is needed:** Validates that the Property repr functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_property_group_repr`

**Why it is needed:** Validates that the Property group repr functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_property_group_get_owner_counts`

**Why it is needed:** Validates that the Property group get owner counts functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_property_unmortgage_error`

**Why it is needed:** Checks mortgage multipliers and nested active boolean state transitions.

**Result:** `Passed`

### `test_property_all_owned_by_none`

**Why it is needed:** Validates that the Property all owned by none functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_dice_repr`

**Why it is needed:** Validates that the Dice repr functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_ui_print_components`

**Why it is needed:** Intercepts deterministic raw standard inputs to secure game loop from malformed types.

**Result:** `Passed`

### `test_ui_safe_int_input`

**Why it is needed:** Intercepts deterministic raw standard inputs to secure game loop from malformed types.

**Result:** `Passed`

### `test_ui_safe_int_input_default`

**Why it is needed:** Intercepts deterministic raw standard inputs to secure game loop from malformed types.

**Result:** `Passed`

### `test_ui_confirm`

**Why it is needed:** Intercepts deterministic raw standard inputs to secure game loop from malformed types.

**Result:** `Passed`

### `test_game_handle_property_tile_buy`

**Why it is needed:** Validates that the Game handle property tile buy functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_handle_property_tile_mortgaged`

**Why it is needed:** Checks mortgage multipliers and nested active boolean state transitions.

**Result:** `Passed`

### `test_game_mortgage_menu`

**Why it is needed:** Checks mortgage multipliers and nested active boolean state transitions.

**Result:** `Passed (Fixed)`

**Bug/Error:** TypeError: '<' not supported between instances of 'method' and 'int'

**Fix:** Changed `self.mortgage_value` to `self.mortgage_value()` in mortgage and menu display so the method is called, not passed as object

### `test_game_unmortgage_menu`

**Why it is needed:** Checks mortgage multipliers and nested active boolean state transitions.

**Result:** `Passed (Fixed)`

**Bug/Error:** TypeError: unsupported operand type(s) for *: 'method' and 'float'

**Fix:** Changed `prop.mortgage_value * 1.1` to `prop.mortgage_value() * 1.1` in `_menu_unmortgage` to call the method

### `test_game_tax_tiles`

**Why it is needed:** Validates that the Game tax tiles functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_special_tiles`

**Why it is needed:** Validates that the Game special tiles functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_trade_menu_decline`

**Why it is needed:** Ensures property exchanges correctly validate ownership and fund transfers.

**Result:** `Passed`

### `test_game_play_turn_basic`

**Why it is needed:** Validates that the Game play turn basic functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** AttributeError: 'Player' object has no attribute 'in_jail'

**Fix:** Changed `player.in_jail` to `player.jail["in_jail"]` in `play_turn` to access jail status from the dict

### `test_game_jail_no_action`

**Why it is needed:** Verifies accurate deduction and turn-handling when jailed.

**Result:** `Passed (Fixed)`

**Bug/Error:** AttributeError: 'Player' object has no attribute 'jail_turns'

**Fix:** Changed `player.jail_turns` to `player.jail["turns"]` in `_handle_jail_turn` to use correct dict access

### `test_game_apply_card_other`

**Why it is needed:** Validates that the Game apply card other functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_interactive_limit`

**Why it is needed:** Validates that the Game interactive limit functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_run_loop_winner`

**Why it is needed:** Validates that the Game run loop winner functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_current_player`

**Why it is needed:** Validates that the Game current player functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_auction`

**Why it is needed:** Validates that the Game auction functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_mortgage_fail`

**Why it is needed:** Checks mortgage multipliers and nested active boolean state transitions.

**Result:** `Passed`

### `test_trade_fail`

**Why it is needed:** Ensures property exchanges correctly validate ownership and fund transfers.

**Result:** `Passed`

### `test_bank_edge_cases`

**Why it is needed:** Validates that the Bank edge cases functionality operates securely without boundary violations.

**Result:** `Passed (Fixed)`

**Bug/Error:** Bank balance unexpectedly dropping when `Bank.collect` is supplied with a negative amount instead of silently ignoring it.

**Fix:** Added a preventative condition `if amount < 0: return` to the beginning of the `collect` method to respect the docstring bounds.

### `test_property_add_existing`

**Why it is needed:** Validates that the Property add existing functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_ui_player_card_full`

**Why it is needed:** Intercepts deterministic raw standard inputs to secure game loop from malformed types.

**Result:** `Passed`

### `test_cards_remaining_methods`

**Why it is needed:** Validates that the Cards remaining methods functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_cards_empty`

**Why it is needed:** Validates that the Cards empty functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_property_add_not_existing`

**Why it is needed:** Validates that the Property add not existing functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_cards_reshuffle`

**Why it is needed:** Validates that the Cards reshuffle functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_main_cli`

**Why it is needed:** Validates that the Main cli functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_property_auction_branch`

**Why it is needed:** Validates that the Game property auction branch functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_bankruptcy_branches`

**Why it is needed:** Ensures bankruptcy processing correctly handles nested player elimination paths and properties are released gracefully.

**Result:** `Passed (Fixed)`

**Bug/Error:** AttributeError: 'Player' object has no attribute 'in_jail'

**Fix:** Same as `test_game_play_turn_basic`, changed `player.in_jail` to `player.jail["in_jail"]` in `play_turn`

### `test_game_pay_rent_bankrupt`

**Why it is needed:** Ensures bankruptcy processing correctly handles nested player elimination paths and properties are released gracefully.

**Result:** `Passed`

### `test_game_interactive_menus`

**Why it is needed:** Validates that the Game interactive menus functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_trade_fully`

**Why it is needed:** Ensures property exchanges correctly validate ownership and fund transfers.

**Result:** `Passed`

### `test_game_trade_logic`

**Why it is needed:** Ensures property exchanges correctly validate ownership and fund transfers.

**Result:** `Passed (Fixed)`

**Bug/Error:** AssertionError: assert 1500 == (1500 + 10)

**Fix:** Added `seller.add_money(cash_amount)` in `trade` method so the seller receives the cash from the buyer

### `test_game_move_and_resolve_branches`

**Why it is needed:** Validates that the Game move and resolve branches functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_fuzz_game_loops`

**Why it is needed:** Validates that the Fuzz game loops functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_pay_rent_unowned`

**Why it is needed:** Validates that the Pay rent unowned functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_mortgage_already_mortgaged`

**Why it is needed:** Checks mortgage multipliers and nested active boolean state transitions.

**Result:** `Passed`

### `test_unmortgage_not_mortgaged`

**Why it is needed:** Checks mortgage multipliers and nested active boolean state transitions.

**Result:** `Passed`

### `test_unmortgage_cannot_afford`

**Why it is needed:** Checks mortgage multipliers and nested active boolean state transitions.

**Result:** `Passed (Fixed)`

**Bug/Error:** TypeError: unsupported operand type(s) for *: 'method' and 'float'

**Fix:** Changed `self.mortgage_value * 1.1` to `self.mortgage_value() * 1.1` in `unmortgage` to call the method

### `test_find_winner_empty_players`

**Why it is needed:** Validates that the Find winner empty players functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_interactive_menu_invalid`

**Why it is needed:** Validates that the Interactive menu invalid functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_menu_trade_player_selection`

**Why it is needed:** Ensures property exchanges correctly validate ownership and fund transfers.

**Result:** `Passed`

### `test_main_coverage`

**Why it is needed:** Validates that the Main coverage functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_run_empty`

**Why it is needed:** Validates that the Game run empty functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_move_railroad`

**Why it is needed:** Validates that the Game move railroad functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_interactive_all_menu_branches`

**Why it is needed:** Validates that the Game interactive all menu branches functionality operates securely without boundary violations.

**Result:** `Passed`

### `test_game_menu_trade_empty_props`

**Why it is needed:** Ensures property exchanges correctly validate ownership and fund transfers.

**Result:** `Passed`
