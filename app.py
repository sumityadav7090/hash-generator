from flask import Flask, request, jsonify, render_template_string
import hashlib
import bcrypt
import argon2
import xxhash
import blake3
from Crypto.Hash import Whirlpool, RIPEMD160, Tiger, GOST

app = Flask(__name__)

@app.route("/")
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return render_template_string(f.read())

@app.route("/generate", methods=["POST"])
def generate_hashes():
    text = request.json.get("text", "")
    data = text.encode('utf-8')
    result = {}

    try:
        algorithms = [
            'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
            'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
            'blake2b', 'blake2s'
        ]
        for algo in algorithms:
            h = hashlib.new(algo)
            h.update(data)
            result[algo.upper()] = h.hexdigest()

        result['SHAKE128'] = hashlib.shake_128(data).hexdigest(64)
        result['SHAKE256'] = hashlib.shake_256(data).hexdigest(64)

        result['BCRYPT'] = bcrypt.hashpw(data, bcrypt.gensalt()).decode()

        ph = argon2.PasswordHasher()
        result['ARGON2'] = ph.hash(text)

        result['XXH32'] = xxhash.xxh32(data).hexdigest()
        result['XXH64'] = xxhash.xxh64(data).hexdigest()
        result['XXH128'] = xxhash.xxh3_128(data).hexdigest()

        result['BLAKE3'] = blake3.blake3(data).hexdigest()
        result['WHIRLPOOL'] = Whirlpool.new(data).hexdigest()
        result['RIPEMD160'] = RIPEMD160.new(data).hexdigest()
        result['TIGER'] = Tiger.new(data).hexdigest()
        result['GOST'] = GOST.new(data).hexdigest()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
