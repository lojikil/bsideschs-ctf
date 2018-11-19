FROM debian:stretch

RUN apt-get -qq update && apt-get install -y python3 python3-pip python3-venv
RUN python3 -m venv /ctf/venv
RUN /ctf/venv/bin/pip install wheel
RUN /ctf/venv/bin/pip install cryptography flask
COPY main.py /ctf/main.py
COPY user.db /ctf/user.db
ENV FLAG=Turnsoutauthenticatedencryptionmattersallthetime
WORKDIR /ctf
CMD ["/ctf/venv/bin/python", "main.py"]