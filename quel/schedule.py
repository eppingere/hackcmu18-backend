from collections import namedtuple
from datetime import date, timedelta

Assignment = namedtuple('Assignment', ['name', 'due', 'hours'])

GAMMA = 2


def days(x):
    return timedelta(days=x)


def schedule(assignments, available_times, *, gamma=GAMMA):

    if len(assignments) == 0:
        return [], available_times

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

    return [result, *rest], available_times


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
