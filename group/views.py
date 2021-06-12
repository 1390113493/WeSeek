from rest_framework.views import APIView

from extensions.response import success, fail
from group.group import Group, group_info, group_list


class InitGroupView(APIView):
    """
    新建队伍
    """

    def post(self, *args, **kwargs):
        uid = self.request.user
        cid = self.request.POST.get('cid')
        requirement = self.request.POST.get('requirement')
        allow_time = self.request.POST.get('allowtime')
        remarks = self.request.POST.get('remarks')
        amount = int(self.request.POST.get('amount', 0))
        if amount < 1:
            return fail('要求人数不得少于1人')
        res = Group(uid).initialise_group(cid, amount, requirement, allow_time, remarks)
        if res[0]:
            return success(res[1])
        else:
            return fail(res[1])


class JoinGroupView(APIView):
    """
    加入队伍
    """

    def post(self, *args, **kwargs):
        uid = self.request.user
        gid = self.request.POST.get('gid')
        res = Group(uid, gid).join_group()
        if res[0]:
            return success(res[1])
        else:
            return fail(res[1])


class CancelGroupView(APIView):
    """
    取消加入队伍
    """

    def post(self, *args, **kwargs):
        uid = self.request.user
        gid = self.request.POST.get('gid')
        res = Group(uid, gid).cancel_join()
        if res[0]:
            return success(res[1])
        else:
            return fail(res[1])


class GroupInfoView(APIView):
    """
    队伍信息
    """
    authentication_classes = []

    def get(self, *args, **kwargs):
        gid = int(self.request.GET.get('gid', 0))
        return success('成功获得队伍信息', group_info(gid))


class GroupListView(APIView):
    """
    队伍列表
    """
    authentication_classes = []

    def get(self, *args, **kwargs):
        cid = int(self.request.GET.get('cid', 0))
        return success('成功获得队伍列表', group_list(cid))


class GroupManagementView(APIView):
    """
    对参加队伍人员进行管理
    """
    def post(self, *args, **kwargs):
        uid = self.request.user
        jid = self.request.POST.get('jid')
        status = int(self.request.POST.get('status'))
        if Group(uid).manage(jid, status):
            return success('处理申请成功')
        else:
            return fail('处理申请失败')

