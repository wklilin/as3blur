#python2
#coding:utf-8

import sys
import os
import re
import random
import shutil
import codecs
from words import randDict



AS3ClassTemplate='''\
package {package}{//{info}
	{parentimport}
{import}
	public class {class} extends {parent}{
{variable}
		public function {class}() {
{constructor}
		}
		
{function}
	}
}'''

def progress(msg,idx,num):
	sys.stdout.write('\r'+msg+':'+str(idx)+'/'+str(num))
	sys.stdout.flush()
	if idx==num:
		print('')
	
class RandomAS3(object):
	
	@staticmethod
	def rateArray(num,max):
		vals = []
		idx=0
		while len(vals) < num:
			idx = max
			while idx>0 and len(vals) < num:
				idx-=1
				vals.append(idx)
		resu = []
		while len(vals) > 0:
			idx = random.randint(0,len(vals)-1)
			resu.append(vals[idx])
			del vals[idx]
		return resu
		
	@staticmethod
	def boolean(rat=0.5):
		return random.random()<rat
		
class EmptyFunction(object):
	def __init__(self,code,clas):
		self.code=code
		self.clas=clas
		self.level=self.code.level_fun
		self.rows=[]
		self.returnNotVoid = RandomAS3.boolean()
		self.returnType = AS3Function.VOID
		if self.returnNotVoid:
			self.returnType = random.choice(AS3Class.DATA_TYPE)
			if self.clas.level > 0 and RandomAS3.boolean(0.3):
				self.returnType = AS3Class.CLASS
			if self.returnType == AS3Class.CLASS:
				self.returnType = self.code.getRandomClassUnderLevel(self.clas.level).name
		self.isParameter = False
		
	def out(self):
		t_rowStr = ''
		for item in self.rows:
			t_rowStr += item.out() + '\n'
		return t_rowStr.rstrip()
		
