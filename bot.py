import sqlite3
import random
import os
from flask import Flask, request

app = Flask(__name__)

# Database setup - Railway তে /data ব্যবহার করলে ভুলবে না
DB = "/data/memory.db"

conn = sqlite3.connect(DB, check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS knowledge (q TEXT PRIMARY KEY, a TEXT)''')
conn.commit()

# Funny attitude replies
FUNNY_REPLIES = [
    "আরে ভাই আমি কি গুগল নাকি? জানি না তো 😑",
    "এই প্রশ্ন শুনে আমার ব্রেন হ্যাং হয়ে গেলো। teach: প্রশ্ন|উত্তর লিখে শিখায় দাও",
    "আমার মাথায় এটা নাই রে। তুমি শিখায় দিলে মনে রাখবো সারাজীবন",
    "চুপ করো তো, এত কঠিন প্রশ্ন করো কেন? শিখায় দাও আগে",
    "আমি কি সবজান্তা শমসের নাকি? জানি না। শিখাও আমাকে"
]

ATTITUDE_REPLIES = [
    "হ্যাঁ বলো, আবার কি সমস্যা?",
    "আবার তুমি? কি হইছে?",
    "বলো শুনতেছি, বেশি প্যাঁচাল পাইরো না",
    "হুম বলো..."
]

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return request.args.get("hub.challenge", "")

    data = request.get_json()
    msg = data.get("message", "").lower().strip()

    if not msg:
        return "ok"

    # TEACH SYSTEM
    if msg.startswith("teach:"):
        try:
            parts = msg[6:].split("|")
            q, a = parts[0].strip(), parts[1].strip()
            c.execute("INSERT OR REPLACE INTO knowledge(q,a) VALUES(?,?)", (q,a))
            conn.commit()
            return f"ঠিক আছে, শিখে নিলাম। এখন থেকে '{q}' জিজ্ঞাস করলে '{a}' বলবো 🔥"
        except:
            return "ভুল ফরম্যাট। লিখো: teach: প্রশ্ন|উত্তর"

    # CHECK KNOWLEDGE
    c.execute("SELECT a FROM knowledge WHERE q=?", (msg,))
    row = c.fetchone()
    if row:
        return row[0]

    # FUNNY ATTITUDE RESPONSE
    if "hi" in msg or "hello" in msg or "হাই" in msg:
        return random.choice(ATTITUDE_REPLIES)

    return random.choice(FUNNY_REPLIES)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
