from bj import Game, PlayerHand, DealerHand, Deck, Card
class ConsoleGame:

    def console_play(balance = 1000):
        deck = Deck(num_decks=8)
        deck.shuffle()
        # Game loop
        while True:
            # Create a new game from the deck
            bet = -1
            while bet < 0:
                try:
                    print("Current Balance:", balance)
                    bet = int(input("Enter bet: ").strip().lower())
                    if(bet < 0):
                        print("Bet must be non-negative. Try again.")
                    if bet > balance:
                        print("Insufficient balance. Try again.")
                        bet = -1
                except ValueError:
                    print("Invalid input. Please enter a valid bet amount.")
                    continue
                
            game = deck.new_game()
            
            # Play the round
            round_result = ConsoleGame.played_hand(game, bet, balance)
            if round_result[0] == 'W' or round_result[0] == 'W!' :
                print("Round Result: Win")
            elif round_result[0] == 'L' :
                print("Round Result: Loss")
            elif round_result[0] == 'P' :
                print("Round Result: Push")
            elif round_result.__len__() >1 and isinstance(round_result, list):
                print("Round Result: Split Hands")
                print("Hands Results:")
                for res in round_result:
                    if res[0] == 'W' or res[0] == 'W!' :
                        print("Win")
                    elif res[0] == 'L' :
                        print("Loss")
                    elif res[0] == 'P' :
                        print("Push")
                
            print("Profit/Loss:", Game.interpret_result(round_result))
            balance += Game.interpret_result(round_result)
            # Clean up the game
            game.end_game()
            
            # Check if deck needs reshuffling (e.g., if less than 25% of cards remain)
            if len(deck.cards) < (52 * 8 * 0.25):  # Less than 25% of cards remain
                print("Reshuffling deck...")
                deck = Deck(num_decks=8)
                deck.shuffle()


    def played_hand_split(game, bet_amount, split_hand=None, handnum=0, balance=0):
        """
        Play ONLY the player's actions for a single split hand and return (final_hand, bet_amount).
        No dealer logic here. Robust to different deal_split implementations.
        """
        # Determine target index robustly
        target_idx = handnum
        if split_hand is not None:
            pre_len = len(game.player_hands)
            game.deal_split(split_hand)
            post_len = len(game.player_hands)

            if post_len > pre_len:
                # A new hand was appended; play that new hand
                target_idx = post_len - 1
            else:
                # No new hand created. Constrain to valid index.
                target_idx = min(handnum, post_len - 1)

        # Constrain index again for safety
        if not game.player_hands:
            raise RuntimeError("No player hands available after split.")
        target_idx = max(0, min(target_idx, len(game.player_hands) - 1))

        hand = game.player_hands[target_idx]

        while not hand.is_busted():
            # Auto-stop at 21
            if hand.get_value() == 21:
                break

            # Display current hand state
            if hand.has_soft_ace():
                msg = f"{hand.get_value() - 10}, {hand.get_value()}"
            else:
                msg = f"{hand.get_value()}"
            print("Player's Hand:", hand.get_cards(), "\nValue:", msg)

            # Prompt for action
            print("Choose your Action")
            print("h: Hit")
            print("s: Stand")
            if hand.num_cards() == 2:
                print("d: Double Down")
            action = input().strip().lower()

            if action == 'h':
                game.player_hit(handnum=target_idx)
                hand = game.player_hands[target_idx]
                if hand.is_busted():
                    break
                continue

            elif action == 's':
                break

            elif action == 'd' and hand.num_cards() == 2 and balance >= bet_amount:
                game.player_hit(handnum=target_idx)
                bet_amount *= 2
                hand = game.player_hands[target_idx]
                # After a double, stand automatically
                break

            else:
                print("Invalid action.")

        return (game.player_hands[target_idx], bet_amount)



    def played_hand(game, bet_amount, balance):
        """
        Main hand flow. Uses game.player_hands as a list where the first hand is index 0.
        """
        # Initialize a fresh hand slot before dealing
        game.new_hand()

        dealer_hand = game.dealer_hand
        game.deal_initial()
        player_hand = game.player_hands[0]

        while not player_hand.is_busted():
            print("Dealer's Hand:", dealer_hand.get_card_shown())
            if player_hand.has_soft_ace():
                msg = f"{player_hand.get_value() - 10}, {player_hand.get_value()}"
            else:
                msg = f"{player_hand.get_value()}"
            print("Player's Hand:", player_hand.get_cards(), "\nValue:", msg)
            if player_hand.blackjack():
                dealer_hand.show_cards()
                if dealer_hand.blackjack():
                    print("Push!")
                    return ("P", bet_amount)
                print("Blackjack! You win!")
                return ("W!", bet_amount)

            if dealer_hand.blackjack():
                print("Dealer has Blackjack! You lose!")
                dealer_hand.show_cards()
                return ("L", bet_amount)

            if player_hand.get_value() == 21:
                print("21: no more action")
                action = 's'
            else:
                print("Choose your Action")
                print("h: Hit")
                print("s: Stand")
                if player_hand.num_cards() == 2:
                    print("d: Double Down")
                if player_hand.can_split():
                    print("v: Split")
                action = input().strip().lower()

            if action == 'h':
                game.player_hit(handnum=0)
                player_hand = game.player_hands[0]
                if player_hand.is_busted():
                    print("Player busted!")
                    dealer_hand.show_cards()
                    return ("L", bet_amount)
                continue

            elif action == 's':
                game.dealer_play(Auto=False)
                dealer_hand.show_cards()
                result = game.get_winner(0)
                print(result)
                return (result, bet_amount)

            elif action == 'd' and player_hand.num_cards() == 2 and balance >= bet_amount:
                bet_amount *= 2
                game.player_hit(handnum=0)
                player_hand = game.player_hands[0]
                if player_hand.is_busted():
                    print("Player busted after doubling down!")
                    dealer_hand.show_cards()
                    return ("L", bet_amount)
                game.dealer_play(Auto=False)
                dealer_hand.show_cards()
                result = game.get_winner(0)
                print(result)
                return (result, bet_amount)

            elif action == 'v' and player_hand.can_split() and balance >= bet_amount:
                print("splitting")

                # Capture the two seed cards before split mutates the hand
                seed_left = player_hand.cards[0]
                seed_right = player_hand.cards[1]
                game.new_hand()
                # Play both split hands
                print("1st split hand:")
                h1, b1 = ConsoleGame.played_hand_split(game, bet_amount, split_hand=seed_left, handnum=0, balance=balance-bet_amount)

                print("2nd split hand:")
                h2, b2 = ConsoleGame.played_hand_split(game, bet_amount, split_hand=seed_right, handnum=1, balance=balance-bet_amount)

                # Dealer plays once for both hands
                game.dealer_play(Auto=False)
                dealer_hand.show_cards()

                # Score each hand independently
                game.player_hands[0] = h1
                game.player_hands[1] = h2
                r1 = game.get_winner(0)
                r2 = game.get_winner(1)
                print(r1)
                print(r2)
                return [(r1, b1), (r2, b2)]

            else:
                print("Invalid action.")

        return ("E", bet_amount)
