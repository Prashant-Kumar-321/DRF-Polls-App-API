from rest_framework import serializers
from .models import Poll, Choice, Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Vote
        fields = '__all__'
    
class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False, read_only=False)

    class Meta:
        model = Choice
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False, read_only=True)

    pub_date = serializers.DateTimeField(
      format='%d-%m-%Y',
      read_only=True
    )

    modified_date = serializers.DateTimeField(
      format='%d-%m-%Y',
      read_only=True
    )


    class Meta: 
        model = Poll 
        fields = '__all__'





