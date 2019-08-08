#!python2
#coding:utf-8

#-----------------------------------------------------------------------
#------把代码中的字符串提出到外部加载
#-----------------------------------------------------------------------

import sys
#sys.dont_write_bytecode = True
import os
import re
import base64
import random
from bytes import ByteArray

class OutString:
	def __init__(self):
		random.seed()
		self.exceptStrList=['alpha']
		#self.exceptDirList=['alpha','onComplete']
		
		self.strFunReg=re.compile('function +\w+ *\(.*?"(.*?)".*?\)')#识别带字符串默认值参数的方法
		self.strKeyReg=re.compile('"(.*?)"\s*:')#识别作为键名的字符串
		self.strEmbedReg=re.compile('\[\w+\((.*?)\)\]')#识别元数据中的字符串
		self.strDanShuangReg=re.compile('\'(\")\'')#识别字符串:'"',用来排除单引号里面的双引号
		self.strFunList=[]
		self.strFunRepl='-**-KeepedStr-**-'
		
		self.noteReg1=re.compile('\/\*([^\*^\/]*|[\*^\/*]*|[^\**\/]*)*\*\/')
		# self.noteReg1=re.compile('/\*(.|\n)*?\*/')#块注释
		self.noteReg2=re.compile(r'(?<!:|\\)//.*')#行注释
		
		self.strReg=re.compile('".*?"')#识别字符串
		self.strLen=2#字符串最小长度
		self.clearNotes=True#是否删掉注释
		
		self.strList=[]
		
	def addExcept(self,mapf):
		if not os.path.isfile(mapf):
			raw_input(' wornning::'+mapf+' not exists! continue?')
			return
		with open(mapf) as f:
			tmpli=f.readlines();
		for tmp in tmpli:
			tmp=tmp.strip()
			tli=tmp.split(':')
			word=tli[2]
			self.exceptStrList.append(word)
		
	def __strKeepFun(self,m):
		gp=m.group()
		ss=m.group(1)
		if ss=='':
			return gp
		idx=len(self.strFunList)
		self.strFunList.append(gp)
		return self.strFunRepl+str(idx)
		
	def __strReplaceFun(self,m):
		gp=m.group()
		ss=gp.strip('"')
		if ss=='' or len(ss)<=self.strLen:
			return gp
		if ss in self.exceptStrList:
			return gp
		if '\\' in gp:
			return gp
		# print('==============>'+gp)
		return self._replaceFun(ss)
	
	def _replaceFun(self,ss):
		try:
			idx=self.strList.index(ss)
		except:
			idx=-1
		if idx<0:
			idx=len(self.strList)
			self.strList.append(ss)
			self.strList.append(str(random.randint(10,9999)))
			if random.random()>0.5:
				self.strList.append(str(random.randint(10,9999)))
		return self.strRepl+'('+str(idx)+')'
	
	def replaceByDir(self,asroot,strLen,replaceStr):
		self.strLen=strLen#字符串最小长度
		self.strRepl=replaceStr#替换函数字符串
		if not os.path.isdir(asroot):
			raw_input(' error::"'+asroot+'" not exists!!')
			return
		for root,dirs,files in os.walk(asroot):
			for file in files:
				#print('--->'+file)
				fp=os.path.join(root,file)
				nm,ext=os.path.splitext(file)
				
				with open(fp,'r') as f:
					cc=f.read()
					
				#去掉注释
				if self.clearNotes:
					cc=self.noteReg1.sub('',cc)
					cc=self.noteReg2.sub('',cc)
				#替换不需要提出来的字符串
				self.strFunList=[]
				cc=self.strFunReg.sub(self.__strKeepFun,cc)
				cc=self.strKeyReg.sub(self.__strKeepFun,cc)
				cc=self.strEmbedReg.sub(self.__strKeepFun,cc)
				cc=self.strDanShuangReg.sub(self.__strKeepFun,cc)
				#替换字符串
				cc=self.strReg.sub(self.__strReplaceFun,cc)
				#还原不需要提出来的字符串
				for idx in range(len(self.strFunList)-1,-1,-1):
					cc=cc.replace(self.strFunRepl+str(idx),self.strFunList[idx])
				
				with open(fp,'w') as f:
					f.write(cc)
					
	def output(self,outfile):
		print('OutString:output '+outfile)
		with open(outfile,'w') as f:
			f.write('\n'.join(self.strList))
			
	def __testKeyReg(self,m):
		print('-------------------->'+m.group())
		return m.group()
			
class OutString64(OutString):
	def __init__(self):
		OutString.__init__(self)
		self.key=list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
		self.value=list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
		random.shuffle(self.value)
		#print(id(self.key))
		#print(id(self.value))
		
	def output(self,outfile):
		print('OutString64:output '+outfile)
		outli=[''.join(self.value)]+self.strList
		with open(outfile,'w') as f:
			f.write('\n'.join(outli))
	
	def output64(self,outfile):
		print('OutString64:output64 '+outfile)
		cc64=base64.b64encode('\n'.join(self.strList))
		cc=''
		for char in cc64:
			cc+=self.value[self.key.index(char)]
		cc64s=''.join(self.value)+cc
		with open(outfile,'w') as f:
			f.write(cc64s)
			
	def output64Bytes(self,outfile):
		print('OutString64:output64Bytes '+outfile)
		bt=ByteArray()
		bt.writeUTF(''.join(self.value))
		for idx,item in enumerate(self.strList):
			tmp64=base64.b64encode(item)
			tmp=''
			for char in tmp64:
				tmp+=self.value[self.key.index(char)]
			bt.writeUTF(tmp)
		bt.save(outfile)
		
	def reEncode(self,src,tar):
		with open(src) as f:
			self.strList=[o.strip() for o in f.readlines()]
		val=self.strList.pop(0)
		self.value=list(val)
		self.output64(tar)
		
	# def reEncodeBytes(self,src,tar):
		# with open(src) as f:
			# self.strList=[o.strip() for o in f.readlines()]
		# val=self.strList.pop(0)
		# self.value=list(val)
		# self.output64(tar)
			
if __name__=='__main__':
	# out=OutString()
	# out.addExcept('blur.txt')
	# out.addExcept('map.txt')
	# out.replaceByDir('src_r',2,'Mapping.getStr')
	# out.output('str.bin')
	# raw_input('over!')
	
	out=OutString64()
	out.value=out.key
	out.strList=['0123','你好','ZXCVB']
	out.output64Bytes('b.bin');
	
	bt=ByteArray(open('b.bin','rb').read())
	print(bt.readUTF())
	print(base64.b64decode(bt.readUTF()))
	print(base64.b64decode(bt.readUTF()))
	print(base64.b64decode(bt.readUTF()))
	
	
	
