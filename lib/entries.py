import requests, socket, time
import bs4
from bs4 import BeautifulSoup

class Entries:
    def __init__(self):
        self.active = self.__get_active_entries()
        self.categorized = self.__categorize_entries()

    def __is_connected(server:str="www.livescores.com") -> bool:
        try:
            host = socket.gethostbyname(server)
            socket.create_connection((host, 80), 2)
            return True
        except:
            return False

    def __get_tz_offset(self):
        offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        return offset / 60 / 60 * -1

    def __get_livescores_url(self, name, event_type):
        tz_offset = self.__get_tz_offset()
        url = "https://www.livescores.com/tennis/live" + f'/?tz={tz_offset}'
        return url

    def __get_soup(self):
        url = self.__get_livescores_url("foo", "bar")
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def __get_entries(self) -> bs4.element.ResultSet:
        soup = self.__get_soup()
        results = soup.find_all("div", {"class": "qb"})
        entries = results[0].find_all("div", {"class": ["Ba", "jd nd"]}, recursive=False)
        return entries

    def __get_active_entries(self) -> bs4.element.ResultSet:
        entries = self.__get_entries()
        active_entries = bs4.element.ResultSet(entries.source)
        for idx, entry in enumerate(entries):
            # Process next entry
            try:
                next_entry_is_match = "jd" in entries[idx+1].get("class")
            except IndexError:
                next_entry_is_match = False
            # Determine if next entry OR entry itself is a match to mark event as active
            if (
                ("Ba" in entry.get("class") and next_entry_is_match) or
                ("jd" in entry.get("class"))
            ):
                active_entries.append(entry)
        return active_entries
    
    def __categorize_entries(self) -> list:
        entries_organized = []
        for idx, entry in enumerate(self.active):
            if 'Ba' in entry.get('class'):
                event = entry
                matches = []
            elif 'jd' in entry.get('class'):
                matches.append(entry)

            try:
                next_class = self.active[idx+1].get('class')
            except IndexError:
                event_done = True
            else:
                event_done = 'jd' not in next_class
            
            if event_done:
                entries_organized.append((event, matches))
        
        return entries_organized


    
