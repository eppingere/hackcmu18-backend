from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/test")
def test():
    return jsonify({
        "test": "success",
    })


if __name__ == "__main__":
    app.run()
