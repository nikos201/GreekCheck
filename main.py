from flask import Flask, request, Response
from greek_accentuation.characters import strip_accents
from greek_accentuation.accentuation import add_accent
from urllib.parse import unquote
import json
import os

app = Flask(__name__)

# Φόρτωση λεξικού από JSON
LEXICON_FILE = os.path.join(os.path.dirname(__file__), "lexicon.json")
if os.path.exists(LEXICON_FILE):
    with open(LEXICON_FILE, encoding="utf-8") as f:
        lexicon = json.load(f)
else:
    lexicon = {}

def add_tonos_word(word):
    """
    Προσθέτει τόνο σε μία ελληνική λέξη.
    Αν υπάρχει στο λεξικό επιστρέφει τονισμένη μορφή.
    Αν όχι, χρησιμοποιεί greek-accentuation (fallback).
    """
    # Έλεγχος λεξικού
    key = word.lower()
    if key in lexicon:
        return lexicon[key]

    # Fallback στη βιβλιοθήκη
    w = strip_accents(word)
    vowels = [i for i, ch in enumerate(w) if ch.lower() in "αεηιουω"]
    if not vowels:
        return word
    idx = vowels[-1]
    try:
        accented = add_accent(w, idx)
    except Exception:
        return word
    if word.isupper():
        return accented.upper()
    elif word.istitle():
        return accented.capitalize()
    return accented

def add_tonos_phrase(phrase):
    words = phrase.strip().split()
    accented_words = [add_tonos_word(word.strip()) for word in words]
    return ' '.join(accented_words)

@app.route("/")
def home():
    return Response(
        "Greek Tonos API is running! Χρησιμοποίησε /accent?text=φράση",
        mimetype="text/plain"
    )

@app.route("/accent")
def accent():
    raw_text = request.args.get("text", "")
    if not raw_text:
        return Response("Δώσε παράμετρο ?text=φράση", status=400, mimetype="text/plain")

    decoded_text = unquote(raw_text)
    accented = add_tonos_phrase(decoded_text)
    return Response(accented.encode('utf-8'), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