class AS3CodeRow(object):
	VAR='var'
	CONST='const'
	FUNCTION='function'
	CODE_TYPE = [VAR, FUNCTION]
	
	def __init__(self, t_func):
		self.fun = t_func
		self.clas=self.fun.clas
		self.code=self.clas.code
		self.codeValue=None
		self.codeName=None
		self.codeDataType=None
		self.codeClass=None
		
	def initWithReturn(self):
		for item in self.fun.rows:
			if item.codeDataType == self.fun.returnType:
				self.codeValue = 'return ' + item.codeName
				break
		if not self.codeValue:
			if self.fun.returnType == AS3Class.STRING:
				self.codeValue = 'return ' + self.StringValue()
			elif self.fun.returnType == AS3Class.INT:
				self.codeValue = 'return ' + self.IntValue()
			elif self.fun.returnType == AS3Class.BOOLEAN:
				self.codeValue = 'return ' + random.choice(['true','false'])
			else:
				self.codeValue = 'return new ' + self.fun.returnType + '()'
		
	def initWithNotReturn(self):
		self.codeType = random.choice(AS3CodeRow.CODE_TYPE)
		if self.clas.level == 0 or self.fun.level == 0:
			self.codeType = AS3CodeRow.VAR
			
		if self.codeType == AS3CodeRow.VAR: 
			self.codeName = randDict.getProto()
			self.codeValue = 'var ' + self.codeName + self.initValue()
			self.nextVar()
			self.selfVar()
			if self.clas.level>0:#Xue
				self.next()
		elif self.codeType == AS3CodeRow.FUNCTION: 
			self.codeValue = self.func()
		
	def out(self):
		return '\t\t\t' + self.codeValue
	
	def func(self):
		t_str = ''
		localFun = RandomAS3.boolean()
		t_fun=None
		t_parameter=''
		if localFun:
			funs = self.clas.getFunctionsUnderLv(self.fun.level)
			t_fun = random.choice(funs)
			if t_fun==self.fun:#Xue
				return self.func()
			if t_fun.returnNotVoid:
				return self.func()
			if not t_fun.isParameter:
				t_str = t_fun.name + '()'
			else:
				t_parameter = ''
				for item in t_fun.parameter:
					if item[1] == AS3Class.STRING:
						t_parameter += self.StringValue() + ','
					elif item[1] == AS3Class.INT:
						t_parameter += self.IntValue() + ','
					elif item[1] == AS3Class.BOOLEAN:
						t_parameter += self.BoolValue() + ','
					else:
						t_parameter += 'new ' + item[1] + '()' + ','
				
				t_str = t_fun.name + '(' + t_parameter[0:-1] + ')'
		else:
			t_arr = self.code.getFunsNotVoid(self.clas.level)
			t_fun = random.choice(t_arr)[0]
			if t_fun==self.fun:#Xue
				return self.func()
			if not t_fun.isParameter:
				t_str = t_fun.clas.name + '.' + t_fun.clas.staticVar.name + '.' + t_fun.name + '()'
			else:
				t_parameter = ''
				for item in t_fun.parameter:
					if item[1] == AS3Class.STRING:
						t_parameter += self.StringValue() + ','
					elif item[1] == AS3Class.INT:
						t_parameter += self.IntValue() + ','
					elif item[1] == AS3Class.BOOLEAN:
						t_parameter += self.BoolValue() + ','
					else:
						t_parameter += 'new ' + item[1] + '()' + ','
				
				t_str = t_fun.clas.name + '.' + t_fun.clas.staticVar.name + '.' + t_fun.name + '(' + t_parameter[0:-1] + ')'
		return t_str+';'
	
	def initValue(self):
		self.codeDataType = random.choice(AS3Class.DATA_TYPE)
		if self.clas.level > 0 and RandomAS3.boolean(0.3):
			self.codeDataType = AS3Class.CLASS
			self.codeClass = self.code.getRandomClassUnderLevel(self.clas.level)#Xue
		
		if self.codeDataType == AS3Class.STRING: 
			return ':String = ' + self.StringValue() + ';'
		elif self.codeDataType == AS3Class.INT: 
			return ':int = ' + self.IntValue() + ';'
		elif self.codeDataType == AS3Class.BOOLEAN: 
			return ':Boolean = ' + self.BoolValue() + ';'
		elif self.codeDataType == AS3Class.CLASS: 
			return ':' + self.codeClass.name + ' = new ' + self.codeClass.name + '();'
		return ''
	
	def next(self):
		#本类调用函数赋值用
		funs = self.clas.getFunctionsUnderLv(self.fun.level)
		if RandomAS3.boolean():
			for item in funs:
				if item.isParameter and not item.returnNotVoid:
					t_arr = item.parameter
					for idx,arr in enumerate(t_arr):
						if arr[1] == self.codeDataType:
							self.cre(item, idx)
							return
			self.next()
		else:#其他类赋值
			tureType=self.codeDataType
			if self.codeDataType == AS3Class.CLASS:
				tureType=self.codeClass.name
			t_list = self.code.getFuns(tureType, self.clas.level)
			if len(t_list)>0:
				t_obj = random.choice(t_list)[0]
				t_arr = t_obj[1].parameter
				for idx,item in enumerate(t_arr):
					if item[1] == self.codeDataType:
						self.cre(t_obj[1], idx, True)
						return
		
		if self.codeDataType == AS3Class.CLASS:
			t_v = self.codeClass.getFuncPublicByNotVoid()
			if len(t_v)>0:
				t_fun = random.choice(t_v)
				t_scc = ''
				if t_fun.isParameter:
					for item in t_fun.parameter:
						if item[1] == AS3Class.STRING:
							t_scc += self.StringValue() + ','
						elif item[1] == AS3Class.INT:
							t_scc += self.IntValue() + ','
						elif item[1] == AS3Class.BOOLEAN:
							t_scc += self.BoolValue() + ','
						else:
							t_value = self.globalVaribleValue(item[1])
							if t_value == '':
								t_scc += 'new ' + item[1] + '()' + ','
							else:
								t_scc += t_value + ','
					t_scc = t_scc[0:-1]
				self.codeValue += '\n\t\t\t' + self.codeName + '.' + t_fun.name + '(' + t_scc + ');'
	
	def nextVar(self):
		t_str = ''
		if self.codeDataType == AS3Class.STRING: 
			t_str = self.StringValue() + ';'
		elif self.codeDataType == AS3Class.INT: 
			t_str = self.IntValue() + ';'
		elif self.codeDataType == AS3Class.BOOLEAN: 
			t_str = self.BoolValue() + ';'
		elif self.codeDataType == AS3Class.CLASS: 
			t_str = self.codeClass.name + '();'
			return
		self.codeValue = self.codeValue + '\n\t\t\t' + self.codeName + ' = ' + t_str
		
	def selfVar(self):
		t_list = self.clas.getVariableByType(self.codeDataType,needOpen=False)
		if len(t_list)>0:
			tvar=random.choice(t_list)
			self.codeValue+='\n\t\t\t'+tvar.name+' = '+self.codeName+';//lalala'
	
	def cre(self, t_fun, index, t_global = False):
		t_str = ''
		t_arr = t_fun.parameter
		for idx,item in enumerate(t_arr):
			if idx == index:
				t_str += self.codeName + ','
			else:
				t_list = self.clas.getVariableByType(item[1])
				if len(t_list)>0:
					t_str += random.choice(t_list).name + ','
				else:
					t_list2 = self.code.getVariable(item[1],self.clas.level)
					if len(t_list2)>0:
						t_class = random.choice(t_list2)
						t_var=random.choice(t_class)
						t_str += t_var.clas.name + '.' + t_var.clas.staticVar.name + '.' + t_var.name + ','
					else:
						t_str += 'new ' + item[1] + '(),'
		
		t_str = t_str[0:-1]
		
		if t_global:
			self.codeValue += '\n\t\t\t' + t_fun.clas.name + '.' + t_fun.clas.staticVar.name + '.' + t_fun.name + '(' + t_str + ')'
		else:
			self.codeValue += '\n\t\t\t' + t_fun.name + '(' + t_str + ')'
	
	def StringValue(self):
		t_str = ''
		#用参数赋值参数
		if self.fun.isParameter:
			if RandomAS3.boolean():
				for item in self.fun.parameter:
					if item[1] == AS3Class.STRING:
						if RandomAS3.boolean():
							t_str = item[0]
							return t_str
		
		#类变量赋值
		if len(self.clas.getVariable())>0:
			if RandomAS3.boolean():
				for item in self.clas.variables:
					if item.dataType == AS3Class.STRING:
						if RandomAS3.boolean():
							t_str = item.name
							return t_str
		
		t_str = self.globalVaribleValue(AS3Class.STRING)
		if not t_str == '' and RandomAS3.boolean():
			return t_str
		
		t_str = self.randomStringValue()
		return t_str
	
	def IntValue(self):
		t_str = ''
		#用参数赋值参数
		if self.fun.isParameter:
			if RandomAS3.boolean():
				for item in self.fun.parameter:
					if item[1] == AS3Class.INT:
						if RandomAS3.boolean():
							t_str = item[0]
							return t_str
		
		#类变量赋值
		if len(self.clas.getVariable())>0:
			if RandomAS3.boolean():
				for item in self.clas.variables:
					if item.dataType == AS3Class.INT:
						if RandomAS3.boolean():
							t_str = item.name
							return t_str
		
		t_str = self.globalVaribleValue(AS3Class.INT)
		if not t_str == '':
			return t_str
		
		t_str = str(random.randint(0,999))
		return t_str
	
	def BoolValue(self):
		t_str = ''
		#用参数赋值参数
		if self.fun.isParameter:
			if RandomAS3.boolean():
				for item in self.fun.parameter:
					if item[1] == AS3Class.BOOLEAN:
						if RandomAS3.boolean():
							t_str = item[0]
							return t_str
		
		#类变量赋值
		if len(self.clas.getVariable())>0:
			if RandomAS3.boolean():
				for item in self.clas.variables:
					if item.dataType == AS3Class.BOOLEAN:
						if RandomAS3.boolean():
							t_str = item.name
							return t_str
		
		t_str = self.globalVaribleValue(AS3Class.BOOLEAN)
		if not t_str == '':
			return t_str
		
		t_str = random.choice(['true','false'])
		return t_str
	
	def globalVaribleValue(self,t_dataType):
		t_str = ''
		#其他类变量赋值
		t_list = self.code.getVoid(t_dataType,self.clas.level)
		if len(t_list)>0:
			t_fun = random.choice(t_list)[0]
			
			if t_fun.isParameter:
				t_str = ''
				t_arr = t_fun.parameter
				for item in t_arr:
					t_list = self.clas.getVariableByType(item[1])
					if len(t_list)>0:
						t_str += random.choice(t_list).name + ','
					else:
						t_list2 = self.code.getVariable(item[1],self.clas.level)
						if len(t_list2):
							t_class = random.choice(t_list2)
							t_var=random.choice(t_class)
							t_str += t_var.clas.name + '.' + t_var.clas.staticVar.name + '.' + t_var.name + ','
						else:
							t_str += 'new ' + item[1] + '(),'
				
				t_str = t_str[0:-1]
				t_str = t_fun.clas.name + '.' + t_fun.clas.staticVar.name + '.' + t_fun.name + '(' + t_str + ')'
				return t_str
			else:
				return t_fun.clas.name + '.' + t_fun.clas.staticVar.name + '.' + t_fun.name + '()'
		return t_str
	
	def randomStringValue(self):
		#Xue
		t_str = ''
		num = random.randint(1,4)
		for i in range(num):
			t_str += str(random.randint(0,9))
		return '"' + t_str + '"'
		
