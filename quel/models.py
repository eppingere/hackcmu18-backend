from collections import namedtuple
from datetime import datetime


def to_iso(dt):
    return dt.isoformat()


def from_iso(iso):
    return datetime.strptime(iso, r"%Y-%m-%dT%H:%M:%S.%f").date()


_Availability = namedtuple('Availability', ['id', 'start', 'duration'])


class Availability(_Availability):
    def to_json(self):
        return {
            'id': self.id,
            'start': to_iso(self.start),
            'duration': self.duration,
        }

    @classmethod
    def from_json(cls, json):
        return cls(
            id=json['id'],
            start=from_iso(json['start']),
            duration=json['duration'],
        )


_Course = namedtuple('Course', ['id', 'name'])


class Course(_Course):
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @classmethod
    def from_json(cls, json):
        return cls(
            id=json['id'],
            name=json['name'],
        )


_Assignment = namedtuple(
    'Assignment', ['id', 'name', 'course', 'hours', 'due'])


class Assignment(_Assignment):
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'course': self.course,
            'hours': self.hours,
            'due': to_iso(self.due),
        }

    @classmethod
    def from_json(cls, json):
        return cls(
            id=json['id'],
            name=json['name'],
            course=json['course'],
            hours=json['hours'],
            due=from_iso(json['due']),
        )
