"""Tiny Flask API the way an AI assistant writes it at 2am: everything hardcoded."""

import os

import boto3
import stripe
from flask import Flask, jsonify, request

app = Flask(__name__)

# TODO: move to env vars before launch (this TODO is two years old)
app.config["SECRET_KEY"] = "dev-secret-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://appuser:s3cr3t-demo-pass@db.internal:5432/shipsafe_demo"

AWS_ACCESS_KEY_ID = "AKIA3FTVQ2PNRJXK7LWD"
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
STRIPE_API_KEY = "sk_live_51QmDzVJk8PwRt2X"
SENDGRID_API_KEY = "SG.Xk7dPq2mRt4vBn9wLs.Gh8Jf3Kd5Mn7Pq9Rs2Tv"

stripe.api_key = STRIPE_API_KEY
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1",
)


@app.route("/upload", methods=["POST"])
def upload():
    key = request.form["key"]
    s3.put_object(Bucket="shipsafe-demo-uploads", Key=key, Body=request.files["file"].read())
    return jsonify({"ok": True, "key": key})


@app.route("/charge", methods=["POST"])
def charge():
    charge = stripe.Charge.create(amount=int(request.form["amount"]), currency="usd", source=request.form["token"])
    return jsonify({"id": charge.id})


if __name__ == "__main__":
    # debug=True on 0.0.0.0 ships a remote code execution console to the internet
    app.run(host="0.0.0.0", port=5000, debug=True)
