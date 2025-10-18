from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Poll, Vote, Choice
from .serializers import PollSerializer, VoteSerializer, ChoiceSerializer

class PollViewSets(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class ChoicesList(APIView): 
    def get(self, request, poll_pk): 
        choices = Choice.objects.filter(poll__id=poll_pk)
        serializer = ChoiceSerializer(choices, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, poll_pk):
        """Create a new choice"""

        # check is the poll with given poll_pk exists
        poll = get_object_or_404(Poll, pk=poll_pk)

        data = request.data
        
        # Add the missing poll pk data
        data['poll'] = poll_pk

        serializer = ChoiceSerializer(data=data)

        if not serializer.is_valid(): 
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class ChoiceDetail(APIView): 
    def get(self, request, poll_pk, choice_pk): 
        choice = get_object_or_404(Choice, pk=choice_pk)

        serializer = ChoiceSerializer(choice)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, poll_pk, choice_pk):
        choice = get_object_or_404(Choice, pk=choice_pk)

        data = request.data
        data['poll'] = poll_pk

        serializer = ChoiceSerializer(instance=choice, data=data)

        if not serializer.is_valid(): 
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, poll_pk, choice_pk):
        choice = get_object_or_404(Choice, pk=choice_pk)

        if choice.poll.id != poll_pk: 
            data = {
              "details": f"poll ({poll_pk}) does not exist."
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        choice.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CreateVote(APIView): 
    def post(self, request, poll_pk, choice_pk): 
        data = request.data

        data['poll'] = poll_pk
        data['choice'] = choice_pk

        serializer = VoteSerializer(data=data)

        if vote_exists := \
            self.delete_any_earlier_vote(poll_pk=poll_pk, choice_pk=choice_pk, voter_pk=data['voter']): 
            return Response(data={"details": "vote already exists"})

        if not serializer.is_valid(): 
            return Response(data=serializer.errors)
    
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_any_earlier_vote(self, poll_pk, voter_pk, choice_pk): 
        """
            Delete the existing vote made by current user on this poll \n
            Return `True` if user has already voted in the same choice of the current poll otherwise `None` \n
            Check if the user has already made a vote on any other choice in this poll
            If yes delete the earlier vote
        """
        try: 
            existing_vote = Vote.objects.get(Q(poll__id=poll_pk) & Q(voter__id=voter_pk))
            
        except: 
            pass 
        
        if existing_vote.choice.id == choice_pk: 
            # user is making a vote for the choice where they has alredy made a vote of the current poll

            return True


        if existing_vote:
            existing_vote.delete() 


            