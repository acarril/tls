import bs4
import re
from .entries import Entries
from dataclasses import dataclass

@dataclass
class Match:
    def __init__(self, match_entry:bs4.element.Tag) -> None:
        self.match_entry = match_entry
        self.players = self.__get_player_names()
        self.serving = self.__get_whos_serving()
        self.set_scores = self.__get_set_scores()
        self.game_scores = self.__get_game_scores()
        self.is_doubles = self.__get_is_doubles()

    def __get_is_doubles(self) -> bool:
        return len(self.match_entry.find_all('div', {'class': 'Gd'})) == 4

    def __get_player_names(self) -> list:
        id_divs = self.match_entry.find_all('div', {'class': 'Id'})
        players = [' & '.join([p.text for p in d.find_all('div', {'class': 'Gd'})]) for d in id_divs]
        return players

    def __get_whos_serving(self) -> int: 
        id_divs = self.match_entry.find_all('div', {'class': 'Id'})
        idx = (id_divs[0].find('div', {'class': 'wd'}) is None) * 1
        return idx
    
    def __get_set_scores(self):
        def process_single_set(span:bs4.element.Tag) -> tuple:
            # Return None if set is not initiated
            # (<span> only content is empty <sup> tag):
            if len(span.contents) == 1:
                return None
            # Else, set is initiated, so we parse the scores 
            # (<span> content has 2 elements: set score and possibly tiebreak score):
            else:
                set_score = span.contents[0]  # first element is set score
                tiebreak_score = span.contents[1].text if span.contents[1].text != '' else None # second element is tiebreak score, but could be empty <sup> tag
                return set_score, tiebreak_score
        set_scores = []
        for p in range(0, 2):
            spans = self.match_entry.find_all(
                'span',
                {'data-testid': re.compile(fr'tennis_match_row-side_score_undefined_{p}_\d')}
            )
            scores = [process_single_set(x) for x in spans]
            set_scores.append(scores)
        return set_scores

    def __get_game_scores(self):
        spans = self.match_entry.find('div', {'class': 'Fd'}).find_all('span')
        return [x.text for x in spans]


@dataclass
class Event:
    def __init__(self, event_entries) -> None:
        self.__event_entry = event_entries[0]
        self.__match_entries = event_entries[1]
        self.matches = [Match(m) for m in self.__match_entries]
        self.type, self.name, self.date = self.__get_event_info()
        self.tour, self.level = self.type.split()
    
    def __get_event_info(self):
        title_elements = [x.text for x in self.__event_entry]
        event_type, event_name = title_elements[0].split('\xa0-\xa0')
        event_date = title_elements[1]
        return event_type, event_name, event_date
    

def get_events(entries=None):
    if entries is None:
        entries = Entries()
    events = [Event(e) for e in entries.categorized]
    return events