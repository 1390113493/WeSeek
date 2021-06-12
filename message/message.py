# -*- coding: utf-8 -*-
# @Time    : 2021/5/28 10:11
# @Author  : HUII
# @FileName: message.py
# @Software: PyCharm
from django.db.models import Q

from user.models import User
from .models import Message


class MessageManagement:
    """
    站内信管理
    """

    def __init__(self, uid):
        self.uid = uid

    def send(self, title, content):
        """
        发送站内信
        :param title:
        :param content:
        :return:
        """
        Message.objects.create(to_user_id=self.uid, message_title=title, message_content=content)

    def user_send(self, to_uid, content):
        """
        用户给其他用户发消息
        :param to_uid: 接收者
        :param content: 内容
        :return:
        """
        try:
            if self.uid == int(to_uid):
                return False
            Message.objects.create(from_user_id=self.uid, to_user_id=to_uid, message_content=content)
            return True
        except:
            return False

    def read(self, mid):
        """
        修改阅读状态
        :param mid:
        :return:
        """
        Message.objects.filter(id=mid, to_user_id=self.uid).update(have_read=True)

    #
    def get_unread_list(self):
        """
        获得未读列表
        :return:
        """
        unreads = Message.objects.filter(from_user__isnull=True, to_user_id=self.uid, have_read=False)
        count = unreads.count()
        unread_list = []
        for unread in unreads:
            unread_list.append({
                'id': unread.id,
                'title': unread.message_title,
                'time': str(unread.create_time).split('.')[0]
            })
        return {
            'count': count,
            'unreadList': unread_list
        }

    def get_message_list(self, to_uid=''):
        """
        获得消息列表
        :return:
        """
        messages = Message.objects.filter(Q(from_user_id=self.uid) | Q(to_user_id=self.uid, from_user__isnull=False))
        message_dict = {}
        user = User.objects.get(id=self.uid)
        avatar2 = user.avatar
        for message in messages:
            if message.from_user_id == self.uid:
                message_dict.setdefault(message.to_user_id, {
                    'nickname': message.to_user.nickname,
                    'avatar1': message.to_user.avatar,
                    'id1': message.to_user_id,
                    'avatar2': avatar2,
                    'id2': self.uid,
                    'pre': message.message_content,
                    'messageList': []
                })
                uid = message.to_user_id
            else:
                message_dict.setdefault(message.from_user_id, {
                    'nickname': message.from_user.nickname,
                    'avatar1': message.from_user.avatar,
                    'id1': message.from_user_id,
                    'avatar2': avatar2,
                    'id2': self.uid,
                    'pre': message.message_content,
                    'messageList': []
                })
                uid = message.from_user_id
            message_dict[uid]['pre'] = message.message_content
            message_dict[uid]['messageList'].append({
                'from': message.from_user_id,
                'content': message.message_content,
                'time': str(message.create_time).split('.')[0]
            })
        if to_uid and not message_dict.get(to_uid):
            user = User.objects.get(id=to_uid)
            message_dict[to_uid] = {
                'nickname': user.nickname,
                'avatar1': user.avatar,
                'id1': to_uid,
                'avatar2': avatar2,
                'id2': self.uid,
                'pre': '',
                'messageList': []
            }
        return list(message_dict.values())[::-1]

    def get_message_detail(self, mid):
        """
        获得消息详细内容
        :param mid:
        :return:
        """
        self.read(mid)
        message = Message.objects.get(id=mid)
        return {
            'message': {
                'id': message.id,
                'title': message.message_title,
                'content': message.message_content,
                'time': str(message.create_time).split('.')[0]
            }
        }

    def get_system_message(self):
        """
        获得系统消息列表
        :return:
        """
        messages = Message.objects.filter(to_user_id=self.uid, from_user__isnull=True).order_by('-id')
        message_list = []
        for message in messages:
            message_list.append({
                'id': message.id,
                'title': message.message_title,
                'unread': not message.have_read
            })
        return message_list
