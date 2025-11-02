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
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        #ranks = ['3']
        #ranks = ['A', '10']
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