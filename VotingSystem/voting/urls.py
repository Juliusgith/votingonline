from django.urls import path
from . import views


urlpatterns = [
    path('vote/', views.vote, name='vote'),  # URL for the voting page
    path('already_voted/', views.already_voted, name='already_voted'),  # URL for the "already voted" page
]
