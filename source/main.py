from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from time import sleep


bandcamp_url = "https://bandcamp.com/"

class BandLeader():
    def __init__(self):
        self.driver = Chrome()
        self.driver.get(bandcamp_url)

        self.current_track_number = 1
        self.track_list = []
        self.tracks()

    def tracks(self):
        sleep(1)

        discover_section = self.driver.find_element(By.CLASS_NAME, "discover-results")
        left_x = discover_section.location['x']
        right_x = left_x + discover_section.size['width']
        
        discover_items = self.driver.find_elements(By.CLASS_NAME, "discover-item")
        self.track_list = [t for t in discover_items
                           if t.location['x'] >= left_x and t.location['x'] < right_x]
        
        for(i,track) in enumerate(self.track_list):
            print(f"[{i+1}]")
            lines = track.text.split("\n")
            print(f"Album  : {lines[0]}")
            print(f"Artist : {lines[1]}")
            print(f"Genre  : {lines[2]}\n")
        
    def more_tracks(self, click='next'):
        sleep(1)

        hey = self.driver.find_elements(By.CLASS_NAME, 'item-page')
        next_button = [e for e in hey
                       if e.text.lower() == click]
        
        if next_button:
            next_button[0].click()
            self.tracks()

    def play(self, track=None):
        if track is None:
                self.driver.find_element(By.CLASS_NAME, "playbutton").click()
        
        elif type(track) is int and track <= len(self.track_list) and track >= 1:
                self.current_track_number = track
                self.track_list[self.current_track_number - 1].click()
        
        sleep(10)

    def pause(self):
         self.play()
