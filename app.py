import os
import uuid
import datetime as dt

from flask import Flask, jsonify, request, render_template
from bson.objectid import ObjectId

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Database layer
# ---------------------------------------------------------------------------
# If MONGO_URI is set (Render env var / Atlas connection string) we use real
# MongoDB via PyMongo. Otherwise we fall back to a tiny in-memory store with
# the same interface, so the app runs locally / in a demo with zero setup.
# ---------------------------------------------------------------------------

MONGO_URI = os.environ.get("MONGO_URI", "").strip()
USE_MONGO = bool(MONGO_URI)

if USE_MONGO:
    from pymongo import MongoClient

    client = MongoClient(MONGO_URI)
db = client["crm_db"]
    customers_col = db["customers"]
    leads_col = db["leads"]
    deals_col = db["deals"]
    tasks_col = db["tasks"]
    events_col = db["events"]
else:
    class MemoryCollection:
        """Minimal drop-in stand-in for a pymongo Collection, in-memory only."""

        def __init__(self):
            self._docs = {}

        def insert_one(self, doc):
            _id = str(uuid.uuid4())
            doc = dict(doc)
            doc["_id"] = _id
            self._docs[_id] = doc
            return type("Result", (), {"inserted_id": _id})

        def find(self, query=None):
            query = query or {}
            return [d for d in self._docs.values() if _matches(d, query)]

        def find_one(self, query):
            for d in self._docs.values():
                if _matches(d, query):
                    return d
            return None

        def update_one(self, query, update):
            doc = self.find_one(query)
            if not doc:
                return type("Result", (), {"matched_count": 0})
            doc.update(update.get("$set", {}))
            return type("Result", (), {"matched_count": 1})

        def delete_one(self, query):
            doc = self.find_one(query)
            if doc:
                del self._docs[doc["_id"]]
                return type("Result", (), {"deleted_count": 1})
            return type("Result", (), {"deleted_count": 0})

        def count_documents(self, query=None):
            return len(self.find(query or {}))

    def _matches(doc, query):
        for k, v in query.items():
            if doc.get(k) != v:
                return False
        return True

    customers_col = MemoryCollection()
    leads_col = MemoryCollection()
    deals_col = MemoryCollection()
    tasks_col = MemoryCollection()
    events_col = MemoryCollection()

    # ---- seed demo data so the UI has something to show immediately -------
    def _seed():
        now = dt.datetime.utcnow()
        c1 = customers_col.insert_one({
            "name": "Aria Fernando", "company": "Lotus Textiles", "email": "aria@lotustex.lk",
            "phone": "+94 77 123 4567", "tags": ["VIP", "Retail"], "created_at": now.isoformat()
        }).inserted_id
        c2 = customers_col.insert_one({
            "name": "Devon Marsh", "company": "Marsh & Co", "email": "devon@marshco.com",
            "phone": "+1 415 555 0192", "tags": ["Enterprise"], "created_at": now.isoformat()
        }).inserted_id
        c3 = customers_col.insert_one({
            "name": "Priya Nair", "company": "Nair Foods", "email": "priya@nairfoods.in",
            "phone": "+91 98 4567 1230", "tags": ["Wholesale", "Repeat"], "created_at": now.isoformat()
        }).inserted_id

        leads_col.insert_one({"name": "Kavindu Silva", "email": "kavindu@brightgoods.lk", "source": "Website",
                               "status": "new", "value": 4200, "created_at": now.isoformat()})
        leads_col.insert_one({"name": "Elena Torres", "email": "elena@torresretail.com", "source": "Referral",
                               "status": "contacted", "value": 8600, "created_at": now.isoformat()})
        leads_col.insert_one({"name": "Sam Okafor", "email": "sam@okaforlogistics.com", "source": "LinkedIn",
                               "status": "qualified", "value": 15300, "created_at": now.isoformat()})
        leads_col.insert_one({"name": "Mira Chen", "email": "mira@chenapparel.com", "source": "Trade show",
                               "status": "lost", "value": 3000, "created_at": now.isoformat()})

        deals_col.insert_one({"title": "Lotus Textiles — Q3 restock", "customer_id": c1, "stage": "proposal",
                               "value": 12500, "created_at": now.isoformat()})
        deals_col.insert_one({"title": "Marsh & Co — annual contract", "customer_id": c2, "stage": "negotiation",
                               "value": 48200, "created_at": now.isoformat()})
        deals_col.insert_one({"title": "Nair Foods — new SKU line", "customer_id": c3, "stage": "new",
                               "value": 9800, "created_at": now.isoformat()})
        deals_col.insert_one({"title": "Marsh & Co — pilot order", "customer_id": c2, "stage": "won",
                               "value": 6200, "created_at": now.isoformat()})

        tasks_col.insert_one({"title": "Call Aria re: restock timeline", "due_date": (now + dt.timedelta(days=1)).date().isoformat(),
                               "done": False, "related_to": "Lotus Textiles"})
        tasks_col.insert_one({"title": "Send proposal to Marsh & Co", "due_date": (now + dt.timedelta(days=2)).date().isoformat(),
                               "done": False, "related_to": "Marsh & Co"})
        tasks_col.insert_one({"title": "Follow up with Sam Okafor", "due_date": (now - dt.timedelta(days=1)).date().isoformat(),
                               "done": False, "related_to": "Sam Okafor"})
        tasks_col.insert_one({"title": "Log Nair Foods call notes", "due_date": now.date().isoformat(),
                               "done": True, "related_to": "Nair Foods"})

        events_col.insert_one({"title": "Discovery call — Kavindu Silva", "date": now.date().isoformat(), "time": "10:00", "type": "call"})
        events_col.insert_one({"title": "Contract review — Marsh & Co", "date": (now + dt.timedelta(days=1)).date().isoformat(), "time": "14:30", "type": "meeting"})
        events_col.insert_one({"title": "Demo — Nair Foods", "date": (now + dt.timedelta(days=3)).date().isoformat(), "time": "11:00", "type": "demo"})

    _seed()


