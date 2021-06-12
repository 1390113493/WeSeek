from rest_framework.views import APIView

from extensions.response import success, fail
from message.message import MessageManagement


class UnreadMessageListView(APIView):
    """
    未读消息列表
    """

    def get(self, *args, **kwargs):
        uid = self.request.user
        data = MessageManagement(uid).get_unread_list()
        return success('成功获得未读列表', data)


class MessageListView(APIView):
    """
    消息列表
    """

    def get(self, *args, **kwargs):
        uid = self.request.user
        to_uid = self.request.GET.get('uid')
        return success('成功获得消息列表', MessageManagement(uid).get_message_list(to_uid))


class SendMessageView(APIView):
    """
    发送消息
    """
    def post(self, *args, **kwargs):
        uid = self.request.user
        to = self.request.POST.get('to')
        message = self.request.POST.get('message')
        if MessageManagement(uid).user_send(to, message):
            return success('发送私信成功')
        else:
            return fail('发送私信失败')


class SystemMessageView(APIView):
    """
    系统消息列表
    """
    def get(self, *args, **kwargs):
        uid = self.request.user
        return success('成功获得消息列表', MessageManagement(uid).get_system_message())


class MessageDetailView(APIView):
    """
    获得系统消息的详细信息
    """
    def get(self, *args, **kwargs):
        uid = self.request.user
        mid = self.request.GET.get('mid')
        return success('成功获得消息内容', MessageManagement(uid).get_message_detail(mid))