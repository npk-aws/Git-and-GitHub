from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["todo_database"]
collection = db["todo_items"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    try:
        item_name = request.form.get("itemName")
        item_description = request.form.get("itemDescription")

        if not item_name or not item_description:
            return render_template(
                "index.html",
                error="Item Name and Item Description are required."
            )

        todo_item = {
            "itemName": item_name,
            "itemDescription": item_description
        }

        collection.insert_one(todo_item)

        return redirect(url_for("success"))

    except Exception as e:
        return render_template(
            "index.html",
            error=str(e)
        )


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
