from django.shortcuts import render
from django.shortcuts import redirect

from .models import Exercise, SessionExercise, Session
from .forms import SetForm


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    if request.method == 'POST':
        Session.make_active(request.user)
        return redirect('exercises')

    return render(request, 'gymbo/home.html')


def exercises(request):
    if request.method == 'POST':
        Session.end()
        return redirect('home')

    all_exercises = Exercise.objects.all()

    return render(request, 'gymbo/exercises.html', context={'exercises': all_exercises})


def detailed(request, exercise_id):
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.session_id = Session.get_active()
            data.exercise_id = Exercise.objects.get(pk=exercise_id)
            data.save()

    exercise = Exercise.objects.get(pk=exercise_id)

    form = SetForm()

    print("This ist he user", request.user)
    return render(request, 'gymbo/detailed.html', context= {
        'exercise': exercise,
        'last_set': SessionExercise.get_last(request.user, exercise_id),
        'curr_set': SessionExercise.get_current(request.user, exercise_id),
        'form': form,
        'pb': SessionExercise.get_pb(request.user, exercise_id)
    })

def current_session(request):
    pass
