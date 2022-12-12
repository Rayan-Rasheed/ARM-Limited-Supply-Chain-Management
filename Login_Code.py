from UI.Login import Ui_LoginWindow
from DL.UserCRUD import *
import sys
#from Stacked_DesignUI1 import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QGraphicsDropShadowEffect,QMessageBox
)
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import (QColor)
#import mysql.connector()
import re  #imported to validate he email
from Manager_UI import ManaMainWindow
#import Manager_UI
import os
from email.message import EmailMessage
import smtplib
from random import randint
class MainWindow(QMainWindow):
    code = 0
    def __init__(self,parent=None):
        QMainWindow.__init__(self)
        self.user=UserCRUD()
        self.user.readFromTable()
        self.ui=Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.forgotbtn.clicked.connect(lambda: self.OpenForgetScreen())
        self.ui.loginbtn.clicked.connect(lambda: self.Handle_Login())
        self.ui.backbtn.clicked.connect(lambda: self.BactTo_Login())
        self.ui.sendbtn.clicked.connect(lambda: self.send_resetmail(self.ui.emailtxt.text() , 6))

        self.show()
    
    
        
    def Handle_Login(self):
        
        Email=self.ui.emailinp.text()
        Password=self.ui.passwordinp.text()
        flag=self.Validate_Email(Email,Password)
        if(flag):
            retrive=self.user.verify(Email,Password)
            print(retrive.userRole)
            
            if(retrive!=None):
                if(retrive.userRole==0):
                    self.Open_Manager_Window()
        else:
            QMessageBox.warning(self,'Error','Incorrect Email and Password')
            self.ui.emailinp.clear()
            self.ui.passwordinp.clear()
            
    def Validate_Email(self,Email,password):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex,Email)):
            if(len(password)>8):
                return True  
        else:   
            return False 
    def send_resetmail(self , email , n) :
        start = 10**(n-1)
        end = (10**n)-1
        code = randint(start,end)
        email_sender = "rasheedrayan514@gmail.com"
        email_password = 'zpzsrqeasritevbu'
        email_receiver = email

        subject = "Forget Password"
        body = '''
        Dear User,
        Your new password of the account is '''+str(code)+'''Enter this now to have access to your account.
        Regards,
        ARM limited
        '''
        em = EmailMessage()
        em['from'] = email_sender
        em['to'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        with smtplib.SMTP_SSL('smtp.gmail.com' , 465 ) as smtp:
            smtp.login(email_sender , email_password)
            smtp.sendmail(email_sender , email_receiver , em.as_string())
        self.Open_newpassword_Screen()
    #def create_newpassword(password) :


    def Open_Manager_Window(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui=ManaMainWindow()
        #self.ui.setupUi(self.MainWindow)
        #self.MainWindow.show()
        
       

    def OpenForgetScreen(self):
        self.ui.loginStackedWidget.setCurrentIndex(1)
    def Open_newpassword_Screen(self):
        self.ui.loginStackedWidget.setCurrentIndex(2)
    def BactTo_Login(self):
        self.ui.loginStackedWidget.setCurrentIndex(0)
        
    
if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())