class AS3FunInfo(object):
	STATIC='static'
	funReg=re.compile('((?:(?:\w+)\s+)*)function\s+((?:get|set)?\s*\w+)\s*\((.*?)\)\s*?(:\s*?\w+?)?\s*?\{')
	# funPrefixs='final|override|static|public|protected|private|internal'
	def __init__(self,mat):
		self.prefixs=re.findall('\w+',mat.group(1))
		self.name=mat.group(2)
		self.argv=mat.group(3)
		self.type=mat.group(4)
		self.isStatic=AS3FunInfo.STATIC in self.prefixs
		
	@staticmethod
	def test(line):
		mat=AS3FunInfo.funReg.match(line)
		if mat:
			return AS3FunInfo(mat)
		else:
			return None
			
class AS3PassLine(object):
	strs=[]
	strs.append('package\\b')#package
	strs.append('import\\b')#import
	strs.append('switch\\b')#switch
	strs.append('return\\b')#return
	strs.append('break\\b')#break
	strs.append('\}')#}
	strs.append('\[\w+\((.*?)\)\]')#元数据
	strs.append('([\w ]+?)?(var|const)\s')#变量定义
	strs.append('[\w ]*?\\bfunction\\b.*?\{.*?\}')#写在单行的函数
	
	strs.append('public\s+class')#class语句
	strs.append('dynamic\s+public\s+class')#class语句
	strs.append('public\s+dynamic\s+class')#class语句
	
	strs.append('for\\b')#for
	strs.append('if\\b')#if
	strs.append('else\\b')#else
	# ifelseReg=re.compile('')#匹配不带大括号的if else
	
	reg=re.compile('|'.join(strs))
	
	def __init__(self):
		pass
		
	@staticmethod
	def test(line):
		return AS3PassLine.reg.match(line)
	
