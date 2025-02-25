import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional
from .games.dice import DiceGame
from .games.poker import PokerGame
from .games.coin import CoinGame
from .market_maker import MarketMaker

class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Market Making Trading Games")
        self.root.geometry("400x800")  # Increased window size
        
        # Initialize all games
        self.dice_game = DiceGame()
        self.poker_game = PokerGame()
        self.coin_game = CoinGame()
        self.player_balance = 1000.0
        
        # Set initial balance for all games
        self.dice_game.set_balance(self.player_balance)
        self.poker_game.set_balance(self.player_balance)
        self.coin_game.set_balance(self.player_balance)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Balance and PnL display at the top
        self.balance_frame = ttk.Frame(self.main_frame)
        self.balance_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(self.balance_frame, text="Balance: $").grid(row=0, column=0)
        self.balance_label = ttk.Label(self.balance_frame, text=str(self.player_balance))
        self.balance_label.grid(row=0, column=1)
        
        # Add PnL display
        ttk.Label(self.balance_frame, text="   PnL: $").grid(row=0, column=2, padx=(20,0))
        self.pnl_label = ttk.Label(self.balance_frame, text="0.00")
        self.pnl_label.grid(row=0, column=3)

        # Create frames for each game - now vertically stacked
        self.setup_dice_section()
        self.setup_poker_section()
        self.setup_coin_section()
        
        # Initialize odds display for all games
        self.update_odds_display("dice")
        self.update_odds_display("poker")
        self.update_odds_display("coin")

        # Add submit button at the bottom for all games
        submit_frame = ttk.Frame(self.main_frame)
        submit_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
        ttk.Button(submit_frame, text="Submit", 
                  command=self.submit_all_games).grid(row=0, column=0, sticky=(tk.W, tk.E))

    def setup_dice_section(self):
        # Create a frame for dice game that will contain both betting and results
        dice_container = ttk.LabelFrame(self.main_frame, text="Dice Game", padding="5")
        dice_container.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Create separate frames for betting and results
        dice_betting_frame = ttk.Frame(dice_container)
        dice_betting_frame.grid(row=0, column=0, padx=5)
        
        dice_results_frame = ttk.Frame(dice_container)
        dice_results_frame.grid(row=0, column=1, padx=5)
        
        # Initialize odds labels dictionary
        self.dice_odds_labels = {}
        self.dice_bet_amounts = {}
        
        # Setup betting panel
        for i, (outcome, desc) in enumerate(self.dice_game.outcomes.items()):
            ttk.Label(dice_betting_frame, text=f"{desc}:").grid(row=i, column=0, sticky=tk.W, padx=(5,10))
            
            odds_value = self.dice_game.current_odds[outcome]
            self.dice_odds_labels[outcome] = ttk.Label(dice_betting_frame, text=f"Odds: {odds_value:.1f}:1")
            self.dice_odds_labels[outcome].grid(row=i, column=1, sticky=tk.W)
            
            bet_frame = ttk.Frame(dice_betting_frame)
            bet_frame.grid(row=i, column=2, padx=5)
            
            ttk.Label(bet_frame, text="$").grid(row=0, column=0)
            bet_amount = ttk.Entry(bet_frame, width=8)
            bet_amount.insert(0, "0")
            bet_amount.grid(row=0, column=1)
            self.dice_bet_amounts[outcome] = bet_amount
        
        # Setup results panel
        ttk.Label(dice_results_frame, text="Results:").grid(row=0, column=0, sticky=tk.W)
        self.dice_results_label = ttk.Label(dice_results_frame, text="", justify=tk.LEFT)
        self.dice_results_label.grid(row=1, column=0, sticky=tk.W)

    def setup_poker_section(self):
        # Create a frame for poker game that will contain both betting and results
        poker_container = ttk.LabelFrame(self.main_frame, text="Poker Game", padding="5")
        poker_container.grid(row=2, column=0, sticky="we", pady=5)
        
        # Create separate frames for betting, market maker, and results
        poker_betting_frame = ttk.Frame(poker_container)
        poker_betting_frame.grid(row=0, column=0, padx=5)
        
        poker_market_frame = ttk.Frame(poker_container)
        poker_market_frame.grid(row=1, column=0, padx=5, pady=10)
        
        poker_results_frame = ttk.Frame(poker_container)
        poker_results_frame.grid(row=0, column=1, rowspan=2, padx=5)
        
        # Initialize odds labels dictionary
        self.poker_odds_labels = {}
        self.poker_bet_amounts = {}
        
        # Setup betting panel
        for i, (outcome, desc) in enumerate(self.poker_game.outcomes.items()):
            ttk.Label(poker_betting_frame, text=f"{desc}:").grid(row=i, column=0, sticky="w", padx=(5,10))
            
            odds_value = self.poker_game.current_odds[outcome]
            self.poker_odds_labels[outcome] = ttk.Label(poker_betting_frame, text=f"Odds: {odds_value:.1f}:1")
            self.poker_odds_labels[outcome].grid(row=i, column=1, sticky="w")
            
            bet_frame = ttk.Frame(poker_betting_frame)
            bet_frame.grid(row=i, column=2, padx=5)
            
            ttk.Label(bet_frame, text="$").grid(row=0, column=0)
            bet_amount = ttk.Entry(bet_frame, width=8)
            bet_amount.insert(0, "0")
            bet_amount.grid(row=0, column=1)
            self.poker_bet_amounts[outcome] = bet_amount
        
        # Setup market maker panel
        ttk.Label(poker_market_frame, text="Market Making - Sum of Cards").grid(row=0, column=0, columnspan=4, sticky="w")
        
        # Market maker trading section
        market_frame = ttk.Frame(poker_market_frame)
        market_frame.grid(row=1, column=0, padx=5)
        
        # Bid/Ask display
        self.poker_bid_label = ttk.Label(market_frame, text="Bid: 10.00")
        self.poker_bid_label.grid(row=0, column=0, padx=5)
        
        self.poker_ask_label = ttk.Label(market_frame, text="Ask: 11.00")
        self.poker_ask_label.grid(row=0, column=1, padx=5)
        
        # Amount entry
        ttk.Label(market_frame, text="Shares:").grid(row=0, column=2, padx=5)
        self.poker_trade_amount = ttk.Entry(market_frame, width=8)
        self.poker_trade_amount.insert(0, "0")
        self.poker_trade_amount.grid(row=0, column=3, padx=5)
        
        # Buy/Sell selection
        self.poker_trade_type = tk.StringVar(value="buy")
        ttk.Radiobutton(market_frame, text="Buy", value="buy", 
                        variable=self.poker_trade_type).grid(row=0, column=4, padx=5)
        ttk.Radiobutton(market_frame, text="Sell", value="sell", 
                        variable=self.poker_trade_type).grid(row=0, column=5, padx=5)
        
        # Setup results panel
        ttk.Label(poker_results_frame, text="Results:").grid(row=0, column=0, sticky="w")
        self.poker_results_label = ttk.Label(poker_results_frame, text="", justify="left")
        self.poker_results_label.grid(row=1, column=0, sticky="w")

    def setup_coin_section(self):
        # Create a frame for coin game that will contain both betting and results
        coin_container = ttk.LabelFrame(self.main_frame, text="Coin Flip", padding="5")
        coin_container.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Create separate frames for betting and results
        coin_betting_frame = ttk.Frame(coin_container)
        coin_betting_frame.grid(row=0, column=0, padx=5)
        
        coin_results_frame = ttk.Frame(coin_container)
        coin_results_frame.grid(row=0, column=1, padx=5)
        
        # Initialize odds labels dictionary
        self.coin_odds_labels = {}
        self.coin_bet_amounts = {}
        
        # Setup betting panel
        for i, (outcome, desc) in enumerate(self.coin_game.outcomes.items()):
            ttk.Label(coin_betting_frame, text=f"{desc}:").grid(row=i, column=0, sticky=tk.W, padx=(5,10))
            
            odds_value = self.coin_game.current_odds[outcome]
            self.coin_odds_labels[outcome] = ttk.Label(coin_betting_frame, text=f"Odds: {odds_value:.1f}:1")
            self.coin_odds_labels[outcome].grid(row=i, column=1, sticky=tk.W)
            
            bet_frame = ttk.Frame(coin_betting_frame)
            bet_frame.grid(row=i, column=2, padx=5)
            
            ttk.Label(bet_frame, text="$").grid(row=0, column=0)
            bet_amount = ttk.Entry(bet_frame, width=8)
            bet_amount.insert(0, "0")
            bet_amount.grid(row=0, column=1)
            self.coin_bet_amounts[outcome] = bet_amount
        
        # Setup results panel
        ttk.Label(coin_results_frame, text="Results:").grid(row=0, column=0, sticky=tk.W)
        self.coin_results_label = ttk.Label(coin_results_frame, text="", justify=tk.LEFT)
        self.coin_results_label.grid(row=1, column=0, sticky=tk.W)

    def update_odds_display(self, game_type):
        if game_type == "dice":
            for outcome, odds in self.dice_game.current_odds.items():
                if outcome in self.dice_odds_labels:
                    self.dice_odds_labels[outcome].config(text=f"Odds: {odds:.1f}:1")
        elif game_type == "poker":
            for outcome, odds in self.poker_game.current_odds.items():
                if outcome in self.poker_odds_labels:
                    self.poker_odds_labels[outcome].config(text=f"Odds: {odds:.1f}:1")
        elif game_type == "coin":
            for outcome, odds in self.coin_game.current_odds.items():
                if outcome in self.coin_odds_labels:
                    self.coin_odds_labels[outcome].config(text=f"Odds: {odds:.1f}:1")

    def submit_all_games(self):
        try:
            has_activity = False
            initial_balance = self.player_balance
            result_summary = ""
            
            # Store initial balances for each game BEFORE placing any bets
            dice_initial = self.dice_game.player_balance
            poker_initial = self.poker_game.player_balance
            coin_initial = self.coin_game.player_balance
            
            # Process market maker trade for poker
            trade_amount = float(self.poker_trade_amount.get() or 0)
            if trade_amount > 0:
                has_activity = True
                is_buy = self.poker_trade_type.get() == "buy"
                success = self.poker_game.place_market_trade(trade_amount, is_buy)
                if not success:
                    messagebox.showerror("Error", "Trade failed")
                    return
            
            # Collect and validate all bets
            total_bet_amount = trade_amount  # Include market maker trade amount
            
            # Update empty entries to show "0"
            for bet_dict in [self.dice_bet_amounts, self.poker_bet_amounts, self.coin_bet_amounts]:
                for bet_entry in bet_dict.values():
                    if not bet_entry.get():  # If entry is empty
                        bet_entry.insert(0, "0")
            
            # Place all bets before playing rounds
            for game_bets, game in [(self.dice_bet_amounts, self.dice_game),
                                   (self.poker_bet_amounts, self.poker_game),
                                   (self.coin_bet_amounts, self.coin_game)]:
                for outcome, bet_entry in game_bets.items():
                    amount = float(bet_entry.get() or 0)
                    if amount > 0:
                        has_activity = True
                        total_bet_amount += amount
                        success = game.place_bet(outcome, amount)
                        if not success:
                            messagebox.showerror("Error", f"Failed to place bet on {outcome}")
                            return
            
            if not has_activity:
                messagebox.showerror("Error", "Please place at least one bet or market maker trade")
                return
            
            # Validate total costs against balance
            if total_bet_amount > self.player_balance:
                messagebox.showerror("Error", "Insufficient balance for all bets")
                return
            
            # Play all games and update results
            game_results = {
                "dice": self.dice_game.play_round(),
                "poker": self.poker_game.play_round(),
                "coin": self.coin_game.play_round()
            }
            
            # Calculate wins/losses from each game
            dice_pnl = self.dice_game.player_balance - dice_initial
            poker_pnl = self.poker_game.player_balance - poker_initial
            coin_pnl = self.coin_game.player_balance - coin_initial
            
            # Update total balance with all games' PnL
            total_pnl = dice_pnl + poker_pnl + coin_pnl
            final_balance = initial_balance + total_pnl
            
            # Update UI with correct PnL and balance
            self.player_balance = final_balance
            self.balance_label.config(text=f"{self.player_balance:.2f}")
            self.pnl_label.config(text=f"{total_pnl:+.2f}")
            
            # Now sync the balances to prepare for next round
            self.sync_game_balances()
            
            # Update result summary
            result_summary = "Game Results:\n"
            if dice_pnl != 0:
                result_summary += f"Dice Game PnL: ${dice_pnl:+.2f}\n"
            if poker_pnl != 0:
                result_summary += f"Poker Game PnL: ${poker_pnl:+.2f}\n"
                if trade_amount > 0:
                    result_summary += f"Market Maker Trade: {'Buy' if is_buy else 'Sell'} {trade_amount} shares\n"
                    result_summary += f"Final Card Sum: {game_results['poker']['sum']}\n"
            if coin_pnl != 0:
                result_summary += f"Coin Game PnL: ${coin_pnl:+.2f}\n"
            
            result_summary += f"\nTotal PnL: ${total_pnl:+.2f}"
            messagebox.showinfo("Results", result_summary)
            
            # Display results for each game
            for game_type, result in game_results.items():
                result_text = self.format_results(game_type, result)
                if game_type == "dice":
                    self.dice_results_label.config(text=result_text)
                elif game_type == "poker":
                    self.poker_results_label.config(text=result_text)
                elif game_type == "coin":
                    self.coin_results_label.config(text=result_text)
            
            # After processing all games, update all odds displays
            self.update_odds_display("dice")
            self.update_odds_display("poker")
            self.update_odds_display("coin")
            
            # Reset all bet entries to "0"
            for bet_dict in [self.dice_bet_amounts, self.poker_bet_amounts, self.coin_bet_amounts]:
                for bet_entry in bet_dict.values():
                    bet_entry.delete(0, tk.END)  # Clear current value
                    bet_entry.insert(0, "0")     # Set to "0"
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid amounts")

    def format_results(self, game_type, results):
        result_text = ""
        if game_type == "dice":
            result_text = f"Dice rolls: {results['dice_rolls']}\n"
            result_text += f"Total: {results['total']}\n"
        elif game_type == "poker":
            cards_text = [f"{card[0]} of {card[1]}" for card in results['cards']]
            result_text = f"Cards drawn: {', '.join(cards_text)}\n"
            result_text += f"Sum of cards: {results['sum']}\n"
            
            # Update bid/ask labels directly instead of showing in results
            bid, ask = results['market_prices']
            self.poker_bid_label.config(text=f"Bid: {bid:.2f}")
            self.poker_ask_label.config(text=f"Ask: {ask:.2f}")
        elif game_type == "coin":
            result_text = f"Coin flips: {' '.join(results['flips'])}\n"
            
        result_text += "Outcomes:\n"
        for outcome, won in results['outcomes'].items():
            result_text += f"{outcome}: {'Won' if won else 'Lost'}\n"
        
        return result_text

    def sync_game_balances(self):
        """Synchronize all game balances with the UI balance"""
        self.dice_game.set_balance(self.player_balance)
        self.poker_game.set_balance(self.player_balance)
        self.coin_game.set_balance(self.player_balance)

def main():
    root = tk.Tk()
    app = GameUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 