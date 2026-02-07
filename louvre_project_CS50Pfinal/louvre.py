import asyncio
import json
import os
from aiohttp import ClientSession, ClientTimeout
from asyncio import Semaphore

BASE = "https://collections.louvre.fr/ark:/53355/"
START_ID = "cl010000006"
END_ID = "cl020630220"
OUTPUT_FILE = "data/items.ndjson"
CHECKPOINT_FILE = "data/checkpoint.txt"
CONCURRENT_REQUESTS = 50   # adjust based on your network

os.makedirs("data", exist_ok=True)

# Load checkpoint if exists
if os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE, "r") as f:
        last_id = f.read().strip()
        if last_id:
            START_ID = last_id
            print(f"[RESUME] Starting from checkpoint: {START_ID}")

# Increment ID correctly (9 digits after 'cl')
def next_id(item_id):
    prefix = item_id[:2]
    number = int(item_id[2:])
    number += 1
    return f"{prefix}{number:09d}"

# Async fetch with retries and SSL bypass
async def fetch(session: ClientSession, item_id: str, sem: Semaphore, retries=3):
    url = BASE + item_id + ".json"
    async with sem:
        for attempt in range(retries):
            try:
                async with session.get(url, ssl=False, timeout=ClientTimeout(total=15)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        # Save as NDJSON line
                        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                            json.dump({"id": item_id, "data": data}, f, ensure_ascii=False)
                            f.write("\n")
                        # Update checkpoint
                        with open(CHECKPOINT_FILE, "w") as f:
                            f.write(item_id)
                        print(f"[SAVED] {item_id}")
                        return
                    elif resp.status == 404:
                        print(f"[MISS] {item_id}")
                        return
                    else:
                        print(f"[WARN] {item_id} -> HTTP {resp.status}")
            except Exception as e:
                print(f"[ERROR] {item_id} attempt {attempt+1} -> {e}")
                await asyncio.sleep(1)  # wait before retry
        print(f"[FAIL] {item_id} after {retries} attempts")

# Async main scraper
async def main():
    sem = Semaphore(CONCURRENT_REQUESTS)
    async with ClientSession() as session:
        current = START_ID
        tasks = []

        while int(current[2:]) <= int(END_ID[2:]):
            task = asyncio.create_task(fetch(session, current, sem))
            tasks.append(task)

            # Limit in-memory tasks to avoid overload
            if len(tasks) >= CONCURRENT_REQUESTS * 2:
                await asyncio.gather(*tasks)
                tasks = []

            current = next_id(current)

        # Await remaining tasks
        if tasks:
            await asyncio.gather(*tasks)

    print("[DONE] Scraping completed!")

# Run scraper
if __name__ == "__main__":
    asyncio.run(main())
