from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from notifications.models import Notification

User = get_user_model()


@login_required
def inbox_view(request):
    conversations = request.user.conversations.all()
    convos_with_other = [
        (convo, convo.get_other_participant(request.user))
        for convo in conversations
    ]
    return render(request, 'messaging/inbox.html', {'convos_with_other': convos_with_other})


@login_required
def conversation_view(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)

    if request.user not in conversation.participants.all():
        return redirect('inbox')

    messages = conversation.messages.all()
    messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            conversation.save()
            other = conversation.get_other_participant(request.user)
            if other:
                Notification.objects.create(
                    recipient=other,
                    sender=request.user,
                    notification_type='comment',
                    message=f"{request.user.username} sent you a message.",
                    link=f"/messages/{conversation.pk}/"
                )
        return redirect('conversation', pk=conversation.pk)

    other = conversation.get_other_participant(request.user)
    return render(request, 'messaging/conversation.html', {
        'conversation': conversation,
        'messages': messages,
        'other': other,
    })


@login_required
def start_conversation(request, username):
    other = get_object_or_404(User, username=username)

    if other == request.user:
        return redirect('inbox')

    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other)

    return redirect('conversation', pk=conversation.pk)

