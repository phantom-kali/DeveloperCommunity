from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Vote, Report

@login_required
def vote(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    obj = get_object_or_404(content_type.model_class(), id=object_id)
    
    vote_value = request.POST.get('vote')
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
            if vote_value == 1:
                obj.upvotes -= 1
            else:
                obj.downvotes -= 1
            vote.delete()
            user_vote = 0
        else:
            # User is changing their vote
            if vote_value == 1:
                obj.upvotes += 1
                obj.downvotes -= 1
            else:
                obj.upvotes -= 1
                obj.downvotes += 1
            vote.vote = vote_value
            vote.save()
            user_vote = vote_value
    else:
        # New vote
        if vote_value == 1:
            obj.upvotes += 1
        else:
            obj.downvotes += 1
        user_vote = vote_value

    obj.save()

    return JsonResponse({
        'success': True,
        'upvotes': obj.upvotes,
        'downvotes': obj.downvotes,
        'score': obj.score,
        'user_vote': user_vote
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