from django.db import models

from django.contrib.auth.models import User

from datetime import datetime


# Create your models here.
class Session(models.Model):
    date_started = models.DateTimeField()
    date_ended = models.DateTimeField(blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_active(cls):
        try:
            print("This is the yes", Session.objects.all())
            return Session.objects.filter(date_ended__isnull=True)[0]
        except IndexError:
            return None


    @classmethod
    def make_active(cls, user):
        old_active = cls.get_active()
        if old_active:
            old_active.delete()

        Session.objects.create(date_started=datetime.now(), user_id=user)

    @classmethod
    def end(cls):
        session = cls.get_active()
        session.date_ended = datetime.now()
        session.save()

    @classmethod
    def get_last_session(cls, exercise_id):
        try:
            exercise_filter = Session.objects.filter(sessionexercise__exercise_id=exercise_id)
            active_filter = exercise_filter.filter(date_ended__isnull=False)
            newest = active_filter.order_by('-date_ended')[0]
            return newest
        except IndexError:
            return None


class Force(models.Model):
    name = models.CharField(max_length=100)


class Equipment(models.Model):
    name = models.CharField(max_length=100)


class Muscle(models.Model):
    name = models.CharField(max_length=100)


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    force = models.ForeignKey(Force, on_delete=models.CASCADE, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True, blank=True)


class ExerciseMuscle(models.Model):
    primary = models.BooleanField(default=False)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    muscle = models.ForeignKey(Muscle, on_delete=models.CASCADE)


class SessionExercise(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    exercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repitions = models.IntegerField()
    weight = models.FloatField()

    @classmethod
    def user_exercises(cls, user):
        return SessionExercise.objects.filter(session_id__user_id=user.id)

    @classmethod
    def get_current(cls, user, exercise):
        user_exercises = SessionExercise.user_exercises(user)

        exercise_filter = user_exercises.filter(exercise_id=exercise)

        session_filter = exercise_filter.filter(session_id=Session.get_active())

        return session_filter

    @classmethod
    def get_last(cls, user, exercise):
        user_exercises = SessionExercise.user_exercises(user)

        # Getting the id of the last session
        last_session = Session.get_last_session(exercise)

        exercise_filter = user_exercises.filter(exercise_id=exercise)

        session_filter = exercise_filter.filter(session_id=last_session)

        user_filter = session_filter.filter(session_id__user_id=user.id)

        return list(user_filter)

    @classmethod
    def get_pb(cls, user, exercise):
        user_exercises = SessionExercise.user_exercises(user)

        exercise_filter = user_exercises.filter(exercise_id=exercise)
        max_weight = exercise_filter.order_by('-weight')

        try:
            return max_weight[0]
        except IndexError:
            return None