def serialize(doc):
    if not doc:
        return doc
    doc = dict(doc)
    doc["_id"] = str(doc["_id"])
    return doc


def serialize_many(docs):
    return [serialize(d) for d in docs]


def oid_query(id_str):
    """Build a query dict that matches _id whether Mongo ObjectId or memory-store uuid string."""
    if USE_MONGO:
        try:
            return {"_id": ObjectId(id_str)}
        except Exception:
            return {"_id": id_str}
    return {"_id": id_str}


# ---------------------------------------------------------------------------
# Routes — pages
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok", "db": "mongodb" if USE_MONGO else "in-memory-demo"})


# ---------------------------------------------------------------------------
# Routes — API: Customers
# ---------------------------------------------------------------------------

@app.route("/api/customers", methods=["GET", "POST"])
def customers():
    if request.method == "POST":
        data = request.get_json(force=True)
        data["created_at"] = dt.datetime.utcnow().isoformat()
        data.setdefault("tags", [])
        result = customers_col.insert_one(data)
        return jsonify(serialize(customers_col.find_one(oid_query(str(result.inserted_id))))), 201
    return jsonify(serialize_many(customers_col.find({})))


@app.route("/api/customers/<cid>", methods=["PUT", "DELETE"])
def customer_detail(cid):
    if request.method == "DELETE":
        customers_col.delete_one(oid_query(cid))
        return jsonify({"ok": True})
    data = request.get_json(force=True)
    customers_col.update_one(oid_query(cid), {"$set": data})
    return jsonify(serialize(customers_col.find_one(oid_query(cid))))


# ---------------------------------------------------------------------------
# Routes — API: Leads
# ---------------------------------------------------------------------------

@app.route("/api/leads", methods=["GET", "POST"])
def leads():
    if request.method == "POST":
        data = request.get_json(force=True)
        data["created_at"] = dt.datetime.utcnow().isoformat()
        data.setdefault("status", "new")
        result = leads_col.insert_one(data)
        return jsonify(serialize(leads_col.find_one(oid_query(str(result.inserted_id))))), 201
    return jsonify(serialize_many(leads_col.find({})))


@app.route("/api/leads/<lid>", methods=["PUT", "DELETE"])
def lead_detail(lid):
    if request.method == "DELETE":
        leads_col.delete_one(oid_query(lid))
        return jsonify({"ok": True})
    data = request.get_json(force=True)
    leads_col.update_one(oid_query(lid), {"$set": data})
    return jsonify(serialize(leads_col.find_one(oid_query(lid))))


