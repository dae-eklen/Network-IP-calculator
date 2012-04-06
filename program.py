import sys
from PyQt4 import QtCore, QtGui
from ui import Ui_MainWindow

class MyForm(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self.computeFunc)
		
	def computeFunc(self):
		# get IP
		try:
			s1 = int(self.ui.lineEdit_s1.text())
			s2 = int(self.ui.lineEdit_s2.text())
			s3 = int(self.ui.lineEdit_s3.text())
			s4 = int(self.ui.lineEdit_s4.text())
			
			if (self.validateFail(s1) or self.validateFail(s2) or self.validateFail(s3) or self.validateFail(s4)
				or int(s1) == 0 or int(s4) == 0):
				QtGui.QMessageBox.about(self, "Error", "Error in IP address!")
				
		except:
			QtGui.QMessageBox.about(self, "Error", "Empty IP address!")
		else:
			
		#get Mask
			#if short
			mode = None
			if str(self.ui.lineEdit_s5.text()) != '':
				mode = 's'
				sMask = str(self.ui.lineEdit_s5.text())
				if (int(sMask) > 32 or int(sMask) < 0):
					QtGui.QMessageBox.about(self, "Error", "Error in short mask!")
				mask = ''
				for i in range(int(sMask)):
					mask += '1'
				while len(mask) != 32:
					mask += '0'
					
				#print mask
				m1 = mask[:8]
				m2 = mask[8:16]
				m3 = mask[16:24]
				m4 = mask[24:32]			
			#if long
			elif (str(self.ui.lineEdit_m1.text()) != '' and str(self.ui.lineEdit_m2.text()) != ''
				and str(self.ui.lineEdit_m3.text()) != '' and str(self.ui.lineEdit_m4.text()) != ''):
				mode = 'l'
				lMask1 = int(self.ui.lineEdit_m1.text())
				lMask2 = int(self.ui.lineEdit_m2.text())
				lMask3 = int(self.ui.lineEdit_m3.text())
				lMask4 = int(self.ui.lineEdit_m4.text())
				#print "{0} {1} {2} {3}".format(lMask1, lMask2, lMask3, lMask4)
				UnitLen = self.validateLongMask(lMask1, lMask2, lMask3, lMask4)
				if UnitLen == -1:
					QtGui.QMessageBox.about(self, "Error", "Error in mask format!")
				else:
					if (lMask1 > 255 or lMask2 > 255 or lMask3 > 255 or lMask4 > 255 or
						lMask1 < 0 or lMask2 < 0 or lMask3 < 0 or lMask4 < 0):
						QtGui.QMessageBox.about(self, "Error", "Error in long mask!")
					else:
						m1 = str(self.make8bits(bin(lMask1)))
						m2 = str(self.make8bits(bin(lMask2)))
						m3 = str(self.make8bits(bin(lMask3)))
						m4 = str(self.make8bits(bin(lMask4)))
			#if empty
			else:
				QtGui.QMessageBox.about(self, "Error", "Empty mask!")
			
			if mode == 's' or mode == 'l':
				binIPDot = self.make8bits(bin(s1))+'.'+self.make8bits(str(bin(s2)))+'.'+\
					self.make8bits(str(bin(s3)))+'.'+self.make8bits(str(bin(s4)))
				self.ui.label_binIP.setText(binIPDot)
				self.ui.label_binIP2.setText(binIPDot)
			
				binMaskDot = m1+'.'+m2+'.'+m3+'.'+m4
				self.ui.label_binMask.setText(binMaskDot)
				self.ui.label_binMask2.setText(binMaskDot)
					
				if mode == 's':
					self.ui.lineEdit_m1.setText(str(int(m1, 2)))
					self.ui.lineEdit_m2.setText(str(int(m2, 2)))
					self.ui.lineEdit_m3.setText(str(int(m3, 2)))
					self.ui.lineEdit_m4.setText(str(int(m4, 2)))
				elif mode == 'l':
					if UnitLen >= 0:
						self.ui.lineEdit_s5.setText(str(UnitLen))
					
			#calculations
				#netAddr		
				netAddrStrBin = str(self.make8bits(bin(s1 & int(m1, 2))))+'.'+str(self.make8bits(bin(s2 & int(m2, 2))))+\
					'.'+str(self.make8bits(bin(s3 & int(m3, 2))))+'.'+str(self.make8bits(bin(s4 & int(m4, 2))))
				netAddrStr = str(s1 & int(m1, 2))+'.'+str(s2 & int(m2, 2))+'.'+str(s3 & int(m3, 2))+'.'+\
					str(s4 & int(m4, 2))
				self.ui.label_netAddr.setText(netAddrStrBin)
				self.ui.label_netAddrDec.setText(netAddrStr)
				
				#broadcastAddr
				broadAddrBin = self.make8bits(bin(s1|self.rev(m1)))+\
							'.'+self.make8bits(bin(s2|self.rev(m2)))+\
							'.'+self.make8bits(bin(s3|self.rev(m3)))+\
							'.'+self.make8bits(bin(s4|self.rev(m4)))
				broadAddrDec = str(s1|self.rev(m1))+\
							'.'+str(s2|self.rev(m2))+\
							'.'+str(s3|self.rev(m3))+\
							'.'+str(s4|self.rev(m4))
				self.ui.label_brodAddr.setText(broadAddrBin)
				self.ui.label_brodAddrDec.setText(broadAddrDec)
			
				#nr of addr
				a = 256 - int(m1, 2)
				b = 256 - int(m2, 2)
				c = 256 - int(m3, 2)
				d = 256 - int(m4, 2)
				allAddr = a*b*c*d
				self.ui.label_allAddr.setText(str(allAddr))
				
				#nr of effective addr
				reservedAddr = a*b*c*2
				effectiveAddr = allAddr - reservedAddr
				if effectiveAddr < 0:
					effectiveAddr = 0
				self.ui.label_effAddr.setText(str(effectiveAddr))

				#class
				if ((s1 >= 0 and s1 <= 127) and\
					(s2 >= 0 and s2 <= 255) and\
					(s3 >= 0 and s3 <= 255) and\
					(s4 >= 0 and s4 <=255)):
					self.ui.label_netClass.setText('A')
				elif ((s1 >= 128 and s1 <= 191) and\
					(s2 >= 0 and s2 <= 255) and\
					(s3 >= 0 and s3 <= 255) and\
					(s4 >= 0 and s4 <=255)):
					self.ui.label_netClass.setText('B')
				elif ((s1 >= 192 and s1 <= 223) and\
					(s2 >= 0 and s2 <= 255) and\
					(s3 >= 0 and s3 <= 255) and\
					(s4 >= 0 and s4 <=255)):
					self.ui.label_netClass.setText('C')
				elif ((s1 >= 244 and s1 <= 239) and\
					(s2 >= 0 and s2 <= 255) and\
					(s3 >= 0 and s3 <= 255) and\
					(s4 >= 0 and s4 <=255)):
					self.ui.label_netClass.setText('D')
				else:
					self.ui.label_netClass.setText('not in class')	
	
	def validateLongMask(self, m1, m2, m3, m4):	
		str = self.make8bits(bin(m1)) + self.make8bits(bin(m2)) + self.make8bits(bin(m3)) \
			+ self.make8bits(bin(m4))
		error = 0
		pos = -1
		c = 0
		for i in range(32):
			if str[i] == '0':
				if c == 0 :
					pos = i
				c = pos
				while c < 32:
					if str[c] == '1':
						error = 1
					c = c + 1
		if error == 1:
			return -1
		else:
			return pos			
		
	# input - raw result after unpack
	# output - str with '0' added in front if needed to make 8 bits long
	def make8bits(self, string_val):
		string_val = str(string_val)
		string_val = string_val[2:]
		while len(string_val) < 8:
			string_val = '0' + string_val
		if len(string_val) > 8:
			string_val = string_val[:8]
		return string_val		
	
	# recersing bin str
	def rev(self, string_val):
		rev_str = ''
		for i in string_val:
			if i == '0':
				rev_str += '1'
			else:
				rev_str += '0'
		return int(rev_str, 2)
	
	# ip validation
	def validateFail(self, ip):
		if not ip:
			return 1
		try:
			if (int(ip) > 255 or int(ip) < 0):
				return 1
			else:
				return 0
		except:
			return 1
		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myApp = MyForm()
	myApp.show()
	sys.exit(app.exec_())
