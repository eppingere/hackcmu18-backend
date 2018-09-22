
def make_schedule(now, days, assignments):
    workPerDay = {}
    for assignment in assignments:
        work = assignment.hoursToComplete
        daysLeft = assignment.dueDate - now
        workPerDay[assignment] = work / daysLeft

    output = {}
    for day in days:
        todo = set()
        for assignment in assignments:
            if assignment.dueDate >= now:
                todo.add(workPerDay[assignment])

        # Somehow sort the todo

        output[day] = {


        }