class AS3Function(object):
	VOID='void'
	def __init__(self, clas, type, lv):
		self.clas = clas
		self.code=clas.code
		self.type = type
		self.level = lv
		self.name = randDict.getFun()
		self.returnNotVoid = RandomAS3.boolean()
		self.returnType = AS3Function.VOID
		if self.returnNotVoid:
			self.returnType = random.choice(AS3Class.DATA_TYPE)
			if self.clas.level > 0 and RandomAS3.boolean(0.3):
				self.returnType = AS3Class.CLASS
			if self.returnType == AS3Class.CLASS:
				self.returnType = self.code.getRandomClassUnderLevel(self.clas.level).name
		self.isParameter = RandomAS3.boolean()
		if self.isParameter:
			self.parameter = self.randomParameter()
		
		self.rows=None
	
	def createValue(self):
		#确定多少行代码
		t_row=random.randint(1,self.code.config['codeMax'])
		self.rows = []
		for idx in range(t_row):
			row=AS3CodeRow(self)
			row.initWithNotReturn()
			self.rows.append(row)
		
		if self.returnNotVoid:
			row=AS3CodeRow(self)
			row.initWithReturn()
			self.rows.append(row)
	
	def outParameter(self):
		if not self.isParameter:
			return ''
		t_str = ''
		for item in self.parameter:
			t_str += item[0] + ':' + item[1] + ', '
		return t_str[0:-1]
	
	def randomParameter(self):
		t_arr = []
		t_length = random.randint(1,3)
		for i in range(t_length):
			t_type = random.choice(AS3Class.DATA_TYPE)
			if self.clas.level > 0 and RandomAS3.boolean(0.3):
				t_type = AS3Class.CLASS
			if t_type == AS3Class.CLASS:
				t_type = self.code.getRandomClassUnderLevel(self.clas.level).name
			t_arr.append([randDict.getProto(), t_type])
		return t_arr
	
	def out(self):
		t_parameter = ''
		if self.isParameter:
			for item in self.parameter:
				t_parameter += item[0] + ':' + item[1] + ','
			t_parameter = t_parameter[0:-1]
		t_void = ':' + self.returnType
		
		t_rowStr = ''
		if len(self.rows)>0:
			for item in self.rows:
				t_rowStr += item.out() + '\n'
		
		t_str = '\t\t' + self.type + ' function ' + self.name + '(' + t_parameter + ')' + t_void + ' {//level:'+str(self.level)+'\n'
		if self.code.debugtrace:
			t_str+='trace("'+self.clas.name+'::'+self.name+'()");\n'
		t_str += t_rowStr
		t_str += '\t\t}\n'
		return t_str
		
	def isOpen(self):
		return self.type == AS3Class.PUBLIC
	
