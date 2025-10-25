from flask import Flask, request, Response
from greek_accentuation.characters import strip_accents
from greek_accentuation.accentuation import add_accent
from urllib.parse import unquote

app = Flask(__name__)

def add_tonos_word(word):
    """
    Προσθέτει τόνο σε μία ελληνική λέξη.
    Αν δεν μπορεί, επιστρέφει την ίδια λέξη.
    """
    from greek_accentuation.characters import strip_accents
    from greek_accentuation.accentuation import add_accent

    w = strip_accents(word)
    vowels = [i for i, ch in enumerate(w) if ch.lower() in "αεηιουω"]
    if not vowels:
        return word
    idx = vowels[-1]
    try:
        accented = add_accent(w, idx)
    except Exception:
        return word  # Αν υπάρξει σφάλμα, επιστρέφουμε τη λέξη όπως είναι
    if word.isupper():
        return accented.upper()
    elif word.istitle():
        return accented.capitalize()
    return accented

def add_tonos_phrase(phrase):
    """
    Τονίζει κάθε λέξη της φράσης
    """
    words = phrase.split()
    accented_words = [add_tonos_word(word) for word in words]
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
    
    # Αποκωδικοποίηση URL (σε περίπτωση που δεν είναι σωστά encoded)
    decoded_text = unquote(raw_text)
    
    accented = add_tonos_phrase(decoded_text)
    return Response(accented.encode('utf-8'), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
