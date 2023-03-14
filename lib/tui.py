from rich import print, box
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.live import Live
from lib.events import get_events

from time import sleep

def __stringify_players_score(match):
    scores = []
    for i in range(0, 2):
        # Player name and serving indicator
        serving_indicator = '[blink bold yellow]> [/blink bold yellow]' if i==match.serving else '  '
        player = serving_indicator + match.players[i]
        # Game score
        game_score = match.game_scores[i]
        # Set score
        def stringify_set_score(x):
            def superscript_digits(digits:str):
                SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
                return digits.translate(SUP)
            
            if isinstance(x, tuple) and len(x)==2:
                set_score = x[0]
                tb_score = superscript_digits(x[1]) if x[1] is not None else ''
                return f'{set_score}{tb_score}'.ljust(3)
            
        set_score = ''.join([stringify_set_score(x) for x in match.set_scores[i] if x is not None])
        scores.append((player, set_score, game_score))
    return scores

def __gen_event_table(event):
    # Event info
    event_info = event.type + ': ' + event.name
    # Matches table
    table = Table(show_header=False, box=box.SIMPLE, expand=True)
    table.add_column("Player", justify="left", style="white", no_wrap=True)
    table.add_column("Sets", justify="left", style="white")
    table.add_column("Score", justify="right", style="white")
    for m in event.matches:
        scores = __stringify_players_score(m)
        table.add_row(*scores[0])
        table.add_row(*scores[1])
        table.add_section()
    return table, event_info

# def display_events(events, tour=None, level=None):
#     panels = []
#     for event in events:
#         if tour is not None:
#             if event.tour.lower() != tour.lower():
#                 continue
#         if level is not None:
#             if event.level.lower() != level.lower():
#                 continue
#         table, event_info = __gen_event_table(event)
#         panels.append(Panel(table, title=event_info, style='bright_black'))
#     print(Columns(panels))

def display_events(events=None, tour=None, level=None):
    if events is None:
        events = get_events()
    panels = []
    for event in events:
        if tour is not None:
            if event.tour.lower() != tour.lower():
                continue
        if level is not None:
            if event.level.lower() != level.lower():
                continue
        table, event_info = __gen_event_table(event)
        panels.append(Panel(table, title=event_info, style='bright_black'))
    return Columns(panels)

def display_live_events(tour, level):
    with Live(display_events(tour=tour, level=level), auto_refresh=False, screen=True) as live:
        while True:
            sleep(10)
            live.update(display_events(tour=tour, level=level), refresh=True)