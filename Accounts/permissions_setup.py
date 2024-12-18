from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Student, LibraryHistory, FeesHistory

def setup_roles_and_permissions():
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    staff_group, _ = Group.objects.get_or_create(name="Office Staff")
    librarian_group, _ = Group.objects.get_or_create(name="Librarian")

    student_ct = ContentType.objects.get_for_model(Student)
    fees_ct = ContentType.objects.get_for_model(FeesHistory)
    library_ct = ContentType.objects.get_for_model(LibraryHistory)

    admin_group.permissions.add(*Permission.objects.filter(content_type__in=[student_ct, fees_ct, library_ct]))

    staff_group.permissions.add(
        Permission.objects.get(codename='view_student'),
        Permission.objects.get(codename='add_feeshistory'),
        Permission.objects.get(codename='change_feeshistory'),
        Permission.objects.get(codename='delete_feeshistory'),
        Permission.objects.get(codename='view_libraryhistory'),
    )

    librarian_group.permissions.add(
        Permission.objects.get(codename='view_student'),
        Permission.objects.get(codename='view_libraryhistory'),
    )
