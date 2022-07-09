# -*- coding: UTF-8 -*-
# power status notifications: This add-on plays a tone when the power status changes.
# Copyright (C) 2019 David CM
# Author: David CM <dhf360@gmail.com>
# Released under GPL 2
#globalPlugins/powerStatusNotifications.py

import addonHandler
import core
import globalPluginHandler
import tones
import winKernel


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	WM_POWERBROADCAST = 0x218
	PBT_APMPOWERSTATUSCHANGE = 0xA
	UNKNOWN_BATTERY_STATUS = 0xFF
	AC_ONLINE = 0X1
	NO_SYSTEM_BATTERY = 0X80

	def __init__(self):
		super().__init__()
		self.oldBatteryStatus = None
		self.handlePowerStatusChange()
		core.post_windowMessageReceipt.register(self.processMessages)

	def terminate(self):
		super().terminate()
		core.post_windowMessageReceipt.unregister(self.processMessages)

	def processMessages(self, msg, wParam, lParam):
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
			# Notification when the battery is plugged in, and now is charging.
			tones.beep(1120, 120, 50)
		else:
			tones.beep(280, 120, 50)