class AS3Variable(object):
	
	def __init__(self,clas,type,isStatic=False,name=None,dataType=None,initValue=False):
		self.value=None
		self.clas=clas
		self.code=clas.code
		self.type = type
		
		self.isStatic=isStatic
		
		if name:
			self.name=name
		else:
			self.name = randDict.getProto()
	
		if dataType:
			self.dataType=dataType
		else:
			self.dataType = random.choice(AS3Class.DATA_TYPE)
			if self.clas.level > 0 and RandomAS3.boolean(0.3):
				self.dataType = AS3Class.CLASS
			if self.dataType == AS3Class.CLASS:
				self.dataType = self.code.getRandomClassUnderLevel(self.clas.level).name
				
		if initValue:
			if self.dataType == AS3Class.STRING:
				self.value=' = "'+str(random.randint(0,20))+'";'
			elif self.dataType == AS3Class.INT:
				self.value=' = '+str(random.randint(0,25))+';'
			elif self.dataType == AS3Class.BOOLEAN:
				self.value=' = false;'
			else:
				self.value=' = new '+self.dataType+'();'
		else:
			self.value=';'
		
	def out(self):
		type=self.type
		if self.isStatic:
			type+=' static'
		t_str = '\t\t' + type + ' var ' + self.name + ':' + self.dataType + self.value
		return t_str
	
	def isOpen(self):
		return self.type == AS3Class.PUBLIC

class ClassObject(object):
	def __init__(self):
		self.path='Object'
		self.name='Object'
	
class ClassShape(ClassObject):
	def __init__(self):
		ClassObject.__init__(self)
		self.path='flash.display.Shape'
		self.name='Shape'
	
class ClassSprite(ClassObject):
	def __init__(self):
		ClassObject.__init__(self)
		self.path='flash.display.Sprite'
		self.name='Sprite'
	
class ClassEventDispatcher(ClassObject):
	def __init__(self):
		ClassObject.__init__(self)
		self.path='flash.events.EventDispatcher'
		self.name='EventDispatcher'
	
