from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfari import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

#router routes for home page
@app.route("/")
def home():
    return render_template('index.html')

#router routes for caesar cipher
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return render_template('caesar.html', encrypt_result=f"Encrypted: {encrypted_text}")

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return render_template('caesar.html', decrypt_result=f"Decrypted: {decrypted_text}")

# VIGENERE
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKey']
    vc = VigenereCipher()
    result = vc.vigenere_encrypt(text, key)
    return render_template('vigenere.html', encrypt_result=f"Encrypted: {result}")

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKey']
    vc = VigenereCipher()
    result = vc.vigenere_decrypt(text, key)
    return render_template('vigenere.html', decrypt_result=f"Decrypted: {result}")

# RAILFENCE
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKey'])
    rc = RailFenceCipher()
    result = rc.rail_fence_encrypt(text, key)
    return render_template('railfence.html', encrypt_result=f"Encrypted: {result}")

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKey'])
    rc = RailFenceCipher()
    result = rc.rail_fence_decrypt(text, key)
    return render_template('railfence.html', decrypt_result=f"Decrypted: {result}")

# PLAYFAIR
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKey']
    pc = PlayFairCipher()
    matrix = pc.create_playfair_matrix(key)
    result = pc.playfair_encrypt(text, matrix)
    return render_template('playfair.html', encrypt_result=f"Encrypted: {result}")

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKey']
    pc = PlayFairCipher()
    matrix = pc.create_playfair_matrix(key)
    result = pc.playfair_decrypt(text, matrix)
    return render_template('playfair.html', decrypt_result=f"Decrypted: {result}")

# TRANSPOSITION
@app.route("/transposition")
def transposition():
    return render_template('transposition.html')

@app.route("/transposition/encrypt", methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKey'])
    tc = TranspositionCipher()
    result = tc.encrypt(text, key)
    return render_template('transposition.html', encrypt_result=f"Encrypted: {result}")

@app.route("/transposition/decrypt", methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKey'])
    tc = TranspositionCipher()
    result = tc.decrypt(text, key)
    return render_template('transposition.html', decrypt_result=f"Decrypted: {result}")

#main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)