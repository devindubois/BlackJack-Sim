class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Initially consider Ace as 11
        else:
            return int(self.rank)
class Deck:
    def __init__(self, num_decks=1):
        self.cards = []
        self.games = []  # List to track all active games
        suits = ["♤", "♡", "♧", "♢"]
        # ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        ranks = ['3']
        for i in range(num_decks):
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(rank, suit))
    
    def shuffle(self):
        import random
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop() if self.cards else None
        
    def new_game(self):
        """Create a new game and add it to the deck's games"""
        game = Game(self)
        self.games.append(game)
        return game
        
    def remove_game(self, game):
        """Remove a completed game from the deck's games"""
        if game in self.games:
            self.games.remove(game)
class Game:
    def __init__(self, deck):
        self.deck = deck  # Store reference to the parent deck
        self.player_hand = PlayerHand()
        self.dealer_hand = DealerHand()
        
    def deal_initial(self, split_card=None, dealer_card=None):
        for _ in range(2):
            self.player_hand.draw_card(self.deck.deal_card())
            self.dealer_hand.draw_card(self.deck.deal_card())
            
    def deal_split(self, split_card):
        self.player_hand.clear()
        self.player_hand.draw_card(split_card)
        self.player_hand.draw_card(self.deck.deal_card())
        
    def player_hit(self):
        self.player_hand.draw_card(self.deck.deal_card())
    
    def dealer_play(self):
        while self.dealer_hand.should_hit():
            self.dealer_hand.draw_card(self.deck.deal_card())
            print(self.dealer_hand.get_cards(), " ", self.dealer_hand.get_value())
            
    def end_game(self):
        """Clean up the game when it's done"""
        self.deck.remove_game(self)
    
    def get_winner(self):
        if self.player_hand.is_busted():
            return "L"
        elif self.dealer_hand.is_busted():
            return "W"
        elif self.player_hand.get_value() > self.dealer_hand.get_value():
            return "W"
        elif self.player_hand.get_value() < self.dealer_hand.get_value():
            return "L"
        else:
            return "P"
class PlayerHand:
    def __init__(self):
        self.cards = []
    def clear(self):
        self.cards = []
    def draw_card(self, card):
        self.cards.append(card)
    def num_cards(self):
        # Return the number of cards in the hand
        return len(self.cards)
    def get_cards(self):
        output = ""
        for card in self.cards:
            output += f"{card.rank} of {card.suit} "
        return output.strip()
    def show_cards(self):
        print(self.get_cards())
    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank
    def get_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            value += card.get_value()
            if card.rank == 'A':
                aces += 1
        
        while value > 21 and aces:
            value -= 10
            aces -= 1
        
        return value
    
    def blackjack(self):
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_busted(self):
        return self.get_value() > 21  
    
class DealerHand(PlayerHand):
    def should_hit(self):
        return self.get_value() < 17
    def get_cards(self):
        output = f"{self.cards[0].rank} of {self.cards[0].suit}"
        return output
    def get_value(self):
        if len(self.cards) == 2:
            return self.cards[0].get_value() + 10  # Hide one card value
        return super().get_value()
    

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

def interpret_result(result):
    """Returns net profit/loss from any result structure"""
    if isinstance(result, tuple):
        outcome, bet = result
        return bet*1.5 if outcome == 'W!' else bet if outcome == 'W' else -bet if outcome == 'L' else 0
    return sum(interpret_result(r) for r in result) if isinstance(result, list) else 0

def auto_play_loop(bet_amount=1, num_games=100, balance=1000):
    deck = Deck(num_decks=8)
    deck.shuffle()
    total_profit = 0
    for _ in range(num_games):
        game = deck.new_game()
        round_result = played_hand(game, bet_amount)
        profit = interpret_result(round_result)
        total_profit += profit
        with open('results.txt', 'w') as f:
            f.write(f"{total_profit}\n")
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
        print("Dealer's Hand:", dealer_hand.get_cards())
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
        if player_hand.get_value() < 17:
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
            results.append(auto_played_hand(game, bet_amount, split_card=player_hand.cards[0])) # Recursive split
            print("2nd split hand:")
            results.append(auto_played_hand(game, bet_amount, split_card=player_hand.cards[1]))
            return results
        else:
            print("Invalid action.")
    return ("E", bet_amount)  # Default return if loop exits unexpectedly E for Error


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
        if round_result[0] == 'W' or round_result[0] == 'W!' :
            print("Round Result: Win")
        elif round_result[0] == 'L' :
            print("Round Result: Loss")
        elif round_result[0] == 'P' :
            print("Round Result: Push")
        else:
            print("Round Result: Undefined Error")
        print("Profit/Loss:", interpret_result(round_result))
        balance += interpret_result(round_result)
        # Clean up the game
        game.end_game()
        
        # Check if deck needs reshuffling (e.g., if less than 25% of cards remain)
        if len(deck.cards) < (52 * 8 * 0.25):  # Less than 25% of cards remain
            print("Reshuffling deck...")
            deck = Deck(num_decks=8)
            deck.shuffle()

def main():
    # Initialize the deck
    print("Welcome to Blackjack!")
    mode = input("Choose mode: (1) Console Play (2) Auto Play\n").strip()
    if mode == '1':
        console_play()
    elif mode == '2':
        if False:
            num_games = int(input("Enter number of games to play: ").strip())
            balance = int(input("Enter starting balance: ").strip())
            bet_amount = int(input("Enter bet amount per game: ").strip())
        else:
            num_games = 100
            balance = 1000
            bet_amount = 10
        auto_play_loop(num_games=num_games, balance=balance, bet_amount=bet_amount)
    else:
        print("Invalid mode selected.")

if __name__ == '__main__':
    main()