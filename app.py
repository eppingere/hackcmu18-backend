from flask import Flask, jsonify

from quel.schedule import predict_hours

app = Flask(__name__)


@app.route("/test")
def test():
    return jsonify({
        "test": "success",
    })

@app.route("/sorted")
def sorted_things():
    return jsonify(sort_a_list([4,3,2]))


@app.route("/trainModel")
def train_model():
    print(predict_hours([], [], "fdghjk"))
    return jsonify({"success?" : True})



if __name__ == "__main__":
    app.run()
