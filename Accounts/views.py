from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .models import Student, FeesHistory, User, LibraryHistory
from .serializers import StudentSerializer, FeesHistorySerializer, UserSerializer, LibraryHistorySerializer
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .decorators import role_required
from django.contrib import messages
from .forms import UserForm
from django.shortcuts import render, redirect, get_object_or_404

# Login and Redirection based on Role
@login_required
@role_required(allowed_roles=['admin', 'staff', 'librarian'])
def dashboard(request):
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'STAFF':
        return redirect('staff_dashboard')
    elif request.user.role == 'LIBRARIAN':
        return redirect('librarian_dashboard')
    return redirect('login')

# Custom Login Function
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect user based on their role
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'STAFF':
                return redirect('staff_dashboard')
            elif user.role == 'LIBRARIAN':
                return redirect('librarian_dashboard')
            else:
                return redirect('login')  # Default to login if no role
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

# Admin Dashboard
@login_required
@role_required(allowed_roles=['ADMIN'])
def admin_dashboard(request):
    # Fetching staff and librarian data
    staff_members = User.objects.filter(role="STAFF")
    librarians = User.objects.filter(role="LIBRARIAN")
    
    # Fetching other data
    students = Student.objects.all()
    fees_history = FeesHistory.objects.all()
    library_history = LibraryHistory.objects.all()

    # Context for the template
    context = {
        "staff_members": staff_members,
        "librarians": librarians,
        "students": students,
        "fees_history": fees_history,
        "library_history": library_history,
        "staff_count": staff_members.count(),
        "librarian_count": librarians.count(),
        "student_count": students.count(),
    }

    return render(request, "admin_dashboard.html", context)
    
# Manage Staff
@login_required
@role_required(allowed_roles=['ADMIN'])
def manage_staff(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "STAFF"
            user.save()
            messages.success(request, "Staff member added successfully!")
            return redirect("manage_staff")
    else:
        form = UserForm()

    # Fetch existing staff from the database
    staff_members = User.objects.filter(role='STAFF')
    return render(request, "manage_staff.html", {"form": form, "staff_members": staff_members})

# Edit Staff
@login_required
@role_required(allowed_roles=['ADMIN'])
def edit_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member updated successfully!")
            return redirect("manage_staff")
    else:
        form = UserForm(instance=user)
    
    return render(request, "edit_staff.html", {"form": form, "user": user})

# Delete Staff
@login_required
@role_required(allowed_roles=['ADMIN'])
def delete_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        user.delete()
        messages.success(request, "Staff member deleted successfully!")
        return redirect("manage_staff")
    
    return render(request, "delete_staff.html", {"user": user})

# Manage Librarians (similar to manage_staff)
@login_required
@role_required(allowed_roles=['ADMIN'])
def manage_librarian(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "LIBRARIAN"
            user.save()
            messages.success(request, "Librarian added successfully!")
            return redirect("manage_librarian")
    else:
        form = UserForm()
    
    librarians = User.objects.filter(role='LIBRARIAN')
    return render(request, "manage_librarian.html", {"form": form, "librarians": librarians})

# Edit Librarian
@login_required
@role_required(allowed_roles=['ADMIN'])
def edit_librarian(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Librarian updated successfully!")
            return redirect("manage_librarian")
    else:
        form = UserForm(instance=user)
    
    return render(request, "edit_librarian.html", {"form": form, "user": user})

# Delete Librarian
@login_required
@role_required(allowed_roles=['ADMIN'])
def delete_librarian(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        user.delete()
        messages.success(request, "Librarian deleted successfully!")
        return redirect("manage_librarian")
    
    return render(request, "delete_librarian.html", {"user": user})

# Staff Dashboard
@login_required
@role_required(allowed_roles=['STAFF'])
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

# Librarian Dashboard
@login_required
@role_required(allowed_roles=['LIBRARIAN'])
def librarian_dashboard(request):
    return render(request, 'librarian_dashboard.html')

# User API ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admin can view all users, others can only view their own profile
        if self.request.user.role == 'ADMIN':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        if self.request.user.role != 'ADMIN':
            raise PermissionDenied("Only Admins can create users.")
        serializer.save()

# Student API View
@api_view(['GET', 'POST'])
@login_required
@role_required(allowed_roles=['STAFF', 'ADMIN'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Fees History API View
@api_view(['GET', 'POST'])
@login_required
@role_required(allowed_roles=['STAFF', 'ADMIN'])
def fees_history_list(request):
    if request.method == 'GET':
        fees = FeesHistory.objects.all()
        serializer = FeesHistorySerializer(fees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FeesHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Library History API ViewSet
class LibraryHistoryViewSet(viewsets.ModelViewSet):
    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Librarians and staff can view library history
        if self.request.user.role in ['LIBRARIAN', 'STAFF']:
            return LibraryHistory.objects.all()
        raise PermissionDenied("You do not have permission to view library history.")

    def perform_create(self, serializer):
        if self.request.user.role != 'ADMIN':
            raise PermissionDenied("Only Admins can add library records.")
        serializer.save()

# Custom Logout Function
def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page
