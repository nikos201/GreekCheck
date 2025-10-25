from flask import Flask, request, jsonify
from greek_accentuation.characters import strip_accents
from greek_accentuation.accentuation import add_accent

app = Flask(__name__)

def add_tonos_auto(word):
    """
    Προσθέτει τόνο σε ελληνική λέξη (απλή εκδοχή).
    """
    w = strip_accents(word)
    vowels = [i for i, ch in enumerate(w) if ch.lower() in "αεηιουω"]
    if not vowels:
        return word
    idx = vowels[-1]  # Τονίζουμε το τελευταίο φωνήεν
    accented = add_accent(w, idx)
    if word.isupper():
        return accented.upper()
    elif word.istitle():
        return accented.capitalize()
    return accented

@app.route("/accent")
def accent():
    word = request.args.get("word", "")
    if not word:
        return jsonify({"error": "Δώσε παράμετρο ?word=λέξη"}), 400
    accented = add_tonos_auto(word)
    return jsonify({"input": word, "accented": accented})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
