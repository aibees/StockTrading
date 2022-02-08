import pythoncom
from PyQt5.QtWidgets import *
import win32com.client

import win32event

StopEvent = win32event.CreateEvent(None, 0, 0, None)


class CpEvent:
    def set_params(self, client, name, caller):
        self.client = client  # CP 실시간 통신 object
        self.name = name  # 서비스가 다른 이벤트를 구분하기 위한 이름
        self.caller = caller  # callback 을 위해 보관

    def OnReceived(self):
        self.caller.updates()
        win32event.SetEvent(StopEvent)
        return


class CpCurReply:
    def __init__(self, objEvent, caller):
        self.name = "stockmst"
        self.obj = objEvent
        self.caller = caller

    def Subscribe(self):
        handler = win32com.client.WithEvents(self.obj, CpEvent)
        handler.set_params(self.obj, self.name, self.caller)


def MessagePump(timeout):
    waitables = [StopEvent]
    while 1:
        rc = win32event.MsgWaitForMultipleObjects(
            waitables,
            0,  # Wait for all = false, so it waits for anyone
            timeout,  # (or win32event.INFINITE)
            win32event.QS_ALLEVENTS
        )  # Accepts all input
        if rc == win32event.WAIT_OBJECT_0:
            # Our first event listed, the StopEvent, was triggered, so we must exit
            break

        elif rc == win32event.WAIT_OBJECT_0 + len(waitables):
            if pythoncom.PumpWaitingMessages():
                break  # we received a wm_quit message
        elif rc == win32event.WAIT_TIMEOUT:
            print('timeout')
            return
            pass
        else:
            print('exception')
            raise RuntimeError("unexpected win32wait return value")


##############################################################
# 2. Request ==> 메시지 펌프 ==>  OnReceived 이벤트 수신
# code : list 형태로 inputvalue에 들어가는 순서대로 넣어져 있어야 함
def process(order, param, obj, caller):
    objReply = CpCurReply(obj, caller)
    objReply.Subscribe()

    for n, v in zip(order, param):
        obj.SetInputValue(n, v)
    obj.Request()
    MessagePump(10000)
