from django.urls import path, include
from .views import UserViewSet, custom_logout
from . import views
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')  # Register UserViewSet
# router.register(r'library_history', LibraryHistoryViewSet, basename='libraryhistory')  # Register LibraryHistoryViewSet

urlpatterns = [
    # Authentication
    path('login/', views.custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),

    # Dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('librarian_dashboard/', views.librarian_dashboard, name='librarian_dashboard'),

    path('add-student/', views.student_list, name='add_student'),
    path('fees_history/', views.fees_history_list, name='fees_history'),
    path('library_history/', views.library_history_api, name='library_history'),

    # Manage staff
    path("manage-staff/", views.manage_staff, name="manage_staff"),
    path('edit_staff/<int:user_id>/', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:user_id>/', views.delete_staff, name='delete_staff'),
    
    # Manage Librarians
    path('manage_librarian/', views.manage_librarian, name='manage_librarian'),
    path('edit_librarian/<int:user_id>/', views.edit_librarian, name='edit_librarian'),
    path('delete_librarian/<int:user_id>/', views.delete_librarian, name='delete_librarian'),
    
    #path('api/', include(router.urls)),
]
# # Include router-generated URLs
# urlpatterns += router.urls