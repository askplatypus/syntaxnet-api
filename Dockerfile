FROM gliacloud/syntaxnet

COPY * /usr/src/api/
RUN cd /usr/src/api && pip install -r requirements.txt

ENV PORT 7000
EXPOSE $PORT

CMD cd /usr/src/api && gunicorn -w 4 flask_server:app