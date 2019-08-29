from django.urls import path
from .views import CommentView

urlpatterns = [
    path('comment', CommentView.as_view()),
    path('comment/<int:comment_id>', CommentView.as_view())
   ]
