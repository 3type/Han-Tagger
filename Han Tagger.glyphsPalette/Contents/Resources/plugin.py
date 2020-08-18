# encoding: utf-8

###########################################################################################################
#
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals

import objc

from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *


class HanTagger(PalettePlugin):

	dialog = objc.IBOutlet()
	textField = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({'en': u'Han Tagger', 'zh': u'汉字标签器'})

		# Create Vanilla window and group with controls
		width = 200
		height = 105
		self.paletteView = Window((width, height))
		self.paletteView.group = Group((0, 0, width, height))

		self.paletteView.group.labels = VerticalStackGroup((10, 0, 15, 70))
		self.paletteView.group.left   = VerticalStackGroup((40, 0, 70, 70))
		self.paletteView.group.right  = VerticalStackGroup((95, 0, 70, 70))

		self.paletteView.group.labels.up   = TextBox((0, 20, 30, 10), Glyphs.localize({'en': u'Up',   'zh': u'上'}), sizeStyle='mini')
		self.paletteView.group.labels.mid  = TextBox((0, 40, 30, 10), Glyphs.localize({'en': u'Mid',  'zh': u'中'}), sizeStyle='mini')
		self.paletteView.group.labels.down = TextBox((0, 60, 30, 10), Glyphs.localize({'en': u'Down', 'zh': u'下'}), sizeStyle='mini')

		self.paletteView.group.initialize = Button(
			posSize=(10, 80, 60, 15),
			title=Glyphs.localize({'en': u'Initialize', 'zh': u'初始化'}),
			sizeStyle='mini',
			callback=self.initializeCallback)

		segment_descriptions = [
			dict(title='0', width=15),
			dict(title='+', width=15),
			dict(title='-', width=15)
		]

		self.paletteView.group.left.text  = TextBox((0, 3, 50, 20), Glyphs.localize({'en': u'Left',  'zh': u'左'}), alignment='center', sizeStyle='mini')
		self.paletteView.group.right.text = TextBox((0, 3, 50, 20), Glyphs.localize({'en': u'Right', 'zh': u'右'}), alignment='center', sizeStyle='mini')

		self.paletteView.group.left.up    = SegmentedButton((0, 23, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.leftUpButtonCallback)
		self.paletteView.group.left.mid   = SegmentedButton((0, 43, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.leftMidButtonCallback)
		self.paletteView.group.left.down  = SegmentedButton((0, 63, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.leftDownButtonCallback)
		self.paletteView.group.right.up   = SegmentedButton((0, 23, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.rightUpButtonCallback)
		self.paletteView.group.right.mid  = SegmentedButton((0, 43, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.rightMidButtonCallback)
		self.paletteView.group.right.down = SegmentedButton((0, 63, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.rightDownButtonCallback)

		# Set dialog to NSView
		self.dialog = self.paletteView.group.getNSView()

	@objc.python_method
	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		Glyphs.addCallback(self.update, UPDATEINTERFACE)

	@objc.python_method
	def __del__(self):
		Glyphs.removeCallback(self.update)
		Glyphs.removeCallback(self.leftUpButtonCallback)
		Glyphs.removeCallback(self.leftMidButtonCallback)
		Glyphs.removeCallback(self.leftDownButtonCallback)
		Glyphs.removeCallback(self.rightUpButtonCallback)
		Glyphs.removeCallback(self.rightMidButtonCallback)
		Glyphs.removeCallback(self.rightDownButtonCallback)
		Glyphs.removeCallback(self.initializeCallback)

	@objc.python_method
	def update(self, sender):
		font = sender.object()

		if font.currentTab:
			# In the Edit View
			pass
		else:
			# In the Font view
			try:
				leftUpKern    = []
				leftMidKern   = []
				leftDownKern  = []
				rightUpKern   = []
				rightMidKern  = []
				rightDownKern = []

				for i in font.selection:
					leftUpKern.append(i.userData['HanTag']['LeftKern'][0])
					leftMidKern.append(i.userData['HanTag']['LeftKern'][1])
					leftDownKern.append(i.userData['HanTag']['LeftKern'][2])
					rightUpKern.append(i.userData['HanTag']['RightKern'][0])
					rightMidKern.append(i.userData['HanTag']['RightKern'][1])
					rightDownKern.append(i.userData['HanTag']['RightKern'][2])

				leftUpKern    = list(set(leftUpKern))
				leftMidKern   = list(set(leftMidKern))
				leftDownKern  = list(set(leftDownKern))
				rightUpKern   = list(set(rightUpKern))
				rightMidKern  = list(set(rightMidKern))
				rightDownKern = list(set(rightDownKern))

				self.paletteView.group.left.up.set(leftUpKern[0] if len(leftUpKern) is 1 else -1)
				self.paletteView.group.left.mid.set(leftMidKern[0] if len(leftMidKern) is 1 else -1)
				self.paletteView.group.left.down.set(leftDownKern[0] if len(leftDownKern) is 1 else -1)
				self.paletteView.group.right.up.set(rightUpKern[0] if len(rightUpKern) is 1 else -1)
				self.paletteView.group.right.mid.set(rightMidKern[0] if len(rightMidKern) is 1 else -1)
				self.paletteView.group.right.down.set(rightDownKern[0] if len(rightDownKern) is 1 else -1)

			except:
				pass

	@objc.python_method
	def leftUpButtonCallback(self, sender):
		for i in Glyphs.font.selection:
			i.userData['HanTag']['LeftKern'][0] = sender.get()

	@objc.python_method
	def leftMidButtonCallback(self, sender):
		for i in Glyphs.font.selection:
			i.userData['HanTag']['LeftKern'][1] = sender.get()

	@objc.python_method
	def leftDownButtonCallback(self, sender):
		for i in Glyphs.font.selection:
			i.userData['HanTag']['LeftKern'][2] = sender.get()

	@objc.python_method
	def rightUpButtonCallback(self, sender):
		for i in Glyphs.font.selection:
			i.userData['HanTag']['RightKern'][0] = sender.get()

	@objc.python_method
	def rightMidButtonCallback(self, sender):
		for i in Glyphs.font.selection:
			i.userData['HanTag']['RightKern'][1] = sender.get()

	@objc.python_method
	def rightDownButtonCallback(self, sender):
		for i in Glyphs.font.selection:
			i.userData['HanTag']['RightKern'][2] = sender.get()

	@objc.python_method
	def initializeCallback(self, sender):
		for i in Glyphs.font.selection:
			if not i.userData['HanTag']:
				i.userData['HanTag'] = {
					'LeftKern':  [0, 0, 0],
					'RightKern': [0, 0, 0],
				}
			print('Initialize HanTag for {}!'.format(i.name))

	@objc.python_method
	def __file__(self):
		'''Please leave this method unchanged'''
		return __file__

	# Temporary Fix
	# Sort ID for compatibility with v919:
	_sortID = 0
	@objc.python_method
	def setSortID_(self, id):
		try:
			self._sortID = id
		except Exception as e:
			self.logToConsole( 'setSortID_: %s' % str(e) )

	@objc.python_method
	def sortID(self):
		return self._sortID
