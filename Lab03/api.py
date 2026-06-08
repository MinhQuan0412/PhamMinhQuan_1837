from flask import Flask, request, jsonify
from cipher.ecc.ecc_cipher import ECCCipher
from cipher.rsa.rsa_cipher import RSACipher
import binascii

app = Flask(__name__)
ecc = ECCCipher()
rsa = RSACipher()

@app.route('/ecc/generate', methods=['GET'])
def generate_keys():
    try:
        ecc.generate_keys()
        return jsonify({'message': 'Keys generated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ecc/sign', methods=['POST'])
def sign():
    try:
        data = request.get_json()
        message = data.get('message', '')
        if not message:
            return jsonify({'error': 'message is required'}), 400

        sk, vk = ecc.load_keys()
        signature = ecc.sign(message, sk)
        # Chuyển bytes sang hex string để trả về JSON
        sig_hex = binascii.hexlify(signature).decode('ascii')
        return jsonify({'signature': sig_hex}), 200
    except FileNotFoundError:
        return jsonify({'error': 'Keys not found. Please generate keys first.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ecc/verify', methods=['POST'])
def verify():
    try:
        data = request.get_json()
        message = data.get('message', '')
        sig_hex = data.get('signature', '')
        if not message or not sig_hex:
            return jsonify({'error': 'message and signature are required'}), 400

        # Chuyển hex string về bytes
        signature = binascii.unhexlify(sig_hex)
        result = ecc.verify(message, signature, None)
        return jsonify({'valid': bool(result)}), 200
    except FileNotFoundError:
        return jsonify({'error': 'Keys not found. Please generate keys first.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== RSA ENDPOINTS ==========

@app.route('/rsa/generate', methods=['GET'])
def rsa_generate_keys():
    try:
        rsa.generate_keys()
        return jsonify({'message': 'RSA keys generated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    try:
        data = request.get_json()
        plain_text = data.get('plain_text', '')
        if not plain_text:
            return jsonify({'error': 'plain_text is required'}), 400

        encrypted_bytes = rsa.encrypt(plain_text)
        cipher_text = binascii.hexlify(encrypted_bytes).decode('ascii')
        return jsonify({'cipher_text': cipher_text}), 200
    except FileNotFoundError:
        return jsonify({'error': 'Keys not found. Please generate keys first.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    try:
        data = request.get_json()
        cipher_text = data.get('cipher_text', '')
        if not cipher_text:
            return jsonify({'error': 'cipher_text is required'}), 400

        cipher_bytes = binascii.unhexlify(cipher_text)
        plain_text = rsa.decrypt(cipher_bytes)
        return jsonify({'plain_text': plain_text}), 200
    except FileNotFoundError:
        return jsonify({'error': 'Keys not found. Please generate keys first.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rsa/sign', methods=['POST'])
def rsa_sign():
    try:
        data = request.get_json()
        message = data.get('message', '')
        if not message:
            return jsonify({'error': 'message is required'}), 400

        signature = rsa.sign(message)
        sig_hex = binascii.hexlify(signature).decode('ascii')
        return jsonify({'signature': sig_hex}), 200
    except FileNotFoundError:
        return jsonify({'error': 'Keys not found. Please generate keys first.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rsa/verify', methods=['POST'])
def rsa_verify():
    try:
        data = request.get_json()
        message = data.get('message', '')
        sig_hex = data.get('signature', '')
        if not message or not sig_hex:
            return jsonify({'error': 'message and signature are required'}), 400

        signature = binascii.unhexlify(sig_hex)
        result = rsa.verify(message, signature)
        return jsonify({'valid': result}), 200
    except FileNotFoundError:
        return jsonify({'error': 'Keys not found. Please generate keys first.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000)
