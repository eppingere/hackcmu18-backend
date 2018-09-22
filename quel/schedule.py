import random
from collections import namedtuple
from datetime import date, timedelta

import numpy as np
from keras.layers import Dense
from keras.models import Sequential

from .models import Assignment

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


def generate_fake_person():
    r = random.uniform(0.8, 1.2)

    return [r * 2, r * 9, r * 7.5], r * 10


def predict_hours():
    random_people = [generate_fake_person() for _ in range(1000)]

    X_train = np.array([p[0] for p in random_people])
    y_train = np.array([p[1] for p in random_people])

    model = Sequential()
    model.add(Dense(16, input_dim=3, activation='relu'))
    model.add(Dense(1, activation='relu'))

    model.compile(loss='mean_squared_error', optimizer='adam')

    # Fit the model
    model.fit(X_train, y_train, epochs=150, batch_size=100)

    X = np.array([[4, 20, 9]])
    return model.predict(X)
