<h1> Welcome to Blackjack simulator!</h1>

<h2>Abstract</h2>
This is a passion project based on my love for statistics and gambling. This project once finished will allow the user to create betting strategies and run any number of blackjack hands and recieve a visual representation in the form of a graph or otherwise of how thier strategy performed over time.  
Included in this will be multiple strategy charts that the program will read from based on the "True Count" of the deck, and yes this simulator will account for card counting to allow users to practice and tweak their card counting strategies.
Currently I am working on transitioning the project from a console program to an application with a UI.

This project demonstrates knowledge of object oriented programming, python, working with lots of data, data visualization, etc.

<h2>Blackjack Rules</h2>
Blackjack pays 3:2 <br>
One split allowed <br>
Double allowed on any 2 cards <br>
Double allowed after split <br>
Dealer stands on soft 17 <br>
Deck amount: 8 <br>
Play after split aces allowed but not a resplit <br>
Surrender not allowed <br>
Insurance not allowed (because it's a sucker's bet) <br>

<h2>How To Run</h2>
Install files <br>
cd to BlackJack-Sim <br>
python ./main.py <br>

<h2>Creation process of Blackjack Sim</h2>
<h3>✅Create a fully functional blackjack console program</h3>
1. Create card and deck logic <br>
2. Create dealer and player hand logic <br>
3. Introduce a game loop <br>
4. Add functionality for splitting with recursive logic <br>
<h3>✅Enable Automatic Betting System</h3>
1. enable automatic playing and writing to output file with no strategy (hit until 17) <br>
2. add reading strategy from excel file and choosing action based on basic strategy <br>
3. add customization of number of hands, bet size, starting balance <br>
4. Optimize program from ~1180 hands per minute (stopwatch timed, too slow) and abstract repeated code <br>
<h3>Modify Automatic Betting System to count cards and change strategy chart based on Count</h3>
1. Read from specific file name based on the card count ✅
2. modify the blackjack engine to count cards during play and return the card count for the next hand
3. change the strategies to reflect optimal play for card count
<h3>Convert the Console Program to an application window, giving it a UI</h3>
<h3>Allow for changing of blackjack Rules</h3>
<h3>Add more customization: changing strategies, bet sizes, number of hands, etc</h3>
<h3>Create a website / Web app to make this publicly accessible</h3>
