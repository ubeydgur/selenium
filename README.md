# Track Storage Selenium

Playing tracks on the bandcamp.com website, accessing more tracks, and saving information about the tracks listened to a database and exporting it to a `CSV` file.

- Track Website: [bandcamp.com](https://bandcamp.com/)
  
## Features

- With the **tracks** and **more_tracks** functions, information about the tracks in the discovery section can be scraped and more tracks can be discovered.
  
- **play**, **pause**, **is_playing** and **currently_playing** functions can be used to play and pause the desired track, and scrape information about the track and artist
  
- The *database* can be updated and saved with the **_update_db** and **save_db** functions.
  
- With the **_maintain** function and the **threading** library, the database is continuously updated in the background by `multi-processing`.

## Dependencies

- [Selenium](https://selenium-python.readthedocs.io/)
  
- [Threading](https://docs.python.org/3/library/threading.html#semaphore-example)
  
- [CSV](https://docs.python.org/3/library/csv.html)

## Usage

1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the script:

    ```bash
    python main.py
    ```

3. Enter your search query when prompted.

4. View the results.
