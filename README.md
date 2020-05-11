# Jackie - Card Game
## Game Desciption:
This project is a Tamil card game colloquially called as 'Jackie'. It is a variation of
the relatively more popular '28' game from Kerala. I was unable to find solid literature 
on the origin and rfules of the game. So a few rules have been programmed as per 
popular consensus.

## Language:
    This project is programmed using python. Tkinter framework is used for frontend.

## Rules:
    - Each game consists of two teams.
    - All players are seated/placed in a circle and every alternate player belong to the same team
    - The game is usually played with 4, 6 or 8 player
    - The game is palyed with the cards J, K, Q, A, 9, 10 from all four suits
    - Heirarchy of the cards: J > 9 > A > 10 > K > Q
    - Points for each card - J=3 pts, 9=2 pts, A=1 pts, 10=1 pts, K=0 pts, Q=0 pts
    - After the cards are dealt, the starting player can set wager
    - The starting player has a mandatory base wager
    - Subsequent players can raise the wager
    - The highest bid is taken for the round
    - The player who sets the highest wager can select a trump suit that is superior over
      other suits
    - The trump suit is not revealed at the start of the game
    - Setting a bid of 15 to 19 gives 1 point on victory and -2 points on defeat
    - Setting a bid of 20 to 28 gives 2 points on victory and -3 points on defeat
    - The cards are dealt to a starting player with scores at nil, nil
    - The start player has to play card
    - The other players have to play a card in the same suit
    - The player who plays the highest card in the lot secures all the cards for teams
    - The points gained is equal to the summation of the points of the cards in the lot
    - If a player doesn't have a suit, he can request the trump suit to be revealed and can use
      a trump card to capture the lot
    - A trump card is superior to any card of other suits
    - A trump suit card of higher precedence is, as usual, superior to a trump suit card of lower order
    - The player who captures the round plays the first card of the next round
    - The team wins by getting the at least as much points as made in the bid

## Additional/Pending Functionality:
    1. Give choice to ask the wager team if they want to declare a win or go for a goat
    2. Set aside a card as trump until trump is opened
