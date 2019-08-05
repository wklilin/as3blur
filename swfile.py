#!/usr/bin/env python3
#coding:utf-8

import os
import struct
import json
import zlib
import math

def trace(args):
	print(args)

	
logs=[]
def callLogger(func):
	def inner(self,*args,**kwargs):
		log=func.__name__+':'+str(self.position)+':'
		val=func(self,*args,**kwargs)
		log=log+str(self.position)
		logs.append(log)
		return val
	return inner

class ByteArray(object):
	def __init__(self,data=b''):
		self.endian='='
		self.raw=data
		#self.length=len(self.raw)
		self.position=0
		
	@property
	def length(self):
		return len(self.raw)
		
	@length.setter
	def length(self,length):
		while len(self.raw)<length:
			self.raw+=b' '
		self.raw=self.raw[0:length]
		if self.position>length:
			self.position=length
		
	# @property
	# def position(self):
		# return self._position
		
	# @position.setter
	# def position(self,pos):
		# self._position=pos
		
	@property
	def bytesAvailable(self):
		return self.length-self.position
	
	def read(self,l):
		by=self.readAt(self.position,l)
		self.position+=l
		return by
		
	def write(self,bytes):
		len_b=len(bytes)
		self.writeAt(bytes,self.position)
		self.position+=len_b
		
	def readAt(self,offset,length):
		by=self.raw[offset:offset+length]
		return by
		
	def writeAt(self,bytes,offset):
		len_b=len(bytes)
		left=self.raw[0:offset]
		if (offset+len_b)>=self.length:
			self.raw=left+bytes
		else:
			self.raw=left+bytes+self.raw[(offset+len_b):]
		self.length=len(self.raw)
		
	@callLogger
	def writeBytes(self,ba,offset=0,length=0):
		if length==0:
			length=ba.length-offset
		by=ba.readAt(offset,length)
		self.write(by)
		
	@callLogger
	def readBytes(self,ba,offset=0,length=0):
		if length==0:
			length=self.bytesAvailable
		by=self.read(length)
		ba.writeAt(by,offset)
	
	@callLogger
	def uncompress(self):
		self.raw=zlib.decompress(self.raw)
		self.length=len(self.raw)
		self.position=0
		
	@callLogger
	def compress(self):
		self.raw=zlib.compress(self.raw)
		self.length=len(self.raw)
		self.position=self.length
		
	@callLogger
	def readByte(self):
		val = struct.unpack(self.endian+'B', self.read(1))[0]
		return val
		
	@callLogger
	def writeByte(self,v):
		bytes = struct.pack(self.endian+'B', v)
		self.write(bytes)
	
	@callLogger
	def readUnsignedByte(self):
		val = struct.unpack(self.endian+'B', self.read(1))[0]
		return val
		
	@callLogger
	def readShort(self):
		val = struct.unpack(self.endian+'h', self.read(2))[0]
		return val
		
	@callLogger
	def writeShort(self,v):
		bytes = struct.pack(self.endian+'h', v)
		self.write(bytes)
	
	@callLogger
	def readUnsignedShort(self):
		val = struct.unpack(self.endian+'H', self.read(2))[0]
		return val
	
	@callLogger
	def readUnsignedInt(self):
		val = struct.unpack(self.endian+'I', self.read(4))[0]
		return val
	
	@callLogger
	def writeUnsignedInt(self,v):
		bytes = struct.pack(self.endian+'I', v)
		self.write(bytes)
	
	@callLogger
	def readInt(self):
		val = struct.unpack(self.endian+'i', self.read(4))[0]
		return val
	
	@callLogger
	def writeInt(self,v):
		bytes = struct.pack(self.endian+'i', v)
		self.write(bytes)
	
	@callLogger
	def readDouble(self):
		val = struct.unpack(self.endian+'q', self.read(8))[0]
		return val
		
	def writeDouble(self,v):
		bytes = struct.pack(self.endian+'q', v)
		self.write(bytes)
		
	@callLogger
	def readUTFBytes(self,length):
		sign = struct.unpack(self.endian+str(length)+'s', self.read(length))[0]#.decode(code)
		return sign
	
	@callLogger
	def writeUTFBytes(self,v):
		length=len(v)
		bytes = struct.pack(self.endian+str(length)+'s', v)
		self.write(bytes)
		
	#@callLogger
	def __getitem__(self,i):
		return self.raw[i]
		
	def __setitem__(self,i,v):
		tmp=bytearray(self.raw)
		tmp[i]=v
		self.raw=bytes(tmp)
		#self.raw[i]=v
		
