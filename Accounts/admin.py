from django.contrib import admin
from .models import Student, User, LibraryHistory, FeesHistory

admin.site.register(Student)
admin.site.register(User)
admin.site.register(LibraryHistory)
admin.site.register(FeesHistory)