import win32com.client
import ctypes
from config import *
from pywinauto import application
from pywinauto import timings

g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
g_objCpTrade = win32com.client.Dispatch('CpTrade.CpTdUtil')
g_objStockMgr = win32com.client.Dispatch('CpUtil.CpStockCode')

def init_plus_check():
    # 관리자 권한으로 실행되었는가
    if ctypes.windll.shell32.IsUserAnAdmin():
        print('정상: 관리자권한으로 실행된 프로세스입니다.')
    else:
        print('오류: 일반권한으로 실행됨. 관리자 권한으로 실행해 주세요')
        return False
    if g_objCpStatus.IsConnect == 0:
        print("PLUS가 정상적으로 연결되지 않음")
        return False
    return True


class CREON:
    init_plus_check()

    def __init__(self):
        self.objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.check_connected()
    def check_connected(self):
        connection = self.objCpCybos.IsConnect
        if connection == 0:
            self.connect()
            connection = self.objCpCybos.IsConnect
            if connection == 0:
                raise ConnectionError("Login failed. Not connected")
            else:
                print("Successfully connected")
        else:
            print("Successfully connected")

    def connect(self):
        app = application.Application()
        app.start(
            'C:\CREON\STARTER\coStarter.exe /prj:cp /id:{id} /pwd:{pwd} /pwdcert:{pwdcert} /autostart'.format(
                id=id, pwd=password, pwdcert=credential
            )
        )

    def check_remain_time(self):
        # 연속 요청 가능 여부 체크
        remainTime = self.objCpCybos.LimitRequestRemainTime# / 1000.
        remainCount = self.objCpCybos.GetLimitRemainCount(1)  # 시세 제한
        print("남은시간: ",remainTime, " 남은개수: ", remainCount)
        if remainCount <= 0:
            print("15초당 60건으로 제한합니다.")
           # time.sleep(remainTime)