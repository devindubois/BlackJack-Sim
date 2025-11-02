from bj import Game, PlayerHand, DealerHand, Deck, Card
class AutoGame:
    def auto_play_loop(bet_amount=1, num_games=100, balance=1000):
        deck = Deck(num_decks=8)
        deck.shuffle()
        total_profit = 0
        open('results.txt', 'w').close()  # Clear results file at start
        for _ in range(num_games):
            game = deck.new_game()
            round_result = AutoGame.auto_played_hand(game, bet_amount)
            profit = Game.interpret_result(round_result)
            total_profit += profit
            with open('results.txt', 'a') as f:
                f.write(f"{total_profit} ,")
            game.end_game()
            if len(deck.cards) < (52 * 8 * 0.25):  # Less than 25% of cards remain
                    print("Reshuffling deck...")
                    deck = Deck(num_decks=8)
                    deck.shuffle()

    def auto_played_hand(game, bet_amount=0, split_card=None):
        player_hand = game.player_hand
        dealer_hand = game.dealer_hand
        if split_card:
            game.player_hand.clear()
            game.deal_split(split_card)
        else:
            game.deal_initial()
        

        while player_hand.is_busted() == False:
            print("Dealer's Hand:", dealer_hand.get_card_shown())
            print("Player's Hand:", player_hand.get_cards(), "\n Value:", player_hand.get_value())
            
            if player_hand.blackjack():
                if split_card:
                    print("21: no more action")
                    game.dealer_play()
                    dealer_hand.show_cards()
                    return ("W!", bet_amount)
                print("Blackjack!")
                dealer_hand.show_cards()
                if(dealer_hand.blackjack()):
                    print("Push!")
                    dealer_hand.show_cards()
                    return ("P", bet_amount)
                else:
                    print("Blackjack! You win!")
                    dealer_hand.show_cards()
                    return ("W!", bet_amount*1.5)
            if(dealer_hand.blackjack()):
                print("Dealer has Blackjack! You lose!")
                dealer_hand.show_cards()
                return ("L", bet_amount)
            print("action: auto-play hit until 17 or more")
            if player_hand.get_value() < 21:
                action = 'h'
            else:
                action = 's'

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
                results.append(AutoGame.auto_played_hand(game, bet_amount, split_card=player_hand.cards[0])) # Recursive split
                print("2nd split hand:")
                results.append(AutoGame.auto_played_hand(game, bet_amount, split_card=player_hand.cards[1]))
                return results
            else:
                print("Invalid action.")
        return ("E", bet_amount)  # Default return if loop exits unexpectedly E for Error

