from rest_framework.views import APIView

from appointment.appoint import add_appointment, cancel_appointment, get_appointments, allow_appointment
from extensions.response import fail, success


class AppointmentSubmitView(APIView):
    """
    提交预约申请
    """

    def post(self, *args, **kwargs):
        uid = self.request.user
        from_time = self.request.POST.get('from')
        to_time = self.request.POST.get('to')
        if not from_time and to_time:
            return fail('时间不得为空')
        if to_time < from_time:
            return fail('结束时间不得小于开始时间')
        remarks = self.request.POST.get('remarks')
        amount = int(self.request.POST.get('amount', 1))
        if amount < 2:
            return fail('预约人数不得少于2人')
        phone = self.request.POST.get('phone')
        name = self.request.POST.get('name')
        title = self.request.POST.get('title')
        content = self.request.POST.get('title')
        if add_appointment(uid, amount, from_time, to_time, remarks, phone, name, title, content):
            return success('新增预约成功，请等待安排')
        else:
            return fail('预约失败')


class AppointmentDeleteView(APIView):
    """
    撤回申请
    """

    def post(self, *args, **kwargs):
        uid = self.request.user
        aid = int(self.request.POST.get('aid'), 0)
        if cancel_appointment(uid, aid):
            return success('撤回申请成功')
        else:
            return fail('撤回申请失败')


class AppointmentListView(APIView):
    """
    申请列表
    """

    def get(self, *args, **kwargs):
        uid = self.request.user
        return success('成功获得申请列表', get_appointments(uid))


class AllowAppointmentView(APIView):
    """
    允许预约申请
    """
    def post(self, *args, **kwargs):
        aid = self.request.POST.get('aid')
        response = self.request.POST.get('response')
        allow_appointment(aid, response)
        return success('成功处理预约')