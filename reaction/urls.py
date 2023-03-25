from django.urls import path

from reaction.views import ReactionView

app_name = 'reaction'
urlpatterns = [
    path('react/', ReactionView.as_view(), name='react'),
]
