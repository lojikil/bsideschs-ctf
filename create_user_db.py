import os
import sqlite3

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


USERS = [
    ("ellen", b"09ijnb4rtgb745yrhbfmcfdeiw0a@(#&", 1),
    ("becca", b"908ygiw42*ho3iu98fx", 0),
]


conn = sqlite3.connect("user.db")
c = conn.cursor()

# Make the table
c.execute("CREATE TABLE users (user text, salt blob, pass blob, admin int)")

# Create users
for username, password, admin in USERS:
    salt = os.urandom(16)
    kdf = Scrypt(salt, 32, 2**14, 8, 1, backend)
    hashed = kdf.derive(password)
    c.execute(
        "INSERT INTO users VALUES (?, ?, ?, ?)",
        [username, salt, hashed, admin]
    )

conn.commit()
