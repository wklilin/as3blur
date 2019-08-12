#!python
#coding:utf-8

import os
import re

def trace(s):
	print(s.decode('utf-8'))
	# print(s.decode('gbk'))
	# print(s)

class AS3Lexer:
	def __init__(self):
		self.regReg=re.compile(r'/.*?[^\\]/')
		self.zimu='_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		self.shuzi='0123456789'
		self.shuzidot='0123456789'
		self.fuhao='()[]{}+-*%=<>!,.?:;&|'
		self.raw=None
		with open(os.path.join('test','RandomSwift.as'),'rb') as f:
			self.raw=f.read()
		# trace(self.raw[0:3].decode('gbk'))
		# trace(self.raw.decode('utf-8'))
		# self.raw=self.raw[3:]
		self.raw=self.raw.replace('\r','')
		self.pos=0
		
	def loop(self):
		while self.pos<len(self.raw):
			self.judgeToken()
		
	def judgeToken(self):
		ch=self.read()
		if ch==' ':
			trace('空格')
			return
		elif ch=='	':
			trace('制表')
			return
		elif ch=='\r':
			trace('换行r')
			return
		elif ch=='\n':
			trace('换行n')
			return
		elif ch in self.shuzi:
			while self.next() in self.shuzidot:
				ch+=self.read()
			trace('数字：'+ch)
			return
		elif ch in self.zimu:
			while self.next() in self.zimu:
				ch+=self.read()
			trace('字符：'+ch)
			return
		elif ch=='/':
			if self.next()=='*':
				ch+=self.read()
				while not self.cur()=='*' or not self.next()=='/':
					ch+=self.read()
				ch+=self.read()
				trace('注释：'+ch)
				return
			elif self.next()=='/':
				while not self.next()=='\r' and not self.next()=='\n':
					ch+=self.read()
				trace('注释：'+ch)
				return
			else:
				line,leng=self.readCurLine()
				line='/'+line
				m=self.regReg.match(line)
				if m and m.span()[0]==0:#正则
					ch+=self.read(m.span()[1]-1)
					trace('正则：'+ch+']')
					return
				else:#除号
					trace('符号：'+ch)
					return
		elif ch=='\'':
			while not self.next()=='\'' or (self.next()=='\'' and self.cur()=='\\'):
				ch+=self.read()
			ch+=self.read()
			trace('字串：'+ch)
			return
		elif ch=='"':
			while not self.next()=='"' or (self.next()=='"' and self.cur()=='\\'):
				ch+=self.read()
			ch+=self.read()
			trace('字串：'+ch)
			return
		elif ch in self.fuhao:
			trace('符号：'+ch)
			return
		else:
			trace(ch)
			input('error')
			return
		
	def next(self,step=0):
		return self.raw[self.pos+step]
		
	def cur(self):
		return self.raw[self.pos-1]
		
	def last(self,step=0):
		return self.raw[self.pos-step-2]
		
	def read(self,step=1):
		val=self.raw[self.pos:self.pos+step]
		self.pos+=step
		return val
		
	def readCurLine(self):
		tpos=0
		item=self.next()
		val=item
		while not item == '\n':
			tpos+=1
			item=self.next(tpos)
			val+=item
		return val,tpos
		
	def backPos(self):
		self.pos-=1
		
		
if __name__=='__main__':
	lex=AS3Lexer()
	lex.loop()
	# reg=re.compile('\w')
	# if reg.match('s'):
		# trace('ss')
















