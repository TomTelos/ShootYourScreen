###########################################
# maintainer: <plnick@vuplus-support.org> #
#    http://www.vuplus-support.org		  #
##		   Modified by TomTelos			 ##
###########################################

#This plugin is free software, you are allowed to
#modify it (if you keep the license),
#but you are not allowed to distribute/publish
#it without source code (this version and your modifications).
#This means you also have to distribute
#source code of your modifications.

# camera icon is taken from oxygen icon theme for KDE 4

from enigma import eActionMap
from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigSelection, ConfigEnableDisable, ConfigYesNo, ConfigInteger
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from time import localtime, time
from os import system, path, mkdir, makedirs
from __init__ import _

pluginversion = "Version: 0.1-r5"
config.plugins.shootyourscreen = ConfigSubsection()
config.plugins.shootyourscreen.enable = ConfigEnableDisable(default=True)
config.plugins.shootyourscreen.switchtext = ConfigYesNo(default=True)
config.plugins.shootyourscreen.path = ConfigSelection(default = "/media/hdd", choices = [("/media/hdd"), ("/media/usb"), ("/media/hdd1"), ("/media/usb1"), ("/tmp", "/tmp")])
config.plugins.shootyourscreen.pictureformat = ConfigSelection(default = "bmp", choices = [("bmp", "bmp"), ("-j", "jpg"), ("-p", "png")])
config.plugins.shootyourscreen.jpegquality = ConfigSelection(default = "100", choices = [("10"), ("20"), ("40"), ("60"), ("80"), ("100")])
config.plugins.shootyourscreen.picturetype = ConfigSelection(default = "all", choices = [("all", "OSD + Video"), ("-v", "Video"), ("-o", "OSD")])
config.plugins.shootyourscreen.picturesize = ConfigSelection(default = "default", choices = [("default", _("Skin resolution")), ("-r 480", "480"), ("-r 576", "576"), ("-r 720", "720"), ("-r 960", "960"), ("-r 1280", "1280"), ("-r 1920", "1920")])
config.plugins.shootyourscreen.timeout = ConfigSelection(default = "5", choices = [("1", "1 sec"), ("3", "3 sec"), ("5", "5 sec"), ("10", "10 sec"), ("off", _("no message"))])

