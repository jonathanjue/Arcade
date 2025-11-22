"""Main entry point for Shape Clicker game"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import main

if __name__ == "__main__":
    main()