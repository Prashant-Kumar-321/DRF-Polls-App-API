from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import Poll


class IsPollCreator(permissions.BasePermission):
    """
    Allow access only to the creator of the poll referenced by 'poll_pk' in the URL.
    Used for views that operate on choices for a given poll (list/create) and similar.
    """

    def has_permission(self, request, view):
        poll_id = view.kwargs.get('poll_pk')

        if not poll_id: 
            # If the view doesn't reference a poll, don't decide here. Return True so other checks can run.

            return True
    
        # 404 if poll doesn't exist
        poll = get_object_or_404(Poll, pk=poll_id)

        # only the pol creator can create/list choices
        return request.user == poll.creator

    # Used in the details view
    def has_object_permission(self, request, view, obj):
        poll = getattr(obj, 'poll', None)
        
        if not poll: 
            # for object without poll attribute(property)
            return True
    

        return request.user == poll.creator


    """
    Order of function call

    has_permission() ----> has_object_permission()

    if has_permission() returns False then second one is not checked
    """