def Plugins(**kwargs):
			return [PluginDescriptor(where = [PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc = autostart),
				PluginDescriptor(name = "ShootYourScreen", description = _("make Screenshots"), where = PluginDescriptor.WHERE_PLUGINMENU, icon="shootyourscreen.png", fnc=startSetup),
				PluginDescriptor(name = "ShootYourScreen", description = _("make Screenshots"), where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=startSetup)]

def autostart(reason, **kwargs):
	if kwargs.has_key("session") and reason == 0:
		session = kwargs["session"]
		print "[ShootYourScreen] start...."
		session.open(getScreenshot)

def startSetup(session, **kwargs):
		print "[ShootYourScreen] start configuration"
		session.open(ShootYourScreenConfig)

def getPicturePath():
	picturepath = config.plugins.shootyourscreen.path.value
	if picturepath.endswith('/'):
		picturepath = picturepath + 'screenshots'
	else:
		picturepath = picturepath + '/screenshots'

	try:
		if (path.exists(picturepath) == False):
			makedirs(picturepath)
	except OSError:
		self.session.open(MessageBox, _("Sorry, your device for screenshots is not writeable.\n\nPlease choose another one."), MessageBox.TYPE_INFO, timeout = 10)
	return picturepath


class getScreenshot(Screen):
	skin = ""
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.skin = getScreenshot.skin
		self.previousflag = 0
		eActionMap.getInstance().bindAction('', -0x7FFFFFFF, self.screenshotKey)

	def screenshotKey(self, key, flag):
		if config.plugins.shootyourscreen.enable.value:
			if key == 388:
				if not config.plugins.shootyourscreen.switchtext.value:
					if flag == 3:
						self.previousflag = flag
						self.grabScreenshot()
						return 1
					if self.previousflag == 3 and flag ==1:
						self.previousflag = 0
						return 1
				else:
					if flag == 0:
						return 1
					if flag == 3:
						self.previousflag = flag
						return 0
					if flag == 1 and self.previousflag == 0:
						self.grabScreenshot()
						return 1
					if self.previousflag == 3 and flag ==1:
						self.previousflag = 0
						return 0
		return 0

	def grabScreenshot(self, ret = None):
		self.filename = self.getFilename()
		print "[ShootYourScreen] grab screenshot to %s" % self.filename
		cmd = "grab"
		if not config.plugins.shootyourscreen.picturetype.value == "all":
			self.cmdoptiontype = " " + str(config.plugins.shootyourscreen.picturetype.value)
			cmd += self.cmdoptiontype
		if not config.plugins.shootyourscreen.picturesize.value == "default":
			self.cmdoptionsize = " " + str(config.plugins.shootyourscreen.picturesize.value)
			cmd += self.cmdoptionsize
		if not config.plugins.shootyourscreen.pictureformat.value == "bmp":
			self.cmdoptionformat = " " + str(config.plugins.shootyourscreen.pictureformat.value)
			cmd += self.cmdoptionformat
			if config.plugins.shootyourscreen.pictureformat.value == "-j":
				self.cmdoptionquality = " " + str(config.plugins.shootyourscreen.jpegquality.value)
				cmd += self.cmdoptionquality
		cmd += " %s" % self.filename
		ret = system(cmd)
		self.gotScreenshot(ret)

	def gotScreenshot(self, ret):
		if not config.plugins.shootyourscreen.timeout.value == "off":
			self.messagetimeout = int(config.plugins.shootyourscreen.timeout.value)
			if ret == 0:
				self.session.open(MessageBox, _("Screenshot successfully saved as:\n%s") % self.filename, MessageBox.TYPE_INFO, timeout = self.messagetimeout)
			else:
				self.session.open(MessageBox, _("Grabbing Screenshot failed !!!"), MessageBox.TYPE_ERROR, timeout = self.messagetimeout)
		else:
			pass

	def getFilename(self):
		time = localtime()
		year = str(time.tm_year)
		month = time.tm_mon
		day = time.tm_mday
		hour = time.tm_hour
		minute = time.tm_min
		second = time.tm_sec
		if month < 10:
			month = "0" + str(month)
		else:
			month = str(month)
		if day < 10:
			day = "0" + str(day)
		else:
			day = str(day)
		if hour < 10:
			hour = "0" + str(hour)
		else:
			hour = str(hour)
		if minute < 10:
			minute = "0" + str(minute)
		else:
			minute = str(minute)
		if second < 10:
			second = "0" + str(second)
		else:
			second = str(second)
		self.screenshottime = "screenshot_" + year + "-" + month + "-" + day + "_" + hour + "-" + minute + "-" + second
		
		if config.plugins.shootyourscreen.pictureformat.value == "bmp":
			self.fileextension = ".bmp"
		elif config.plugins.shootyourscreen.pictureformat.value == "-j":
			self.fileextension = ".jpg"
		elif config.plugins.shootyourscreen.pictureformat.value == "-p":
			self.fileextension = ".png"

		self.picturepath = getPicturePath()
		if self.picturepath.endswith('/'):
			self.screenshotfile = self.picturepath + self.screenshottime + self.fileextension
		else:
			self.screenshotfile = self.picturepath + '/' + self.screenshottime + self.fileextension
		return self.screenshotfile

class ShootYourScreenConfig(Screen, ConfigListScreen):

	skin = """
		<screen position="center,center" size="650,400" title="ShootYourScreen" >
		<widget name="config" position="10,10" size="630,350" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ShootYourScreen/pic/button_red.png" zPosition="2" position="10,370" size="25,25" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ShootYourScreen/pic/button_green.png" zPosition="2" position="130,370" size="25,25" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ShootYourScreen/pic/button_yellow.png" zPosition="2" position="270,370" size="25,25" alphatest="on" />
		<widget name="buttonred" position="40,372" size="100,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
		<widget name="buttongreen" position="160,372" size="100,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
		<widget name="buttonyellow" position="300,372" size="100,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
		</screen>"""

	def __init__(self,session):
		self.session = session
		Screen.__init__(self,session)
		
		self.createConfigList()

		ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)

		self["buttonred"] = Label(_("Exit"))
		self["buttongreen"] = Label(_("Save"))
		self["buttonyellow"] = Label(_("Default"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"green": self.keyGreen,
				"red": self.cancel,
				"yellow": self.revert,
				"cancel": self.cancel,
				"ok": self.keyGreen,
			}, -2)
			
		self.onShown.append(self.setWindowTitle)
		
	def setWindowTitle(self):
		self.setTitle(_("ShootYourScreen - %s") % pluginversion)
		
	def createConfigList(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Enable ShootYourScreen :"), config.plugins.shootyourscreen.enable))
		if config.plugins.shootyourscreen.enable.value == True:
			self.list.append(getConfigListEntry(_("Screenshot of :"), config.plugins.shootyourscreen.picturetype))
			self.list.append(getConfigListEntry(_("Format for screenshots :"), config.plugins.shootyourscreen.pictureformat))
			if config.plugins.shootyourscreen.pictureformat.value == "-j":
				self.list.append(getConfigListEntry(_("Quality of jpg picture :"), config.plugins.shootyourscreen.jpegquality))
			self.list.append(getConfigListEntry(_("Picture size (width) :"), config.plugins.shootyourscreen.picturesize))
			self.list.append(getConfigListEntry(_("Path for screenshots :"), config.plugins.shootyourscreen.path))
			self.list.append(getConfigListEntry(_("Switch TEXT and TEXT long button :"), config.plugins.shootyourscreen.switchtext))
			self.list.append(getConfigListEntry(_("Timeout for info message :"), config.plugins.shootyourscreen.timeout))

	def changedEntry(self):
		self.createConfigList()
		self["config"].setList(self.list)

	def save(self):
		for x in self["config"].list:
			x[1].save()
		self.changedEntry()

	def keyGreen(self):
		self.save()
		self.close(False,self.session)

	def cancel(self):
		if self["config"].isChanged():
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _("Really close without saving settings?"), MessageBox.TYPE_YESNO, default = True)
		else:
			for x in self["config"].list:
				x[1].cancel()
			self.close(False,self.session)

	def cancelConfirm(self, result):
		if result is None or result is False:
			print "[ShootYourScreen] Cancel not confirmed."
		else:
			print "[ShootYourScreen] Cancel confirmed. Configchanges will be lost."
			for x in self["config"].list:
				x[1].cancel()
			self.close(False,self.session)

	def revert(self):
		self.session.openWithCallback(self.keyYellowConfirm, MessageBox, _("Reset ShootYourScreen settings to defaults?"), MessageBox.TYPE_YESNO, timeout = 20, default = True)

	def keyYellowConfirm(self, confirmed):
		if not confirmed:
			print "[ShootYourScreen] Reset to defaults not confirmed."
		else:
			print "[ShootYourScreen] Setting Configuration to defaults."
			config.plugins.shootyourscreen.enable.setValue(1)
			config.plugins.shootyourscreen.switchtext.setValue(1)
			config.plugins.shootyourscreen.path.setValue("/media/hdd")
			config.plugins.shootyourscreen.pictureformat.setValue("bmp")
			config.plugins.shootyourscreen.jpegquality.setValue("100")
			config.plugins.shootyourscreen.picturetype.setValue("all")
			config.plugins.shootyourscreen.picturesize.setValue("default")
			config.plugins.shootyourscreen.timeout.setValue("5")
			self.save()
