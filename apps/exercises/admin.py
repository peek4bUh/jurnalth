from django.contrib import admin

from .models import ExerciseLevel, Exercise, ExerciseForce, ExerciseMechanic, ExerciseBodyRegion, ExerciseCategory


@admin.register(ExerciseForce)
class ExerciseForceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']


@admin.register(ExerciseMechanic)
class ExerciseMechanicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']


@admin.register(ExerciseBodyRegion)
class ExerciseBodyRegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']


@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']


@admin.register(ExerciseLevel)
class ExerciseLevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'level']
    list_filter = ['level', 'force']
    search_fields = ['name', 'description']
