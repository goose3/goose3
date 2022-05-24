from flask import Flask, jsonify
from api.routes import api
from os import environ
from werkzeug.routing import BaseConverter


class WildcardConverter(BaseConverter):
    regex = r".*?"
    weight = 200


app = Flask(__name__)
app.url_map.converters["wildcard"] = WildcardConverter


@app.route("/")
def route_default_():
    return "<h1>Welcome to duck-goose API''s</h1>"


app.register_blueprint(api)

if __name__ == "__main__":
    port = int(environ.get("PORT", 5001))
    app.debug = True
    app.run(host="0.0.0.0", port=port)
