#!python2
#coding:utf-8

'''
-----------------------------------
           as3代码混淆
-----------------------------------
'''

import sys
#sys.dont_write_bytecode = True
import os
import shutil
import re
import random
import time
from words import randDict


class AdditionFun():
	def __init__(self):
		#注释正则，去掉注释用
		self.noteReg1=re.compile('/\*(.|\n)*?\*/')#块注释
		self.noteReg2=re.compile(r'(?<!:|\\)//.*')#行注释
		#function，if，eles正则
		self.funReg=re.compile(r'((?:public|protected|private|internal)?)\s+function\s+?(\w+)\s*\((.*?)\)\s*?(:\s*?\w+?)?\s*?\{')
		self.ifReg=re.compile(r'\sif *\(.*?\)\s*{')
		self.elseReg=re.compile(r'}\s*else\s*{')
		#class正则
		self.clsReg=re.compile('([	]*)(?:\[.*?\]\s*)*\s*?([	]*)[a-z ]*class\s+\w+\\b')
		# self.clsReg=re.compile('\\n([ 	])*[a-z ]*class\s+\w+\\b')
		
		#代码产出函数
		self.funsFun=None
		#一个代码list，随机调取
		self.funsList=None
		#要替换的字段的正则列表
		self.replRegs=[]
		#排除不更改的类文件
		self.exceptClass=[]
		#rand的文档类
		self.randDoc=None
		
		
	#----------------------------------------------------------------
	def addReplaceReg(self,regStr):
		self.replRegs.append(re.compile(regStr))
		
	#----------------------------------------------------------------
	def setFunsList(self,randp):
		docp=os.path.join(randp,'doc.txt')
		funp=os.path.join(randp,'functions.txt')
		
		with open(docp) as f:
			self.randDoc=f.read().strip()
		with open(funp) as f:
			self.funsList=f.read().splitlines()
			
		self.funsFun=self._funsListFun
		
	def _funsListFun(self):
		code=random.choice(self.funsList)
		return code
		
	#----------------------------------------------------------------
	def setFunStrCreater(self,fun):
		# print('')
		# print(u'  警告：这个方法已经不建议使用，按任意键继续。（setFunStrCreater()）')
		raw_input()
		self.funsFun=fun
		
	def setFunStr(self,fustr):
		# print('')
		# print(u'  警告：这个方法已经不建议使用，按任意键继续。（setFunStr()）')
		raw_input()
		fstr=fustr
		fstr=fstr.replace(';','')
		fstr=fstr.replace('()','')
		def strFun():
			return fstr+'('+str(random.randint(0,555))+');'
		self.funsFun=strFun
	
	#----------------------------------------------------------------
	def addExceptClass(self,val):
		self.exceptClass.append(val)
		
	def add(self,cls,cc):
		cc=self.delNote(cc)
		if cls in self.exceptClass:
			return cc
		
		if self.randDoc:
			cc=self.clsReg.sub(self._subClassFun,cc)
		
		if len(self.replRegs)>0:
			for reg in self.replRegs:
				cc=reg.sub(self._subReplFun,cc)
		
		cc=self.funReg.sub(self._subCodeFun,cc)
		cc=self.ifReg.sub(self._subCodeFun,cc)
		cc=self.elseReg.sub(self._subCodeFun,cc)
		
		return cc
	
	def _subClassFun(self,m):
		gp=m.group()
		t=m.group(1)
		if not t:
			t=m.group(2)
		if not t:
			t=''
		# print(gp)
		return '\n'+t+'import '+self.randDoc+';\n'+gp
		
	def _subReplFun(self,m):
		#print(m.group())
		return self.funsFun()
		
	def _subCodeFun(self,m):
		#print(m.group())
		return m.group()+'\n\t\t'+self.funsFun()+'\n'
		
	#去掉注释
	def delNote(self,cc):
		cc=self.noteReg1.sub('',cc)
		cc=self.noteReg2.sub('',cc)
		return cc
		
	def test(self):
		with open(os.path.join('src','x_Game.as')) as f:
			cc=f.read()
		cc=self.add(cc,'x_Log.log();')
		print(cc)

