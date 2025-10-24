from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.request import Request
from rest_framework import viewsets, status, generics
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .models import Poll, Vote, Choice
from .serializers import PollSerializer, VoteSerializer, ChoiceSerializer
from .permissions import IsPollCreator

class PollViewSets(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def create(self, request, *args, **kwargs):
        # add missing data
        # request.data['creator'] = request.user.id

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=kwargs['pk'])

        if request.user != poll.creator: 
            raise PermissionDenied('Access Denied: You can not delete the poll.') 

        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=kwargs['pk'])

        if request.user != poll.creator: 
            raise PermissionDenied('Access Denied: You can not update the poll.')
        
        # add missing user Id
        request.data['creator'] = request.user.id

        return super().update(request, *args, **kwargs)

class ChoicesList(generics.ListCreateAPIView): 
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, IsPollCreator]

    def get_queryset(self):
        """
        Filter the choices to those belonging to the specific poll
        """
        poll_pk = self.kwargs['poll_pk']
        return Choice.objects.filter(poll__pk=poll_pk)


    def perform_create(self, serializer): # view hook
        """
        Add the poll foreign key during creation.
        The authorization check is already performed in get_queryset (which is called before perform_create).
        """
        
        poll_pk = self.kwargs['poll_pk']
        poll = get_object_or_404(Poll, pk=poll_pk)

        # Save the choices with the current poll
        serializer.save(poll=poll)

class ChoiceDetail(generics.GenericAPIView, UpdateModelMixin, DestroyModelMixin): 
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, IsPollCreator]

    def get_queryset(self): 
        poll_pk = self.kwargs['poll_pk']

        return Choice.objects.filter(poll__id=poll_pk)

    def get_object(self): 
        choice_pk = self.kwargs['choice_pk']
        choice = get_object_or_404(Choice, pk=choice_pk)

        self.check_object_permissions(self.request, choice)

        return choice

    # Map put---update and delete---destroy methods
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs): 
        return self.destroy(self, request, *args, **kwargs)


class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        choice = get_object_or_404(Choice, pk=self.kwargs['choice_pk'])

        serializer.save(choice=choice, poll=choice.poll, voter=self.request.user)


    def create(self, request, *args, **kwargs): 
        if self.delete_any_earlier_vote(request, **kwargs):
            return Response(data={"details": "vote already exists"})

        return super().create(request, *args, **kwargs)

    def delete_any_earlier_vote(self, request, **kwargs): 
        """
            Delete the existing vote made by current user on this poll \n
            Return `True` if user has already voted in the same choice of the current poll otherwise `None` \n
            Check if the user has already made a vote on any other choice in this poll
            If yes delete the earlier vote
        """
        existing_vote = None

        try: 
            existing_vote = Vote.objects.get(Q(poll__id=kwargs['poll_pk']) & Q(voter=request.user))
        except Vote.DoesNotExist:
            """ 
            User is making vote in this pole for the first time
            """
            return None
        
        # It is guranteed that existing_vote will have vote object here
        if existing_vote.choice.id == kwargs['choice_pk']: 
            # user has already voted in this choice
            # no need perform any vote
            return True


        if existing_vote:
            existing_vote.delete() 
