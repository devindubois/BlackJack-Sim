
def console_play():
    deck = Deck(num_decks=8)
    deck.shuffle()
    balance = 1000
    # Game loop
    while True:
        # Create a new game from the deck
        bet = -1
        while bet < 0:
            try:
                print("Current Balance:", balance)
                bet = int(input("Enter bet: ").strip().lower())
                if bet > balance:
                    print("Insufficient balance. Try again.")
                    bet = -1
            except ValueError:
                print("Invalid input. Please enter a valid bet amount.")
                continue
            print("Invalid input. Please enter a valid bet amount.")
        game = deck.new_game()
        
        # Play the round
        round_result = played_hand(game, bet)
        print("Round Result:", round_result)
        print("Profit/Loss:", interpret_result(round_result))
        # Clean up the game
        game.end_game()
        
        # Check if deck needs reshuffling (e.g., if less than 25% of cards remain)
        if len(deck.cards) < (52 * 8 * 0.25):  # Less than 25% of cards remain
            print("Reshuffling deck...")
            deck = Deck(num_decks=8)
            deck.shuffle()


def played_hand(game, bet_amount=0, split_card=None):
    player_hand = game.player_hand
    dealer_hand = game.dealer_hand
    if split_card:
        game.player_hand.clear()
        game.deal_split(split_card)
    else:
        game.deal_initial()
    

    while player_hand.is_busted() == False:
        print("Dealer's Hand:", dealer_hand.get_cards())
        print("Player's Hand:", player_hand.get_cards(), "\n Value:", player_hand.get_value())
        if player_hand.blackjack():
            if split_card:
                print("21: no more action")
                game.dealer_play()
                dealer_hand.show_cards()
                return ("W", bet_amount)
            print("Blackjack!")
            dealer_hand.show_cards()
            if(dealer_hand.blackjack()):
                print("Push!")
                dealer_hand.show_cards()
                return ("P", bet_amount)
            else:
                print("Blackjack! You win!")
                dealer_hand.show_cards()
                return ("W!", bet_amount)
        if(dealer_hand.blackjack()):
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
            game.player_hit()
            if game.player_hand.is_busted():
                print("Player busted!")
                dealer_hand.show_cards()
                return ("L", bet_amount)
            else:
                continue
        elif action == 's':
            # Dealer plays and determine winner
            game.dealer_play()
            dealer_hand.show_cards()
            print(game.get_winner())
            return (game.get_winner(), bet_amount)
        elif action == 'd' and player_hand.num_cards() == 2:
            bet_amount *= 2
            game.player_hit()
            if game.player_hand.is_busted():
                print("Player busted after doubling down!")
                dealer_hand.show_cards()
                return ("L", bet_amount)
            else:
                game.dealer_play()
                dealer_hand.show_cards()
                print(game.get_winner())
            return (game.get_winner(), bet_amount)
        elif action == 'v' and player_hand.can_split():
            print("splitting") 
            results = []
            print("1st split hand:")
            results.append(played_hand(game, bet_amount, split_card=player_hand.cards[0])) # Recursive split
            print("2nd split hand:")
            results.append(played_hand(game, bet_amount, split_card=player_hand.cards[1]))
            return results
        else:
            print("Invalid action.")
    return ("E", bet_amount)  # Default return if loop exits unexpectedly E for Error
