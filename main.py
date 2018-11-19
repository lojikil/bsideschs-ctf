import binascii
import json
import os
import sqlite3
import logging
import time

from waitress import serve
from cryptography.exceptions import InvalidKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from paste.translogger import TransLogger

from flask import Flask, abort, request, redirect, url_for


app = Flask(__name__)

FLAG = "Turnsoutauthenticatedencryptionmattersallthetime"
AES_KEY = os.urandom(32)


@app.route("/flag")
def admin_only():
    token = binascii.unhexlify(request.headers.get('X-AUTH-TOKEN'))
    if check_admin(token):
        return FLAG
    else:
        abort(403, "missing X-AUTH-TOKEN header?")


@app.route("/api-token", methods=["POST"])
def api_token():
    user = request.form["user"]
    password = request.form["password"].encode("utf8")
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    result = c.execute(
        "SELECT salt, pass, admin from users where user=?", [user]
    ).fetchone()
    conn.close()
    if result is None:
        abort(403)

    salt, spass, admin = result
    kdf = Scrypt(
        salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend()
    )
    try:
        kdf.verify(password, spass)
    except InvalidKey:
        print("invalid password")
        abort(403)

    payload = json.dumps({"admin": admin, "user": user}, sort_keys=True)
    # encrypt the payload
    return _encrypt(payload)

def _encrypt(payload):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CTR(iv), default_backend())
    enc = cipher.encryptor()
    return binascii.hexlify(
        iv + enc.update(payload.encode("ascii")) + enc.finalize()
    )


def check_admin(token):
    iv = token[:16]
    data = token[16:]
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CTR(iv), default_backend())
    dec = cipher.decryptor()
    blob = dec.update(data) + dec.finalize()
    user = json.loads(blob.decode("ascii"))
    return user["admin"] == 1

@app.route("/login")
def login():
    return redirect("/")

@app.route("/hint")
def hint():
	return """<pre>
@app.route("/flag")
def admin_only():
    token = binascii.unhexlify(request.headers.get('X-AUTH-TOKEN'))
    if check_admin(token):
        return FLAG
    else:
        abort(403, "missing X-AUTH-TOKEN header?")


@app.route("/api-token", methods=["POST"])
def api_token():
    user = request.form["user"]
    password = request.form["password"].encode("utf8")
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    result = c.execute(
        "SELECT salt, pass, admin from users where user=?", [user]
    ).fetchone()
    conn.close()
    if result is None:
        abort(403)

    salt, spass, admin = result
    kdf = Scrypt(
        salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend()
    )
    try:
        kdf.verify(password, spass)
    except InvalidKey:
        print("invalid password")
        abort(403)

    payload = json.dumps({"admin": admin, "user": user}, sort_keys=True)
    # encrypt the payload
    return _encrypt(payload)

def _encrypt(payload):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CTR(iv), default_backend())
    enc = cipher.encryptor()
    return binascii.hexlify(
        iv + enc.update(payload.encode("ascii")) + enc.finalize()
    )


def check_admin(token):
    iv = token[:16]
    data = token[16:]
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CTR(iv), default_backend())
    dec = cipher.decryptor()
    blob = dec.update(data) + dec.finalize()
    user = json.loads(blob.decode("ascii"))
    return user["admin"] == 1
    </pre>"""


@app.route("/")
def main():
        return """
<html>
  <head>
    <title>Login</title>
  </head>
  <body>
    <h1>Login</h1>
    <h3>Server Error</h3>
    <p> hey sorry, the crypto server is closed, there's no CTF this year. <b>BUT</b> you could probably do something bad
    by POSTing to /api-token with user=becca and password=908ygiw42*ho3iu98fx
   <br>
   There's also probably some sort of like /flag thing, idek. Maybe even /hint works
    </p>
    <pre>written by <a href="https://twitter.com/reaperhulk">reaperhulk</a>,
ruined by <a href="https://twitter.com/lojikil">lojikil</a>, artisanally up-cycled
for <a href="https://twitter.com/bsideschs">BSides Charleston</a>. Find lojikil (green VOLUNTEER shirt) if you find the flag.
    </pre>
    <address>SeriousServer v.6ce32b9c-56e8-44cd-b6c9-1feb181c8e0d</address>
    <i>Also, need help with your crypto for realises? Trail of Bits: <a href="https://blog.trailofbits.com/2018/11/07/we-crypto-now/">We crypto now.</a></i>
  </body>
</html>"""


if __name__ == "__main__":
    start_stamp = time.ctime().replace(' ', '-')
    logger = logging.getLogger('wsgi')
    logger.setLevel(logging.INFO)
    ch = logging.FileHandler("logs/wsgi-{0}.log".format(start_stamp))
    logger.addHandler(ch)
    serve(TransLogger(app), listen="0.0.0.0:8080")
