from rest_framework import serializers
from .models import Student, FeesHistory, User, LibraryHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'class_name', 'date_of_birth', 'guardian_name', 'contact_number']

class LibraryHistorySerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = LibraryHistory
        fields = ['id', 'student', 'student_name', 'book_name', 'borrow_date', 'return_date', 'status']

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

class FeesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesHistory
        fields = ['id', 'student', 'fee_type', 'amount_paid', 'payment_date', 'payment_status']
