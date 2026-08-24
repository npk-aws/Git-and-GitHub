from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["flask_assignment"]
collection = db["users"]


# Task 1: JSON API Route
@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Task 2: Frontend Form
@app.route("/", methods=["GET", "POST"])
def home():
    error = None

    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")

            if not name or not email:
                raise ValueError("Name and email are required.")

            user_data = {
                "name": name,
                "email": email
            }

            collection.insert_one(user_data)

            return redirect(url_for("success"))

        except Exception as e:
            error = str(e)

    return render_template("index.html", error=error)


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
