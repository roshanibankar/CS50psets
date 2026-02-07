# Louvre Collection Scraper and Browser
#### Description:

The **Louvre Collection Scraper and Browser** is a full-stack Python application designed to archive and visualize digitized artwork data from the Louvre Museum's public API. This project was born out of a desire to create a local, searchable interface for art history research, allowing users to browse thousands of items without relying on the museum's external web interface once the data is cached.

### Project Functionality
The application operates in two distinct phases:

1.  **The Scraper (Asynchronous Data Collection):** Using `aiohttp` and Python's `asyncio` library, the script performs high-speed, non-blocking HTTP requests to the Louvre's JSON API. Because the collection contains hundreds of thousands of items, a standard sequential scraper would be too slow. This implementation utilizes a `Semaphore` to manage 50 concurrent requests, balancing speed with server etiquette. It includes a checkpoint system that saves the last successfully downloaded ID to a text file, allowing the user to stop and resume the process without losing progress.

2.  **The Web Interface (Flask Application):** Once data is stored locally in an `ndjson` (Newline Delimited JSON) format, the Flask server provides a luxury-themed gallery. Users can search by title or use dynamic dropdown filters. These filters (Artist, Material, Technique, Collection, and Location) are generated dynamically based on the actual contents of the local dataset, ensuring that the UI always matches the data.

### File Structure
- `project.py`: The heart of the application. It contains the `main()` function, the asynchronous scraping logic, the Flask route definitions, and the search/filtering algorithms.
- `test_project.py`: Contains unit tests for the data normalization and safety functions to ensure the application doesn't crash when encountering inconsistent JSON structures from the API.
- `requirements.txt`: Lists the external libraries (`flask` and `aiohttp`) required to run the project.
- `data/`: A directory created at runtime to store the `items.ndjson` database and the `checkpoint.txt` file.

### Design Choices
During development, I encountered significant inconsistencies in the Louvre's metadata. For example, the "index" field in their JSON sometimes appears as a single dictionary and other times as a list of dictionaries. To handle this, I implemented the `normalize_index` function. This ensures that regardless of the API's format, the web server can always find the "Material" or "Technic" fields. 

Another design choice was using **NDJSON** for storage. Unlike a standard JSON list, NDJSON allows the scraper to append new records to the file one line at a time. This prevents data loss if the script crashes and allows the program to read large files line-by-line without loading the entire database into RAM, making the application more memory-efficient.

### How to Run
First, install dependencies:
`pip install -r requirements.txt`

To gather data:
`python project.py --scrape`

To view the gallery:
`python project.py`
