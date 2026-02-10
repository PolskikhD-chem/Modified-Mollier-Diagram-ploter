# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 13:27:05 2023

@author: Студент
"""
import numpy as np
#import os
import sys
from PyQt5 import uic, QtCore #, QtGui#
from PyQt5.QtWidgets import QMainWindow, QApplication #,  QFileDialog#, QWidget, QTreeWidget, QTreeWidgetItem
#from PyQt5.QtGui import QPixmap, QIcon

#from scipy.interpolate import Akima1DInterpolator as inter
#from scipy.optimize import curve_fit as fit
#from sklearn.metrics import r2_score
import pyqtgraph as pg        
pg.setConfigOption('background', '#D0D0D0')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)
#import matplotlib.pyplot as plt


# Основные настройки


         
class MainWindow(QMainWindow):
   def __init__(self):
      super(MainWindow, self).__init__()
      uic.loadUi('modified_Mollier_diagram.ui', self)
      self.setupUi()
      
      
   def setupUi(self):
        self.MaxMV = float(self.MaxM.toPlainText())
        self.MinMV = float(self.MinM.toPlainText())
        self.MaxTV = float(self.MaxT.toPlainText())
        self.MinTV = float(self.MinT.toPlainText())
        self.FMatrAppend = []

        self.MainPlotWid.getAxis('left').setLabel("<b>Temperature / °C</b>",color='#000000', **{'font-size': '16pt'}) #<span style=font-family: Arial;> </span>
        self.MainPlotWid.getAxis('bottom').setLabel("<b>Moisture content, g(H<sub>2</sub>O)/ kg(dry air)</b>",color='#000000', **{'font-size': '16pt'})
        self.MainPlotWid.showGrid(x=True,y=True)
        #self.MainPlotWid.addLegend(pen = "#808080", brush = "#F0F0F0")
        #self.MainPlotWid.plot([0,0],[0,0], pen = '#000096', name = '<b>Polanyi potential isoline</b>')
        
        self.setDefaultButtons()
        self.colors = ["#FF0000","#800080","#FF4500","#D2691E","#483D8B","#32CD32","#000080","#8B0000","#C71585","#FFA500","#808000","#FF00FF","#2E8B57","#0000FF",
                  "#DC143C","#FF69B4","#FF7F50","#FFD700","#8A2BE2","#008000","#4682B4","#556B2F","#5F9EA0","#008B8B", '#2F4F4F' ]
        self.PlotMainWid()


       
        
   def setDefaultButtons(self):
        """Moisture content range"""
        self.MaxM_p10.clicked.connect(self.MaxM_p10Func)
        self.MaxM_p1.clicked.connect(self.MaxM_p1Func)
        self.MaxM_m10.clicked.connect(self.MaxM_m10Func)
        self.MaxM_m1.clicked.connect(self.MaxM_m1Func)
        self.MinM_p10.clicked.connect(self.MinM_p10Func)
        self.MinM_p1.clicked.connect(self.MinM_p1Func)
        self.MinM_m10.clicked.connect(self.MinM_m10Func)
        self.MinM_m1.clicked.connect(self.MinM_m1Func)
        
        """Temperature range"""
        self.MaxT_p10.clicked.connect(self.MaxT_p10Func)
        self.MaxT_p1.clicked.connect(self.MaxT_p1Func)
        self.MaxT_m10.clicked.connect(self.MaxT_m10Func)
        self.MaxT_m1.clicked.connect(self.MaxT_m1Func)
        self.MinT_p10.clicked.connect(self.MinT_p10Func)
        self.MinT_p1.clicked.connect(self.MinT_p1Func)
        self.MinT_m10.clicked.connect(self.MinT_m10Func)
        self.MinT_m1.clicked.connect(self.MinT_m1Func)
        
        self.Rescale.clicked.connect(self.PlotMainWid)
        self.Clear.clicked.connect(self.ClearF)
        #self.checkBox.checkStateChanged(self.PlotMainWid)
       
   def PlotMainWid(self):
       self.MainPlotWid.clear()
       self.checkRange()
       a = self.MinMV
       if self.MinMV<0:   
           self.MinMV = 0
       minF = dF(self.MinTV+(self.MaxTV-self.MinTV)*0.2 + 273.15,self.MaxMV)    
       maxF = dF(self.MaxTV+273.15,self.MinMV+(self.MaxMV-self.MinMV)*0.2)
       if minF<0: self.FMatr = np.round(np.linspace(0,dF(self.MaxTV+273.15,self.MinMV+(self.MaxMV-self.MinMV)*0.2),12))
       else:  self.FMatr = np.round(np.linspace(minF,maxF,11))
       
       #print(self.FMatr)
       for F in self.FMatr:
           #print(F)
           T = np.linspace(self.MinTV,self.MaxTV, num = int(self.MaxTV - self.MinTV + 1)*10)
           #print(np.shape(T), int(self.MaxTV - self.MinTV + 1), self.MaxTV - self.MinTV + 1)
           x = X(P0(T+273.15)*PvVP0(np.zeros(np.shape(T))+F*1000,T+273.15))
           #print(self.MaxMV,self.MinMV,self.MaxTV,self.MinTV)
           mask = ~((x > self.MaxMV) | (x < self.MinMV) | (T > self.MaxTV) | (T < self.MinTV) | (T < -273.15))
           xp = x[mask]
           Tp = T[mask]
           #self.MainPlotWid.addLegend(pen = "#808080", brush = "#F0F0F0")
           #self.MainPlotWid.setTitle("<b></b>")
           self.MainPlotWid.plot(xp,Tp, pen = "#000096")#, name = "<b></b>")
           
           text = pg.TextItem(html=('<div style="text-align: center; color: #000096; font-size: 10pt;"><b> %.f </b></div>' % F), color='#000096', anchor=(0, 1))
           text.setPos(max(xp), max(Tp))  # Устанавливаем позицию в координатах данных
           self.MainPlotWid.addItem(text)
       for F in self.FMatrAppend:
         if F>minF:  #print(F)
           T = np.linspace(self.MinTV,self.MaxTV, num = int(self.MaxTV - self.MinTV + 1)*10)
           #print(np.shape(T), int(self.MaxTV - self.MinTV + 1), self.MaxTV - self.MinTV + 1)
           x = X(P0(T+273.15)*PvVP0(np.zeros(np.shape(T))+F*1000,T+273.15))
           #print(self.MaxMV,self.MinMV,self.MaxTV,self.MinTV)
           mask = ~((x > self.MaxMV) | (x < self.MinMV) | (T > self.MaxTV) | (T < self.MinTV) | (T < -273.15))
           xp = x[mask]
           Tp = T[mask]
           #self.MainPlotWid.addLegend(pen = "#808080", brush = "#F0F0F0")
           #self.MainPlotWid.setTitle("<b></b>")
           self.MainPlotWid.plot(xp,Tp, pen = "#000096")#, name = "<b></b>")
           text = pg.TextItem(html=('<div style="text-align: center; color: #000096; font-size: 10pt;"><b> %.3f </b></div>' % F), color='#000096', anchor=(0, 1))
           text.setPos(max(xp), max(Tp))  # Устанавливаем позицию в координатах данных
           self.MainPlotWid.addItem(text)    
           
       #print(self.MaxMV,self.MinMV,self.MaxTV,self.MinTV)

       maxRH = RH(self.MaxMV, self.MinTV+(self.MaxTV-self.MinTV)*0.2 + 273.15)    
       minRH = RH(self.MinMV+(self.MaxMV-self.MinMV)*0.2, self.MaxTV+273.15)
       if maxRH>100: self.RHMatr = np.hstack([np.round(np.linspace(min(minRH*5,20),100,4)),np.round(np.linspace(minRH,min(minRH*4,20),4))])
       else:  self.RHMatr = np.hstack([np.round(np.linspace(min(minRH*10,maxRH/2),maxRH,4)),np.round(np.linspace(minRH,min(minRH*5,maxRH/3),4))])
       print(minRH,self.RHMatr)
       for rh in self.RHMatr:
          if self.checkBox.checkState(): 
           T = np.linspace(self.MinTV,self.MaxTV, num = int(self.MaxTV - self.MinTV + 1)*10)
           #print(np.shape(T), int(self.MaxTV - self.MinTV + 1), self.MaxTV - self.MinTV + 1)
           P0D = P0(T+273.15)
           print(P0(T+273.15))
           x = X((np.zeros(np.shape(T))+rh/100)*P0D)
           print(x)
           #print(self.MaxMV,self.MinMV,self.MaxTV,self.MinTV)
           mask = ~((x > self.MaxMV) | (x < self.MinMV) | (T > self.MaxTV) | (T < self.MinTV) | (T < -273.15))
           xp = x[mask]
           Tp = T[mask]
           #self.MainPlotWid.addLegend(pen = "#808080", brush = "#F0F0F0")
           #self.MainPlotWid.setTitle("<b></b>")
           self.MainPlotWid.plot(xp,Tp, pen = "#009600")#, name = "<b></b>")
           text = pg.TextItem(html=('<div style="text-align: center; color: #009600; font-size: 10pt;"><b> %.0f</b></div>' % rh), color='#009600', anchor=(1, 1))
           text.setPos(max(xp), max(Tp))  # Устанавливаем позицию в координатах данных
           self.MainPlotWid.addItem(text)  
       
       viewbox = self.MainPlotWid.getViewBox()
       DX = self.MaxMV-self.MinMV
       DY = self.MaxTV-self.MinTV  

       viewbox.setLimits(
    xMin=self.MinMV-DX*0.1,     # Минимальная граница по X
    xMax=self.MaxMV+DX*0.1,    # Максимальная граница по X  
    yMin=self.MinTV-DY*0.1,    # Минимальная граница по Y
    yMax=self.MaxTV+DY*0.1)     # Максимальная граница по Y
    
    # Минимальный диапазон (самое важное!)
  #  minXRange=1.0,  # Минимальная ширина видимой области по X
  #  minYRange=0.5,  # Минимальная высота видимой области по Y
  #  maxXRange=20,   # Максимальная ширина
  #  maxYRange=20    # Максимальная высота

       self.MinMV = a 
       self.MainPlotWid.setXRange(self.MinMV,self.MaxMV*1.1,padding = 0.05) 
       self.MainPlotWid.setYRange(self.MinTV,self.MaxTV,padding = 0.05)       
       
       #print(self.MaxTV)
       #print((self.MaxMV-self.MinMV)/10)
       #print(dF(self.MaxTV+273.15,(self.MaxMV-self.MinMV)/10))
       
          
   def ClearF(self):
       self.FMatrAppend = []
       self.PlotMainWid()
       
   def checkRange(self):
       try:
           self.MaxMV = float(self.MaxM.toPlainText())
       except: self.MaxM.setText(str(self.MaxMV))
       try:
           self.MinMV = float(self.MinM.toPlainText())
       except: self.MinM.setText(str(self.MinMV))
       try:
           self.MaxTV = float(self.MaxT.toPlainText())
       except: self.MaxT.setText(str(self.MaxTV))
       try:
           self.MinTV = float(self.MinT.toPlainText())
       except: self.MinT.setText(str(self.MinTV))
       if self.MaxMV <= self.MinMV:
          self.MaxMV = self.MinMV+10
          self.MaxM.setText(str(self.MaxMV))
          self.MinMV = float(self.MinM.toPlainText())
       if self.MaxTV <= self.MinTV:
          self.MaxTV = self.MinTV+10
          self.MinT.setText(str(self.MinTV))
          self.MaxT.setText(str(self.MaxTV))
   
    
   def mousePressEvent(self, event):
        """Обработка нажатия кнопок мыши"""
        viewbox = self.MainPlotWid.getViewBox()
        pos = event.pos()
        scene_pos = viewbox.mapSceneToView(pos)
        button = event.button()
        #print(scene_pos)
        a = scene_pos.x()
        b = scene_pos.y()
        Mtext = ('<div style="text-align: center; font-size: 14pt;"><b> %.3f </b></div>' % a)# color: #FFFFFF;
        Ttext = ('<div style="text-align: center; font-size: 14pt;"><b> %.3f </b></div>' % b) #color: #FFFFFF;
        Ftext = ('<div style="text-align: center; font-size: 14pt;"><b> %.3f </b></div>' % dF(b+273.15,a))
        RHtext = ('<div style="text-align: center; font-size: 14pt;"><b> %.3f </b></div>' % RH(a,b+273.15))
        #print(Mtext, Ttext, Ftext)
        if button == QtCore.Qt.LeftButton:                
            self.ClickM.setText(Mtext)
            self.ClickT.setText(Ttext)
            self.ClickF.setText(Ftext)
            self.ClickRH.setText(RHtext)

        
   def mouseDoubleClickEvent(self, event):
        """Обработка двойного клика"""
        viewbox = self.MainPlotWid.getViewBox()
        pos = event.pos()
        scene_pos = viewbox.mapSceneToView(pos)
        button = event.button()
        print(scene_pos)

        # Получаем координаты по осям графика
        a = scene_pos.x()
        b = scene_pos.y()
        button = event.button()

        print(a, str(round(a)), b)
        if button == QtCore.Qt.LeftButton:
            T = np.linspace(self.MinTV,self.MaxTV, num = int(self.MaxTV - self.MinTV + 1)*10)    
            F = dF(b+273.15,a)
            self.FMatrAppend.append(F)
            x = X(P0(T+273.15)*PvVP0(np.zeros(np.shape(T))+F*1000,T+273.15))
            #print(self.MaxMV,self.MinMV,self.MaxTV,self.MinTV)
            mask = ~((x > self.MaxMV) | (x < self.MinMV) | (T > self.MaxTV) | (T < self.MinTV) | (T < -273.15))
            xp = x[mask]
            Tp = T[mask]
            #self.MainPlotWid.addLegend(pen = "#808080", brush = "#F0F0F0")
            #self.MainPlotWid.setTitle("<b></b>")
            self.MainPlotWid.plot(xp,Tp, pen = "#000096")#, name = "<b></b>")
            text = pg.TextItem(html=('<div style="text-align: center; color: #000096; font-size: 10pt;"><b> %.3f </b></div>' % F), color='b', anchor=(0, 1))
            text.setPos(max(xp), max(Tp))  # Устанавливаем позицию в координатах данных
            self.MainPlotWid.addItem(text)
            
   def MaxM_p10Func(self):
       try:
           self.MaxMV = float(self.MaxM.toPlainText())
           self.MaxMV+=10
           self.MaxM.setText(str(self.MaxMV))
       except: self.MaxMV+=10;self.MaxM.setText(str(self.MaxMV))
       self.PlotMainWid()       
   def MaxM_p1Func(self):
       try:
           self.MaxMV = float(self.MaxM.toPlainText())
           self.MaxMV+=1
           self.MaxM.setText(str(self.MaxMV))
       except: self.MaxMV+=1;self.MaxM.setText(str(self.MaxMV))
       self.PlotMainWid() 
   def MaxM_m10Func(self):
       try:
           self.MaxMV = float(self.MaxM.toPlainText())
           self.MaxMV-=10
           self.MaxM.setText(str(self.MaxMV))
       except: self.MaxMV-=10;self.MaxM.setText(str(self.MaxMV))
       self.PlotMainWid()
   def MaxM_m1Func(self):
       try:
           self.MaxMV = float(self.MaxM.toPlainText())
           self.MaxMV-=1
           self.MaxM.setText(str(self.MaxMV))
       except: self.MaxMV-=1;self.MaxM.setText(str(self.MaxMV))
       self.PlotMainWid()
       
   def MinM_p10Func(self):
       try:
           self.MinMV = float(self.MinM.toPlainText())
           self.MinMV+=10
           self.MinM.setText(str(self.MinMV))
       except: self.MinMV+=10;self.MinM.setText(str(self.MinMV))
       self.PlotMainWid()      
   def MinM_p1Func(self):
       try:
           self.MinMV = float(self.MinM.toPlainText())
           self.MinMV+=1
           self.MinM.setText(str(self.MinMV))
       except: self.MinMV+=1;self.MinM.setText(str(self.MinMV))
       self.PlotMainWid()    
   def MinM_m10Func(self):
       try:
           self.MinMV = float(self.MinM.toPlainText())
           self.MinMV-=10
           self.MinM.setText(str(self.MinMV))
       except: self.MinMV-=10;self.MinM.setText(str(self.MinMV))
       self.PlotMainWid() 
   def MinM_m1Func(self):
       try:
           self.MinMV = float(self.MinM.toPlainText())
           self.MinMV-=1
           self.MinM.setText(str(self.MinMV))
       except: self.MinMV-=1;self.MinM.setText(str(self.MinMV))
       self.PlotMainWid()
           
   def MaxT_p10Func(self):
       try:
           self.MaxTV = float(self.MaxT.toPlainText())
           self.MaxTV+=10
           self.MaxT.setText(str(self.MaxTV))
       except: self.MaxTV+=10;self.MaxT.setText(str(self.MaxTV))
       self.PlotMainWid()       
   def MaxT_p1Func(self):
       try:
           self.MaxTV = float(self.MaxT.toPlainText())
           self.MaxTV+=1
           self.MaxT.setText(str(self.MaxTV))
       except: self.MaxTV+=1;self.MaxT.setText(str(self.MaxTV))
       self.PlotMainWid() 
   def MaxT_m10Func(self):
       try:
           self.MaxTV = float(self.MaxT.toPlainText())
           self.MaxTV-=10
           self.MaxT.setText(str(self.MaxTV))
       except: self.MaxTV-=10;self.MaxT.setText(str(self.MaxTV))
       self.PlotMainWid()
   def MaxT_m1Func(self):
       try:
           self.MaxTV = float(self.MaxT.toPlainText())
           self.MaxTV-=1
           self.MaxT.setText(str(self.MaxTV))
       except: self.MaxTV-=1;self.MaxT.setText(str(self.MaxTV))
       self.PlotMainWid()
       
   def MinT_p10Func(self):
       try:
           self.MinTV = float(self.MinT.toPlainText())
           self.MinTV+=10
           self.MinT.setText(str(self.MinTV))
       except: self.MinTV+=10;self.MinT.setText(str(self.MinTV))
       self.PlotMainWid()      
   def MinT_p1Func(self):
       try:
           self.MinTV = float(self.MinT.toPlainText())
           self.MinTV+=1
           self.MinT.setText(str(self.MinTV))
       except: self.MinTV+=1;self.MinT.setText(str(self.MinTV))
       self.PlotMainWid()    
   def MinT_m10Func(self):
       try:
           self.MinTV = float(self.MinT.toPlainText())
           self.MinTV-=10
           self.MinT.setText(str(self.MinTV))
       except: self.MinTV-=10;self.MinT.setText(str(self.MinTV))
       self.PlotMainWid() 
   def MinT_m1Func(self):
       try:
           self.MinTV = float(self.MinT.toPlainText())
           self.MinTV-=1
           self.MinT.setText(str(self.MinTV))
       except: self.MinTV-=1;self.MinT.setText(str(self.MinTV))
       self.PlotMainWid()
         

def P0(T):
    return(np.exp(-40700/8.314*(1/T-1/373.15)))

def PvVP0(F,T):
    return(np.exp(F/(-8.314*T)))
def X(Pv):
    return(622*Pv/(1-Pv))
def Pv(x):
    return(x/(x+622))
def RH(x,t):
    return(Pv(x)/P0(t)*100)
def dF(T,X):
    return(-8.314*T*np.log(Pv(X)/P0(T))/1000)
       
   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())  
    a = np.linespace(0,100,1)