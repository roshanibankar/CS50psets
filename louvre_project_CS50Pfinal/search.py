import json
import sys
from pathlib import Path
from flask import Flask, render_template_string, request

DATA_FILE = Path("data/items.ndjson")

# ============================================================
# SAFETY HELPERS
# ============================================================

def safe_list(x):
    return x if isinstance(x, list) else []

def safe_dict(x):
    return x if isinstance(x, dict) else {}

def extract_title(data):
    return data.get("title") or ""

# ------------------------------------------------------------

def normalize_index(index_field):
    """
    Louvre dataset inconsistency fixer:
    index may be:
        - dict { material: [...], technic: [...] }
        - list of dicts [ {material: [...]}, {technic: [...]} ]
    """
    index_clean = {}

    if isinstance(index_field, dict):
        return index_field

    if isinstance(index_field, list):
        for entry in index_field:
            if isinstance(entry, dict):
                for k, v in entry.items():
                    if k not in index_clean:
                        index_clean[k] = v

    return index_clean


# ============================================================
# LOAD AND PARSE ITEMS
# ============================================================

def load_items():
    items = []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            d = obj["data"]

            # --- Fix inconsistent fields ---
            idx = normalize_index(d.get("index"))
            d["index_normalized"] = idx

            obj["title"] = extract_title(d)
            items.append(obj)

    return items


# ============================================================
# SEARCH + FILTERING
# ============================================================

def search_items(keyword, filters):
    keyword = keyword.lower().strip()
    results = load_items()

    # TEXT SEARCH
    if keyword:
        results = [
            i for i in results
            if keyword in (i["title"] or "").lower()
        ]

    # FILTERING
    if filters:
        for key, val in filters.items():
            if not val:
                continue
            v = val.lower().strip()

            for item in results[:]:
                d = item["data"]
                idx = d["index_normalized"]

                if key == "material":
                    mats = [m.get("value","").lower() for m in safe_list(idx.get("material"))]
                    if v not in mats:
                        results.remove(item)

                elif key == "technic":
                    tcs = [t.get("value","").lower() for t in safe_list(idx.get("technic"))]
                    if v not in tcs:
                        results.remove(item)

                elif key == "period":
                    period = d.get("displayDateCreated","").lower()
                    if v not in period:
                        results.remove(item)

                elif key == "collection":
                    col = d.get("collection","").lower()
                    if v not in col:
                        results.remove(item)

                elif key == "location":
                    loc = d.get("currentLocation","").lower()
                    if v not in loc:
                        results.remove(item)

                elif key == "artist":
                    creators = [c.get("label", "").lower() for c in safe_list(d.get("creator"))]
                    if v not in creators:
                        results.remove(item)

    return results


# ============================================================
# HTML TEMPLATE
# ============================================================

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Louvre Collection</title>
    <!-- Google Font similar to Dior -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
    <style>
        body { font-family: Arial, sans-serif; background:#f5f5f5; margin:30px; }
        
        /* Luxury Dior-style header */
        h1 { 
            font-family: 'Playfair Display', serif; 
            font-style: italic; 
            font-weight: 700; 
            font-size: 3em;
            letter-spacing: 2px;
            color: #111;
            text-align: center;
        }

        h2 { font-family: 'Playfair Display', serif; font-weight: 600; margin-bottom:15px; }
        h3 { font-family: Arial, sans-serif; margin:8px 0; }

        .search-box { padding:10px; background:white; border-radius:8px; margin-bottom:25px; }
        .item-grid { display:flex; flex-wrap:wrap; gap:20px; }
        .card {
            width:260px; background:white; padding:15px;
            border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1);
        }
        img { width:100%; border-radius:6px; }

        select,input[type=text] { padding:6px; margin-right:10px; }
        button {
            padding:7px 14px; background:#333; color:white;
            border:none; border-radius:4px; cursor:pointer;
        }
    </style>
</head>
<body>

<h1>Louvre Collections</h1>

