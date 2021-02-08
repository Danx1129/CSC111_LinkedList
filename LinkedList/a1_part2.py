import random
from typing import Tuple

import pygame
from pygame.colordict import THECOLORS

from a1_linked_list import LinkedList, _Node

################################################################################
# Graphics constants
################################################################################
# You should not change SCREEN_SIZE or GRID_SIZE, but may add your own constants underneath.
SCREEN_SIZE = (800, 800)  # (width, height)
GRID_SIZE = 8


################################################################################
# Pygame helper functions
################################################################################
def initialize_screen(screen_size: tuple[int, int], allowed: list) -> pygame.Surface:
    """Initialize pygame and the display window.

    allowed is a list of pygame event types that should be listened for while pygame is running.
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(THECOLORS['white'])
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed)

    return screen


def draw_text(screen: pygame.Surface, text: str, pos: tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', 22)
    text_surface = font.render(text, True, THECOLORS['black'])
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


def draw_grid(screen: pygame.Surface) -> None:
    """Draws a square grid on the given surface.

    The drawn grid has GRID_SIZE columns and rows.
    You can use this to help you check whether you are drawing nodes and edges in the right spots.
    """
    color = THECOLORS['grey']
    width, height = screen.get_size()

    for col in range(1, GRID_SIZE):
        x = col * (width // GRID_SIZE)
        pygame.draw.line(screen, color, (x, 0), (x, height))

    for row in range(1, GRID_SIZE):
        y = row * (height // GRID_SIZE)
        pygame.draw.line(screen, color, (0, y), (width, y))


################################################################################
# 1. Drawing nodes and links
################################################################################
def draw_node(screen: pygame.Surface, node: _Node, pos: Tuple[int, int]) -> None:
    """Draw a node on the screen at the given position.

    pos represents the coordinates of the *top-left* corner of the node.

    Your drawing of the the node should include:
        - A rectangle split vertically into two halves.
        - The item stored in the node, displayed in the left half.
          You may assume the string representation of item is at most 3 characters
          long. You'll need to use the draw_text function we've provided above.

    NOTE: Do not draw the arrow representing the link to the next node in this function.
    You'll implement that part of the visualization separately in the draw_link function.

    We strongly recommend initializing new constants at the top of this file to represent
    node width, height, and colour.
    """
    h = int(SCREEN_SIZE[0] // (GRID_SIZE * 1.5))
    v = SCREEN_SIZE[1] // (2 * GRID_SIZE)
    rec = (pos[0], pos[1], h, v)
    blue = (0, 100, 255)
    black = (0, 0, 0)
    lin1 = (pos[0] + h // 2, pos[1])
    lin2 = (pos[0] + h // 2, pos[1] + int(0.98 * v))
    circ = (pos[0] + int(0.75 * h), pos[1] + int(v // 2))
    tex = (pos[0] + 5, pos[1] + 5)
    pygame.draw.rect(screen, blue, rec)
    pygame.draw.line(screen, black, lin1, lin2, 3)
    pygame.draw.circle(screen, black, circ, 5)
    draw_text(screen, str(node.item), tex)


def draw_link(screen: pygame.Surface, start: Tuple[int, int], end: Tuple[int, int]) -> None:
    """Draw a line representing a link from `start` to `end`.

    To indicate which end is the "start" of the line, draw a small circle at the starting point
    (like the diagrams we've seen in class).

    The rest of your link can be a simple line; you may, but are not required, to draw an
    arrowhead at the end of the line.
    """
    red = (255, 0, 0)
    pygame.draw.line(screen, red, start, end)


def draw_three_nodes(screen_size: Tuple[int, int]) -> None:
    """Draw three nodes on a pygame screen of the given size.

    You may choose the coordinates for the nodes, as long as they do not overlap with each other
    and are separated by at least 10 pixels. Each link must start in the CENTRE of the start node's
    right half, and must end on the border of the end node (not inside the end node).
    This matches the style of node from lecture.

    The third node should link to "None", which you should visualize by calling draw_text.
    """
    screen = initialize_screen(screen_size, [])
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3

    draw_node(screen, node1, (10, 10))
    draw_node(screen, node2, (160, 10))
    draw_node(screen, node3, (310, 10))
    draw_link(screen, (60, 35), (160, 35))
    draw_link(screen, (210, 35), (310, 35))
    draw_link(screen, (360, 35), (450, 35))
    draw_text(screen, 'NONE', (460, 30))
    ...

    # Don't change the code below (it simply waits until you close the Pygame window)
    pygame.display.flip()
    pygame.event.wait()
    pygame.display.quit()


################################################################################
# 2. Drawing a full linked list
################################################################################
def draw_list(screen: pygame.Surface, lst: LinkedList, show_grid: bool = False) -> None:
    """Draw the given linked list on the screen.

    The linked list nodes should be drawn in a grid pattern with GRID_SIZE rows and columns.
    See the assignment handout for details and constraints on your drawing.

    If the show_grid parameter is True, the grid is drawn on the board. You can use
    the grid to help you make sure you're drawing nodes in the correct locations.
    By default, show_grid is False.

    Preconditions:
        - len(lst) < GRID_SIZE * GRID_SIZE

    As with draw_node, we strongly recommend initializing new constants at the top of this file
    to store numbers used to position the nodes.

    We have started the linked list traversal pattern for you. Note that we're accessing
    a private LinkedList attribute _first, which is generally not a good practice but we're
    allowing you to do so here to simplify your code a little.
    """
    hs = SCREEN_SIZE[0] // GRID_SIZE
    vs = SCREEN_SIZE[1] // GRID_SIZE
    sta = (SCREEN_SIZE[0] // 40, SCREEN_SIZE[0] // 40)
    if show_grid:
        draw_grid(screen)
    curr = lst._first
    curr_index = 1
    if curr is None:
        draw_text(screen, 'NONE', sta)
    else:
        draw_node(screen, curr, sta)
        while curr.next is not None:
            row = (curr_index // GRID_SIZE)
            spacing = (curr_index % GRID_SIZE)
            xcoord = sta[0] + spacing * hs
            ycoord = sta[1] + row * vs
            draw_node(screen, curr.next, (xcoord, ycoord))
            if spacing != 0:
                loc = (int(xcoord - (SCREEN_SIZE[0] // (2 * GRID_SIZE))),
                       int((SCREEN_SIZE[1] // (4 * GRID_SIZE)) + ycoord))
                draw_link(
                    screen, loc, (loc[0] + (SCREEN_SIZE[0] // (2 * GRID_SIZE)), loc[1]))
            else:
                loc = (SCREEN_SIZE[0] - (SCREEN_SIZE[0] // (4 * GRID_SIZE)),
                       ycoord - vs + (SCREEN_SIZE[1] // (4 * GRID_SIZE)))
                draw_link(screen, loc, (loc[0], loc[1] + (vs // 2)))
                draw_link(screen, (
                    (SCREEN_SIZE[0] // (2 * GRID_SIZE)),
                    loc[1] + (SCREEN_SIZE[1] // (2 * GRID_SIZE))), (
                        SCREEN_SIZE[0] - (SCREEN_SIZE[0] // (4 * GRID_SIZE)),
                        loc[1] + (vs // 2)))
                draw_link(screen, (
                    (SCREEN_SIZE[0] // (2 * GRID_SIZE)),
                    loc[1] + (SCREEN_SIZE[1] // (2 * GRID_SIZE))), (
                        (SCREEN_SIZE[0] // (2 * GRID_SIZE)),
                        loc[1] + int(1.5 * (SCREEN_SIZE[1] // (2 * GRID_SIZE)))))
            curr = curr.next
            curr_index = curr_index + 1
        spacing = (curr_index % GRID_SIZE)
        row = (curr_index // GRID_SIZE)
        xcoord = sta[0] + spacing * hs
        ycoord = sta[1] + row * vs
        if curr_index % GRID_SIZE == 0:
            loc = (SCREEN_SIZE[0] - (SCREEN_SIZE[0] // (4 * GRID_SIZE)),
                   ycoord - vs + (SCREEN_SIZE[1] // (4 * GRID_SIZE)))
            draw_link(screen, loc, (loc[0], loc[1] + (vs // 2)))
            draw_link(screen, (
                (SCREEN_SIZE[0] // (2 * GRID_SIZE)),
                loc[1] + (SCREEN_SIZE[1] // (2 * GRID_SIZE))), (
                    SCREEN_SIZE[0] - (SCREEN_SIZE[0] // (4 * GRID_SIZE)),
                    loc[1] + (vs // 2)))
            draw_link(screen, (
                (SCREEN_SIZE[0] // (2 * GRID_SIZE)),
                loc[1] + (SCREEN_SIZE[1] // (2 * GRID_SIZE))), (
                    (SCREEN_SIZE[0] // (2 * GRID_SIZE)),
                    loc[1] + int(1.5 * (SCREEN_SIZE[1] // (2 * GRID_SIZE)))))
        else:
            loc = (int(xcoord - (SCREEN_SIZE[0] // (2 * GRID_SIZE))),
                   int((SCREEN_SIZE[1] // (4 * GRID_SIZE)) + ycoord))
            draw_link(
                screen, loc, (loc[0] + (SCREEN_SIZE[0] // (2 * GRID_SIZE)), loc[1]))
        row = (curr_index // GRID_SIZE)
        spacing = (curr_index % GRID_SIZE)
        xcoord = sta[0] + spacing * hs
        ycoord = sta[1] + row * vs
        draw_text(screen, 'NONE', (xcoord, ycoord + 15))


################################################################################
# 3. Handling user events
################################################################################
def run_visualization(screen_size: tuple[int, int], ll_class: type,
                      show_grid: bool = True) -> None:
    """Run the linked list visualization.

    Initialize a screen of the given size, and show the grid when show_grid is True.
    ll_class is the type of linked list to use.

    Preconditions:
        - ll_class is LinkedList or issubclass(ll_class, LinkedList)

    This function is provided for you for Part 3, and you *should not change it*.
    Instead, your task is to implement the helper function handle_mouse_click (and
    any other helpers you decide to add).
    """
    # Initialize the Pygame screen, allowing for mouse click events.
    screen = initialize_screen(screen_size, [pygame.MOUSEBUTTONDOWN])

    # Initialize a random linked list of length 50.
    lst = ll_class(random.sample(range(-99, 1000), 50))

    while True:
        # Draw the list (on a white background)
        screen.fill(THECOLORS['white'])
        draw_list(screen, lst, show_grid)
        pygame.display.flip()

        # Wait for an event (either pygame.MOUSEBUTTONDOWN or pygame.QUIT)
        event = pygame.event.wait()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Call our event handling method
            handle_mouse_click(lst, event, screen.get_size())
        elif event.type == pygame.QUIT:
            break

    pygame.display.quit()


def handle_mouse_click(lst: LinkedList, event: pygame.event.Event,
                       screen_size: Tuple[int, int]) -> None:
    """Handle a mouse click event.

    A pygame mouse click event object has two attributes that are important for this method:
        - event.pos: the (x, y) coordinates of the mouse click
        - event.button: an int representing which mouse button was clicked.
                        1: left-click, 3: right-click

    The screen_size is a tuple of (width, height), and should be used together with
    event.pos to determine which cell is being clicked. If a click happens exactly on
    the boundary between two cells, you may decide which cell is selected.

    Preconditions:
        - event.type == pygame.MOUSEBUTTONDOWN
        - screen_size[0] >= 200
        - screen_size[1] >= 200
    """
    hs = screen_size[0] // GRID_SIZE
    vs = screen_size[1] // GRID_SIZE
    co = event.pos
    xco = (co[0] // hs)
    yco = (co[1] // vs)
    index = (GRID_SIZE * yco) + xco
    if index <= len(lst) - 1:
        if event.button == 1:
            lst.pop(index)
        elif event.button == 3:
            lst.__contains__(lst[index])


if __name__ == '__main__':
    import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'disable': ['E1136'],
    #     'exclude-protected': ['_first'],
    #     'extra-imports': ['random', 'pygame', 'pygame.colordict', 'a1_linked_list'],
    #     'generated-members': ['pygame.*']
    # })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
    import a1_part1
    run_visualization(SCREEN_SIZE, a1_part1.MoveToFrontLinkedList)
    # or
    # run_visualization(SCREEN_SIZE, a1_part1.SwapLinkedList)
    # or
    # run_visualization(SCREEN_SIZE, a1_part1.CountLinkedList)
