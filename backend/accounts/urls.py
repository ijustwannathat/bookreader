
from django.urls import path

from .views import UserDetailView, UserView

urlpatterns = [        
    path("", UserView.as_view(), name='user-view'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail-view')
]