class AdditionArgv():
	def __init__(self):
		self.reg=re.compile('function\s+?(?P<funname>\w+?)\((?P<argvs>.*?)\)')
		self.repl='function funname(argvs)'
		
		self.big='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		self.small='abcdefghijklmnopqrstuvwxyz'
		
		self.notChangeFile=[]
		self.notChangeFun=['dispose','toString','clone']
		self.dict={}#记录函数名字对应的参数
	
		argvFun={}
		argvFun['Array']=self.argvArray
		argvFun['String']=self.argvString
		argvFun['int']=self.argvInt
		argvFun['uint']=self.argvInt
		argvFun['Number']=self.argvNumber
		argvFun['Boolean']=self.argvBoolean
		argvFun['Object']=self.argvObject
		self.argvFun=argvFun
		self.argvTypes=[]
		for key in self.argvFun:
			self.argvTypes.append(key)
	
	def creat(self,asfile,nm):
		if 'extends Proxy' in asfile:#适配06模版
			return asfile
		if nm in self.notChangeFile:
			return asfile
		# if 'implements' in asfile:
			# return asfile
		# asfile='public function testfun():void{\n}\n'
		# asfile=asfile+'public function testfun1(t:Array):void{\n}\n'
		# asfile=asfile+'public function testfun2(s:String):void{\n}\n'
		# print(asfile)
		# print('---------------------------------------------------------')
		asfile=self.reg.sub(self.subFun,asfile)
		#print(asfile)
		return asfile
	
	def subFun(self,m):
		gp=m.group()
		if 'set ' in gp or 'get ' in gp:
			return gp
		fname=m.group(1)
		argvs=m.group(2).strip()
		
		if fname in self.notChangeFun:
			return gp
		
		repl=self.repl.replace('funname',fname)
		repl=repl.replace('argvs',self.getMoarArgvs(fname,argvs))
		return repl
	
	def getMoarArgvs(self,fname,argv):
		if '...' in argv:
			return argv
		if fname in self.dict:
			margv=self.dict[fname]
		else:
			count=1
			argv=argv.strip()
			argvli=[]
			num=random.randint(0,4)
			if num==0:
				margv=''
			else:
				for i in range(0,num):
					idx=random.randint(0,len(self.argvTypes)-1)
					type=self.argvTypes[idx]
					# name=self.randName(3,7)+str(count)
					name='argv'+str(count)
					fun=self.argvFun[type]
					argvli.append(name+':'+type+' = '+fun())
					count+=1
				margv=', '.join(argvli)
			self.dict[fname]=margv
			
		if argv=='':
			argv=margv
		else:
			if not margv=='':
				argv=argv+', '+margv
		return argv
	
	def argvString(self):
		return '"null"'
	
	def argvArray(self):
		return 'null'
	
	def argvInt(self):
		return '0'
	
	def argvNumber(self):
		return '1'
	
	def argvBoolean(self):
		return 'false'
	
	def argvObject(self):
		return 'null'
	
	#获取一个随机名字
	def randName(self,min,max):
		result=''
		num=random.randint(min,max)
		for i in range(0,num):
			result=result+self.small[random.randint(0,len(self.small)-1)]
		return result

