#python3
#coding:utf-8

import os
import struct
import zlib

class ByteArray(object):
	def __init__(self,bytes=None):
		if not bytes:
			self.bytes=b''
		else:
			self.bytes=bytes
		self.endian='>'
		# self.length=len(self.bytes)
		self.position=0
		# print(self.bytes)
		# print(self.length)
		
	@property
	def length(self):
		return len(self.bytes)
	
	@length.setter
	def length(self,val):
		if val<self.length:
			self.bytes=self.bytes[0:val]
		elif val>self.length:
			while self.length<val:
				self.bytes+=b' '
		self.position=0
		
	def __getitem__(self,idx):
		return self.bytes[idx]
		
	def __setitem__(self,idx,val):
		self.bytes[idx]=val
		
		
	def _write(self,val):
		length=len(val)
		if self.position+length>=self.length:
			self.bytes=self.bytes[0:self.position]+val
		self.position+=length
			
	def _read(self,length):
		bt=self.bytes[self.position:self.position+length]
		self.position+=length
		return bt
		
	def read8(self):
		resp=struct.unpack(self.endian+'b',self._read(1))
		return resp[0]
	
	def readU8(self):
		resp=struct.unpack(self.endian+'B',self._read(1))
		return resp[0]
		
	def read16(self):
		resp=struct.unpack(self.endian+'h',self._read(2))
		return resp[0]
	
	def readU16(self):
		resp=struct.unpack(self.endian+'H',self._read(2))
		return resp[0]
	
	def read32(self):
		resp=struct.unpack(self.endian+'i',self._read(4))
		return resp[0]
	
	def readU32(self):
		resp=struct.unpack(self.endian+'I',self._read(4))
		return resp[0]
		
	def readUTFBytes(self,length):
		resp=struct.unpack(self.endian+str(length)+'s',self._read(length))
		return resp[0]
		
	def readUTF(self):
		return self.readUTFBytes(self.readU16())
		
	def write8(self,val):
		bt=struct.pack(self.endian+'b',val)
		self._write(bt)
		
	def writeU8(self,val):
		bt=struct.pack(self.endian+'B',val)
		self._write(bt)
		
	def write16(self,val):
		bt=struct.pack(self.endian+'h',val)
		self._write(bt)
	
	def writeU16(self,val):
		bt=struct.pack(self.endian+'H',val)
		self._write(bt)
	
	def write32(self,val):
		bt=struct.pack(self.endian+'i',val)
		self._write(bt)
	
	def writeU32(self,val):
		bt=struct.pack(self.endian+'I',val)
		self._write(bt)
	
	def writeUTFBytes(self,val):
		length=len(val)
		bt=struct.pack(self.endian+str(length)+'s',val)
		self._write(bt)
	
	def writeUTF(self,val):
		self.writeU16(len(val))
		self.writeUTFBytes(val)
		
	def writeBytes(self,bt,offset=0,length=0):
		left=b''
		if (self.position+length)<self.length:
			left=self.bytes[self.position+length:]
		self.bytes=self.bytes[0:self.position]+bt.bytes[offset:offset+length]+left
		
	def compress(self):
		self.bytes=zlib.compress(self.bytes)
		self.position=0
		
	def uncompress(self):
		self.bytes=zlib.decompress(self.bytes)
		self.position=0
		
	def save(self,tar):
		with open(tar,'wb') as f:
			f.write(self.bytes)
	
	
	def test_common(self):
		bt=ByteArray(open('b.bin','rb').read())
		print(bt.readU8())
		print(bt.read32())
		print(bt.readUTFBytes(5))
		print(bt.readUTF())
		
		bt=ByteArray();
		# print(bt.readU8())
		# print(bt.read32())
		# print(bt.readUTFBytes(5))
		# print(bt.readUTF())
		bt.write8(10)
		# bt.position=0
		# print(bt.readU8())
		# bt.position=1
		bt.write32(20)
		# bt.position=1
		# print(bt.read32())
		# bt.position=5
		bt.writeUTFBytes("hello")
		# bt.position=5
		# print(bt.readUTFBytes(5))
		# bt.position=10
		bt.writeUTF("world!")
		# bt.position=10
		# print(bt.readUTF())
		with open('b.bin','wb') as f:
			f.write(bt.bytes)
			
	def test_writeBytes(self):
		bt1=ByteArray(b'123456')
		bt2=ByteArray(b'123456')
		
		bt1.position=3
		bt1.writeBytes(bt2,1,1)
		print(bt1.bytes)


def unicodeBytes(utf8string):
	src = ByteArray()
	src.writeUTFBytes(utf8string)
	src.position=0
	def getU8(bt,idx):
		bt.position=idx
		return bt.readU8() 
	out = []
	len = src.length
	if len == 0:
		return out
	idx=0
	while True:
		c=getU8(src,idx)
		if (c & 128) == 0:
			idx = (idx + 1)
			out.append(c)
		elif (c & 224) == 192:
			uni = ((c & 31) << 6)
			idx = (idx + 1)
			uni = (uni | (getU8(src,idx) & 63))
			idx = (idx + 1)
			out.append(uni)
		elif (c & 240) == 224:
			uni = ((c & 15) << 12)
			idx = (idx + 1)
			uni = (uni | ((getU8(src,idx) & 63) << 6))
			idx = (idx + 1)
			uni = (uni | (getU8(src,idx) & 63))
			idx = (idx + 1)
			out.append(uni)
		else:
			print('error')
		if idx >= len:
			break
	return out
	
if __name__=='__main__':
	bt=ByteArray(b'')
	bt.test_writeBytes()
	
	
	
	
	
	
	