class AS3Class(object):
	PUBLIC='public'
	PRIVATE='private'
	
	PARENTS=[ClassObject(),ClassShape(),ClassEventDispatcher(),ClassSprite()]
	
	CLASS='class'
	INTERFACE='interface'
	STRING='String'
	INT='int'
	BOOLEAN='Boolean'
	DATA_TYPE = [STRING, INT, BOOLEAN]
	
	def __init__(self,code,nm,pkg,lv):
		self.code=code
		self.name = nm
		self.package = pkg
		self.level = lv
		self.parent=random.choice(AS3Class.PARENTS)
		self.filePath=(self.package.replace('.', '\\') + '\\' + self.name + '.as').strip('\\')
		self.staticVar=None#自身类型的静态属性
		self.variables=None
		self.functions=None
		
		#------------------------------------------------------------------------------------
		
		self.baseContent=None
		self.type=None#class or interface
		self.insertRate=1#插入代码的几率，1表示每行后都插入代码，0表示完全不插入代码
	
	def createVariables(self,isStatic=False):
		if isStatic:
			self.staticVar=AS3Variable(self,AS3Class.PUBLIC,True,None,self.name,True)
		self.variables = []
		num = random.randint(0,self.code.config['varMax']) + self.code.config['varMin']
		for idx in range(num):
			t_obj = AS3Variable(self,AS3Class.PUBLIC,initValue=RandomAS3.boolean(self.code.initVar))
			self.variables.append(t_obj)
			if RandomAS3.boolean():
				t_obj = AS3Variable(self,AS3Class.PRIVATE,initValue=RandomAS3.boolean(self.code.initVar))
				self.variables.append(t_obj)
	
	def createFunctions(self):
		num = random.randint(0,self.code.config['funMax']) + self.code.config['funMin']
		levels = RandomAS3.rateArray(num, self.code.level_fun)#Xue
		self.functions = []
		for idx in range(num):
			t_obj = AS3Function(self, AS3Class.PUBLIC, levels.pop())
			self.functions.append(t_obj)
			if RandomAS3.boolean():
				t_obj = AS3Function(self, AS3Class.PRIVATE, random.randint(0,self.code.level_fun))
				self.functions.append(t_obj)
	
	def createFunctionsValue(self):
		for item in self.functions:
			item.createValue()
	
	def out(self):
		tStr = AS3ClassTemplate
		tStr = tStr.replace('{package}', self.package)
		tStr = tStr.replace('{parentimport}', 'import '+self.parent.path+';')
		tStr = tStr.replace('{parent}', self.parent.name)
		tStr = tStr.replace('{import}', self.code.importStr)
		tStr = tStr.replace('{class}', self.name)
		tStr = tStr.replace('{variable}', self.outVariables())
		tStr = tStr.replace('{constructor}', '')
		tStr = tStr.replace('{function}', self.outFunctions())
		tStr = tStr.replace('{info}', 'level:' + str(self.level))
		return tStr
		
	def outVariables(self):
		t_str = ''
		if self.staticVar:
			t_str += self.staticVar.out() + '\n'
		for item in self.variables:
			t_str += item.out() + '\n'
		return t_str
	
	def outFunctions(self):
		t_str = ''
		for item in self.functions:
			t_str += item.out() + '\n'
		return t_str
	
	def getVariable(self):
		t_arr=[]
		for item in self.variables:
			if item.isOpen():
				t_arr.append(item)
		return t_arr
	
	def getVariableByType(self,t_dataType,needOpen=True):
		t_arr = []
		for item in self.variables:
			if item.dataType == t_dataType:
				if not needOpen:
					t_arr.append(item)
				elif item.isOpen():
					t_arr.append(item)
		return t_arr
	
	#获取属性中类型是自定义类的属性
	def getClassVariable(self,needOpen=True):
		t_arr = []
		for item in self.variables:
			if not item.dataType in AS3Class.DATA_TYPE:
				if not needOpen:
					t_arr.append((self, item))
				elif item.isOpen():
					t_arr.append((self, item))
		return t_arr
	
	def getFunc(self):
		t_arr=[]
		for item in self.functions:
			if item.isOpen():
				t_arr.append(item)
		return t_arr
	
	def getFuncPublicByParameter(self,t_ParameterType):
		t_arr=[]
		for item in self.functions:
			if item.isParameter and item.isOpen() and not item.returnNotVoid:
				for funArr in item.parameter:
					if funArr[1] == t_ParameterType:
						t_arr.append([self.name, item])
		return t_arr
	
	def getFuncPublicByNotVoid(self):
		t_arr = []
		for item in self.functions:
			if not item.returnNotVoid and item.isOpen():
				t_arr.append(item)
		return t_arr
	
	def getVoidByType(self,t_voidType):
		t_arr = []
		for item in self.functions:
			if item.returnNotVoid and item.isOpen() and item.returnType == t_voidType:
				t_arr.append(item)
		return t_arr
	
	def getFunctionsUnderLv(self,lv):
		arr=[]
		for item in self.functions:
			if item.level < lv:
				arr.append(item)
		return arr
	
	'''在代码行之间插入混淆代码'''
	def insertRandCode(self):
		if self.type==AS3Class.INTERFACE:
			return
		curFun=None
		# funObj=None#Xue
		
		newLines=[]
		lines=self.baseContent.splitlines()
		while len(lines)>0:
			line=lines.pop(0)
			newLines.append(line)
			
			line=line.strip()
			
			fun=AS3FunInfo.test(line)
			if fun:
				curFun=fun
			if curFun and curFun.isStatic:
				continue
			
			ps=AS3PassLine.test(line)
			if not ps and RandomAS3.boolean(self.insertRate):
				funObj=EmptyFunction(self.code,self)
				num=random.randint(1,3)
				for i in range(num):
					row=AS3CodeRow(funObj)
					row.initWithNotReturn()
					funObj.rows.append(row)
				newLines.append(AS3Confuse.markBlur(funObj.out()))
		self.baseContent='\n'.join(newLines)
		
	'''把生成的随机属性和方法插入到代码'''
	def addRandCode(self):
		if self.type==AS3Class.CLASS:
			self.baseContent=self.code.pkgReg.sub(self._pkgRegSubFun,self.baseContent)
			self.baseContent=self.code.clsReg.sub(self._clsRegSubFun,self.baseContent)
		
	def _pkgRegSubFun(self,m):
		impt=AS3Confuse.markBlur(self.code.importStr)
		return m.group()+'\n'+impt
		
	def _clsRegSubFun(self,m):
		gp=m.group()
		members=AS3Confuse.markBlur(self.outVariables()+'\n'+self.outFunctions())
		return gp+members
		
class AS3File(object):
	def __init__(self):
		pass
	
