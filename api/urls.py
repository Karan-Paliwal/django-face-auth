from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'api'

urlpatterns = [
    path('blogposts/', login_required(views.BlogPostListCreate.as_view(), login_url='/login/'), name='blogpost-view-create'),
    path('blogposts/<int:pk>/', login_required(views.BlogPostRetrieveUpdateDestroy.as_view(), login_url='/login/'), name='blogpost-retrieve-update-destroy'),
    path('logout/', views.LogoutView.as_view(), name='logout'),  # New logout endpoint
]