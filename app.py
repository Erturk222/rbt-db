from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from rbt import RedBlackTree

app = Flask(__name__)
CORS(app)

db = RedBlackTree()

def parse_query(query: str) -> dict:
    parts = query.strip().split(None, 2)
    if not parts:
        return {"error": "Empty query"}

    cmd = parts[0].upper()

    if cmd == "SET":
        if len(parts) < 3:
            return {"error": "Usage: SET <key> <value>"}
        key = parts[1]
        value = parts[2]
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        db.clear_log()
        result = db.insert(key, value)
        result["tree"] = db.to_dict()
        result["log"] = db._operation_log[:]
        result["size"] = db.size()
        return result

    elif cmd == "GET":
        if len(parts) < 2:
            return {"error": "Usage: GET <key>"}
        db.clear_log()
        result = db.search(parts[1])
        result["tree"] = db.to_dict()
        result["log"] = db._operation_log[:]
        return result

    elif cmd == "DEL":
        if len(parts) < 2:
            return {"error": "Usage: DEL <key>"}
        db.clear_log()
        result = db.delete(parts[1])
        result["tree"] = db.to_dict()
        result["log"] = db._operation_log[:]
        result["size"] = db.size()
        return result

    elif cmd == "KEYS":
        return {"keys": db.all_keys(), "tree": db.to_dict()}

    elif cmd == "VERIFY":
        result = db.full_verify()
        result["tree"] = db.to_dict()
        return result

    elif cmd == "CLEAR":
        db.__init__()
        return {"action": "clear", "message": "Database cleared", "tree": None}

    elif cmd == "INFO":
        verify = db.full_verify()
        return {
            "size": db.size(),
            "black_height": verify["black_height"],
            "valid": verify["valid"],
            "tree": db.to_dict(),
        }

    else:
        return {"error": f"Unknown command: {cmd}"}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/query", methods=["POST"])
def query():
    data = request.get_json()
    q = data.get("query", "")
    result = parse_query(q)
    return jsonify(result)

@app.route("/api/tree", methods=["GET"])
def get_tree():
    return jsonify({"tree": db.to_dict(), "size": db.size()})

@app.route("/api/verify", methods=["GET"])
def verify():
    return jsonify(db.full_verify())

if __name__ == "__main__":
    print("RBT.db çalışıyor → http://localhost:5000")
    app.run(debug=True, port=5000)