from django import forms
from django.forms import inlineformset_factory

from apps.exercises.models import Exercise

from .models import Workout, WorkoutExercise

INPUT_CLASS = (
    "mt-1 block w-full rounded-sm border border-gray-200 bg-white px-3 py-2 "
    "text-sm text-gray-800 focus:border-gray-700 focus:outline-none "
    "focus:ring-0"
)


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ("date",)
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASS


class WorkoutExerciseForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(
        queryset=Exercise.objects.order_by("name"),
        empty_label="Selecciona un ejercicio",
        widget=forms.HiddenInput,
    )
    volume = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"placeholder": "Ej. 3x6-10 o 1x5x80, 1x7x60"}),
    )
    rest = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ej. 90s"}),
    )

    class Meta:
        model = WorkoutExercise
        fields = ("volume", "rest")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.exercise_name = self.cleaned_data["exercise"].name
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, is_edit=False, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["exercise"].initial = Exercise.objects.filter(
                name=self.instance.exercise_name).first()
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASS


WorkoutExerciseFormSet = inlineformset_factory(
    Workout,
    WorkoutExercise,
    form=WorkoutExerciseForm,
    extra=0,
    can_delete=True,
    min_num=0,
    validate_min=False,
)