<form method="GET" class="search-box">
    <input type="text" name="q" placeholder="Search title..." value="{{ request.args.get('q','') }}">

    <!-- CATEGORY FILTERS -->
    <select name="material">
        <option value="">Material</option>
        {% for m in materials %}
            <option value="{{m}}" {% if request.args.get('material')==m %}selected{% endif %}>{{m}}</option>
        {% endfor %}
    </select>

    <select name="technic">
        <option value="">Technic</option>
        {% for t in technics %}
            <option value="{{t}}" {% if request.args.get('technic')==t %}selected{% endif %}>{{t}}</option>
        {% endfor %}
    </select>

    <select name="collection">
        <option value="">Collection</option>
        {% for c in collections %}
            <option value="{{c}}" {% if request.args.get('collection')==c %}selected{% endif %}>{{c}}</option>
        {% endfor %}
    </select>

    <select name="location">
        <option value="">Location</option>
        {% for l in locations %}
            <option value="{{l}}" {% if request.args.get('location')==l %}selected{% endif %}>{{l}}</option>
        {% endfor %}
    </select>

    <select name="artist">
        <option value="">Artist</option>
        {% for a in artists %}
            <option value="{{a}}" {% if request.args.get('artist')==a %}selected{% endif %}>{{a}}</option>
        {% endfor %}
    </select>

    <button type="submit">Search</button>
</form>

<h2>Found {{items|length}} item(s)</h2>

<div class="item-grid">
{% for item in items %}
    {% set d = item.data %}
    {% set idx = d.index_normalized %}
    {% set imgs = d.image if d.image is sequence else [] %}

    <div class="card">
        {% if imgs and imgs[0].urlThumbnail %}
            <img src="{{ imgs[0].urlThumbnail }}">
        {% endif %}

        <h3>{{ d.title }}</h3>

        {% if d.creator %}
            <p><b>Artist:</b> {{ d.creator | map(attribute='label') | join(', ') }}</p>
        {% endif %}

        {% if d.displayDateCreated %}
            <p><b>Period:</b> {{ d.displayDateCreated }}</p>
        {% endif %}

        {% if d.materialsAndTechniques %}
            <p><b>Materials:</b>
                {{ d.materialsAndTechniques.split(';') | map('trim') | join(', ') }}
            </p>
        {% endif %}

        {% if idx.technic %}
            <p><b>Techniques:</b>
                {{ idx.technic | map(attribute='value') | join(', ') }}
            </p>
        {% endif %}

        {% if d.collection %}
            <p><b>Collection:</b> {{ d.collection }}</p>
        {% endif %}

        {% if d.currentLocation %}
            <p><b>Location:</b> {{ d.currentLocation }}</p>
        {% endif %}

        {% if d.objectNumber %}
            <p><b>Inventory:</b> {{ d.objectNumber | map(attribute='value') | join(', ') }}</p>
        {% endif %}
    </div>
{% endfor %}
</div>

</body>
</html>

"""


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


@app.route("/")
def index():
    keyword = request.args.get("q", "")

    filters = {
        "material": request.args.get("material", ""),
        "technic": request.args.get("technic", ""),
        "collection": request.args.get("collection", ""),
        "location": request.args.get("location", ""),
        "artist": request.args.get("artist", ""),
    }

    all_items = load_items()

    # Build dropdown unique sets
    materials = set()
    technics = set()
    collections = set()
    locations = set()
    artists = set()

    for obj in all_items:
        d = obj["data"]
        idx = d["index_normalized"]

        for m in safe_list(idx.get("material")):
            if isinstance(m, dict) and m.get("value"):
                materials.add(m["value"])

        for t in safe_list(idx.get("technic")):
            if isinstance(t, dict) and t.get("value"):
                technics.add(t["value"])

        if d.get("collection"):
            collections.add(d["collection"])

        if d.get("currentLocation"):
            locations.add(d["currentLocation"])

        # ---- ARTISTS FROM creator[*].label ----
        for creator in safe_list(d.get("creator")):
            if isinstance(creator, dict) and creator.get("label"):
                artists.add(creator["label"])

    items = search_items(keyword, filters)

    return render_template_string(
        TEMPLATE,
        items=items,
        materials=sorted(materials),
        technics=sorted(technics),
        collections=sorted(collections),
        locations=sorted(locations),
        artists=sorted(artists),
        request=request
    )


if __name__ == "__main__":
    print("Running on http://127.0.0.1:5000/")
    app.run(debug=True)
