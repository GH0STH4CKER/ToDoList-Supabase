from flask import Flask, render_template, request, jsonify
from supabase import create_client

#------------------------------
SUPABASE_URL = "https://vvukbjtvmlnhnkkxnsyc.supabase.co"
SUPABASE_KEY = ""
#-----------------------------
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# -----------------------------

@app.route("/")
def index():
    return render_template("index.html")

# ----------------------------
@app.route("/todos", methods=["GET"])
def get_todos():
    rows = supabase.table("todos").select("*").order("id").execute()
    return jsonify(rows.data if hasattr(rows, "data") else rows)

# ----------------------------
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title required"}), 400
    new_row = {"title": title, "done": False}
    res = supabase.table("todos").insert(new_row).execute()
    return jsonify(res.data if hasattr(res, "data") else res), 201

# ----------------------------
@app.route("/todos/<int:todo_id>", methods=["PATCH"])
def update_todo(todo_id):
    data = request.json
    updates = {}
    if "title" in data:
        updates["title"] = data["title"]
    if "done" in data:
        updates["done"] = bool(data["done"])
    if not updates:
        return jsonify({"error": "No fields to update"}), 400
    res = supabase.table("todos").update(updates).eq("id", todo_id).execute()
    return jsonify(res.data if hasattr(res, "data") else res)

# ----------------------------
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    res = supabase.table("todos").delete().eq("id", todo_id).execute()
    return jsonify(res.data if hasattr(res, "data") else res)

# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
