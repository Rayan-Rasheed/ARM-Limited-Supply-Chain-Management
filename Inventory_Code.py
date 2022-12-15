import sys
from Inventory_Supervisor import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QGraphicsDropShadowEffect,QMessageBox
)
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import (QColor)
import re
from Core.Shoe import Shoe
from Core.ProductList import ProducList
from DL.StockOrder_DL import StockOrder_DL
from DL.Inventory import Inventory
from random import randint
from datetime import datetime



class InventoryMainWindow(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        inventory=Inventory()
        inventory.readFromTable()
        self.orderStockDL=StockOrder_DL()
        self.orderStockDL.loadFromTable()
        self.temp_OrderList=[]
        self.total = 0
        #self.prodList=ProducList()

        #self.ShoesDL=Inventory()
        #self.ShoesDL=ProducList(ShoeList, productID)
        self.ui.btnBuyStock.clicked.connect(lambda: self.OpenPages(0))
        self.ui.btn_Update_Stock.clicked.connect(lambda: self.OpenPages(1))
        self.ui.btn_ViewStock.clicked.connect(lambda: self.OpenPages(2))
        self.ui.btn_AddtoCart.clicked.connect(lambda: self.AddToCart_Stock())
        self.ui.btn_RequestOrder.clicked.connect(lambda: self.orderStockFromCart())
        
        
        self.show()
    def orderStockFromCart(self):
        now = datetime.now()
        date = now.strftime("%d-%m-%Y %H:%M:%S")
        order=ProducList(self.orderStockDL.generateOrderID(),date,self.temp_OrderList,0)
        self.orderStockDL.Insert(order)
        self.row_cart.clear()
        self.emptyTableAndList()
        if(len(self.row_cart)==0):
            self.ui.btn_RequestOrder.setEnabled(0)
        else:
            self.ui.btn_RequestOrder.setEnabled(1)
    def emptyTableAndList(self):
        self.ui.Table_BuyCartStock.clearContents()
        self.temp_OrderList.clear()
    def OpenPages(self,idx):
        if(len(self.row_cart)==0):
            self.ui.btn_RequestOrder.setEnabled(0)
        self.ui.btn_CheckIn.setEnabled(0)
        self.ui.mainBody.setCurrentIndex(idx)
        self.table_CheckInLoad()
    def table_CheckInLoad(self):
        if(self.orderStockDL.head.data.getStatus()==1):
            row=0
            DlinkList=self.orderStockDL.getDLinklist()
            while(DlinkList!=None):
                if(DlinkList.data.getStatus()==1):
                    # for prod in DlinkList.data.getShoeList():
                    #     self.ui.table_CheckInStockLoad.setItem(row, 0, QtWidgets.QTableWidgetItem(str(prod.getProductCategory())))
                    #     self.ui.table_CheckInStockLoad.setItem(row, 1, QtWidgets.QTableWidgetItem(str(prod.getColor())))
                    #     self.ui.table_CheckInStockLoad.setItem(row, 2, QtWidgets.QTableWidgetItem(str(prod.getBuyPrice())))
                    #     self.ui.table_CheckInStockLoad.setItem(row, 3, QtWidgets.QTableWidgetItem(str('Received')))
                    #     self.ui.table_CheckInStockLoad.setRowCount(row)
                    self.ui.table_UpdateStock.setItem(row, 0, QtWidgets.QTableWidgetItem(str(DlinkList.data.getOrderID())))
                    self.ui.table_UpdateStock.setItem(row, 1, QtWidgets.QTableWidgetItem(str(DlinkList.data.date)))
                    self.ui.table_UpdateStock.setItem(row, 2, QtWidgets.QTableWidgetItem(str('Received')))
                    row +=1
                        
                DlinkList=DlinkList.next
                
                
    def AddToCart_Stock(self):
        Product_Category=self.ui.cmb_Category.currentText()
        Product_Quantity=self.ui.spb_Quantity.text()
        Product_Size=self.ui.spb_Size.text()
        Product_Color=self.ui.cmb_Color.currentText()
        Product_Price=self.ui.txt_PriceperShoes.text()
        t_price=0
        self.row_cart.append((Product_Category,Product_Quantity,Product_Size,Product_Color,Product_Price,t_price))
        prodID=self.generateProdID()
        self.clearField()
        for i in range(int(Product_Quantity)):
            shoe = Shoe(Product_Category, Product_Price, 0 , Product_Size, 0 , Product_Color, prodID,"men")
            t_price +=int(Product_Price)
            self.temp_OrderList.append(shoe)
        self.loadUpdate_tableWidget(t_price)
        
        QMessageBox.information(self,"ADDED" ,"Product Added")
    def clearField(self):
        self.ui.cmb_Category.clearEditText()
        self.ui.spb_Quantity.cleanText()
        self.ui.spb_Size.cleanText()
        self.ui.cmb_Color.clearEditText()
        self.ui.txt_PriceperShoes.clear()
    def generateProdID(self):
        import random
        return "%0.12d" % random.randint(0,999999999999)

    def loadUpdate_tableWidget(self,t_price):
        row=0
        self.ui.Table_BuyCartStock.setRowCount(len(self.temp_OrderList))
        for prod in self.temp_OrderList:

            self.ui.Table_BuyCartStock.setItem(row, 0, QtWidgets.QTableWidgetItem(str(prod.getprodID())))
            self.ui.Table_BuyCartStock.setItem(row, 1, QtWidgets.QTableWidgetItem(str(prod.getProductCategory())))
            self.ui.Table_BuyCartStock.setItem(row, 2, QtWidgets.QTableWidgetItem(str(prod.getShoeSize())))
            self.ui.Table_BuyCartStock.setItem(row, 3, QtWidgets.QTableWidgetItem(prod.getColor()))
            self.ui.Table_BuyCartStock.setItem(row, 4, QtWidgets.QTableWidgetItem(str(prod.getBuyPrice())))
            row=row+1
    def create_object(self, temp_OrderList):
        order_obj= ProducList(temp_OrderList, "001")
        

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=InventoryMainWindow()
    window.show()
    sys.exit(app.exec_())