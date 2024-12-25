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
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group

@login_required
def register_user(request):
    # Only allow admins to access this view
    if request.user.role != 'ADMIN':
        messages.error(request, "You are not authorized to register users.")
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('admin_dashboard')  # Redirect back to the dashboard
    else:
        form = UserRegistrationForm()

    return render(request, 'register_user.html', {'form': form})

# Login and Redirection based on Role
@login_required
@role_required(allowed_roles=['ADMIN', 'STAFF', 'LIBRARIAN'])
def dashboard(request):
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'STAFF':
        return redirect('staff_dashboard')
    elif request.user.role == 'LIBRARIAN':
        return redirect('librarian_dashboard')
    return redirect('login')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)          

            # Redirect based on role
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'STAFF':
                return redirect('staff_dashboard')
            elif user.role == 'LIBRARIAN':
                return redirect('librarian_dashboard')
            else:
                messages.error(request, "Your role is not defined.")
                return redirect('login')  # Redirect back to login if no valid role
        else:
            messages.error(request, "Invalid username or password.")
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
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "STAFF"
            user.save()
            messages.success(request, "Staff member added successfully!")
            return redirect("manage_staff")
    else:
        form = UserRegistrationForm()

    # Fetch existing staff from the database
    staff_members = User.objects.filter(role='STAFF')
    return render(request, "manage_staff.html", {"form": form, "staff_members": staff_members})

# Edit Staff
@login_required
@role_required(allowed_roles=['ADMIN'])
def edit_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member updated successfully!")
            return redirect("manage_staff")
    else:
        form = UserRegistrationForm(instance=user)
    
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
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "LIBRARIAN"
            user.save()
            messages.success(request, "Librarian added successfully!")
            return redirect("manage_librarian")
    else:
        form = UserRegistrationForm()
    
    librarians = User.objects.filter(role='LIBRARIAN')
    return render(request, "manage_librarian.html", {"form": form, "librarians": librarians})

# Edit Librarian
@login_required
@role_required(allowed_roles=['ADMIN'])
def edit_librarian(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Librarian updated successfully!")
            return redirect("manage_librarian")
    else:
        form = UserRegistrationForm(instance=user)
    
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
    
@api_view(['GET', 'POST'])
@login_required
@role_required(allowed_roles=['LIBRARIAN', 'ADMIN'])
def library_history_api(request):
    # For 'GET' request: Retrieve library history
    if request.method == 'GET':
        # Check user role for permission
        if request.user.role not in ['LIBRARIAN', 'ADMIN', 'STAFF']:
            raise PermissionDenied("You do not have permission to view library history.")
        
        library_history = LibraryHistory.objects.all()
        serializer = LibraryHistorySerializer(library_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # For 'POST' request: Add a new library history record
    elif request.method == 'POST':
        # Check user role for permission
        if request.user.role != 'ADMIN':
            raise PermissionDenied("Only Admins can add library records.")
        
        serializer = LibraryHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Custom Logout Function
def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page

