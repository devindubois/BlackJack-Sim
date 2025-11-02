from console import ConsoleGame
from auto import AutoGame
from bj import Game, PlayerHand, DealerHand, Deck, Card

def main():
    # Initialize the deck
    print("Welcome to Blackjack!")
    mode = input("Choose mode: (1) Console Play (2) Auto Play\n").strip()
    if mode == '1':
        ConsoleGame.console_play()
    elif mode == '2':
        if False:
            num_games = int(input("Enter number of games to play: ").strip())
            balance = int(input("Enter starting balance: ").strip())
            bet_amount = int(input("Enter bet amount per game: ").strip())
        else:
            num_games = 100
            balance = 1000
            bet_amount = 10
            print(f"Auto-playing {num_games} games with starting balance {balance} and bet amount {bet_amount} per game.")
        AutoGame.auto_play_loop(num_games=num_games, balance=balance, bet_amount=bet_amount)
    else:
        print("Invalid mode selected.")

if __name__ == '__main__':
    main()