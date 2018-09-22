from datetime import datetime

from flask import Flask, jsonify, request

import rethinkdb as r
from quel.models import Assignment, Availability, Course, from_iso, to_iso
from quel.schedule import predict_hours, schedule

app = Flask(__name__)
conn = r.connect(db='quel')


@app.route("/availability/<uuid>", methods=['GET'])
def availability(uuid):
    return jsonify(r.table('availability').get(uuid).run(conn))


@app.route("/availability", methods=['POST'])
def post_availability():
    uuid = r.table('availability') \
            .insert(request.json) \
            .run(conn)['generated_keys'][0]

    return jsonify(r.table('availability').get(uuid).run(conn))


@app.route("/course/<uuid>", methods=['GET'])
def course(uuid):
    return jsonify(r.table('course').get(uuid).run(conn))


@app.route("/course", methods=['POST'])
def post_course():
    uuid = r.table('course') \
            .insert(request.json) \
            .run(conn)['generated_keys'][0]

    return jsonify(r.table('course').get(uuid).run(conn))


@app.route("/assignment/<uuid>", methods=['GET'])
def assignment(uuid):
    return jsonify(r.table('assignment').get(uuid).run(conn))


@app.route("/assignment", methods=['POST'])
def post_assignment():
    uuid = r.table('assignment') \
            .insert(request.json) \
            .run(conn)['generated_keys'][0]

    return jsonify(r.table('assignment').get(uuid).run(conn))


@app.route("/schedule")
def schedule_route():
    assignments = list(map(
        Assignment.from_json,
        r.table('assignment').run(conn)
    ))

    available_times = {from_iso(a['start']): a['duration']
                       for a in r.table('availability').run(conn)}

    plan, remaining = schedule(assignments, available_times)
    result = {a.id: _clean_plan(p) for (a, p) in plan.items()}
    return jsonify(result)


def _clean_plan(plan):
    return {d.isoformat(): hours for (d, hours) in plan.items()}

@app.route("/sorted")
def sorted_things():
    return jsonify(sort_a_list([4,3,2]))


@app.route("/predict")
def train_model():
    prediction = predict_hours()
    return jsonify(prediction.tolist())



if __name__ == "__main__":
    app.run()
