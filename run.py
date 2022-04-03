import os
import arcade

from src.main import Game


def main():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    window = Game(curr_dir)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
