from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from . import models


class UserChatsListView(LoginRequiredMixin, generic.ListView):
    model = models.Chat
    context_object_name = 'user_chats'
    template_name = 'chat/index.html'


def room(request, room_id):
    return render(request, 'chat/room.html', {
        'room_id': room_id
    })
