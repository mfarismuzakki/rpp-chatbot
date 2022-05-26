from django.shortcuts import render
from django.views.generic import View
from chat.apis.chat_apis import ChatApi

class ChatListView(View):
    @classmethod
    def get(cls, request):
        user_id = request.GET['user_id']
        chat_list = ChatApi.get_user_chat(user_id)
        
        context = {
            'chat_list' : chat_list,
        }

        return render(request, 'chat/messages/list.html', context)
    
    @classmethod
    def post(cls, request):

        user_id = request.GET['user_id']
        message = request.POST['message']

        ChatApi.store_message(user_id, message)
        
        chat_list = ChatApi.get_user_chat(user_id)
        
        context = {
            'chat_list' : chat_list,
        }

        return render(request, 'chat/messages/list.html', context)
