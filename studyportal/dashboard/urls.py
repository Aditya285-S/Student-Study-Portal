from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    
    path('notes/', notes, name = 'notes'),
    path('delete-note/<int:pk>', delete_note, name = 'delete-note'),
    path('note-info/<int:pk>', note_info, name = 'note-info'),
    # path('notes-detail/<int:pk>', note_details.as_view(), name = 'notes-detail'),
    
    path('homework/', homework, name = 'homework'),
    path('update-homework/<int:pk>', update_hw, name = 'update-homework'),
    path('delete-homework/<int:pk>', delete_hw, name = 'delete-homework'),
    
    path('youtube/', youtube, name = 'youtube'),
    
    path('todo/', todo, name = 'todo'),
    path('update-todo/<int:pk>', update_todo, name = 'update-todo'),
    path('delete-todo/<int:pk>', delete_todo, name = 'delete-todo'),
]