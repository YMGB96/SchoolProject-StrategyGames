import game_gui as gg
import menu_gui as mg
from database import database
import pygame as pg
import game_logic

run = True

def setup():
    """Set everything up"""
    pg.init()
    mg.menu_gui = mg.MenuGui()

def running():
    """Handle every frame"""
    # End the loop when the window is closed
    if pg.event.get(pg.QUIT):
        global run
        run = False
    # If there is a game_gui render that ...
    if gg.game_gui:
        gg.game_gui.render()
    # ... render the menu if not
    elif mg.menu_gui:
        mg.menu_gui.render()
    # Update Window
    pg.display.update()
    # Wait 50ms -> 20 fps
    pg.time.wait(50)

def clean_up():
    """Close everything down"""
    database.close()
    pg.quit()

def main():
    setup()
    while run:
        running()
    clean_up()

if __name__ == "__main__":
    main()
