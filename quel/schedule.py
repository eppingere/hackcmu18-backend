from collections import namedtuple
from datetime import date, timedelta

import numpy
from keras.layers import Dense
from keras.models import Sequential

Assignment = namedtuple('Assignment', ['name', 'due', 'hours'])

GAMMA = 2


def days(x):
    return timedelta(days=x)


def schedule(assignments, available_times, *, gamma=GAMMA):

    if len(assignments) == 0:
        return {}, available_times

    soonest = min(assignments, key=lambda a: a.due)
    ind = assignments.index(soonest)

    result = schedule_one(soonest, available_times, gamma=gamma)
    if result is None:
        return

    available_times = available_times.copy()

    for (date, hours) in result.items():
        if hours == 0:
            continue
        available_times[date] -= hours

    rest, available_times = schedule(
        [*assignments[:ind], *assignments[ind + 1:]],
        available_times, gamma=gamma
    )

    return {soonest: result, **rest}, available_times


def schedule_one(assignment, available_times, *, gamma=GAMMA):
    today = date.today()
    period = assignment.due - today

    time_until = list(available_times.get(today + days(d), 0)
                      for d in range(period.days + 1))
    total_free = sum(time_until)

    if total_free < assignment.hours:
        return

    hours = _schedule_one(time_until, assignment.hours, gamma)

    return {today + days(d): h for (d, h) in zip(range(period.days + 1), hours)}


def _schedule_one(available, hours, gamma):
    n_days = len(available)

    i = 0
    result = [0 for _ in range(n_days)]

    while hours > 0:
        delta = min(available[i], gamma, hours)
        result[i] += delta
        available[i] -= delta
        hours -= delta

        i += 1
        i %= n_days

    return result

def predict_hours(assignments, yourPastAsssignments, assignmentName):

    assignments = []
    assignmentName = ["Random Lab", "Bignum Lab", "Skyline Lab", "Paren Lab"]

    yourPastAsssignments = [
            Assignment(name="Random Lab", due="sdgfhjk", hours=3.6),
            Assignment(name="Bignum Lab", due="sdgfhjk", hours=2.6),
            Assignment(name="Skyline Lab", due="sdgfhjk", hours=12.9),
            Assignment(name="Paren Lab", due="sdgfhjk", hours=5.2),
            Assignment(name="Integral Lab", due="sdgfhjk", hours=1.5)
        ]

    assignmentName = "Test Lab"
    assignmentHours = 5

    for a in assignments:
        if a.name == assignmentName:
            assignmentHours = a.hours

    commonAssignments = []
    for a1 in assignments:
        for a2 in yourPastAsssignments:
            if a1.name == a2.name:
                commonAssignments.append((a1, a2))
    X = []
    for (a, _) in commonAssignments:
        X.append(a.hours)

    Y = []
    for (_, a) in commonAssignments:
        Y.append(a.hours)

    model = Sequential()
    model.add(Dense(12, input_dim=1, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='relu'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(X, Y, epochs=150, batch_size=10)

    scores = model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    return model.predict([assignmentHours])
