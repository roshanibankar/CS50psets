import asyncio
import json
from unittest.mock import MagicMock, patch
import louvre

# Helper to run async code synchronously
def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


# ---------------------- next_id ----------------------
def test_next_id():
    assert louvre.next_id("cl010000006") == "cl010000007"
    assert louvre.next_id("cl019999999") == "cl020000000"
    assert louvre.next_id("cl000000000") == "cl000000001"



# ---------------------- fetch 404 ----------------------
def test_fetch_404(tmp_path):
    output = tmp_path / "items.ndjson"
    checkpoint = tmp_path / "checkpoint.txt"

    louvre.OUTPUT_FILE = str(output)
    louvre.CHECKPOINT_FILE = str(checkpoint)

    class FakeResp:
        def __init__(self, status):
            self.status = status

        async def json(self):
            return {}

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    async def fake_get(*args, **kwargs):
        return FakeResp(404)

    mock_session = MagicMock()
    mock_session.get = fake_get

    sem = asyncio.Semaphore(1)
    run(louvre.fetch(mock_session, "cl000000002", sem))

    assert not output.exists()
    assert not checkpoint.exists()



# ---------------------- main loop ----------------------
def test_main_loop(tmp_path):
    louvre.START_ID = "cl000000000"
    louvre.END_ID = "cl000000002"

    output = tmp_path / "items.ndjson"
    checkpoint = tmp_path / "checkpoint.txt"

    louvre.OUTPUT_FILE = str(output)
    louvre.CHECKPOINT_FILE = str(checkpoint)

    async def fake_fetch(session, item_id, sem, retries=3):
        with open(output, "a") as f:
            json.dump({"id": item_id, "data": {}}, f)
            f.write("\n")
        with open(checkpoint, "w") as f:
            f.write(item_id)

    with patch("louvre.fetch", fake_fetch):
        run(louvre.main())

    ids = [json.loads(line)["id"] for line in open(output)]
    assert ids == ["cl000000000", "cl000000001", "cl000000002"]
    assert checkpoint.read_text() == "cl000000002"
