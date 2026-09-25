from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from apps.exercises.models import Exercise

from .forms import WorkoutExerciseFormSet, WorkoutForm
from .models import Workout, WorkoutExercise


@login_required(login_url='login')
def workouts_index(request):
    workouts = Workout.objects.prefetch_related('exercises').all()
    actions = [
        {'route': 'workout_create', 'label': 'New'},
    ]

    return render(request, 'workouts/list-workout.jinja2', {
        'workouts': workouts,
        'header_actions': actions,
    })


@login_required(login_url='login')
def workout_create(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        exercise_formset = WorkoutExerciseFormSet(
            request.POST, form_kwargs={'is_edit': False})
        if form.is_valid() and exercise_formset.is_valid():
            with transaction.atomic():
                workout = form.save()
                exercise_formset.instance = workout
                exercise_formset.save()
            return redirect('workouts_index')
    else:
        form = WorkoutForm()
        exercise_formset = WorkoutExerciseFormSet(
            form_kwargs={'is_edit': False})

    return render(request, 'workouts/create-workout.jinja2', {
        'form': form,
        'exercise_formset': exercise_formset,
    })


@login_required(login_url='login')
def workout_edit(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)

    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        exercise_formset = WorkoutExerciseFormSet(
            request.POST, instance=workout, form_kwargs={'is_edit': True})
        if form.is_valid() and exercise_formset.is_valid():
            with transaction.atomic():
                form.save()
                exercise_formset.save()
            return redirect('workouts_index')
    else:
        form = WorkoutForm(instance=workout)
        exercise_formset = WorkoutExerciseFormSet(
            instance=workout, form_kwargs={'is_edit': True})

    return render(request, 'workouts/edit-workout.jinja2', {
        'form': form,
        'exercise_formset': exercise_formset,
        'is_edit': True,
        'workout': workout,
    })


@login_required(login_url='login')
def workout_delete(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    if request.method == 'POST':
        workout.delete()
    return redirect('workouts_index')


@login_required(login_url='login')
def last_exercise_data(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    workout_exercise = (WorkoutExercise.objects
                        .filter(exercise_name=exercise.name)
                        .order_by('-workout__date', '-created_at')
                        .first())

    if not workout_exercise:
        return JsonResponse({'volume': '', 'rest': ''})

    return JsonResponse({
        'volume': workout_exercise.volume,
        'rest': workout_exercise.rest,
    })
