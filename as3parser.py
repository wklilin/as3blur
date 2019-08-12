#!python
#coding:utf-8

import os
import re

def trace(msg):
	print(msg.decode('utf-8'))

class Token(object):
	def __init__(self,chars,type,row,col,msg=None):
		self.chars=chars
		self.type=type
		self.row=row
		self.col=col
		self.msg=msg
		
class LexerType(object):
	SPACE=1
	TABLE=2
	ENTER=3
	NOTES=4
	
	WORD=101
	NUM=102
	OPERATOR=103
	STRING=104
	REGULAR=105

class AS3Lexer(object):
	def __init__(self):
		self.regReg=re.compile(r'/.*?[^\\]/')
		self.zimu='_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		self.shuzi='0123456789'
		self.shuzidot='0123456789'
		self.fuhao='()[]{}+-*%=<>!,.?:;&|'
		with open(os.path.join('test','RandomSwift.as'),'rb') as f:
			self.raw=f.read()
		# print(self.raw.decode('utf-8'))
		# self.raw=self.raw[3:]
		self.raw=self.raw.replace('\r','')
		self.pos=0
		self.tokens=[]
		self.row=0
		self.col=0
		self.rowend=0
		self.colend=0
		
	def loop(self):
		while self.pos<len(self.raw):
			self.judgeToken()
		
	def addToken(self,chars,type,msg):
		# trace(msg)
		self.tokens.append(Token(chars,type,self.rowend,self.colend-len(chars),msg))
		
	def judgeToken(self):
		ch=self.read()
		if ch==' ':
			self.addToken(ch,LexerType.SPACE,'空格')
		elif ch=='	':
			self.addToken(ch,LexerType.TABLE,'制表')
		elif ch=='\n':
			self.addToken(ch,LexerType.ENTER,'换行')
		elif ch in self.shuzi:
			while self.next() in self.shuzidot:
				ch+=self.read()
			self.addToken(ch,LexerType.NUM,'数字：'+ch)
		elif ch in self.zimu:
			while self.next() in self.zimu:
				ch+=self.read()
			self.addToken(ch,LexerType.WORD,'字符：'+ch)
		elif ch=='/':
			if self.next()=='*':
				ch+=self.read()
				while not self.cur()=='*' or not self.next()=='/':
					ch+=self.read()
				ch+=self.read()
				self.addToken(ch,LexerType.NOTES,'注释：'+ch)
			elif self.next()=='/':
				while not self.next()=='\r' and not self.next()=='\n':
					ch+=self.read()
				self.addToken(ch,LexerType.NOTES,'注释：'+ch)
			else:#Xue
				line,leng=self.curLine()
				line='/'+line
				m=self.regReg.match(line)
				if m and m.span()[0]==0:#正则
					# ch+=self.read(m.span()[1]-1)
					while not self.next()=='/' or (self.next()=='/' and self.cur()=='\\'):
						ch+=self.read()
					ch+=self.read()
					self.addToken(ch,LexerType.REGULAR,'正则：'+ch)
				else:#除号
					self.addToken(ch,LexerType.OPERATOR,'符号：'+ch)
		elif ch=='\'':
			while not self.next()=='\'' or (self.next()=='\'' and self.cur()=='\\'):
				ch+=self.read()
			ch+=self.read()
			self.addToken(ch,LexerType.STRING,'字串：'+ch)
		elif ch=='"':
			while not self.next()=='"' or (self.next()=='"' and self.cur()=='\\'):
				ch+=self.read()
			ch+=self.read()
			self.addToken(ch,LexerType.STRING,'字串：'+ch)
		elif ch in self.fuhao:
			self.addToken(ch,LexerType.OPERATOR,'符号：'+ch)
		else:
			trace(ch)
			input('error')
	
	def next(self,step=0):
		return self.raw[self.pos+step]
		
	def cur(self):
		return self.raw[self.pos-1]
		
	def last(self,step=0):
		return self.raw[self.pos-step-2]
		
	def read(self):
		val=self.raw[self.pos:self.pos+1]
		self.pos+=1
		if val=='\n':
			self.rowend+=1
			self.colend=0
		else:
			self.colend+=1
		return val
		
	def curLine(self):
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
















