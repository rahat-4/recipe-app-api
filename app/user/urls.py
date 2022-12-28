"""URL mappings for the user API"""

from django.urls import path

from .views import UserApiView, CreateUserTokenApiView, ManageUserView

app_name = 'user'

urlpatterns = [
    path('create/', UserApiView.as_view(), name='create'),
    path('token/', CreateUserTokenApiView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
]