class AS3BlurTool():
	
	def __init__(self):
		random.seed()
		
		#额外参数
		self.argv=AdditionArgv()
		#额外函数
		# self.additionFun=AdditionFun()
		#要替换的关键字字典
		self.replDict={}
		#replDict键值翻转，用来查找原字段名
		self.re_replDict={}
		#要替换的关键字列表
		self.replList=[]
		
		self.regCls=re.compile('\\b(class|interface)\s+(\w+)\\b')#匹配class定义
		self.regVar=re.compile('\\b(var|const)\s+(\w+)\\b')#匹配定义变量
		self.regFun=re.compile('\\bfunction\s+?(get|set)?\s*(\w+)\\b')#匹配函数语句
		# self.RegX=re.compile('\\b(_?x?_)(\w+)\\b')#匹配含前缀 _,x_
		# self.RegX=re.compile('\\b((_x_)|(x_))\w+\\b')#匹配含前缀 x_,_x_
		self.RegX=re.compile('\\b(\w*)_(\w*)\\b')#匹配含有下划线的单词
		#始终混淆文件名，不管文件名是不是匹配self.RegX
		self.blurAllClass=False
		#始终混淆变量名
		self.blurAllVar=False
		#始终混淆函数名
		self.blurAllFun=False
		
		#不混淆的单词
		self.addExcept('_','i','flash','root','play','stop')#Xue
	
	def addReplace(self,power,oldkey,newkey):
		if oldkey in self.replDict:
			item=self.replDict[oldkey]
			if item['new']==newkey:
				return
			else:
				raise Exception('[addReplace] Error-> word:\''+oldkey+'\' has existed in replDict!!\n power:'+str(power)+'  oldkey:'+oldkey+'  newkey:'+newkey)
		rep={'power':power,'old':oldkey,'new':newkey}
		rep['re']=re.compile('\\b'+oldkey.replace('.','\.')+'\\b')
		rep['dif']=not oldkey==newkey
		self.replDict[oldkey]=rep
		randDict.addKeyWord(oldkey,newkey)
		return rep
	
	#添加不需要混淆的字
	def addExcept(self,*lst):
		for item in lst:
			# print(item)
			self.addReplace(10000,item,item)
	
	#添加额外需要单独替换的单词表，一般是SWC的资源类名、元件名字混淆，因为不满足默认混淆，需要单独处理
	def loadExcept(self,classf):
		if not os.path.isfile(classf):
			raw_input('wornning! file '+classf+' not exists!')
		with open(classf) as f:
			items=f.readlines()
		for item in items:
			item=item.strip()
			arr=item.split(':')
			
			self.addReplace(0,arr[2],arr[2])#Xue 防止带下划线的单词再次被匹配被替换掉
			if not arr[1]==arr[2]:
				self.addReplace(len(arr[1]),arr[1],arr[2])
			
	#替换需要替换的单词
	def replAllWords(self,asfile):
		for item in self.replList:
			if item['dif']:
				asfile=item['re'].sub(item['new'],asfile)
		return asfile
		
	#扫描读取要混淆的关键字
	def _readKeyWords(self,d):
		#优先混淆包路径和文件类名
		for root,dirs,files in os.walk(d):
			rootli=root.split('\\')
			del rootli[0]
			# trootli=rootli
			# power=len(rootli)
			# oldpkg='.'.join(rootli)#原包名
			# newpkg='.'.join(trootli)#新包名
			# print(oldpkg)
			# if power>0:#添加新老包名，导入路径替换，排除顶层包路径
				# self.addReplace(power+10000, 'package '+oldpkg, 'package '+newpkg)
				# self.addReplace(power+1000, oldpkg+'.', newpkg+'.')
				# self.addReplace(power+100, oldpkg, newpkg)
			for idx,oldpkg in enumerate(rootli):
				if not oldpkg in self.replDict:
					newpkg=oldpkg
					self.addReplace(len(oldpkg)+1000, oldpkg, newpkg)
			for file in files:
				fp=os.path.join(root,file)
				oldname,ext=os.path.splitext(file)
				newname=oldname
				if self.RegX.match(oldname) or self.blurAllClass:
					if oldname in self.replDict:
						newname=self.replDict[oldname]['new']
					else:
						newname=randDict.getClass(oldname)
						self.addReplace(len(oldname),oldname,newname)
				else:
					if not oldname in self.replDict:
						self.addReplace(0,oldname,newname)
		#文件内容
		for root,dirs,files in os.walk(d):
			for file in files:
				fp=os.path.join(root,file)
				with open(fp) as f:
					filec=f.read()
				self.RegX.sub(self._regXSubFun,filec)
				# if self.blurAllClass:
					# self.regCls.sub(self._clsSubFun,filec)
				# if self.blurAllVar:
					# self.regVar.sub(self._varSubFun,filec)
				# if self.blurAllFun:
					# self.regFun.sub(self._funSubFun,filec)
		
		self.re_replDict=zip(self.replDict.values(),self.replDict.keys())
		self.replList=self.replDict.values()
		self.replList.sort(key=lambda obj:obj.get('power'), reverse=True)
		
	def _regXSubFun(self,m):
		word=m.group()
		resu=word
		if word in self.replDict:
			resu=self.replDict[word]['new']
		else:
			if word.isupper():#Xue  排除全是大写的情况
				resu=word
			else:
				resu=randDict.getProto(word)
				self.addReplace(0,word,resu)
		return resu
		
	def _clsSubFun(self,m):
		word=m.group(2)
		resu=word
		if word in self.replDict:
			resu=self.replDict[word]['new']
		else:
			if word.isupper():#Xue  排除全是大写的情况
				resu=word
			else:
				resu=randDict.getClass(word)
				self.addReplace(0,word,resu)
		return resu
	
	def _varSubFun(self,m):
		word=m.group(2)
		resu=word
		if word in self.replDict:
			resu=self.replDict[word]['new']
		else:
			if word.isupper():#Xue  排除全是大写的情况
				resu=word
			else:
				resu=randDict.getProto(word)
				self.addReplace(0,word,resu)
		return resu
		
	def _funSubFun(self,m):
		word=m.group(2)
		resu=word
		if word in self.replDict:
			resu=self.replDict[word]['new']
		else:
			if word.isupper():#Xue  排除全是大写的情况
				resu=word
			else:
				resu=randDict.getFun(word)
				self.addReplace(0,word,resu)
		return resu
		
	def _moveFile(self,pdir,tdir):
		for root,dirs,files in os.walk(pdir):
			for dir in dirs:
				dp=os.path.join(root,dir)
				dpli=dp.split('\\')
				dpli[0]=tdir
				for i in range(1,len(dpli)):
					dpli[i]=self.replDict[dpli[i]]['new']
				tdp='\\'.join(dpli)
				if not os.path.isdir(tdp):
					os.makedirs(tdp)
			
			for file in files:
				fp=os.path.join(root,file)
				nm,ext=os.path.splitext(file)
				fpli=fp.split('\\')
				fpli[0]=tdir
				fpli[-1]=nm
				for i in range(1,len(fpli)):
					fpli[i]=self.replDict[fpli[i]]['new']
				tfp='\\'.join(fpli)+ext
				
				with open(fp) as f:
					filec=f.read()
				#额外rand方法
				# filec=self.additionFun.add(nm,filec)
				#替换需要替换的单词
				filec=self.replAllWords(filec)
				#添加额外参数
				filec=self.argv.creat(filec,nm)
				#保存
				with open(tfp,'w') as f:
					f.write(filec)
		
	def blur(self,pdir,tdir):
		print('AS3BlurTool start')
		
		if os.path.exists(tdir):
			shutil.rmtree(tdir)
		self._readKeyWords(pdir)
		self._moveFile(pdir,tdir)
		
		print('AS3BlurTool end')
		
	def outputBlur(self,file):
		data=''
		for key in self.replDict:
			data+='begin:'+key+':'+self.replDict[key]['new']+':end\n'
		with open(file,'w') as f:
			f.write(data)
			
	def getBlur(self,key):
		if not key in self.replDict:
			return key
		else:
			return self.replDict[key]['new']
			
	
	#获取一个随机名字
	def randName(self,length):
		big='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		small='abcdefghijklmnopqrstuvwxyz'
		result=''
		for num in range(0,length):
			result=result+small[random.randint(0,len(small)-1)]
		return result
		
def testAdditionFun():
	af=AdditionFun()
	af.setFunStr('x_Loger.x_toSelfLog();')
	with open(os.path.join('src','x_Game.as')) as f:
		cc=f.read()
	cc=af.add('x_Game',cc)
	
def test():
	dirf='src'
	dirt='src_r'
	if len(sys.argv)>=3:
		dirf=sys.argv[1]
		dirt=sys.argv[2]
	elif len(sys.argv)==2:
		dirf=sys.argv[1]
		dirt=dirf+'_r'
	
	tool=AS3BlurTool()
	tool.loadExcept('map.txt')
	tool.additionFun.addExceptClass('x_Loger')
	tool.additionFun.setFunStr('x_Loger.x_toSelfLog();')
	tool.blur(dirf,dirt)
	tool.outputBlur('blur.txt')
	#tool.test()
	#raw_input("over!")
	#time.sleep(1)
	
def testAddReaplace():
	tool=AS3BlurTool()
	tool.addExcept('Main','Main')

if __name__=='__main__':
	testAddReaplace()
	
	
	
	
