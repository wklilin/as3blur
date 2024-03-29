#!python2
#coding:utf-8

'''
-----------------------------------
           2.6.1
-----------------------------------
'''

import sys
#sys.dont_write_bytecode = True
import os
import random
import time

def word_only_one(func):
	def wrapper(self,basw=None):
		# val=self.getUsedWordByKey(basw)
		val=None#Xue   参数baseWord并不是要混淆的字符串，而是一个参考字符串
		if not val:
			val=func(self,basw)
			while self.inUsedList(val):
				val=func(self,basw)
			self.addKeyWord(basw,val)
		return val
	return wrapper

class RandDict():
	inited=False
	usedList=[]#已经生成的词
	usedDict={}#已经生成的词
	wlistall=[]#字典all
	wlist10=[]#字典10
	wlist6=[]#字典6
	upper='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	lower='abcdefghijklmnopqrstuvwxyz'
	shengmu='bcdfghjklmnpqrstvwxyz'
	prefix=['mc','btn','res','ui','scene','vo','lib','tool','utils','img','bmp','txt','se','sound','data','ios','max','view','stage']
	def __init__(self):
		if RandDict.inited:
			return
		RandDict.inited=True
		random.seed()
		# self.creatpkg=False
		
		with open(os.path.join(os.path.dirname(__file__),'words','keyword.txt')) as f:
			tlist=f.readlines()
		for w in tlist:
			w=w.strip()
			if w!='':
				RandDict.wlistall.append(w);
				if len(w)<=10:
					RandDict.wlist10.append(w)
				if len(w)<=6:
					RandDict.wlist6.append(w)
		
	def getUsedWordByKey(self,key):
		if not key in RandDict.usedDict:
			return None
		return RandDict.usedDict[key]
		
	def inUsedList(self,val):
		return val in RandDict.usedList
	
	def addKeyWord(self,key,word):
		RandDict.usedDict[key]=word
		RandDict.usedList.append(word)
		
	
	def bool(self,val=50):
		return random.randint(0,100)>val
		
	def randChar(self):
		idx=random.randint(0,25)
		word=RandDict.lower[idx]
		return word
		
	def randLetters(self):
		idx=random.randint(0,25)
		word=RandDict.lower[idx]
		if self.bool(50):
			idx=random.randint(0,25)
			word+=RandDict.lower[idx]
		return word
		
	def randOne(self,wlist=0):
		tlist=RandDict.wlistall
		if wlist==10:
			tlist=RandDict.wlist10
		if wlist==6:
			tlist=RandDict.wlist6
		idx=random.randint(0,len(tlist)-1)
		word=tlist[idx]
		
		#修改单词第一个字母
		# if self.bool():
			# word=RandDict.shengmu[random.randint(0,20)]+word[1:]
		
		return word
		
	def randWordPrefix(self):
		word=self.randOne(10)
		num=random.randint(3,5)
		if len(word)<=num:
			return word
		else:
			return word[0:num]
		
	def randPrefix(self):
		idx=random.randint(0,len(RandDict.prefix)-1)
		word=RandDict.prefix[idx]
		return word
		
	#去掉字段中的_和.
	def formatBaseWord(self,baseWord=None):
		if baseWord is None:
			baseWord=self.randOne()
		if baseWord.find('.')>0:
			baseWord=baseWord.split('.').pop()
		if baseWord.find('_')>0:
			li=baseWord.split('_')
			li.pop(0)
			baseWord=random.choice(li)
		return baseWord
		
	@word_only_one
	def getClass(self,baseWord=None):
		word=self.formatBaseWord(baseWord).capitalize()
		if len(word)<7:#如果字符串比较短
			if self.bool(80):
				if self.bool(50):
					word=self.randOne(10).capitalize()+'_'+word
				else:
					word=word+self.randOne(10).capitalize()
				return word
		if self.bool(30):
			word=self.randOne(10).capitalize()
		if self.bool(60):#使用预设词缀
			pre=self.randPrefix().capitalize()
			if self.bool(80):#全大写
				pre=pre.upper()
			#if self.bool()>60:#前缀加下划线
				#pre=pre+'_'
			word=pre+word
		else:#使用单词组合
			tword=self.randOne(10).capitalize()
			if self.bool(80):
				tword='_'+tword
			word+=tword
		return word
		
	@word_only_one
	def getProto(self,baseWord=None):
		word=self.formatBaseWord(baseWord).lower()
		if self.bool(30):
			word=self.randOne(6)
		if self.bool(70):
			word=word.capitalize()
		rate=random.randint(0,100)
		if rate>80:#预设前缀
			word=self.randPrefix()+'_'+word
		elif rate>60:#随机前缀
			word=self.randWordPrefix()+'_'+word
		elif rate>40:#字符前缀
			word=self.randLetters()+'_'+word
		else:#随机单词后缀
			tword=self.randOne(6).capitalize()
			if self.bool(70):
				tword='_'+tword.lower()
			word+=tword
		
		if self.bool(80) and not word[0]=='_':#下划线前缀
			word='_'+word
		
		return word
		
	def getFun(self,baseWord=None):
		word=self.getClass(baseWord)
		return word[0].lower()+word[1:]
	
	@word_only_one
	def getPkg(self,baseWord=None):
		return self.randOne(6)
		
	@word_only_one
	def getOneWord(self,length=0):
		return self.randOne(length)
		
randDict=RandDict()

if __name__=='__main__':
	rd=RandDict()
	# rd.creatpkg=False
	# print(rd.getClass('btn_play'))
	for i in range(0,10):
		# print(rd.randOne(10))
		# print(rd.getClass('btn_play'))
		print(rd.getProto('btn_play'))
	# print(RandDict.usedList)
	# print(RandDict.usedDict)
	raw_input("over!")
	
	
	
	
