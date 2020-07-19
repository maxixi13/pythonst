import win32api
import win32con
import win32gui

# 左点击

# win32api.SetCursorPos([2560, 1420])
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


str="微信"
aa=win32gui.FindWindow(0, str)
left, top, right, bottom = win32gui.GetWindowRect(aa)
# title = win32gui.GetWindowText(aa)   # name   
# clsname = win32gui.GetClassName(aa)  # class name     TrayNotifyWnd
win32gui.SetWindowPos(aa,win32con.HWND_TOP,0,0,1000,1000,win32con.SWP_NOMOVE)
print(left, top, right, bottom)