from django.db import models
from django.contrib.auth.models import User
import uuid

class Poll(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    question = models.CharField(max_length=200, verbose_name='Poll Question', help_text='Enter the poll question')
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='polls')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Publishded Date and Time')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Last modified Date Time')

    def __str__(self):
        return self.question
    

class Choice(models.Model): 
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    poll = models.ForeignKey(to=Poll, on_delete=models.CASCADE, related_name='choices')
    body = models.CharField(max_length=100, verbose_name='Choice Text')

    def __str__(self): 
        return self.body

class Vote(models.Model): 
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    choice = models.ForeignKey(to=Choice, on_delete=models.CASCADE, related_name='votes')
    poll = models.ForeignKey(to=Poll, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='votes')

    class Meta: 
        unique_together = ['poll', 'voter']
    
    def __str__(self):
        return f"{self.voter} voted for {self.choice}"



