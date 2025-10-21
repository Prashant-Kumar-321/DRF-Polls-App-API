from django.urls import path
from rest_framework.routers import DefaultRouter
from  .views import PollViewSets, ChoicesList, ChoiceDetail, CreateVote
from .user_views import CreateUser

router = DefaultRouter()
router.register(prefix='polls', viewset=PollViewSets, basename='polls')

urlpatterns = [
    path('polls/<uuid:poll_pk>/choices/', ChoicesList.as_view(), name='choices-list'),
    path('polls/<uuid:poll_pk>/choices/<uuid:choice_pk>/', ChoiceDetail.as_view(), name='choice-detail'),
    path('polls/<uuid:poll_pk>/choices/<uuid:choice_pk>/vote/', CreateVote.as_view(), name='create-vote'),
    path('account/user/', CreateUser.as_view(), name='create-user'),
]

urlpatterns += router.urls

"""
    The above line will add following urls 
    /polls/ <--- Polls list
    /polls/<pk>/ <--- Poll Detial
"""