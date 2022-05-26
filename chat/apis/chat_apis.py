from email.errors import CharsetError
import os

from django.views.generic import View
from django.db.models import Q
from django.utils import timezone

from user.models import *
from chat.models import * 

import pickle


class ChatApi(View):

    @classmethod
    def get_user_chat(cls, user_id):
        """
        mendapatkan list grup chat
        """
        user_id = int(user_id)

        # filter
        filter = Q(sender_id=user_id) | Q(recipient_id=user_id) 

        chat_list = \
            Chat.objects \
                .filter(filter) \
                .order_by('-create_dt') \
                .values('sender_id', 'recipient_id',
                        'sender__username', 
                        'recipient__username', 
                        'message', 'create_dt')
    

        chat_list, _ = cls.get_chat_list(chat_list, user_id)

        return chat_list
        
    @classmethod
    def get_chat_list(cls, chat_list, user_id, target_id=1):
        result = []
        target_username = ''

        if target_id == None:
            return [], ''
        
        target_id = int(target_id)

        for chat in reversed(chat_list):
            if chat['sender_id'] == user_id and chat['recipient_id'] == target_id:
                result.append({
                    "message" : chat['message'],
                    "create_dt" : chat['create_dt'],
                    "sender" : 0
                })
                if target_username == '':
                    target_username = chat['recipient__username']
            
            if chat['sender_id'] == target_id:
                result.append({
                    "message" : chat['message'],
                    "create_dt" : chat['create_dt'],
                    "sender" : 1
                })
                if target_username == '':
                    target_username = chat['sender__username']
        
        return result, target_username

    @classmethod
    def get_username_list(cls, chat_list, user_id):
        """
        mendapatkan list nomor telepon chat
        """
        # username_list = []
        # result = []

        # for chat in chat_list: 
        #     if chat['sender__username'] not in username_list and \
        #        chat['sender_id'] != user_id:

        #         username_list.append(chat['sender__username'])
            
        #     if chat['recipient__username'] not in username_list and \
        #        chat['recipient_id'] != user_id:

        #         username_list.append(chat['recipient__username'])
 
        # result = []       
        # for chat in chat_list:
        #     if len(username_list) == 0:
        #         break

        #     if chat['recipient__username'] in username_list:
        #         result.append({
        #             "username" : chat['recipient__username'],
        #             "user_id" : chat['recipient_id'],
        #             "message" : chat['message'],
        #             "create_dt" : chat['create_dt'],
        #             "type" : chat['type__type'],
        #         })
        #         index = username_list.index(chat['recipient__username'])
        #         username_list.pop(index)

        #     if chat['sender__username'] in username_list:
        #         result.append({
        #             "username" : chat['sender__username'],
        #             "user_id" : chat['sender_id'],
        #             "message" : chat['message'],
        #             "create_dt" : chat['create_dt'],
        #             "type" : chat['type__type'],
        #         })
        #         index = username_list.index(chat['sender__username'])
        #         username_list.pop(index)

        return []

    @classmethod
    def store_message(cls, sender_id, message):
        """
        menyimpan pesan
        """
        
        # recipient is botadmin
        recipient = User.objects \
            .filter(id = 1) \
            .first()
       
        new_message_data = CharsetError(
            message = message,
            recipient = recipient,
            sender_id = sender_id,
            create_dt = timezone.now()
        )

        new_message_data.save()

        cls.reply_message_by_bot(sender_id, message)

    
    @classmethod
    def reply_message_by_bot(cls, sender_id, message):
        """
        menyimpan balasan pesan dari bot
        """

        # recipient is botadmin
        recipient = User.objects \
            .filter(id = sender_id) \
            .first()

        bot_message = cls.response_by_bot(message)

        new_message_data = CharsetError(
            message = bot_message,
            recipient = sender_id,
            sender_id = 1,
            create_dt = timezone.now()
        )
        
        new_message_data.save()

    @classmethod
    def response_by_bot(cls, message):
        """
        inferensi balasan dari admin
        """

        return "saat ini admin sedang sibuk, maaf :("



