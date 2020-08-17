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
			dict(title='+', width=15),
			dict(title='-', width=15),
			dict(title='0', width=15)
		]

		self.paletteView.group.left.text  = TextBox((0, 3, 50, 20), Glyphs.localize({'en': u'Left',  'zh': u'左'}), alignment='center', sizeStyle='mini')
		self.paletteView.group.right.text = TextBox((0, 3, 50, 20), Glyphs.localize({'en': u'Right', 'zh': u'右'}), alignment='center', sizeStyle='mini')

		self.paletteView.group.left.up    = SegmentedButton((0, 23, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.buttonCallback)
		self.paletteView.group.left.mid   = SegmentedButton((0, 43, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.buttonCallback)
		self.paletteView.group.left.down  = SegmentedButton((0, 63, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.buttonCallback)
		self.paletteView.group.right.up   = SegmentedButton((0, 23, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.buttonCallback)
		self.paletteView.group.right.mid  = SegmentedButton((0, 43, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.buttonCallback)
		self.paletteView.group.right.down = SegmentedButton((0, 63, 55, 10), segment_descriptions, sizeStyle='mini', selectionStyle='one', callback=self.buttonCallback)

		self.buttonValueMapping = {1:0, -1:1, 0:2}

		# Set dialog to NSView
		self.dialog = self.paletteView.group.getNSView()

	@objc.python_method
	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		Glyphs.addCallback(self.update, UPDATEINTERFACE)
		# Glyphs.addCallback(self.buttonCallback, UPDATEINTERFACE)
		# Glyphs.addCallback(self.buttonLeftUpCallback, UPDATEINTERFACE)
		# Glyphs.addCallback(self.initializeCallback, UPDATEINTERFACE)

	@objc.python_method
	def __del__(self):
		Glyphs.removeCallback(self.update)
		Glyphs.removeCallback(self.buttonCallback)
		Glyphs.removeCallback(self.initializeCallback)

	@objc.python_method
	def update(self, sender):
		font = sender.object()
		print('Font:', font)

		if font.currentTab:
			# In the Edit View
			pass
		else:
			# In the Font view
			try:
				if len(font.selection) is 1:
					hanTag = font.selection[0].userData['HanTag']
					self.paletteView.group.left.up.set(self.buttonValueMapping[hanTag['LeftKern'][0]])
					self.paletteView.group.left.mid.set(self.buttonValueMapping[hanTag['LeftKern'][1]])
					self.paletteView.group.left.down.set(self.buttonValueMapping[hanTag['LeftKern'][2]])
					self.paletteView.group.right.up.set(self.buttonValueMapping[hanTag['RightKern'][0]])
					self.paletteView.group.right.mid.set(self.buttonValueMapping[hanTag['RightKern'][1]])
					self.paletteView.group.right.down.set(self.buttonValueMapping[hanTag['RightKern'][2]])
				else:
					self.paletteView.group.left.up.set(-1)
					self.paletteView.group.left.mid.set(-1)
					self.paletteView.group.left.down.set(-1)
					self.paletteView.group.right.up.set(-1)
					self.paletteView.group.right.mid.set(-1)
					self.paletteView.group.right.down.set(-1)
				# s = set([i.userData['HanTag']['LeftKern'][0] for i in font.selection])
				# print(s)
				# if len(s) is 1:
				# 	self.paletteView.group.left.up.set(self.buttonValueMapping[s[0]])
			except:
				pass

	# 	# Send text to dialog to display
	# 	# self.textField.setStringValue_('\n'.join(text))
	# 	self.paletteView.group.text.set('\n'.join(text))


	def buttonCallback(self, sender):
		print('button hit!')
		print(sender)

	@objc.python_method
	def initializeCallback(self, sender):
		for i in Glyphs.font.glyphs:
			if not i.userData['HanTag']:
				i.userData['HanTag'] = {
					'LeftKern':  (0, 0, 0),
					'RightKern': (0, 0, 0),
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
