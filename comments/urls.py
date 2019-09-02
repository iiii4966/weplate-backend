from django.urls import path
from .views import *

urlpatterns = [
    path('comment', CommentView.as_view()),
    path('comment/<int:comment_id>', CommentUpdateDeleteView.as_view()),
   ]