class AS3Confuse(object):
	#添加表示混淆代码的注释
	@staticmethod
	def markBlur(cc):
		return '\n//-%-confuse-start-%-\n'+cc+'\n//-%-confuse-end-%-\n'
	
	def __init__(self):
		self.debugtrace=False
		self.initVar=0.4
		
		self.config={'varMin': 5, 'varMax': 10, 'funMin': 5, 'funMax': 10, 'codeMax': 4}
		self.level_class=3
		self.level_fun=3
		
		self.numClass = 50
		self.clsPkg=None
		self.importStr=None
		self.classList=None
		
		self.nativePath=None
		
		#------------------------------------------------------------------------------------------
		self.globalInsertRate=1
		self.insertRateDict={}
		
		self.noteReg=re.compile('\\/\\*(\\s|.)*?\\*\\/|(?<!:)\\/\\/.*')#注释
		self.braceReg=re.compile('(?<=\S)\s+\{')#大括号左半部分
		self.elseReg=re.compile('\}\s*else\\b')#else
		self.spaceReg=re.compile('(?<=\n)[ 	]*\n')#空行
		self.unpubReg=re.compile('\\binternal\s+class\\b')#internal/final class
		# strReg=re.compile(''.*?'|\'.*?\'')#字符串
		# reReg=re.compile('')#正则
		
		self.pkgReg=re.compile('\\bpackage\s*(.*?)\{')#匹配package定义，添加import
		self.clsReg=re.compile('(?:dynamic\s+)?(?:public\s+)?(?:dynamic\s+)?(class|interface)\s+(\w+)\s*(?:[\w\s.,]+)?\{')#匹配public class类定义，添加属性和方法，不包括包外类
		self.simpleClsReg=re.compile('\\b(class|interface)\s+(\w+)')
		
	def creat(self,t_path,t_num):
		self.formatFiles(t_path)
		self.createClass(t_num)
		self.insertCode(t_path)
		self.outFiles(t_path)
	
	'''格式化代码，检查代码格式'''
	def formatFiles(self,t_path):
		print(u'格式化代码...')
		for root,dirs,files in os.walk(t_path):
			for file in files:
				fp=os.path.join(root,file)
				nm,ext=os.path.splitext(file)
				if ext=='.as':
					with open(fp) as f:
						cc=f.read()
					if cc[:3]==codecs.BOM_UTF8:#去掉bom头
						cc=cc[3:]
					cc=self.noteReg.sub('',cc)
					cc=self.braceReg.sub('{',cc)
					cc=self.elseReg.sub('}else',cc)
					cc=self.unpubReg.sub('public class',cc)
					cc=self.spaceReg.sub('',cc)
					cc=cc.strip()#Xue 去掉文件开头和末尾的空字符
					self.checkFormat(fp,cc)
					
					with open(fp,'w') as f:
						f.write(cc)
		
	'''检查代码格式'''
	def checkFormat(self,fp,asfile):
		m=self.pkgReg.match(asfile)
		if not m:
			print(u'-->警告：在文件中找不到package定义。file:'+fp)
			raise Exception(fp)
		
		nm,ext=os.path.splitext(os.path.basename(fp))
		clsli=self.simpleClsReg.findall(asfile)
		if len(clsli)>=2:
			print(u'-->警告：不支持包内类定义，一个文件中只允许定义一个同名类。file:'+fp)
			raise Exception(fp)
		
		m=self.clsReg.search(asfile)
		if m:
			if m.group(2)!=nm:
				print(u'-->警告：文件中类定义和文件名不匹配。file:'+fp)
				raise Exception(fp)
		else:
			print(u'-->警告：在文件中找不到类定义。file:'+fp)
			raise Exception(fp)
	
	def insertCode(self,tpath):
		tmpClassList=[]
		rootdir=os.getcwd()
		os.chdir(tpath)
		for root,dirs,files in os.walk('.'):
			pkg=root.replace('\\','.').strip('.')
			for file in files:
				fp=os.path.join(root,file)
				nm,ext=os.path.splitext(file)
				if ext=='.as':
					asCls=AS3Class(self,nm,pkg,self.level_class)
					with open(fp) as f:
						asCls.baseContent=f.read()
					tmpClassList.append(asCls)
					m=self.clsReg.search(asCls.baseContent)
					asCls.type=m.group(1)
		
		os.chdir(rootdir)
		num=len(tmpClassList)
		for idx,item in enumerate(tmpClassList):
			item.createVariables()
			progress(u'生成类变量',idx+1,num)
		for idx,item in enumerate(tmpClassList):
			item.createFunctions()
			progress(u'生成类方法',idx+1,num)
		for idx,item in enumerate(tmpClassList):
			item.createFunctionsValue()
			progress(u'代码填充',idx+1,num)
		
		for idx,item in enumerate(tmpClassList):
			item.insertRate=self.globalInsertRate
			if item.name in self.insertRateDict:
				item.insertRate=self.insertRateDict[item.name]
			item.insertRandCode()
			progress(u'插入代码',idx+1,num)
			
		for idx,item in enumerate(tmpClassList):
			item.addRandCode()
			progress(u'添加代码',idx+1,num)
		
		self.nativePath=tpath.replace('/','\\')
		for idx,item in enumerate(tmpClassList):
			self.saveFile(item.filePath, item.baseContent)
			progress(u'保存代码文件',idx+1,num)
	
	'''设置插入代码的几率，1表示每行后都插入代码，0表示完全不插入代码，默认1'''
	def setGlobalInsertRate(self,rate):
		self.globalInsertRate=rate
		
	'''设置特定类（文件）插入代码的几率，1表示每行后都插入代码，0表示完全不插入代码'''
	def setInsertRate(self,name,rate):
		self.insertRateDict[name]=rate
	
	def createClass(self, t_num):
		self.numClass = t_num
		
		self.clsPkg = 'com.' + randDict.getPkg() + '.' + randDict.getPkg()
		self.importStr = '\timport ' + self.clsPkg + '.*;'
		
		self.classList = []
		print(u'开始生成类...')
		
		self.updateCreateClass()
		self.updatecreateVariable()
		self.updatecreateFunctions()
		self.updatecreateFunctionsValue()
		
	
	#创建类
	def updateCreateClass(self):
		levels=RandomAS3.rateArray(self.numClass,self.level_class)
		for idx in range(self.numClass):
			self.classList.append(AS3Class(self, randDict.getClass(), self.clsPkg, levels.pop()))
			progress(u'生成类',idx+1,self.numClass)
	
	#创建变量
	def updatecreateVariable(self):
		for idx,item in enumerate(self.classList):
			item.createVariables(True)
			progress(u'生成类变量',idx+1,self.numClass)
	
	#创建方法
	def updatecreateFunctions(self):
		for idx,item in enumerate(self.classList):
			item.createFunctions()
			progress(u'生成类方法',idx+1,self.numClass)
	
	#创建方法内容
	def updatecreateFunctionsValue(self):
		for idx,item in enumerate(self.classList):
			item.createFunctionsValue()
			progress(u'代码填充',idx+1,self.numClass)
		
	def outFiles(self,root):
		self.nativePath=root.replace('/','\\')
		for idx,item in enumerate(self.classList):
			self.saveFile(item.filePath, item.out())
			progress(u'保存代码文件',idx+1,self.numClass)
		
		print(u'全部代码生成完成!')
	
	def saveFile(self, filePath, t_code):
		filePath=filePath.replace('/','\\')
		t_f=os.path.join(self.nativePath,filePath)
		targetParent=os.path.dirname(t_f)
		if not os.path.isdir(targetParent):
			os.makedirs(targetParent)
		with open(t_f,'w') as f:
			f.write(t_code)
	
	def getVariable(self, t_dataType, lv):
		t_arr=[]
		for item in self.classList:
			if item.level<lv:
				t_list = item.getVariableByType(t_dataType)
				if len(t_list)>0:
					t_arr.append(t_list)
		return t_arr
	
	def getFuns(self, t_dataType, lv):
		t_arr=[]
		for item in self.classList:
			if item.level<lv:
				t_obj = item.getFuncPublicByParameter(t_dataType)
				if len(t_obj)>0:
					t_arr.append(t_obj)
		return t_arr
	
	def getFunsNotVoid(self, lv):
		t_arr=[]
		for idx,item in enumerate(self.classList):
			if item.level < lv:#Xue
				t_obj = item.getFuncPublicByNotVoid()
				if len(t_obj)>0:
					t_arr.append(t_obj)
		return t_arr
	
	def getVoid(self, t_voidType, lv):
		t_arr=[]
		for idx,item in enumerate(self.classList):
			if item.level < lv:#Xue
				t_obj = item.getVoidByType(t_voidType)
				if len(t_obj)>0:
					t_arr.append(t_obj)
		return t_arr
	
	def getRandomClass(self):
		return random.choice(self.classList)
	
	
	def getRandomClassByLevel(self, lv):
		classArr=[]
		for item in self.classList:
			if item.level == lv:
				classArr.append(item)
		if len(classArr)>0:
			return random.choice(classArr)
		else:
			return None
	
	def getRandomClassUnderLevel(self, lv):
		classArr=[]
		for item in self.classList:
			if item.level < lv:
				classArr.append(item)
		if len(classArr):
			return random.choice(classArr)
		else:
			return None
	
if __name__=='__main__':
	# src='rand/src'
	# if os.path.isdir(src):
		# shutil.rmtree(src)
	# shutil.copytree('D:\h5pkg\develop\src',src)
	
	# ac=AS3Confuse()
	# ac.formatFiles(src)
	# ac.createClass(20)
	# ac.insertCode(src)
	# ac.outFiles(src)
	print(AS3ClassTemplate)















