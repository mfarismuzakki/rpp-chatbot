import os
import re

from core.config import *

from django.views.generic import View
from django.db.models import Q
from django.utils import timezone

from user.models import *
from chat.models import * 

from chat.utils.neo4j_setup import Neo4jConnection
from chat.utils.query_handler import createQuery

class ChatApi(View):

    conn = Neo4jConnection(uri=NEO4J_URI, user=NEO4J_USER, pwd=NEO4J_PWD)
    notFound = "Mohon ulangi pertanyaan anda"

    def __init__(self):
        pass

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
    def store_message(cls, sender_id, message):
        """
        menyimpan pesan
        """
        
        # recipient is botadmin
        recipient = User.objects \
            .filter(id = 1) \
            .first()
       
        new_message_data = Chat(
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
        bot_message = cls.response_by_bot(message)
        if bot_message != cls.notFound:
            bot_message = cls.listToString(bot_message)

        new_message_data = Chat(
            message = bot_message,
            recipient_id = sender_id,
            sender_id = 1,
            create_dt = timezone.now()
        )

        new_message_data.save()

    @classmethod
    def listToString(cls, s): 
        # initialize an empty string
        str1 = "" 
        
        # traverse in the string  
        for ele in s: 
            str1 += " "
            str1 += ele  
        
        # return string  
        return str1 

    @classmethod
    def response_by_bot(cls, message):
        """
        inferensi balasan dari admin
        """

        list_query_special= [
            '''
            MATCH (a:Amalan {name:"solat"})-[:jenis_amalan]->(j:JenisAmalan)
            MATCH (a)-[:amalan_wajib]->(f:Farduain)
            MATCH (a)-[:amalan_sunnah]->(s:Sunnah)
            MATCH (a)-[:amalan_fardu_kifayah]->(fk:FarduKifayah)
            RETURN j,f,fk
            ''',
            '''
            MATCH (a:Amalan {name:"shaum"})-[:jenis_amalan]->(j:JenisAmalan)
            MATCH (a)-[:amalan_wajib]->(f:Farduain)
            MATCH (a)-[:amalan_sunnah]->(s:Sunnah)
            RETURN j,f
            '''
        ]

        stemp = createQuery(message)
        check = False
        for x in list_query_special:
            try:
                if stemp.replace(" ","") == x.replace(" ",""):
                    check = True
                    break
            except:
                pass

        if not check:
            result = cls.conn.query(stemp)
            if result:
                temp = []
                for r in result: 
                    if r[0].get('name') != None: #jika properti name
                        if r[0].get('name') not in temp:
                            temp.append(r[0].get('name'))
                    elif r[0].get('detail') != None: #jika properti detail
                        if r[0].get('name') not in temp:
                            temp.append(r[0].get('detail'))
                    else: #jika properti type (relasi / predikat)
                        tampungan = result[0][0].type
                        tampungan = tampungan.replace("amalan","")
                        tampungan = tampungan.replace("_"," ")
                        tampungan = tampungan.replace(" ","",1)
                        if tampungan not in temp:
                            temp.append(tampungan)

                return (temp)
            else:
                return (cls.notFound)
        else:
            result = cls.conn.query(stemp)
            if result:
                temp = []
                for r in result:
                    for i in range(len(r)):
                        try:
                            if r[i].get('name') != None: #jika properti name
                                if r[i].get('name') not in temp:
                                    temp.append(r[i].get('name'))
                            if r[i].get('detail') != None: #jika properti detail
                                if r[i].get('detail') not in temp:
                                    temp.append(r[i].get('detail'))
                        except:
                            if r[i].get('name') != None: #jika properti name
                                if r[i].get('name') not in temp:
                                    temp.append(r[i].get('name'))
                return(temp)
            else:
                return(cls.notFound)
