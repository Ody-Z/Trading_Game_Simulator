# Market Making Trading Games

A interactive trading platform that simulates market making across different games of chance, allowing users to place bets and trade positions with varying odds and conditions.

## Project Structure
market_maker/
├── main.py              # Entry point and application initialization
├── games/               # Game implementations
│   ├── __init__.py
│   ├── game.py         # Base abstract class for all games
│   ├── dice.py         # Dice game implementation
│   ├── poker.py        # Poker game implementation
│   └── coin.py         # Coin flip game implementation
├── market_maker.py      # Market making engine and logic
└── ui.py               # User interface (using Tkinter)

## Games Description

### 1. Dice Game
- 3 dices are rolled
- There are different outcomes with different odds that you can bet you money on

### 2. Poker Game
- 3 cards are drawn with replacement
- There are different outcomes with different odds that you can bet your money on
- Market Making: The game provides bid/ask prices for the sum of the 3 cards
  - You can buy (bet the sum will be higher)
  - You can sell (bet the sum will be lower)
  - Prices update after each trade

### 3. Coin Flip
- 3 coins are flipped at the same time
- Bet on patterns, different outcomes have different odds. 
- Streak betting options (consecutive heads/tails): All heads or 2 consecutive heads
- Multiple coin flip combinations: Alternating (HTH or THT), 2 heads, or 2 tails


## Features
- Real-time odds updating after each trade
- Real-time bid and ask updating after each trade (for cards only)
- Virtual currency system: you can set the money of your initial account, PNL is calculated each round. 


## Getting Started
1. Install required dependencies
2. CD to the project directory 
3. Run **python -m market_maker.main** to start the application



