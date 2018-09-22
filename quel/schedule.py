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

    hours_given, overflow = fill_to(assignment.hours, gamma, period.days + 1)
    hours = _schedule_one(time_until, hours_given, overflow)

    return {today + days(d): h for (d, h) in zip(range(period.days + 1), hours)}


def _schedule_one(available, requested, overflow=0):
    chops = chopped(available, requested)

    overflow += sum(chops)
    assert overflow >= 0

    if not overflow:
        return requested

    not_full = [day == 0 for day in chops]
    delta = overflow / sum(not_full)

    requested_ = [(r - c if c else r + delta)
                  for (r, c) in zip(requested, chops)]

    return _schedule_one(available, requested_)


def chopped(available, requested):
    return [max(r - a, 0) for (r, a) in zip(requested, available)]


def fill_to(value, maximum, length):
    zeros = [0 for _ in range(length)]  # HACK
    result = [*([maximum] * (value // maximum)), value % maximum, *zeros]

    return result[:length], sum(result[length:])
