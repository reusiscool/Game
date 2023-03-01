from app import App


def start_game():
    app = App()
    app.run()


def run_silver_tool():
    import pygame
    from puzzles.silverTool import SilverTool
    pygame.init()
    sc = pygame.display.set_mode((1600, 900))
    tool = SilverTool(sc)
    tool.run()


if __name__ == '__main__':
    start_game()
    # run_silver_tool()