class KeyWords(object):
	arrWords = [b'', b'flash', b'CHANGE', b'backgroundColor', b'close', b'connect', b'colorTransform', b'hide', b'show', b'type', b'TextField', b'flash.text', b'text', b'addChild', b'void', b'int', b'file', b'flash.display', b'Sprite', b'Object', b'EventDispatcher', b'flash.events', b'DisplayObject', b'InteractiveObject', b'DisplayObjectContainer', b'graphics', b'beginFill', b'drawRect', b'endFill', b'loaderInfo', b'Event', b'addEventListener', b'removeEventListener', b'Loader', b'contentLoaderInfo', b'ProgressEvent', b'URLRequest', b'flash.net', b'load', b'removeChildAt', b'numChildren', b'String', b'PROGRESS', b'COMPLETE', b'flash.utils', b'ByteArray', b'uint', b'stage', b'StageScaleMode', b'NO_SCALE', b'scaleMode', b'StageAlign', b'TOP_LEFT', b'align', b'showDefaultContextMenu', b'URLLoaderDataFormat', b'BINARY', b'dataFormat', b'parameters', b'name', b'flash.display:Sprite', b'flash.display:DisplayObjectContainer', b'flash.display:InteractiveObject', b'flash.display:DisplayObject', b'flash.events:EventDispatcher', b'setInterval', b'target', b'data', b'navigateToURL', b'Endian', b'LITTLE_ENDIAN', b'endian', b'writeByte', b'readBytes', b'position', b'length', b'writeBytes', b'loadBytes', b'URLLoader', b'_blank', b'MovieClip', b'x', b'y', b'writeUTFBytes', b'Stage', b'readUTFBytes', b'Class', b'Boolean', b'Number', b'Array', b'URLStream', b'mp3', b'Socket', b'flash.geom', b'Rectangle', b'Transform', b'Point', b'LoaderInfo', b'flash.accessibility', b'AccessibilityProperties', b'XML', b'Function', b'Bitmap', b'IDataInput', b'IOErrorEvent', b'SecurityErrorEvent', b'MouseEvent', b'flash.system', b'LoaderContext', b'ApplicationDomain', b'Dictionary', b'autoLayout', b'toString', b'IBitmapDrawable', b'IEventDispatcher', b'root', b'parent', b'mask', b'visible', b'scaleX', b'scaleY', b'mouseX', b'mouseY', b'rotation', b'alpha', b'width', b'height', b'cacheAsBitmap', b'opaqueBackground', b'scrollRect', b'filters', b'blendMode', b'transform', b'scale9Grid', b'globalToLocal', b'localToGlobal', b'getBounds', b'getRect', b'hitTestObject', b'hitTestPoint', b'accessibilityProperties', b'measuredHeight', b'measuredWidth', b'move', b'setActualSize', b'flash.media', b'SoundChannel', b'SoundTransform', b'volume', b'bottom', b'left', b'LEFT', b'RIGHT', b'DOWN', b'UP', b'right', b'top', b'clone', b'flag', b'version', b'offset', b'time', b'method', b'flash.errors', b'IOError', b'lable', b'enabled', 'TOP', b'stageFocusRect', b'frameRate', b'StageQuality', b'BEST', b'quality', b'Error', b'contains', b'removeChild', b'pop', b'htmlText', b'writeUnsignedInt', b'connect', b'readInt', b'getTimer', b'writeInt', b'flush', b'MAX_VALUE', b'trace', b'readUnsignedInt', b'ENTER_FRAME', b'System', b'totalMemory', b'appendText', b'maxScrollV', b'scrollV', b'getQualifiedClassName', b'setChildIndex', b'Math', b'ceil', b'children', b'id', b'mouseEnabled', b'textColor', b'textWidth', b'textHeight', b'flash.utils:IDataInput', b'readShort', b'readUnsignedShort', b'currentDomain', b'applicationDomain', b'IO_ERROR', b'Sound', b'CONNECT', b'CLOSE', b'SECURITY_ERROR', b'SOCKET_DATA', b'bytesAvailable', b'readBoolean', b'readUTF', b'readByte', b'writeUTF', b'CLICK', b'push', b'clear', b'push', b'shift', b'loaderURL', b'indexOf', b'random', b'substr', b'charCodeAt', b'join', b'SecurityError', b'result', b'indices', b'Date', b'slice', b'splice', b'bytesLoaded', b'bytesTotal', b'unload', b'loader', b'bitmapData', b'auto', b'getDefinition', b'flash.filters', b'GlowFilter', b'currentTarget', b'MOUSE_UP', b'MOUSE_DOWN', b'startDrag', b'stopDrag', b'ROLL_OVER', b'gotoAndStop', b'ROLL_OUT', b'buttonMode', b'totalFrames', b'currentFrame', b'nextFrame', b'stopImmediatePropagation', b'stopPropagation', b'pause', b'http://adobe.com/AS3/2006/builtin', b'TextFormat', b'KeyboardEvent', b'ErrorEvent', b'SystemManager', b'Graphics', b'Bindable', b'allowDomain', b'addChildAt', b'getChildAt', b'getChildByName', b'getChildIndex', b'getObjectsUnderPoint', b'getDefinitionByName', b'Timer', b'BitmapData', b'Shape', b'RENDER', b'KEY_DOWN', b'selectable', b'invalidate', b'lock', b'fillRect', b'copyPixels', b'unlock', b'ctrlKey', b'shiftKey', b'dispatchEvent', b'min', b'max', b'stageWidth', b'stageHeight', b'content', b'rect', b'label', b'gb2312', b'hasEventListener', b'RESIZE', b'Vector', b'CENTER', b'TextFieldAutoSize', b'writeShort', b'connected","__AS3__.vec', b'autoSize', b'::', b'fullYear', b'month', b'date', b'day', b'hours', b'minutes', b'seconds', b'charAt', b'ENTER', b'DOWN', b'UP', b'Keyboard', b'flash.ui', b'keyCode', b'dispose', b'getCharBoundaries', b'verticalScrollPosition', b'update', b'maxVerticalScrollPosition', b'split', b'substring', b'addItem', b'getItemAt', b'focus', b'setSelection', b'fromCharCode', b'value', b'selectedIndex', b'setRendererStyle', b'maxChars', b'setStyle', b'textPadding', b'addItems', b'dataProvider', b'wordWrap', b'multiline', b'LINK', b'setTextFormat', b'source', b'defaultTextFormat', b'replace', b'search', b'exec', b'textField', b'dropdown', b'bold', b'symbol', b'writeMultiByte', b'readMultiByte', b'leading', b'font', b'letterSpacing', b'readFloat', b'readDouble', b'soundTransform', b'toFixed', b'stop', b'play', b'TextEvent', b'RegExp', b'size', b'.', b'\n', b'DropShadowFilter', b'getUTCHours', b'getUTCMinutes', b'getUTCSeconds', b'setHours', b'fullYearUTC', b'monthUTC', b'dateUTC', b'currentLabel', b'currentFrameLabel', b'abs', b'moveTo', b'lineTo', b'hasDefinition', b'Capabilities', b'readObject', b'writeObject', b'drawRoundRect', b'PI', b'pow', b'eventPhase', b'getSeconds', b'getMinutes', b'getHours', b'getFullYear', b'getMonth', b'getDay', b'getTextFormat', b'LocalConnection', b'TIMER_COMPLETE', b'repeatCount', b'XMLNodeType', b'TEXT_NODE', b'ELEMENT_NODE', b'nodeValue', b'nodeType', b'childNodes', b'nodeName', b'ColorMatrixFilter', b'filter', b'getTime', b'setTime', b'NUMERIC', b'XMLDocument', b'contextMenu', b'ContextMenu', b'ContextMenuItem', b'customItems', b'getParagraphLength', b'getLineOffset', b'replaceText', b'getLineText', b'numLines', b'lastIndexOf', b'setTimeout', b'writeBoolean', b'TEXT_INPUT', b'INPUT', b'maxScrollH', b'scrollH', b'styleSheet', b'fontSize', b'underline', b'textDecoration', b'RangeError', b'TypeError', b'hasSimpleContent', b'localName', b'attributes', b'XMLList', b'MOUSE_FOCUS_CHANGE', b'tabChildren', b'TAB_CHILDREN_CHANGE', b'TAB_INDEX_CHANGE', b'TAB_ENABLED_CHANGE', b'REMOVED', b'ADDED', b'getQualifiedSuperclassName', b'scaleZ', b'getLocal', b'HTTP_STATUS', b'HTTPStatusEvent', b'OPEN', b'INIT', b'TAB', b'preventDefault', b'charCode', b'ESCAPE', b'relatedObject', b'KEY_FOCUS_CHANGE', b'describeType', b'DEACTIVATE', b'isDefaultPrevented', b'stageY', b'Mouse', b'MOUSE_MOVE', b'stageX', b'DESCENDING', b'NaN', b'MOUSE_OUT', b'MOUSE_OVER', b'DYNAMIC', b'TextFieldType', b'currentCount', b'delay', b'TIMER', b'useHandCursor', b'SPACE', b'hasOwnProperty', b'DOUBLE_CLICK', b'doubleClickEnabled', b'floor', b'PAGE_DOWN', b'PAGE_UP', b'HOME', b'END', b'toUpperCase', b'apply', b'mouseChildren', b'MOUSE_WHEEL', b'UNKNOWN', b'IMEConversionMode', b'conversionMode', b'IME', b'isNaN', b'round', b'KEY_UP', b'FOCUS_OUT', b'FOCUS_IN', b'focusRect', b'defaultDisabledTextFormat', b'TextFormatAlign', b'call', b'ExternalInterface', b'flash.external', b'ADDED_TO_STAGE', b'mx_internal', b'getUnqualifiedClassName', b'displayObjectToString', b'createUniqueName', b'testCharacter', b'substitute', b'isWhitespace', b'trimArrayElements', b'breakDownBloxUtils', b'validInterval', b'getLocalName', b'http://www.adobe.com/2006/flex/mx/internal', b'VERSION', b'readLong', b'SUCCESS', b'StyleSheet', b'isDocument', b'getLineMetrics', b'sortOn', b'merge', b'concat', b'SharedObject', b'SimpleButton', b'FocusEvent', b'TimerEvent', b'restrict', b'color', b'tabEnabled', b'selected', b'editable', b'sort', b'reset', b'start']
	arrSelfWords = []
	#收集包名
	isEncryptPackage = True
	#收集类名
	isEncryptClass = True
	#收集方法名
	isEncryptMethod = True
	#收集变量名
	isEncryptVariable = True
	#用于记录被替换字符串的原始字符和替换后字符，替换时无论如何都应该先搜索这个字典，这样保证相同的字符替换后不会出现字符差异
	dictReplace={}
	#需要加密的字符串，所有Method_body_info中解析出的code的initproperty指令参数
	arrNeedEncryptStr=[]
	
	strCount=0
	isSimpleMode=False
	randomList=[]
	randomData={}
	def __init__(self):
		pass
		
	@staticmethod
	def isKeyWords(str):
		return str in KeyWords.arrWords or str in KeyWords.arrSelfWords
		
	@staticmethod
	def addNeedEncryptStr(str):
		if not str in KeyWords.arrNeedEncryptStr and not KeyWords.isKeyWords(str):
			KeyWords.arrNeedEncryptStr.append(str)
			return True
		return False
		
	@staticmethod
	def encryptStr(str):
		if str in KeyWords.arrNeedEncryptStr:
			if not str in KeyWords.dictReplace:
				KeyWords.dictReplace[str] = KeyWords.getNextEncryptStr(str)
			return KeyWords.dictReplace[str]
		return str
		
	@staticmethod
	def getNextEncryptStr(s):
		KeyWords.strCount+=1
		#Xue
		#if KeyWords.isSimpleMode:
		ns=("par_" + str(KeyWords.strCount)).encode('utf8')
		return ns
		#return randomString(s)
		
	@staticmethod
	def randomString(str):
		return str
		
class Tools(object):
	abcFile=None
	@staticmethod
	def readUBits(bytes,bitStartPosition,bitLength):
		result=0
		bitCursor= int(bitStartPosition % 8)
		bytes.position = int(bitStartPosition / 8)
		if bitCursor == 0:
			bitBuffer = bytes.readUnsignedByte()
			bitCursor = 8
		else:
			bitBuffer = bytes.readUnsignedByte()
			bitBuffer = bitBuffer & (0xFF >> bitCursor)
			bitCursor = 8 - bitCursor
		while bytes.bytesAvailable > 0:
			remainLength = bitLength - bitCursor
			if remainLength > 0:
				result = result | (bitBuffer << remainLength)
				bitLength -= bitCursor
				bitBuffer = bytes.readUnsignedByte()
				bitCursor = 8
			else:
				result = result | (bitBuffer >> -remainLength)
				return result
			
		return 0
		
	@staticmethod
	def readSBits(bytes, bitStartPosition, bitLength):
		result = Tools.readUBits(bytes, bitStartPosition, bitLength)
		offset = 32 - bitLength
		result = ((result << offset) >> offset)
		return result
		
	@staticmethod
	def wirteBits(bytes, bitStartPosition, bitLength, v):
		v_startIndex = 0
		bitCursor = bitStartPosition % 8
		bytes.position = int(bitStartPosition / 8)
		
		while bitLength > v_startIndex:
			v_len = 8 - bitCursor
			if v_len > (bitLength - v_startIndex):
				v_len=bitLength - v_startIndex
			#v_len = v_len > (bitLength - v_startIndex) ? (bitLength - v_startIndex) : v_len
			
			bitBuffer = bytes.readUnsignedByte()
			bitBuffer &= Tools.getAndPar(bitCursor, 8 - bitCursor)
			
			v_value = v & Tools.getAndPar(v_len, bitLength - v_startIndex - v_len)
			v -= v_value
			
			v_value >>= (bitLength - v_startIndex - v_len)
			v_value <<= (8 - (bitCursor + v_len))
			# trace(bitBuffer | v_value)
			bytes[bytes.position - 1] = bitBuffer | v_value
			
			bitCursor = 0
			v_startIndex += v_len
				
	@staticmethod
	def getAndPar(num, leftCount):
		v = int(math.pow(2, num) - 1)
		return v << leftCount
		
	
		
