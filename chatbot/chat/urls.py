from django.urls import path
from chat.views.list_views import *

app_name = 'chat'

urlpatterns = [
    # views
    path('list/', \
        ChatListView.as_view(), \
        name='chat-list'),
]