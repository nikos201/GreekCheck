from flask import Flask, request, Response
from greek_accentuation.characters import strip_accents
from greek_accentuation.accentuation import add_accent

app = Flask(__name__)

def add_tonos_word(word):
    w = strip_accents(word)
    vowels = [i for i, ch in enumerate(w) if ch.lower() in "αεηιουω"]
    if not vowels:
        return word
    idx = vowels[-1]
    accented = add_accent(w, idx)
    if word.isupper():
        return accented.upper()
    elif word.istitle():
        return accented.capitalize()
    return accented

def add_tonos_phrase(phrase):
    words = phrase.split()
    accented_words = [add_tonos_word(word) for word in words]
    return ' '.join(accented_words)

@app.route("/accent")
def accent():
    text = request.args.get("text", "")
    if not text:
        return Response("Δώσε παράμετρο ?text=φράση", status=400, mimetype="text/plain")
    accented = add_tonos_phrase(text)
    return Response(accented, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)