class DString(object):
	def __init__(self):
		pass
		
	@staticmethod
	def read(bt):
		str = ''
		position = bt.position
		btLen = bt.length
		strLen = 0
		while btLen > (position + strLen):
			if bt[position + strLen] == 0:
				break
			strLen +=1
		
		if strLen > 0:
			str = bt.readUTFBytes(strLen)
		
		bt.position+=1
		return str
		
	@staticmethod
	def write(bt, v):
		bt.writeUTFBytes(v)
		bt.writeByte(0)
		
class EncodedU32(object):
	def __init__(self):
		pass
	@staticmethod
	def read(bt):
		position = bt.position
		result = bt[position + 0]
		if not(result & 0x00000080):
			bt.position+=1
			return result
		
		result = (result & 0x0000007f) | bt[position + 1]<<7
		if not(result & 0x00004000):
			bt.position += 2
			return result
		
		result = (result & 0x00003fff) | bt[position + 2]<<14
		if not (result & 0x00200000):
			bt.position += 3
			return result
		
		result = (result & 0x001fffff) | bt[position + 3]<<21
		if not (result & 0x10000000):
			bt.position += 4
			return result
		
		result = (result & 0x0fffffff) | bt[position + 4]<<28
		bt.position += 5
		return result
		
	@staticmethod
	def write(bt, v):
		btTmp = ByteArray()
		btTmp.length = 5
		int_7_bit=0
		index = 0
		
		int_7_bit = v & 0x0000007f
		# v >>>= 7
		v=v >> 7#Xue
		if v:
			btTmp[index] = (int_7_bit | 0x00000080)
		else:
			btTmp[index] = int_7_bit
		#btTmp[index] = v ? (int_7_bit | 0x00000080) : int_7_bit
		index += 1
		while v:
			int_7_bit = v & 0x0000007f
			#v >>>= 7
			v=v >> 7#Xue
			if v:
				btTmp[index] = (int_7_bit | 0x00000080)
			else:
				btTmp[index] = int_7_bit
			#btTmp[index] = v ? (int_7_bit | 0x00000080) : int_7_bit
			index +=1
		bt.writeBytes(btTmp, 0, index)
	
		
		