# ---------------------------------------------------------------------------
# Routes — API: Pipeline (deals)
# ---------------------------------------------------------------------------

@app.route("/api/deals", methods=["GET", "POST"])
def deals():
    if request.method == "POST":
        data = request.get_json(force=True)
        data["created_at"] = dt.datetime.utcnow().isoformat()
        data.setdefault("stage", "new")
        result = deals_col.insert_one(data)
        return jsonify(serialize(deals_col.find_one(oid_query(str(result.inserted_id))))), 201
    return jsonify(serialize_many(deals_col.find({})))


@app.route("/api/deals/<did>", methods=["PUT", "DELETE"])
def deal_detail(did):
    if request.method == "DELETE":
        deals_col.delete_one(oid_query(did))
        return jsonify({"ok": True})
    data = request.get_json(force=True)
    deals_col.update_one(oid_query(did), {"$set": data})
    return jsonify(serialize(deals_col.find_one(oid_query(did))))


# ---------------------------------------------------------------------------
# Routes — API: Tasks
# ---------------------------------------------------------------------------

@app.route("/api/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        data = request.get_json(force=True)
        data.setdefault("done", False)
        result = tasks_col.insert_one(data)
        return jsonify(serialize(tasks_col.find_one(oid_query(str(result.inserted_id))))), 201
    return jsonify(serialize_many(tasks_col.find({})))


@app.route("/api/tasks/<tid>", methods=["PUT", "DELETE"])
def task_detail(tid):
    if request.method == "DELETE":
        tasks_col.delete_one(oid_query(tid))
        return jsonify({"ok": True})
    data = request.get_json(force=True)
    tasks_col.update_one(oid_query(tid), {"$set": data})
    return jsonify(serialize(tasks_col.find_one(oid_query(tid))))


# ---------------------------------------------------------------------------
# Routes — API: Calendar events
# ---------------------------------------------------------------------------

@app.route("/api/events", methods=["GET", "POST"])
def events():
    if request.method == "POST":
        data = request.get_json(force=True)
        result = events_col.insert_one(data)
        return jsonify(serialize(events_col.find_one(oid_query(str(result.inserted_id))))), 201
    return jsonify(serialize_many(events_col.find({})))


@app.route("/api/events/<eid>", methods=["DELETE"])
def event_detail(eid):
    events_col.delete_one(oid_query(eid))
    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# Routes — API: Reports (aggregated on the fly)
# ---------------------------------------------------------------------------

@app.route("/api/reports/summary")
def reports_summary():
    all_leads = serialize_many(leads_col.find({}))
    all_deals = serialize_many(deals_col.find({}))
    all_tasks = serialize_many(tasks_col.find({}))
    all_customers = serialize_many(customers_col.find({}))

    stages = ["new", "proposal", "negotiation", "won", "lost"]
    pipeline_by_stage = {s: {"count": 0, "value": 0} for s in stages}
    for d in all_deals:
        s = d.get("stage", "new")
        pipeline_by_stage.setdefault(s, {"count": 0, "value": 0})
        pipeline_by_stage[s]["count"] += 1
        pipeline_by_stage[s]["value"] += float(d.get("value", 0) or 0)

    lead_statuses = ["new", "contacted", "qualified", "lost"]
    leads_by_status = {s: 0 for s in lead_statuses}
    for l in all_leads:
        s = l.get("status", "new")
        leads_by_status[s] = leads_by_status.get(s, 0) + 1

    won_value = pipeline_by_stage.get("won", {}).get("value", 0)
    open_value = sum(v["value"] for k, v in pipeline_by_stage.items() if k not in ("won", "lost"))

    today = dt.date.today().isoformat()
    overdue_tasks = sum(1 for t in all_tasks if not t.get("done") and t.get("due_date", "9999") < today)
    open_tasks = sum(1 for t in all_tasks if not t.get("done"))

    return jsonify({
        "customers_count": len(all_customers),
        "leads_count": len(all_leads),
        "deals_count": len(all_deals),
        "pipeline_by_stage": pipeline_by_stage,
        "leads_by_status": leads_by_status,
        "won_value": won_value,
        "open_value": open_value,
        "open_tasks": open_tasks,
        "overdue_tasks": overdue_tasks,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
