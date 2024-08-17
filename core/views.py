from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Vote, Report
import json

@login_required
def vote(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    obj = get_object_or_404(content_type.model_class(), id=object_id)
    
    data = json.loads(request.body)
    vote_value = data.get('vote')
    if vote_value not in ['1', '-1']:
        return JsonResponse({'success': False, 'error': 'Invalid vote value'})

    vote_value = int(vote_value)
    vote, created = Vote.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id,
        defaults={'vote': vote_value}
    )

    if not created:
        if vote.vote == vote_value:
            # User is un-voting
            vote.delete()
            vote_value = 0
        else:
            # User is changing their vote
            vote.vote = vote_value
            vote.save()
    
    # Recalculate vote counts
    upvotes = Vote.objects.filter(content_type=content_type, object_id=object_id, vote=1).count()
    downvotes = Vote.objects.filter(content_type=content_type, object_id=object_id, vote=-1).count()
    
    obj.upvotes = upvotes
    obj.downvotes = downvotes
    obj.save()

    return JsonResponse({
        'success': True,
        'upvotes': obj.upvotes,
        'downvotes': obj.downvotes,
        'score': obj.score,
        'user_vote': vote_value
    })

@login_required
def report(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    obj = get_object_or_404(content_type.model_class(), id=object_id)
    
    reason = request.POST.get('reason')
    if reason:
        Report.objects.create(
            content_type=content_type,
            object_id=object_id,
            reported_by=request.user,
            reason=reason
        )
        return JsonResponse({'success': True, 'message': 'Content reported successfully.'})
    else:
        return JsonResponse({'success': False, 'error': 'Please provide a reason for reporting.'})