class RGB(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.red = bt.readUnsignedByte()
		self.green = bt.readUnsignedByte()
		self.blue = bt.readUnsignedByte()
		
	def write(self,bt):
		bt.writeByte(self.red)
		bt.writeByte(self.green)
		bt.writeByte(self.blue)
		
class String_info(object):
	def __init__(self,bt):
		self.needEncrypt=False
		self.read(bt)
		
	def read(self,bt):
		self._size = EncodedU32.read(bt)
		self._str = bt.readUTFBytes(self._size)
		#trace('['+_str.decode('utf-8')+']')
		
	def write(self,bt):
		EncodedU32.write(bt, self._size)
		bt.writeUTFBytes(self._str)
		
	def toString(self):
		return self._str
		
	def addToEncryptWords(self):
		if not b'fl.' in self._str:
			self.needEncrypt = KeyWords.addNeedEncryptStr(self._str)
		return self.needEncrypt
		
	@property
	def str(self):
		return self._str
		
	@str.setter
	def str(self,v):
		self._str = v
		btTmp = ByteArray()
		# btTmp.endian = Endian.LITTLE_ENDIAN
		btTmp.writeUTFBytes(self._str)
		self._size = btTmp.length
		btTmp.length = 0
		
		
class Namespace_info(object):
	def __init__(self,bt):
		self.read(bt)
		
	def read(self,bt):
		self.kind = bt.readUnsignedByte()
		self.nameIndex = EncodedU32.read(bt)
		
	def write(self,bt):
		bt.writeByte(self.kind)
		EncodedU32.write(bt, self.nameIndex)
		
	def toFullString(self,arrString):
		if self.nameIndex <= 0:
			return b''
		return arrString[self.nameIndex - 1].toString()
		
	def addToEncryptWords(self):
		if KeyWords.isEncryptPackage:
			if self.nameIndex <= 0:
				return
			Tools.abcFile.cpool_info.arrString[self.nameIndex - 1].addToEncryptWords()
		
		
class Ns_set_info(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.count = EncodedU32.read(bt)
		self.arrNS = []
		for i in range(self.count):
			self.arrNS.append(EncodedU32.read(bt))
			
	def write(self,bt):
		EncodedU32.write(bt, self.count)
		for i in range(self.count):
			EncodedU32.write(bt, self.arrNS[i])
		
			
	def toFullString(self,arrNamespace):
		fullString = b'count:' + bytes(self.count)
		for i in range(self.count):
			fullString += b'\n\t\t' + arrNamespace[self.arrNS[i]-1] + b';'
		return fullString
		
	def addToEncryptWords(self):
		pass
	
class Multiname_info(object):
	def __init__(self,bt):
		self.read(bt)
		
	def read(self,bt):
		self.kind = bt.readUnsignedByte()
		if self.kind == 0x07 or self.kind == 0x0D:
			self.ns = EncodedU32.read(bt)
			self.name = EncodedU32.read(bt)
		elif self.kind == 0x0F or self.kind == 0x10:
			self.name = EncodedU32.read(bt)
		elif self.kind == 0x09 or self.kind == 0x0E:
			self.name = EncodedU32.read(bt)
			self.ns_set = EncodedU32.read(bt)
		elif self.kind == 0x1B or self.kind == 0x1C:
			self.ns_set = EncodedU32.read(bt)
		elif self.kind ==  0x1D:
			self.dataVctr = {}
			self.dataVctr['v1'] = EncodedU32.read(bt)
			self.dataVctr['v2'] = EncodedU32.read(bt)
			arr = []
			for i in range(self.dataVctr['v2']):
				arr.append(EncodedU32.read(bt))
			self.dataVctr['v3'] = arr
		else:
			input('Multiname_info unknow kind:' + self.kind.encode('utf-8'))
			
	def write(self,bt):
		bt.writeByte(self.kind)
		#switch(self.kind){
		if self.kind == 0x07 or self.kind == 0x0D:
			EncodedU32.write(bt, self.ns)
			EncodedU32.write(bt, self.name)
		elif self.kind == 0x0F or self.kind == 0x10:
			EncodedU32.write(bt, self.name)
		elif self.kind == 0x09 or self.kind == 0x0E:
			EncodedU32.write(bt, self.name)
			EncodedU32.write(bt, self.ns_set)
		elif self.kind == 0x1B or self.kind == 0x1C:
			EncodedU32.write(bt, self.ns_set)
		elif self.kind == 0x1D:
			EncodedU32.write(bt, self.dataVctr['v1'])
			EncodedU32.write(bt, self.dataVctr['v2'])
			arr = self.dataVctr['v3']
			for i in range(self.dataVctr['v2']):
				EncodedU32.write(bt, arr[i])
			
			
	def toFullString(self,arrString, arrNamespace, arrNs_set):
		return self.getDataString(arrString, arrNamespace, arrNs_set)
		
	def getDataString(self,arrString, arrNamespace, arrNs_set):
		sstr = b''
		if self.kind == 0x07 or self.kind == 0x0D:
			if self.ns == 0:
				sstr=b''
			else:
				sstr=arrNamespace[self.ns - 1]
			
			if not sstr == b'':
				sstr += b'.'
			
			if self.name == 0:
				sstr+=b'*'
			else:
				sstr+=arrString[self.name - 1].toString()
		elif self.kind == 0x0F or self.kind == 0x10:
			if self.name == 0:
				sstr=b'*'
			else:
				sstr=arrString[self.name - 1].toString()
		elif self.kind == 0x11 or self.kind == 0x12:
			sstr = b'*'
		elif self.kind == 0x09 or self.kind == 0x0E:
			#sstr = (self.name == 0 ? '*' : arrString[self.name - 1]) + '.' + arrNs_set[self.ns_set - 1]
			if self.name == 0:
				sstr=b'*'
			else:
				sstr=arrString[self.name - 1].toString()
			sstr+=b'.' + arrNs_set[self.ns_set - 1]
		elif self.kind == 0x1B or self.kind == 0x1C:
			sstr = arrNs_set[self.ns_set - 1]
		elif self.kind == 0x1D:
			sstr = str(self.dataVctr['v1']) + ',' + str(self.dataVctr['v2']) + ',' + str(self.dataVctr['v3'])
		return sstr
		
	def addToEncryptWords(self):
		#switch(kind){
		if self.kind == 0x07 or self.kind == 0x0D:
			Tools.abcFile.cpool_info.arrNamespace[self.ns - 1].addToEncryptWords()
			if Traits_info.isReadingClass:
				if KeyWords.isEncryptClass:
					Tools.abcFile.cpool_info.arrString[self.name - 1].addToEncryptWords()
			else:
				Tools.abcFile.cpool_info.arrString[self.name - 1].addToEncryptWords()
		elif self.kind == 0x0F or self.kind == 0x10:
			if Traits_info.isReadingClass:
				if KeyWords.isEncryptClass:
					Tools.abcFile.cpool_info.arrString[self.name - 1].addToEncryptWords()
			else:
				Tools.abcFile.cpool_info.arrString[self.name - 1].addToEncryptWords()
		elif self.kind == 0x09 or self.kind == 0x0E:
			Tools.abcFile.cpool_info.arrNs_set[self.ns_set - 1].addToEncryptWords()
			if Traits_info.isReadingClass:
				if KeyWords.isEncryptClass:
					Tools.abcFile.cpool_info.arrString[self.name - 1].addToEncryptWords()
			else:
				Tools.abcFile.cpool_info.arrString[self.name - 1].addToEncryptWords()
		elif self.kind == 0x1B or self.kind == 0x1C:
			Tools.abcFile.cpool_info.arrNs_set[self.ns_set - 1].addToEncryptWords()
		
	
		
class Cpool_info(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.int_count = EncodedU32.read(bt)
		self.arrInt = []
		for i in range(1,self.int_count):
			self.arrInt.append(EncodedU32.read(bt))
			
		self.uint_count = EncodedU32.read(bt)
		self.arrUint = []
		for i in range(1,self.uint_count):
			self.arrUint.append(EncodedU32.read(bt))
		
		self.double_count = EncodedU32.read(bt)
		self.arrDouble = []
		for i in range(1,self.double_count):
			self.arrDouble.append(bt.readDouble())
		
		self.string_count = EncodedU32.read(bt)
		self.arrString = []
		for i in range(1,self.string_count):
			self.arrString.append(String_info(bt))
		
		self.namespace_count = EncodedU32.read(bt)
		self.arrNamespace = []
		self.arrNamespace_S = []
		for i in range(1,self.namespace_count):
			self.arrNamespace.append(Namespace_info(bt))
			self.arrNamespace_S.append(self.arrNamespace[i - 1].toFullString(self.arrString))
		
		self.ns_set_count = EncodedU32.read(bt)
		self.arrNs_set = []
		self.arrNs_set_S = []
		for i in range(1,self.ns_set_count):
			self.arrNs_set.append(Ns_set_info(bt))
			self.arrNs_set_S.append(self.arrNs_set[i - 1].toFullString(self.arrNamespace_S))
		
		self.multiname_count = EncodedU32.read(bt)
		self.arrMultiname = []
		self.arrMultiname_S = []
		for i in range(1,self.multiname_count):
			self.arrMultiname.append(Multiname_info(bt))
			self.arrMultiname_S.append(self.arrMultiname[i - 1].toFullString(self.arrString, self.arrNamespace_S, self.arrNs_set_S))
			
	def encrypt(self):
		for strInfo in self.arrString:
			strInfo.str = KeyWords.encryptStr(strInfo.str)
			
	def write(self,bt):
		EncodedU32.write(bt, self.int_count)
		for i in range(1,self.int_count):
			EncodedU32.write(bt, self.arrInt[i - 1])
		
		EncodedU32.write(bt, self.uint_count)
		for i in range(1,self.uint_count):
			EncodedU32.write(bt, self.arrUint[i - 1])
		
		EncodedU32.write(bt, self.double_count)
		for i in range(1,self.double_count):
			bt.writeDouble(self.arrDouble[i - 1])
		
		EncodedU32.write(bt, self.string_count)
		for i in range(1,self.string_count):
			self.arrString[i - 1].write(bt)
		
		EncodedU32.write(bt, self.namespace_count)
		for i in range(1,self.namespace_count):
			self.arrNamespace[i - 1].write(bt)
		
		EncodedU32.write(bt, self.ns_set_count)
		for i in range(1,self.ns_set_count):
			self.arrNs_set[i - 1].write(bt)
		
		EncodedU32.write(bt, self.multiname_count)
		for i in range(1,self.multiname_count):
			self.arrMultiname[i - 1].write(bt)
		
	
	
class Option_detail(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.val = EncodedU32.read(bt)
		self.kind = bt.readUnsignedByte()
		
	def write(self,bt):
		EncodedU32.write(bt, self.val)
		bt.writeByte(self.kind)
	
class Option_info(object):
	def __init__(self,bt=None):
		if bt:
			self.read(bt)
	def read(self,bt):
		self.option_count = EncodedU32.read(bt)
		self.arrOption = []
		for i in range(self.option_count):
			self.arrOption.append(Option_detail(bt))
		
	def write(self,bt):
		EncodedU32.write(bt, self.option_count)
		for i in range(self.option_count):
			self.arrOption[i].write(bt)
		
	
class Method_info(object):
	NEED_ARGUMENTS = 0x01
	NEED_ACTIVATION = 0x02
	NEED_REST = 0x04
	HAS_OPTIONAL = 0x08
	SET_DXNS = 0x40
	HAS_PARAM_NAMES = 0x80
	def __init__(self,bt):
		self.strName=b''
		self.read(bt)
	def read(self,bt):
		self.param_count = EncodedU32.read(bt)
		self.return_type = EncodedU32.read(bt)
		self.arrParam_type = []
		for i in range(self.param_count):
			self.arrParam_type.append(EncodedU32.read(bt))
		
		self.name = EncodedU32.read(bt)
		self.flags = bt.readUnsignedByte()
		self.options = Option_info()
		if (self.flags & Method_info.HAS_OPTIONAL) == Method_info.HAS_OPTIONAL:
			self.options.read(bt)
		
		self.arrParam_names = []
		if (self.flags & Method_info.HAS_PARAM_NAMES) == Method_info.HAS_PARAM_NAMES:
			for i in range(self.param_count):
				self.arrParam_names.append(EncodedU32.read(bt))
				
	def encrypt(self):
		self.name = 0
		
	def write(self,bt):
		EncodedU32.write(bt, self.param_count)
		EncodedU32.write(bt, self.return_type)
		
		for i in range(self.param_count):
			EncodedU32.write(bt, self.arrParam_type[i])
		
		EncodedU32.write(bt, self.name)
		bt.writeByte(self.flags)
		if (self.flags & Method_info.HAS_OPTIONAL) == Method_info.HAS_OPTIONAL:
			self.options.write(bt)
		
		if (self.flags & Method_info.HAS_PARAM_NAMES) == Method_info.HAS_PARAM_NAMES:
			for i in range(self.param_count):
				EncodedU32.write(bt, self.arrParam_names[i])
		
			
class Item_info(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.key = EncodedU32.read(bt)
		self.value = EncodedU32.read(bt)
		
	def write(self,bt):
		EncodedU32.write(bt, self.key)
		EncodedU32.write(bt, self.value)
		
		

class Metadata_info(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.name = EncodedU32.read(bt)
		self.item_count = EncodedU32.read(bt)
		self.arrItem_infos = []
		for i in range(self.item_count):
			self.arrItem_infos.append(Item_info(bt))
			
	def write(self,bt):
		EncodedU32.write(bt, self.name)
		EncodedU32.write(bt, self.item_count)
		for i in range(self.item_count):
			self.arrItem_infos[i].write(bt)
			
class Trait_slot(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.slot_id = EncodedU32.read(bt)
		self.type_name = EncodedU32.read(bt)
		self.vindex = EncodedU32.read(bt)
		self.vkind=0
		if not self.vindex == 0:
			self.vkind = bt.readUnsignedByte()
	
	def encrypt(self):
		pass

	def write(self,bt):
		EncodedU32.write(bt, self.slot_id)
		EncodedU32.write(bt, self.type_name)
		EncodedU32.write(bt, self.vindex)
		if not self.vindex == 0:
			bt.writeByte(self.vkind)
		
		
		
class Trait_method(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.disp_id = EncodedU32.read(bt)
		self.method_v = EncodedU32.read(bt)
	
	def encrypt(self):
		pass

	def write(self,bt):
		EncodedU32.write(bt, self.disp_id)
		EncodedU32.write(bt, self.method_v)
		
		
class Trait_class(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.slot_id = EncodedU32.read(bt)
		self.classi = EncodedU32.read(bt)
	
	def encrypt(self):
		pass

	def write(self,bt):
		EncodedU32.write(bt, self.slot_id)
		EncodedU32.write(bt, self.classi)
		
class Trait_function(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.slot_id = EncodedU32.read(bt)
		self.function_v = EncodedU32.read(bt)

	def encrypt(self):
		pass

	def write(self,bt):
		EncodedU32.write(bt, self.slot_id)
		EncodedU32.write(bt, self.function_v)
		
class Traits_info(object):
	Trait_Slot = 0
	Trait_Method = 1
	Trait_Getter = 2
	Trait_Setter = 3
	Trait_Class = 4
	Trait_Function = 5
	Trait_Const = 6

	ATTR_Final = 0x1
	ATTR_Override = 0x2
	ATTR_Metadata = 0x4

	isReadingClass=False

	def __init__(self,bt):
		self.read(bt)
		
	@property
	def traitType(self):
		return self.kind & 0xF
		
	def read(self,bt):
		self.name = EncodedU32.read(bt)
		self.kind = bt.readByte()
		_traitType = self.traitType
		
		
		#switch
		if _traitType==Traits_info.Trait_Slot or _traitType==Traits_info.Trait_Const:
			self.trait = Trait_slot(bt)
			if KeyWords.isEncryptVariable:
				Tools.abcFile.cpool_info.arrMultiname[self.name - 1].addToEncryptWords()
		elif _traitType==Traits_info.Trait_Method:
			if KeyWords.isEncryptMethod:
				Tools.abcFile.cpool_info.arrMultiname[self.name - 1].addToEncryptWords()
			#Xue
			self.trait = Trait_method(bt)
			method_index = self.trait.method_v
			Tools.abcFile.arrMethod[method_index].strName = Instance_info.name_S + b'.' + Tools.abcFile.cpool_info.arrMultiname_S[self.name - 1]
			#Xue
		elif _traitType==Traits_info.Trait_Getter or _traitType==Traits_info.Trait_Setter:
			self.trait = Trait_method(bt)
			method_index = self.trait.method_v
			Tools.abcFile.arrMethod[method_index].strName = Instance_info.name_S + b'.' + Tools.abcFile.cpool_info.arrMultiname_S[self.name - 1]
		elif _traitType==Traits_info.Trait_Class:
			Traits_info.isReadingClass = True
			self.trait = Trait_class(bt)
			if KeyWords.isEncryptClass or KeyWords.isEncryptPackage:
				if not b'fl.' in Tools.abcFile.cpool_info.arrMultiname_S[self.name - 1]:
					Tools.abcFile.cpool_info.arrMultiname[self.name - 1].addToEncryptWords()
			Traits_info.isReadingClass = False
		elif _traitType==Traits_info.Trait_Function:
			self.trait = Trait_function(bt)
		
		self.metadata_count = 0
		self.arrMetadata = []
		self.traitAttributes = self.kind >> 4
		if (self.traitAttributes & Traits_info.ATTR_Metadata):
			self.metadata_count = EncodedU32.read(bt)
			for i in range(self.metadata_count):
				self.arrMetadata.append(EncodedU32.read(bt))
				
				
	def encrypt(self):
		self.trait.encrypt()
		
	def write(self,bt):
		EncodedU32.write(bt, self.name)
		bt.writeByte(self.kind)
		traitType = self.kind & 0xF

		#switch(traitType)
		# case Trait_Slot:
		# case Trait_Const:
			# self.trait.write(bt)
			# break;
		# case Trait_Method:
		# case Trait_Getter:
		# case Trait_Setter:
			# self.trait.write(bt)
			# break;
		# case Trait_Class:
			# self.trait.write(bt)
			# break;
		# case Trait_Function:
			# self.trait.write(bt)
			# break;
		self.trait.write(bt)
		
		self.traitAttributes = self.kind >> 4
		if (self.traitAttributes & Traits_info.ATTR_Metadata):
			EncodedU32.write(bt, self.metadata_count)
			for i in range(self.metadata_count):
				EncodedU32.write(bt, self.arrMetadata[i])
		
		
		
class Instance_info(object):
	CONSTANT_ClassSealed = 0x01
	CONSTANT_ClassFinal = 0x02
	CONSTANT_ClassInterface = 0x04
	CONSTANT_ClassProtectedNs = 0x08
	name_S=b''
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.name = EncodedU32.read(bt)
		Instance_info.name_S = Tools.abcFile.cpool_info.arrMultiname_S[self.name - 1]
		self.super_name = EncodedU32.read(bt)
		self.flags = bt.readByte()
		if self.flags < 0:
			trace(b'flags:'+self.flags)
		
		if (self.flags & Instance_info.CONSTANT_ClassProtectedNs):
			self.protectedNs = EncodedU32.read(bt)
		
		self.intrf_count = EncodedU32.read(bt)
		self.arrInterface = []
		self.arrInterface_S = []
		for i in range(self.intrf_count):
			self.arrInterface.append(EncodedU32.read(bt))
			self.arrInterface_S.append(Tools.abcFile.cpool_info.arrMultiname_S[self.arrInterface[i] - 1])
		
		self.iinit = EncodedU32.read(bt)
		self.trait_count = EncodedU32.read(bt)
		self.arrTraits = []
		for i in range(self.trait_count):
			self.arrTraits.append(Traits_info(bt))
			
	def write(self,bt):
		EncodedU32.write(bt, self.name)
		EncodedU32.write(bt, self.super_name)
		bt.writeByte(self.flags)
		if (self.flags & Instance_info.CONSTANT_ClassProtectedNs):
			EncodedU32.write(bt, self.protectedNs)
		
		EncodedU32.write(bt, self.intrf_count)
		for i in range(self.intrf_count):
			EncodedU32.write(bt, self.arrInterface[i])
		
		EncodedU32.write(bt, self.iinit)
		EncodedU32.write(bt, self.trait_count)
		for i in range(self.trait_count):
			self.arrTraits[i].write(bt)
		
		
		
class Class_info(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.cinit = EncodedU32.read(bt)
		self.trait_count = EncodedU32.read(bt)
		self.arrTraits = []
		for i in range(self.trait_count):
			self.arrTraits.append(Traits_info(bt))
			
	def write(self,bt):
		EncodedU32.write(bt, self.cinit)
		EncodedU32.write(bt, self.trait_count)
		for i in range(self.trait_count):
			self.arrTraits[i].write(bt)
		
		
		
class Script_info(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.init = EncodedU32.read(bt)
		self.trait_count = EncodedU32.read(bt)
		self.arrTraits = []
		for i in range(self.trait_count):
			self.arrTraits.append(Traits_info(bt))
			
	def encrypt(self):
		for i in range(self.trait_count):
			self.arrTraits[i].encrypt()
		
	
	def write(self,bt):
		EncodedU32.write(bt, self.init)
		EncodedU32.write(bt, self.trait_count)
		for i in range(self.trait_count):
			self.arrTraits[i].write(bt)
		
class Exception_info(object):
	def __init__(self,bt):
		self.read(bt)

	def read(self,bt):
		self.from_ = EncodedU32.read(bt)
		self.to = EncodedU32.read(bt)
		self.target = EncodedU32.read(bt)
		self.exc_type = EncodedU32.read(bt)
		self.var_name = EncodedU32.read(bt)

	def write(self,bt):
		EncodedU32.write(bt, self.from_)
		EncodedU32.write(bt, self.to)
		EncodedU32.write(bt, self.target)
		EncodedU32.write(bt, self.exc_type)
		EncodedU32.write(bt, self.var_name)
		
class Method_body_info(object):
	def __init__(self,bt):
		self.read(bt)
	def read(self,bt):
		self.method = EncodedU32.read(bt)
		self.max_stack = EncodedU32.read(bt)
		self.local_count = EncodedU32.read(bt)
		self.init_scope_depth = EncodedU32.read(bt)
		self.max_scope_depth = EncodedU32.read(bt)
		
		code_length = EncodedU32.read(bt)
		
		self.btCode = ByteArray()
		#btCode.endian = Endian.LITTLE_ENDIAN
		bt.readBytes(self.btCode, 0, code_length)
		self.btCode.position = 0
		
		self.exception_count = EncodedU32.read(bt)
		self.arrException = []
		for i in range(self.exception_count):
			self.arrException.append(Exception_info(bt))
		
		self.trait_count = EncodedU32.read(bt)
		self.arrTrait = []
		for i in range(self.trait_count):
			self.arrTrait.append(Traits_info(bt))
		
	def write(self,bt):
		EncodedU32.write(bt, self.method)
		EncodedU32.write(bt, self.max_stack)
		EncodedU32.write(bt, self.local_count)
		EncodedU32.write(bt, self.init_scope_depth)
		EncodedU32.write(bt, self.max_scope_depth)
		
		EncodedU32.write(bt, self.btCode.length)
		bt.writeBytes(self.btCode)
		
		EncodedU32.write(bt, self.exception_count)
		for i in range(self.exception_count):
			self.arrException[i].write(bt)
		
		EncodedU32.write(bt, self.trait_count)
		for i in range(self.trait_count):
			self.arrTrait[i].write(bt)
		
		
		
class AbcFile(object):
	def __init__(self,bt):
		self.read(bt)
		
	def read(self,bt):
		Tools.abcFile=self
		self.minor_version = bt.readUnsignedShort()
		self.major_version = bt.readUnsignedShort()
		self.cpool_info = Cpool_info(bt)
		self.method_count = EncodedU32.read(bt)
		self.arrMethod = []
		for i in range(self.method_count):
			method_info = Method_info(bt)
			self.arrMethod.append(method_info)
		
		self.metadata_count = EncodedU32.read(bt)
		self.arrMetadata = []
		for i in range(self.metadata_count):
			metadata_info = Metadata_info(bt)
			self.arrMetadata.append(metadata_info)
		
		self.class_count = EncodedU32.read(bt)
		self.arrInstance = []
		for i in range(self.class_count):
			instance_info = Instance_info(bt)
			self.arrInstance.append(instance_info)
		
		self.arrClass = []
		for i in range(self.class_count):
			class_info = Class_info(bt)
			self.arrClass.append(class_info)
		
		self.script_count = EncodedU32.read(bt)
		self.arrScript = []
		for i in range(self.script_count):
			script_info = Script_info(bt)
			self.arrScript.append(script_info)
		
		self.method_body_count = EncodedU32.read(bt)
		self.arrMethodBody = []
		for i in range(self.method_body_count):
			method_body_info = Method_body_info(bt)
			self.arrMethodBody.append(method_body_info)
		
		if bt.bytesAvailable > 0:
			input('AbcFile not read to end')
			
	def encrypt(self):
		Tools.abcFile = self
		self.cpool_info.encrypt()
		
	def write(self,bt):
		Tools.abcFile = self
		bt.writeShort(self.minor_version)
		bt.writeShort(self.major_version)
		self.cpool_info.write(bt)
		EncodedU32.write(bt, self.method_count)
		for i in range(self.method_count):
			method_info = self.arrMethod[i]
			method_info.write(bt)
		
		EncodedU32.write(bt, self.metadata_count)
		for metadata_info in self.arrMetadata:
			metadata_info.write(bt)
		
		EncodedU32.write(bt, self.class_count)
		for i in range(self.class_count):
			instance_info = self.arrInstance[i]
			instance_info.write(bt)
		
		for i in range(self.class_count):
			class_info = self.arrClass[i]
			class_info.write(bt)
		
		EncodedU32.write(bt, self.script_count)
		for i in range(self.script_count):
			script_info = self.arrScript[i]
			script_info.write(bt)
		
		EncodedU32.write(bt, self.method_body_count)
		for i in range(self.method_body_count):
			method_body_info = self.arrMethodBody[i]
			method_body_info.write(bt)
		
		
		
class Tag(object):
	#是否允许子类反序列化
	allowChildParse=True
	#是否允许子类序列化
	allowChildEncode=True
	#是否允许子类加密
	allowChildEncrypt=True
	def __init__(self):
		self.bt=ByteArray()
		self.tagType=0
		self.tagLength=0
		
	def parse(self):
		self.bytesLen = self.bt.bytesAvailable
		#bt.endian = Endian.LITTLE_ENDIAN
		self.bt.position = 0
		
	def encrypt(self):
		pass
		
	def encode(self):
		btTmp = ByteArray()
		# btTmp.endian = Endian.LITTLE_ENDIAN
		btTmp.writeBytes(self.bt)
		tmpLen = btTmp.length
		# if not tmpLen == self.tagLength:
			# trace(tagName + b':' + tmpLen + b',' + self.tagLength)
			# input('error')
		self.tagLength = tmpLen
		self.bt.length = 0
		if btTmp.length >= 0x3F:
			self.bt.writeShort((self.tagType << 6) | 0x3F)
			self.bt.writeUnsignedInt(self.tagLength)
		else:
			self.bt.writeShort((self.tagType << 6) | self.tagLength)
		
		self.bt.writeBytes(btTmp)
		btTmp.length = 0
		# input(str(self.bt.length))
		
class EndTag(Tag):
	def __init__(self):
		Tag.__init__(self)
	def parse(self):
		Tag.parse(self)
	
class ShowFrameTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineShapeTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
		if not Tag.allowChildParse:
			return
	
class PlaceObjectTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class RemoveObjectTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineBitsTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineButtonTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class JPEGTablesTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class SetBackgroundColorTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
		if not Tag.allowChildParse:
			return
		self.rgb = RGB(self.bt)
		
	def encode(self):
		if Tag.allowChildEncode:
			self.bt = ByteArray()
			#self.bt.endian = Endian.LITTLE_ENDIAN
			self.rgb.write(self.bt)
		Tag.encode(self)
	
class DefineFontTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineTextTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DoActionTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineFontInfoTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineSoundTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class StartSoundTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineButtonSoundTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class SoundStreamHeadTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class SoundStreamBlockTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineBitsLosslessTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineBitsJPEG2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineShape2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineButtonCxformTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class ProtectTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class PlaceObject2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class RemoveObject2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineShape3Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineText2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineButton2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineBitsJPEG3Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineBitsLossless2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineEditTextTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineSpriteTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class ProductInfoTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
		if not Tag.allowChildParse:
			return
		productID = self.bt.readInt()
		edition = self.bt.readInt()
		majorVersion = self.bt.readUnsignedByte()
		minorVersion = self.bt.readUnsignedByte()
		buildLow = self.bt.readInt()
		buildHigh = self.bt.readInt()
		compilationDateLow = self.bt.readInt()
		compilationDateHigh = self.bt.readInt()
	
class FrameLabelTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
		if not Tag.allowChildParse:
			return
		self.Name = DString.read(self.bt)
		
	def encrypt(self):
		if not Tag.allowChildEncrypt:
			return
		self.Name = KeyWords.encryptStr(self.Name)
		
	def encode(self):
		if Tag.allowChildEncode:
			bt = ByteArray()
			#bt.endian = '>'
			DString.write(bt, self.Name)
			trace(self.Name)
		Tag.encode(self)
		
	
class SoundStreamHead2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineMorphShapeTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineFont2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class ExportAssetsTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class ImportAssetsTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class EnableDebuggerTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DoInitActionTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineVideoStreamTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class VideoFrameTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineFontInfo2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class EnableDebugger2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
	
	def parse(self):
		Tag.parse(self)
		
	def encrypt(self):
		pass
	
class ScriptLimitsTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
		maxRecursionDepth = self.bt.readUnsignedShort()
		scriptTimeoutSeconds = self.bt.readUnsignedShort()
		
	def encode(self):
		if Tag.allowChildEncode:
			pass
		Tag.encode(self)
		
	
class SetTabIndexTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class FileAttributesTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		if Tag.allowChildParse:
			self.reserved = Tools.readUBits(self.bt, 0, 1)
			self.useDirectBlit = Tools.readUBits(self.bt, 1, 1)
			self.useGPU = Tools.readUBits(self.bt, 2, 1)
			self.gasMetadata = Tools.readUBits(self.bt, 3, 1)
			self.actionScript3 = Tools.readUBits(self.bt, 4, 1)
			self.reserved1 = Tools.readUBits(self.bt, 5, 2)
			self.useNetwork = Tools.readUBits(self.bt, 7, 1)
			self.reserved2 = Tools.readUBits(self.bt, 8, 24)
			self.bt.position = 4
		
		Tag.parse(self)
		
	def encrypt(self):
		pass
		
	def encode(self):
		if Tag.allowChildEncode:
			Tools.wirteBits(self.bt, 0, 1, self.reserved)
			Tools.wirteBits(self.bt, 1, 1, self.useDirectBlit)
			Tools.wirteBits(self.bt, 2, 1, self.useGPU)
			Tools.wirteBits(self.bt, 3, 1, self.gasMetadata)
			Tools.wirteBits(self.bt, 4, 1, self.actionScript3)
			Tools.wirteBits(self.bt, 5, 2, self.reserved1)
			Tools.wirteBits(self.bt, 7, 1, self.useNetwork)
			Tools.wirteBits(self.bt, 8, 24, self.reserved2)
			self.bt.position = 4
		Tag.encode(self)
		
		
class PlaceObject3Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class ImportAssets2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineFontAlignZonesTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class CSMTextSettingsTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineFont3Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
		
class Symbol(object):
	def __init__(self):
		pass
	
class SymbolClassTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
		if not Tag.allowChildParse:
			return
		self.NumSymbols = self.bt.readUnsignedShort()
		self.arrSymbols = []
		for i in range(self.NumSymbols):
			symbol = Symbol()
			symbol.tag = self.bt.readUnsignedShort()
			symbol.Name = DString.read(self.bt)
			self.arrSymbols.append(symbol)
			
	def encrypt(self):
		if not Tag.allowChildEncrypt:
			return
		for symbol in self.arrSymbols:
			try:
				dotLastIndex = symbol.Name.rindex(b'.')
			except:
				dotLastIndex=-1
			if dotLastIndex==-1:
				str1=b''
			else:
				str1=symbol.Name[0:dotLastIndex]
			#str1 = symbol.Name[0, (dotLastIndex < 0 ? 0 : dotLastIndex)]
			str2 = symbol.Name[dotLastIndex+1:]
			
			str1 = KeyWords.encryptStr(str1)
			str2 = KeyWords.encryptStr(str2)
			
			if not str1 == b'':
				str1=str1 + b'.'
			#str1 = (str1 == b'' ? str1 : str1 + b'.')
			symbol.Name = str1 + str2
			
	def encode(self):
		if Tag.allowChildEncode:
			self.bt = ByteArray()
			#bt.endian = Endian.LITTLE_ENDIAN
			self.bt.writeShort(self.NumSymbols)
			for i in range(self.NumSymbols):
				symbol = self.arrSymbols[i]
				self.bt.writeShort(symbol.tag)
				DString.write(self.bt, symbol.Name)
		Tag.encode(self)
		
	
class MetadataTag(Tag):
	def __init__(self):
		# self.v=b'<swftool author='pw' e-mail='82376048@qq.com' date='000'/>'
		self.tagType=TagTypes.TAG_METADATA
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
		if not Tag.allowChildParse:
			return
		self.v=DString.read(self.bt)
		# trace(self.v)
		
	def encrypt(self):
		pass
		
	def encode(self):
		if Tag.allowChildEncode:
			self.bt = ByteArray()
			#bt.endian = Endian.LITTLE_ENDIAN
			DString.write(self.bt, self.v)
		Tag.encode(self)
		
		
class DefineScalingGridTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DoABCTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
		if not Tag.allowChildParse:
			return
		self.Flags = self.bt.readUnsignedInt()
		self.Name = DString.read(self.bt)
		self.abcFile = AbcFile(self.bt)
		
	def encrypt(self):
		if not Tag.allowChildEncrypt:
			return
		self.Name = KeyWords.encryptStr(self.Name)
		self.abcFile.encrypt()
		
	def encode(self):
		if Tag.allowChildEncode:
			btRemain = ByteArray()
			# btRemain.endian = Endian.LITTLE_ENDIAN
			self.bt.readBytes(btRemain)
			
			self.bt = ByteArray()
			# self.bt.endian = Endian.LITTLE_ENDIAN
			self.bt.writeUnsignedInt(self.Flags)
			DString.write(self.bt, self.Name)
			self.abcFile.write(self.bt)
			
			self.bt.writeBytes(btRemain)
		Tag.encode(self)
		
	def __lt__(self,abc):
		if self.Name<abc.Name:
			return True
		else:
			return False
			
	def __gt__(self,abc):
		if self.Name>abc.Name:
			return True
		else:
			return False
			
	def __eq__(self,abc):
		if self.Name==abc.Name:
			return True
		else:
			return False
	
class DefineShape4Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineMorphShape2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineSceneAndFrameLabelDataTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineBinaryDataTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineFontNameTag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class StartSound2Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineBitsJPEG4Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
		
	def parse(self):
		Tag.parse(self)
	
class DefineFont4Tag(Tag):
	def __init__(self):
		Tag.__init__(self)
	def parse(self):
		Tag.parse(self)
	
		
class Rect(object):
	def __init__(self,bt):
		self.bt=bt
		self.read(self.bt)
		
	def read(self,bt):
		start=bt.position*8
		self.length = Tools.readUBits(bt, start, 5)
		self.xMinTwips = Tools.readSBits(bt, start + 5, self.length)
		self.xMaxTwips = Tools.readSBits(bt, start + 5 + self.length, self.length)
		self.yMinTwips = Tools.readSBits(bt, start + 5 + self.length * 2, self.length)
		self.yMaxTwips = Tools.readSBits(bt, start + 5 + self.length * 3, self.length)
		pass
		
	def write(self,bt):
		start = bt.position * 8
		Tools.wirteBits(bt, start, 5, self.length)
		
		Tools.wirteBits(bt, start + 5, self.length, self.xMinTwips)
		Tools.wirteBits(bt, start + 5 + self.length, self.length, self.xMaxTwips)
		Tools.wirteBits(bt, start + 5 + self.length * 2, self.length, self.yMinTwips)
		Tools.wirteBits(bt, start + 5 + self.length * 3, self.length, self.yMaxTwips)
		
class TagTypes(object):
	TAG_END = 0
	TAG_SHOWFRAME = 1
	TAG_DEFINESHAPE = 2
	TAG_FREECHARACTER = 3
	TAG_PLACEOBJECT = 4
	TAG_REMOVEOBJECT = 5
	TAG_DEFINEBITS = 6
	TAG_DEFINEBUTTON = 7
	TAG_JPEGTABLES = 8
	TAG_SETBACKGROUNDCOLOR = 9
	TAG_DEFINEFONT = 10
	TAG_DEFINETEXT = 11
	TAG_DOACTION = 12
	TAG_DEFINEFONTINFO = 13
	TAG_DEFINESOUND = 14
	TAG_STARTSOUND = 15
	TAG_STOPSOUND = 16
	TAG_DEFINEBUTTONSOUND = 17
	TAG_SOUNDSTREAMHEAD = 18
	TAG_SOUNDSTREAMBLOCK = 19
	# Flash 2 tags
	TAG_DEFINEBITSLOSSLESS = 20
	TAG_DEFINEBITSJPEG2 = 21
	TAG_DEFINESHAPE2 = 22
	TAG_DEFINEBUTTONCXFORM = 23
	TAG_PROTECT = 24
	TAG_PATHSAREPOSTSCRIPT = 25
	# Flash 3 tags
	TAG_PLACEOBJECT2 = 26
	
	TAG_REMOVEOBJECT2 = 28
	TAG_SYNCFRAME = 29
	
	TAG_FREEALL = 31
	TAG_DEFINESHAPE3 = 32
	TAG_DEFINETEXT2 = 33
	TAG_DEFINEBUTTON2 = 34
	TAG_DEFINEBITSJPEG3 = 35
	TAG_DEFINEBITSLOSSLESS2 = 36
	# Flash 4 tags
	TAG_DEFINEEDITTEXT = 37
	TAG_DEFINEVIDEO = 38
	TAG_DEFINESPRITE = 39
	TAG_NAMECHARACTER = 40
	TAG_PRODUCTINFO = 41
	TAG_DEFINETEXTFORMAT = 42
	TAG_FRAMELABEL = 43
	# Flash 5 tags
	TAG_DEFINEBEHAVIOR = 44
	TAG_SOUNDSTREAMHEAD2 = 45
	TAG_DEFINEMORPHSHAPE = 46
	TAG_FRAMETAG = 47
	TAG_DEFINEFONT2 = 48
	TAG_GENCOMMAND = 49
	TAG_DEFINECOMMANDOBJ = 50
	TAG_CHARACTERSET = 51
	TAG_FONTREF = 52
	TAG_DEFINEFUNCTION = 53
	TAG_PLACEFUNCTION = 54
	TAG_GENTAGOBJECT = 55
	TAG_EXPORTASSETS = 56
	TAG_IMPORTASSETS = 57
	TAG_ENABLEDEBUGGER = 58
	# Flash 6 tags
	TAG_DOINITACTION = 59
	TAG_DEFINEVIDEOSTREAM = 60
	TAG_VIDEOFRAME = 61
	TAG_DEFINEFONTINFO2 = 62
	TAG_DEBUGID = 63
	TAG_ENABLEDEBUGGER2 = 64
	TAG_SCRIPTLIMITS = 65
	# Flash 7 tags
	TAG_SETTABINDEX = 66
	# Flash 8 tags
	
	
	TAG_FILEATTRIBUTES = 69
	TAG_PLACEOBJECT3 = 70
	TAG_IMPORTASSETS2 = 71
	TAG_DEFINEFONTALIGNZONES = 73
	TAG_CSMTEXTSETTINGS = 74
	TAG_DEFINEFONT3 = 75
	TAG_SYMBOLCLASS = 76
	TAG_METADATA = 77
	TAG_SCALINGGRID = 78
	
	
	
	TAG_DOABC = 82
	TAG_DEFINESHAPE4 = 83
	TAG_DEFINEMORPHSHAPE2 = 84
	
	# Flash 9 tags
	TAG_DEFINESCENEANDFRAMELABELDATA = 86
	TAG_DEFINEBINARYDATA = 87
	TAG_DEFINEFONTNAME = 88
	TAG_STARTSOUND2 = 89
	TAG_DEFINEBITSJPEG4 = 90
	# Flash 10 tags
	TAG_DEFINEFONT4 = 91


	TAG_CLASS = [EndTag,ShowFrameTag,DefineShapeTag,None,PlaceObjectTag,RemoveObjectTag,DefineBitsTag,DefineButtonTag,JPEGTablesTag,SetBackgroundColorTag,DefineFontTag,DefineTextTag,DoActionTag,DefineFontInfoTag,DefineSoundTag,StartSoundTag,None,DefineButtonSoundTag,SoundStreamHeadTag,SoundStreamBlockTag,DefineBitsLosslessTag,DefineBitsJPEG2Tag,DefineShape2Tag,DefineButtonCxformTag,ProtectTag,None,PlaceObject2Tag,None,RemoveObject2Tag,None,None,None,DefineShape3Tag,DefineText2Tag,DefineButton2Tag,DefineBitsJPEG3Tag,DefineBitsLossless2Tag,DefineEditTextTag,None,DefineSpriteTag,None,ProductInfoTag,None,FrameLabelTag,None,SoundStreamHead2Tag,DefineMorphShapeTag,None,DefineFont2Tag,None,None,None,None,None,None,None,ExportAssetsTag,ImportAssetsTag,EnableDebuggerTag,DoInitActionTag,DefineVideoStreamTag,VideoFrameTag,DefineFontInfo2Tag,None,EnableDebugger2Tag,ScriptLimitsTag,SetTabIndexTag,None,None,FileAttributesTag,PlaceObject3Tag,ImportAssets2Tag,None,DefineFontAlignZonesTag,CSMTextSettingsTag,DefineFont3Tag,SymbolClassTag,MetadataTag,DefineScalingGridTag,None,None,None,DoABCTag,DefineShape4Tag,DefineMorphShape2Tag,None,DefineSceneAndFrameLabelDataTag,DefineBinaryDataTag,DefineFontNameTag,StartSound2Tag,DefineBitsJPEG4Tag,DefineFont4Tag]
		
	@staticmethod
	def getTagClassByTagType(tagType):
		return TagTypes.TAG_CLASS[tagType] or None
		
class SwfFile(object):
	addEncryptDoABCTag=False
	def __init__(self,bt):
		self.bt=bt
		self.parse()
		
	def parse(self):
		self.signature=self.bt.readUTFBytes(3)
		self.version=self.bt.readByte()
		self.fileLength=self.bt.readUnsignedInt()
		# return
		if self.signature==b'CWS':
			tempBytes=ByteArray()
			tempBytes.writeBytes(self.bt,self.bt.position)
			tempBytes.uncompress()
			
			temp=self.bt.position
			self.bt.length=self.bt.position
			self.bt.writeBytes(tempBytes)
			tempBytes.length=0
			self.bt.position=temp
			
		self.rect=Rect(self.bt)
		self.bt.position+=1
		self.frameRate = self.bt.readByte()
		self.frameCount = self.bt.readUnsignedShort()
		self.readTags(self.bt)
		
	def readTags(self,bytes):
		self.tags=[]
		count=0
		while bytes.bytesAvailable > 0:
			tagType = self.readTagType(bytes)
			tagLength = self.readTagLength(bytes)
			
			TagClass = TagTypes.getTagClassByTagType(tagType)
			trace('tagType:'+str(tagType))
			if TagClass == None:
				TagClass = Tag
			tag = TagClass()
			trace(str(type(tag))+'   p:'+str(bytes.position)+'   l:'+str(tagLength))
			tag.tagType = tagType
			tag.tagLength = tagLength
			
			if tag.tagLength < 0 or (bytes.position + tag.tagLength) > bytes.length:
				continue
			
			if tagLength > 0:
				#tag.bt.writeBytes(bytes, 0, tagLength)
				bytes.readBytes(tag.bt, 0, tagLength)
			
			tag.parse()
			
			if tagType == TagTypes.TAG_DOACTION :
				continue
			if (tagType == TagTypes.TAG_DEFINEBITSJPEG2 or tagType == TagTypes.TAG_DEFINEBITS or tagType == TagTypes.TAG_DEFINEBITSLOSSLESS) and tagLength == 0:
				continue
			
			self.tags.append(tag)
			count+=1
			if tagType == TagTypes.TAG_END:
				break
			
	def readTagType(self,bytes):
		result = bytes.readUnsignedShort()
		result = result >> 6
		bytes.position -= 2
		return result
		
	def readTagLength(self,bytes):
		tagLength = (bytes.readUnsignedShort() & 0x3F)
		if tagLength == 0x3F:
			tagLength = bytes.readUnsignedInt()
		if tagLength < 0:
			trace('SWFReader:无效的tag长度')
		return tagLength
		
	def encrypt(self):
		for tag in self.tags:
			tag.encrypt()
		
	def encode(self):
		trace('---------------------encode---------------------')
		self.bt = ByteArray()
		# self.bt.endian = Endian.LITTLE_ENDIAN
		
		self.bt.writeUTFBytes(self.signature)
		self.bt.writeByte(self.version)
		
		tempBytes = ByteArray()
		# tempBytes.endian = Endian.LITTLE_ENDIAN
		tempBytes.length = 20
		self.rect.write(tempBytes)
		tempBytes.writeByte(0)
		tempBytes.writeByte(self.frameRate)
		tempBytes.writeShort(self.frameCount)
		
		for tag in self.tags:
			tag.encode()
			trace(str(type(tag))+'    '+str(len(tag.bt.raw)))
			tempBytes.writeBytes(tag.bt)
			
			# if tag.tagType == TagTypes.TAG_METADATA:
				# metadataTag = MetadataTag()
				# allow = Tag.allowChildEncode
				# Tag.allowChildEncode = True
				# metadataTag.encode()
				# Tag.allowChildEncode = allow
				# tempBytes.writeBytes(metadataTag.bt)
			
			if SwfFile.addEncryptDoABCTag and tag.tagType == TagTypes.TAG_SHOWFRAME:
				encryptABCTag = DoABCTag()
				encryptABCTag.abcFile.metadata_count = 0xffffff
				allow = Tag.allowChildEncode
				Tag.allowChildEncode = True
				encryptABCTag.encode()
				Tag.allowChildEncode = allow
				tempBytes.writeBytes(encryptABCTag.bt)
				SwfFile.addEncryptDoABCTag = False
		
		self.bt.writeUnsignedInt(self.bt.position + 4 + tempBytes.length)
		
		trace(tempBytes.length)
		trace(tempBytes.position)
		if self.signature == b'CWS':
			tempBytes.compress()
		trace(tempBytes.length)
		trace(tempBytes.position)
		self.bt.writeBytes(tempBytes)
		tempBytes.length = 0
		trace('---------------------encode end---------------------')
		
	
class SWFBlurTool(object):
	def __init__(self):
		self.fileXml=[]
		self.classNameData={}#需要解析的类名

	def blur(self,swfp,swft):
		self.fileName=swfp
		self.tarFile=swft
		bytes=ByteArray(open(swfp,'rb').read())
		self.swfFile=SwfFile(bytes)
		tags = self.swfFile.tags
		doABCtags = []
		for tag in tags:
			if isinstance(tag,DoABCTag):
				doABCtags.append(tag)
		#trace(doABCtags)
		self.parseTag(doABCtags, self.swfFile, self.fileName)
		self.startBlur()
		
	def parseTag(self, doABCtags, swfFile, fileName):
		doABCtags.sort(reverse=True)
		for doABCtag in doABCtags:
			if doABCtag.Name:
				self.addNode(self.fileXml, doABCtag.Name, doABCtag)
		trace(self.fileXml)

			
	def addNode(self, xml, name, doABCtag):
		array = name.split(b'/')
		node = array.pop()
		for item in array:
			xml.append({b'label': item, b'isFile': False, b'select': True})
		xml.append({b'label':node,b'isFile':True,b'select':True})
		self.classNameData[node] = doABCtag
			
	def startBlur(self):
		if self.swfFile == None:
			return
		
		# KeyWords.arrNeedEncryptStr = []
		
		needEncryptClassArray = []
		noEncryptClassArray = []
		self.getClassName(self.fileXml, needEncryptClassArray, noEncryptClassArray)
		
		#不需要混淆的字段
		noEncryptStr = self.getWordsByClass(noEncryptClassArray, True, True, True, True)
		self.removeEncryptField(noEncryptStr)
		KeyWords.arrSelfWords = noEncryptStr
		
		trace('类不混淆数量:')
		trace(noEncryptClassArray)
		trace('总共不混淆数量:')
		trace(KeyWords.arrSelfWords)
		
		#需要混淆的字段
		arrNeedEncryptStr = self.getWordsByClass(needEncryptClassArray, True, True, True, True)
		KeyWords.arrNeedEncryptStr += arrNeedEncryptStr
		
		trace('类混淆数量:')
		trace(needEncryptClassArray)
		trace('总共混淆数量:')
		trace(KeyWords.arrNeedEncryptStr)
		
		SwfFile.addEncryptDoABCTag = False
		
		self.swfFile.encrypt()
		self.swfFile.encode()
			
		with open(self.tarFile,'wb') as f:
			f.write(self.swfFile.bt.raw)
		trace('混淆完毕')
		
		with open('log.txt','w') as f:
			f.write('\n'.join(logs))

	def getClassName(self, data, encryptArray, noEncryptArray):
		for item in data:
			if item[b'isFile']:
				label = item[b'label']
				if item[b'select']:
					if not label in encryptArray:
						encryptArray.append(label)
				else:
					if not label in noEncryptArray:
						noEncryptArray.push(label)
		
	def getWordsByClass(self, classArray, packageSelect, classSelect, methodSelect, fieldSelect):
		data = []
		if packageSelect:
			packageArray = self.addEncryptPackageName(classArray)
		
		if methodSelect:
			methodArray = self.addEncryptMethodName(classArray)
		
		if fieldSelect:
			filedsArray = self.addEncryptFieldName(classArray)
		
		#包名
		if packageSelect:
			data += packageArray
		
		#类名
		if classSelect:
			data += classArray
		
		#方法
		if methodSelect:
			data += methodArray
		
		#字段
		if fieldSelect:
			data += filedsArray
		
		return data
		
	#移除不需要加密的字段 这个暂时没用到
	def removeEncryptField(self,array):
		pass
		# noEncrypt = b''
		# noEncrypts = noEncrypt.split(b'\r')
		# for field in noEncrypts:
			# if not field in array:
				# array.append(field)
		
	#根据所选择的，添加需要混淆的包名
	def addEncryptPackageName(self,data):
		array = []
		for className in data:
			doABCtag = self.classNameData[className]
			if doABCtag:
				tmpArr = doABCtag.Name.split(b'/')
				array.append(doABCtag.Name)
				if len(tmpArr) > 1:
					tmpArr.pop()
					packageName = b'.'.join(tmpArr)
					if not packageName in array:
						array.append(packageName)
		return array
		
	#根据所选择的，添加需要混淆的方法
	def addEncryptMethodName(self,data):
		array = []
		for className in data:
			doABCtag = self.classNameData[className]
			if doABCtag:
				for method_info in doABCtag.abcFile.arrMethod:
					if method_info.strName == b'':
						continue
					tmpArr = method_info.strName.split(b'.')
					methodName = tmpArr[len(tmpArr) - 1]
					if not methodName in array and not KeyWords.isKeyWords(methodName):
						array.append(methodName)
		return array
		
	#根据所选择的，添加需要混淆的属性名字
	def addEncryptFieldName(self,data):
		array = []
		for className in data:
			doABCtag = self.classNameData[className]
			if doABCtag:
				cpool_info = doABCtag.abcFile.cpool_info
				for class_info in doABCtag.abcFile.arrClass:
					self.parseTraits(class_info.arrTraits, array, cpool_info)
				for instance_info in doABCtag.abcFile.arrInstance:
					self.parseTraits(instance_info.arrTraits, array, cpool_info)
		return array
		
	def parseTraits(self,traits, saveArray, cpool_info):
		for traits_info in traits:
			if traits_info.traitType == Traits_info.Trait_Const or traits_info.traitType == Traits_info.Trait_Slot:
				field = cpool_info.arrString[cpool_info.arrMultiname[traits_info.name - 1].name - 1].str
				if not field in saveArray and not KeyWords.isKeyWords(field):
					saveArray.append(field)
		
		
	
		
if __name__=='__main__':
	tool=SWFBlurTool()
	# tool.blur('E:/h5pkg/srcipt/ascode/Main.swf','E:/h5pkg/srcipt/ascode/m.swf')
	tool.blur('bin/Main.swf','m.swf')
	# input('over')
	
	
	
	
	
	
	
	
	