import json
from flask import Flask
from config import BaseConfig
from db import initialize_db
from api import initialize_api
from parser import import_users

app = Flask(__name__)
app.config.from_object(BaseConfig)

initialize_db(app)

initialize_api(app)

@app.before_first_request
def before_first_request():
    print("[INFO] Importing users...")
    import_users()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
