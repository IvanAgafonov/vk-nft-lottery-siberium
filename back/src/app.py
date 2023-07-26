import configparser
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from threading import Lock

from flask import Flask, request
from flask import abort
from flask import jsonify
from yoyo import get_backend
from yoyo import read_migrations

from refresh import refresh
from mint import mint
from SQLiteClient import SQLiteClient

os.chdir(os.path.dirname(__file__))
app = Flask(__name__)

# Config
config = configparser.ConfigParser()
config.read("../data/config.ini")

# database
sql_client = SQLiteClient('../data/main.db')

backend = get_backend('sqlite:///../data/main.db')
migrations = read_migrations('../migrations')
with backend.lock():
    backend.apply_migrations(backend.to_apply(migrations))

# logging
handler = TimedRotatingFileHandler(filename='../data/py_log', when='midnight', backupCount=1,
                                   encoding='utf-8', delay=False)
logging.basicConfig(level=logging.INFO, handlers=[handler],
                    format="%(asctime)s %(levelname)s %(message)s")
logging.info("START")

lock = Lock()


@app.after_request
def cors(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "*"
    response.headers['Content-type'] = "application/json"

    return response


@app.route('/api/mint', methods=['POST'])
def mint_token():
    logging.info(f"mint_token {request.json}")
    with lock:
        try:
            if not request.json or 'address' not in request.json or "vkId" not in request.json:
                logging.error(f'mint_token - address or vkId is null')
                abort(400)

            if (sql_client.execute_select_one("SELECT * FROM user WHERE vkId = (?);", (int(request.json['vkId']),))
                    is not None):
                abort(418)
            else:
                user_id = sql_client.execute_insert("INSERT INTO user (vkId) VALUES (?);",
                                                    (int(request.json['vkId']),))

            token_id, metadata = mint(request.json['address'], config)
            sql_client.execute_insert("INSERT INTO nft (metadata, tokenId, creatorId, address) VALUES (?, ?, ?, ?);",
                                      (metadata, token_id, user_id, request.json['address']))
        except Exception as err:
            sql_client.execute_delete("DELETE FROM user WHERE vkId = (?);",
                                      (int(request.json['vkId']),))
            abort(500)

        response = jsonify({'tokenId': token_id})

        return response, 201


@app.route('/api/token', methods=['GET'])
def get_tokens():
    try:
        logging.info(f"get_tokens {request.args}")

        args = request.args
        address = args.get('address')
        if address is not None:
            items = sql_client.execute_select("SELECT * FROM nft WHERE address = (?);", (address, ))
        else:
            items = sql_client.execute_select("SELECT * FROM nft;")

        for item in items:
            try:
                item['metadata'] = json.loads(item['metadata'])
            except json.JSONDecodeError as err:
                logging.error(err)
            except TypeError as err:
                logging.error(err)
    except:
        abort(500)

    response = jsonify({'items': items})
    return response, 200


@app.route('/api/token/<int:token_id>', methods=['GET'])
def get_token_by_id(token_id):
    try:
        logging.info(f"get_token_by_id {token_id}")

        item = sql_client.execute_select_one("SELECT * FROM nft WHERE tokenId = (?);", (token_id, ))
        if item is not None:
            item['metadata'] = json.loads(item['metadata'])
    except:
        abort(500)

    return jsonify({'item': item}), 200


@app.route('/api/refresh', methods=['GET'])
def refresh_get():
    try:
        logging.info(f"refresh_get")

        refresh(config, sql_client)
    except:
        abort(500)

    return '', 200


if __name__ == '__main__':
    app.run()
