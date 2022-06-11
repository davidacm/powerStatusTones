# -*- coding: UTF-8 -*-
# power status notiffications: This add-on plays a tone when the power status changes.
# Copyright (C) 2019 David CM
# Author: David CM <dhf360@gmail.com>
# Released under GPL 2
#globalPlugins/powerStatusNotiffications.py

import extensionPoints, globalPluginHandler, tones, windowUtils, winKernel, addonHandler

post_windowMessageReceipt = extensionPoints.Action()

class MessageWindow(windowUtils.CustomWindow):
	className = u"PowerStatusNotiffications"
	WM_POWERBROADCAST = 0x218
	PBT_APMPOWERSTATUSCHANGE = 0xA
	UNKNOWN_BATTERY_STATUS = 0xFF
	AC_ONLINE = 0X1
	NO_SYSTEM_BATTERY = 0X80
	def __init__(self, windowName=None):
		super(MessageWindow, self).__init__(windowName)
		self.oldBatteryStatus = None
		self.handlePowerStatusChange()

	def windowProc(self, hwnd, msg, wParam, lParam):
		post_windowMessageReceipt.notify(msg=msg, wParam=wParam, lParam=lParam)
		if msg == self.WM_POWERBROADCAST and wParam == self.PBT_APMPOWERSTATUSCHANGE:
			self.handlePowerStatusChange()

	def handlePowerStatusChange(self):
		sps = winKernel.SYSTEM_POWER_STATUS()
		if not winKernel.GetSystemPowerStatus(sps) or sps.BatteryFlag is self.UNKNOWN_BATTERY_STATUS or sps.BatteryFlag & self.NO_SYSTEM_BATTERY or sps.ACLineStatus == self.oldBatteryStatus:
			return
		if self.oldBatteryStatus is None:
			self.oldBatteryStatus = sps.ACLineStatus
			return
		self.oldBatteryStatus = sps.ACLineStatus
		if sps.ACLineStatus & self.AC_ONLINE:
			# Notiffication when the battery is plugged in, and now is charging.
			tones.beep(1120, 120, 50)
		else: tones.beep(280, 120, 50)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.messageWindow = MessageWindow()

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		self.messageWindow.destroy()
