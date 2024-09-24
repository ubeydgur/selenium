from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from collections import namedtuple
from threading import Thread
from time import sleep
import csv


bandcamp_url = "https://bandcamp.com/"

TrackRec = namedtuple('TrackRec', [
    'title',
    'artist',
    'artist_url',
    'album',
    'album_url'
])

class BandLeader():
    def __init__(self, csvpath=None):
        self.driver = Chrome()
        self.driver.get(bandcamp_url)

        self.database_path = csvpath
        self.database = []
        self._current_track_record = None

        self._current_track_number = 1
        self.track_list = []

        self.thread = Thread(target=self._maintain)
        self.thread.daemon = True
        self.thread.start()
        
        # multithreading was used to continuously update 
        # the database in the backend while the code was running.


    def tracks(self):
        sleep(1)

        discover_section = self.driver.find_element(By.CLASS_NAME, "discover-results")
        left_x = discover_section.location['x']
        right_x = left_x + discover_section.size['width']
        
        discover_items = self.driver.find_elements(By.CLASS_NAME, "discover-item")
        self.track_list = [t for t in discover_items
                           if t.location['x'] >= left_x and t.location['x'] < right_x]
        
        """for(i,track) in enumerate(self.track_list):
            print(f"[{i+1}]")
            lines = track.text.split("\n")
            print(f"Album  : {lines[0]}")
            print(f"Artist : {lines[1]}")
            print(f"Genre  : {lines[2]}\n")
        """
        

    def more_tracks(self, click_button='next'):
        sleep(1)

        items = self.driver.find_elements(By.CLASS_NAME, 'item-page')
        next_button = [item for item in items
                       if item.text.lower() == click_button]
        
        if next_button:
            next_button[0].click()


    def play(self, track=None):
        if track is None:
            self.driver.find_element(By.CLASS_NAME, "playbutton").click()
        
        elif type(track) is int and track <= len(self.track_list) and track >= 1:
            self.current_track_number = track
            self.track_list[self.current_track_number - 1].click()
        
        sleep(3)

        if self.is_playing():
            self._current_track_record = self.currently_playing()   


    def pause(self):
        self.play()


    def is_playing(self):
        play_button = self.driver.find_element(By.CLASS_NAME, 'playbutton')

        return play_button.get_attribute('class').find("playing") > -1
    

    def currently_playing(self):
        if self.is_playing():
            title = self.driver.find_element(By.CLASS_NAME, 'title').text
            album_detail = self.driver.find_element(By.CSS_SELECTOR, ".detail-album > a")
            album_title = album_detail.text
            album_url = album_detail.get_attribute('href')
            artist_detail = self.driver.find_element(By.CSS_SELECTOR, ".detail-artist > a")
            artist_name = artist_detail.text
            artist_url = artist_detail.get_attribute('href')
            
            # The reason CSS_SELECTOR is used here is because 
            # the 'a' tag does not have a class.

            # The use of '.' at the beginning indicates that it is a class 
            # and the use of '>' after it indicates that 'a' is a child tag.

            return TrackRec(title, artist_name, artist_url, album_title, album_url) 
    

    def _maintain(self):
        while True:
            self._update_db()
            sleep(1)

    
    def _update_db(self):
        check = (self._current_track_record is not None 
                and (len(self.database) == 0
                     or self.database[-1] != self._current_track_record)
                and self.is_playing())
        
        if check:
            self.database.append(self._current_track_record)

    
    def save_db(self):
        with open(self.database_path, 'w', newline='') as dbfile:
            dbwriter = csv.writer(dbfile)
            dbwriter.writerow(list(TrackRec._fields))

            for entry in self.database:
                dbwriter.writerow(list(entry))


path = "/Users/ubeydgur/Projects/python/web-scraping-projects/track-storage-selenium/database.csv"

if __name__ == "__main__":
    band_leader = BandLeader(path)
    
    band_leader.play()
    band_leader.more_tracks()
    band_leader.tracks()

    for num in range(len(band_leader.track_list)):
        band_leader.play(num + 1)
        sleep(2)

    band_leader.save_db()
    band_leader.driver.quit()