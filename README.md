# Overview

People participating in the CTF should be given `main.py` along with the following valid username and password:

user: becca
password: 908ygiw42*ho3iu98fx

Additional information:

* The database table is structured as: CREATE TABLE users (user text, salt blob, pass blob, admin int)
* There are two users, becca (non-admin), and ellen (admin).
* You can give the entire user.db file to the participants. ellen is just misdirection as there's no need to care about that user to gain admin access

Server runs on port 5000 in the container, so `docker run --rm -p 80:5000 csaw` will give you a port 80 server.

# Loji's Mods

- using waitress
- logging
- added an actual `/login` route

