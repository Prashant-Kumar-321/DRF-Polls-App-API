from rest_framework import serializers
from .models import Poll, Choice, Vote

class VoteSerializer(serializers.ModelSerializer):
	class Meta: 
		model = Vote
		fields = '__all__'

		extra_kwargs = {
			'poll': {
				'read_only': True
			}, 
			
			'choice': {
				'read_only': True
			}, 
			
			'voter': {
				'read_only': True
			}
		}

class ChoiceSerializer(serializers.ModelSerializer):
	votes = VoteSerializer(many=True, required=False, read_only=True)

	# Only use poll field for read operations, write will be handled by view
	poll = serializers.PrimaryKeyRelatedField(
		read_only=True
	)

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

		extra_kwargs = {
			'creator': {
				'read_only': True
			}
		}





