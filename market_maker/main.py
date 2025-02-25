import tkinter as tk
import sys
import os
from pathlib import Path
from typing import Optional
from .ui import GameUI

class MarketMakingApp:
    def __init__(self):
        self.root: Optional[tk.Tk] = None
        self.ui: Optional[GameUI] = None
        
    def setup_environment(self) -> None:
        """Setup necessary environment variables and paths"""
        # Add project root to Python path
        project_root = Path(__file__).parent
        sys.path.append(str(project_root))
        
        # Create necessary directories if they don't exist
        log_dir = project_root / "logs"
        log_dir.mkdir(exist_ok=True)

    def initialize(self) -> None:
        """Initialize the application"""
        try:
            # Setup Tkinter root
            self.root = tk.Tk()
            
            # Set window title and icon
            self.root.title("Market Making Trading Games")
            
            # Configure window properties
            self.root.minsize(800, 600)
            
            # Configure grid weights
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            
            # Initialize UI
            self.ui = GameUI(self.root)
            
        except Exception as e:
            print(f"Error initializing application: {e}")
            sys.exit(1)

    def run(self) -> None:
        """Run the application"""
        try:
            # Setup environment
            self.setup_environment()
            
            # Initialize application
            self.initialize()
            
            # Start the main event loop
            if self.root:
                self.root.mainloop()
                
        except KeyboardInterrupt:
            print("\nApplication terminated by user")
            sys.exit(0)
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)
        finally:
            # Cleanup code here if needed
            pass

def main():
    """Main entry point for the application"""
    try:
        # Create and run application
        app = MarketMakingApp()
        app.run()
        
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 