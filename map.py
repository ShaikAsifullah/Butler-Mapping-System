'''
Created on 29-Aug-2014

@author: Kashaj
'''
try:
    from PyQt4 import Qt, QtCore, QtGui
    import json
    import os
    import re
    import requests
    import sys
    

except:
    print("Make Sure you have PyQt4, requests libraries\n If not, install now using sudo apt-get and then rerun.. :)")
    quit()

STOP = 0
class CreateNewMap(object):
    def __init__(self,t):
        self.startx = int(t[0][0])
        self.endx = int(t[1][0])
        self.starty = int(t[0][1])
        self.endy = int(t[1][1])
        self.minx = min(self.startx,self.endx)
        self.maxx = max(self.startx,self.endx)
        self.miny = min(self.starty,self.endy)
        self.maxy = max(self.starty,self.endy)
        self.start()
        
    def create_barcode(self,y,x):
        stry = str(y)
        strx = str(x)
        if(len(stry)<3):
            while(len(stry) != 3):
                stry = "0"+stry
        if(len(strx)<3):
            while(len(strx) != 3):
                strx = "0"+strx
        barcode = stry+"."+strx
        return barcode
    
    def give_neighbours(self,y,x):
        lis = []
        if(y == self.miny):
            NORTH = [0,1,1]
            
        else:
            NORTH = [1,1,1]
        
        if(y == self.maxy):
            SOUTH = [0,1,1]
        else:
            SOUTH = [1,1,1]
        
        if(x == self.minx):
            WEST = [0,1,1]
        else:
            WEST = [1,1,1]
        
        if(y == self.maxx):
            EAST = [0,1,1]
        else:
            EAST = [1,1,1]
        lis.append(NORTH)
        lis.append(EAST)
        lis.append(SOUTH)
        lis.append(WEST)
        return lis

    def give_coordinate(self,y,x):
        retstr = "["
        retstr = retstr + str(x)+","+str(y)+"]"
        return retstr
    
    def get_storestatus(self):
        return(1)
    
    def get_sizeinfo(self):
        a = [1,1,1,1]
        return(a)
    
    def start(self):
        self.created_list = []
        for i in range(self.minx,(self.maxx+1)):
            for j in range(self.miny,(self.maxy+1)):
                dicty = {}
                dicty['coordinate'] = self.give_coordinate(j,i)
                dicty['store_status'] = self.get_storestatus()
                dicty['neighbours'] = self.give_neighbours(j, i)
                dicty['barcode'] = self.create_barcode(j, i)
                dicty['size_info'] = self.get_sizeinfo()
                self.created_list.append(dicty)
        
            
    
    
  
    
CSVONCE = 1    
class Info(object):
    neighbours = []

    def __init__(self, given_dict):
        try:
            self.barcode_name = given_dict['barcode']
            self.coordinates = given_dict['coordinate']
            self.neighbours = given_dict['neighbours']
            self.store_status = given_dict['store_status']
            #self.size_info = given_dict['size_info']
        except Exception:
            print(Exception.message)

    def get_barcode(self):
        return (self.barcode_name)

    def get_coordinates(self):
        return (self.coordinates)

    def set_neighbours(self, nbr):
        self.neighbours = nbr

    def get_neighbours(self):
        return self.neighbours

    def get_store_status(self):
        return (self.store_status)

    def get_size_info(self):
        return (self.size_info)

    def set_image(self, Img,xdiff,ydiff,running):
        global SHOWRACK
        global SHOWNORACK
        if(SHOWRACK == 1):
            neibur = self.get_neighbours()
            DIR_neibur = []
            for t in range(4):
                DIR_neibur.append(int(neibur[t][1]))
            self.Image = make_object(Img,self.barcode_name,xdiff,ydiff,running,DIR_neibur[0],DIR_neibur[1],DIR_neibur[2],DIR_neibur[3])
        elif(SHOWNORACK == 1):
            neibur = self.get_neighbours()
            DIR_neibur = []
            for t in range(4):
                DIR_neibur.append(int(neibur[t][2]))
            self.Image = make_object(Img,self.barcode_name,xdiff,ydiff,running,DIR_neibur[0],DIR_neibur[1],DIR_neibur[2],DIR_neibur[3])
        else:
            self.Image = make_object(Img,self.barcode_name,xdiff,ydiff,running)

    def get_image(self):
        return self.Image

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return (self.x)

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return (self.y)
 

class CSV(object):
    ret_lst = []

    def __init__(self, file_name,already_list = 0):
        
        self.file_name = file_name
        self.alre = already_list

    description = "This gives minimum and maximum x & y's"

    def get_list(self, strng):
        lis = re.findall(r'\[(-?\d+)\,(-?\d+)\]', strng)
        lst = []
        for elem in lis:
            for ele in elem:
                lst.append(int(ele))
        return (lst)

    def get_max(self):
        if(self.alre == 0):
            if(self.file_name == ""):
                global FILENAME
                self.file_name = FILENAME
            
            try:
                lfst = open(self.file_name,'r')
                why = 0
            except:
                print("Loading Wait!!!")
            lst = json.load(lfst)
            lfst.close()
        else:
            lst = self.file_name
        max_x = min_y = min_x = max_y = 0
        for i in range(0, len(lst)):
            strng = lst[i]['coordinate']
            lis = re.findall(r'\[(-?\d+)\,(-?\d+)\]', strng)
            ###
            co_lst = []

            for elem in lis:
                for ele in elem:

                    co_lst.append(int(ele))

            if (i == 0):
                min_x = max_x = co_lst[0]
                min_y = max_y = co_lst[1]

            else:
                if (min_x > co_lst[0]):
                    min_x = co_lst[0]
                if (max_x < co_lst[0]):
                    max_x = co_lst[0]
                if (min_y > co_lst[1]):
                    min_y = co_lst[1]
                if (max_y < co_lst[1]):
                    max_y = co_lst[1]

        CSV.ret_lst.append(min_x)
        CSV.ret_lst.append(max_x)
        CSV.ret_lst.append(min_y)
        CSV.ret_lst.append(max_y)
        
        return CSV.ret_lst


save_list = []
two = 0 
selected = []  
thispos = (-22240,-22240) 
ctrlprsd = 0
points = []
shftprsd = 0
MAXX = [0,0]
class make_object(object):
    
    def __init__(self,qp,barcode,xdiff,ydiff,running,north=0,east=0,south=0,west=0):
        self.text = barcode
        self.make_now(qp,xdiff,ydiff,running,north,east,south,west)
    
    def make_now(self,qp,xdiff,ydiff,running,north,east,south,west):
        global chng_y
        global chng_x
        global zoom
        global thispos
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)
        tx = int((20+(xdiff*80)+chng_x)*zoom)
        ty = int((45+(ydiff*80)+chng_y)*zoom)
        if(MAXX[0]<tx):
            MAXX[0] = tx
        if(MAXX[1]<ty):
            MAXX[1]= ty
        if(running == 1):
            qp.setBrush(QtGui.QColor(255, 0, 0, 200))
        
        else:
            qp.setBrush(QtGui.QColor(25, 0, 90, 200))
        
        qp.drawRect(tx,ty,int( 75*zoom), int(75*zoom))
        qp.setPen(QtGui.QColor(255,255,255))
        qp.setFont(QtGui.QFont('Decorative', int(10*zoom)))
        qp.drawText(tx,ty, int(75*zoom), int(75*zoom),QtCore.Qt.AlignCenter, self.text)
        
        if(east == 1):
            ####EAST#########        
            qp.drawLine((tx+int(65*zoom)),(ty+int(38*zoom)),(tx+int(73*zoom)),(ty+int(38*zoom)))
            qp.drawLine((tx+int(69*zoom)),(ty+int(34*zoom)),(tx+int(73*zoom)),(ty+int(38*zoom)))
            qp.drawLine((tx+int(69*zoom)),(ty+int(42*zoom)),(tx+int(73*zoom)),(ty+int(38*zoom)))
        
        if(west == 1):
            ###WEST##########
            qp.drawLine((tx+int(0*zoom)),(ty+int(38*zoom)),(tx+int(10*zoom)),(ty+int(38*zoom)))
            qp.drawLine((tx+int(4*zoom)),(ty+int(34*zoom)),(tx+int(0*zoom)),(ty+int(38*zoom)))
            qp.drawLine((tx+int(4*zoom)),(ty+int(42*zoom)),(tx+int(0*zoom)),(ty+int(38*zoom)))
        
        if(north == 1):
            ###NORTH##########
            qp.drawLine((tx+int(36*zoom)),(ty+int(0*zoom)),(tx+int(36*zoom)),(ty+int(10*zoom)))
            qp.drawLine((tx+int(32*zoom)),(ty+int(4*zoom)),(tx+int(36*zoom)),(ty+int(0*zoom)))
            qp.drawLine((tx+int(40*zoom)),(ty+int(4*zoom)),(tx+int(36*zoom)),(ty+int(0*zoom)))
        
        if(south == 1):
            ###SOUTH##########
            qp.drawLine((tx+int(36*zoom)),(ty+int(65*zoom)),(tx+int(36*zoom)),(ty+int(75*zoom)))
            qp.drawLine((tx+int(32*zoom)),(ty+int(71*zoom)),(tx+int(36*zoom)),(ty+int(75*zoom)))
            qp.drawLine((tx+int(40*zoom)),(ty+int(71*zoom)),(tx+int(36*zoom)),(ty+int(75*zoom)))
       
#To Drag And Drop
class TestListView(QtGui.QListWidget):
    def __init__(self, type, parent=None):
        super(TestListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(72, 72))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()

        
#Global Variables
FILENAME = ""
DRAGNDROP = 0
BARCODESLIST = []
xydata = 0
chng_x = 0
chng_y = 0
zoom = 1
selec = []
running = 0
SHOWRACK = 0
SHOWNORACK = 0
selected_imgs = []
lst = None
ekbaar = 1
undo_list = []
prevpos = (-22900,-22900)
newpos = (-22900,-22900)
shiftact = 0
mappos = {}
selAll = 0
ARROWTOGGLE = 0
newp = 0
SAVEFILE = "updatedFile.csv"


class Map(QtGui.QMainWindow):
    
    def __init__(self,parentQExampleScrollArea=None,parentQWidget = None):
        super(Map,self).__init__()
        self.parentQExampleScrollArea = parentQExampleScrollArea
        self.selnew = 0
        self.w = None
        
        self.initUI()
       
        
    
    #Initialize the UI
    def initUI(self):
        
        #TEXT FOR DRAG N DROP
        self.text = '0001.0001'
        self.once = 0
        self.position = (20,45)
        #Generate a new Map
        createMap = QtGui.QAction(QtGui.QIcon('Create.png'),'&Create Map', self)
        createMap.setShortcut('Ctrl+N')
        createMap.setStatusTip('This Creates a New Map')
        createMap.triggered.connect(self.create_new)
        
        #To open from a file browser
        openFile = QtGui.QAction(QtGui.QIcon(''), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)
        
        #Drop open
        openDrop = QtGui.QAction(QtGui.QIcon(''), 'Open Drop', self)
        openDrop.setShortcut('Ctrl+.')
        openDrop.setStatusTip('Open new File Using Drop')
        openDrop.triggered.connect(self.dropAction)
        
        
        #To Save currentfile
        saveFile = QtGui.QAction(QtGui.QIcon(''), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Saves the File')
        saveFile.triggered.connect(self.saveFun)
        
        #To save as currentFile
        saveas = QtGui.QAction(QtGui.QIcon(''), 'Save As', self)
        saveas.setShortcut('Ctrl+Shift+S')
        saveas.setStatusTip('Saves the File')
        saveas.triggered.connect(self.showDialog1)
        
        #From the Server
        fromserver = QtGui.QAction(QtGui.QIcon(''), 'From Server', self)
        fromserver.setShortcut('Ctrl+Alt+O')
        fromserver.setStatusTip('From the server')
        fromserver.triggered.connect(self.browserFun)
        
        toserver = QtGui.QAction(QtGui.QIcon(''), 'Upload to Server', self)
        toserver.setShortcut('Ctrl+Alt+P')
        toserver.setStatusTip('Upload to Server')
        toserver.triggered.connect(self.tobrowserFun)
        
        
        
        ###InitializeN Edit Menu#######
        selectAll = QtGui.QAction(QtGui.QIcon(''), 'Select All', self)
        selectAll.setShortcut('Ctrl+A')
        selectAll.setStatusTip('Selects all the blocks')
        selectAll.triggered.connect(self.allFun)
        
        #Exist Button
        exists = QtGui.QAction(QtGui.QIcon(''), '', self) 
        exists.setIconText("Exists")        
        exists.setShortcut('Ctrl+E')
        exists.setStatusTip('Exist Status')
        exists.triggered.connect(self.ExistFun)
        
        
        #WithRack Button
        with_rack = QtGui.QAction(QtGui.QIcon(''), '', self)        
        with_rack.setText("With Rack")        
        #with_rack.setIconText("With Rack")        
        with_rack.setShortcut('Ctrl+R')
        with_rack.setStatusTip('With Rack Status')
        with_rack.triggered.connect(self.WithRackFun)
        
        #WithoutRack Button
        without_rack = QtGui.QAction(QtGui.QIcon(''), '', self)    
        without_rack.setIconText("Without Rack")        
        without_rack.setShortcut('Ctrl+T')
        without_rack.setStatusTip('Without Rack Status')
        without_rack.triggered.connect(self.WithoutRackFun)
        
        #Default Button
        default = QtGui.QAction(QtGui.QIcon(''), '', self) 
        default.setIconText("Default")        
        default.setShortcut('Ctrl+/')
        default.setStatusTip('Make this original')
        default.triggered.connect(self.defaultFun)
        
        #Delete Button
        delete = QtGui.QAction(QtGui.QIcon(''), '', self) 
        delete.setIconText("Delete")        
        delete.setShortcut('Delete')
        delete.setStatusTip('Delete this Item/Items')
        delete.triggered.connect(self.deleteFun)
        
        #Undo Button
        undo = QtGui.QAction(QtGui.QIcon(''), '', self) 
        undo.setIconText("Undo")        
        undo.setShortcut('Ctrl+Z')
        undo.setStatusTip('Undo Item/Items')
        undo.triggered.connect(self.undoFun)
      
        # To Exit
        exitAction = QtGui.QAction(QtGui.QIcon(''), '', self)        
        exitAction.setIconText("Quit")        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        ###END OF ACTIONS############################################################
        
        ##############START THE MENU AND TOOL BARS#########################################
        #set status to Ready when it is Ready
        self.statusBar().showMessage('Ready')
        
        #Adding Menu Bar
        menubar = self.menuBar()
        
        #File Menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(createMap)
        fileMenu.addAction(openFile)
        fileMenu.addAction(openDrop)
        fileMenu.addAction(fromserver)
        fileMenu.addAction(toserver)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(saveas)
        fileMenu.addAction(exitAction)
        
        
        #Edit Menu
        editMenu = menubar.addMenu("&Edit")
        editMenu.addAction(selectAll)
        
        
        
        
        #Tool Bar
        self.toolbar = self.addToolBar('Action Tool Bar')
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        
        self.toolbar.addAction(exists)
        self.toolbar.addAction(with_rack)
        self.toolbar.addAction(without_rack)
        self.toolbar.addAction(default)
        self.toolbar.addAction(delete)
        self.toolbar.addAction(undo)
        self.toolbar.addAction(exitAction)
        
        
        
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)    
        
        #Sizing and positioning the windows
        self.resize(1000, 500)
        self.center()
        self.setWindowTitle('Butler Mapping System')
        self.setWindowIcon(QtGui.QIcon('Grey Orange Logo.png'))    
        self.show()
      
   
    
    #To Display at the center of the Screem
   
    def center(self):        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    
    #To show message box at the time of Quit
    def closeEvent(self, event):        
        reply = QtGui.QMessageBox.question(self, 'Message',
            "This is built with great effort in Pygame and PyQt\nAre you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
            
    #To Show open File Dialog Box
    def showDialog(self,saveas="Good"):
        print(saveas)
        if(saveas):
            print("In save as!!!")
            fileName = QtGui.QFileDialog.getSaveFileName(self,'Save file','/')
            if fileName:
                self.saveFun(fileName)
                self.repaint()
                return
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/')
        global FILENAME
        if fname:
            FILENAME = fname
        print("Finally")    
   
    def showDialog1(self):
        
        global STOP
        STOP = 1
        fileName = QtGui.QFileDialog.getSaveFileName(self,'Save file','/')
        if fileName:
            self.saveFun(fileName)
            STOP = 0
            return
        
        
    #To show open Dialog through Drop
   
    def dropAction(self):
        self.view = TestListView(self)
        
        self.connect(self.view, QtCore.SIGNAL("dropped"), self.pictureDropped)
        self.setCentralWidget(self.view)
        global DRAGNDROP
        DRAGNDROP = 1
    
    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Up:
            self.ArrowEffects(0)
        elif key == QtCore.Qt.Key_Right:
            self.ArrowEffects(1)
        elif key == QtCore.Qt.Key_Down:
            self.ArrowEffects(2)
        elif key == QtCore.Qt.Key_Left:
            self.ArrowEffects(3)
        else:
            pass
        

        if type(event) == QtGui.QKeyEvent:
            
            global zoom
            #For Escape if pressed!!!
            try:
                self.view.close()
            except:
                print("Drag Drop is already Closed")
       
            self.update()
            
            event.accept()
        else:
            event.ignore()   

    def pictureDropped(self, l):
        for url in l:
            if os.path.exists(url):
                global FILENAME
                FILENAME = url
                self.view.close()
    
    def paintEvent(self, e):
        global FILENAME
        global STOP
        if(FILENAME == "" or STOP == 1):
            if(STOP == 1):
                print("If you have pressed Save As or Open, the barcodes are still preserved in background. Don't panic")
            return
        
        qp = QtGui.QPainter()
        qp.begin(self)
        
        self.drawPoints(qp)
        
        qp.end()
             
            
    def drawPoints(self, qp):
        global FILENAME
        global chng_y
        global chng_x
        global CSVONCE
        if(CSVONCE == 1):
            CSVONCE = CSV(FILENAME)
            
        global xydata
        global selec
        global lst
        xydata = CSVONCE.get_max()[:4]
        
        global thispos
        global prev
        global selected_imgs
        global ekbaar
        global save_list
        global newp
        ##Opening in JSON Mode
        if(ekbaar == 1):
            f = open(FILENAME, 'r')
            lst = json.load(f)
            
            save_list = lst
            ekbaar = 0
        if(self.selnew == 1 and ekbaar == 0):
            ekbaar = -1
            lst = self.fromnew
            save_list = lst
            self.selnew = 0
            
            xydata = self.newxydata
            
            newp = 1
           
           
        if(newp == 1):
            xydata = self.newxydata
        global ctrlprsd
        global shftprsd
        global prevpos
        global newpos
        global MAXX
        MAXX = [0,0]
        global mappos
        global selAll
        for i in range(0, len(lst)):
            img = Info(lst[i])
            srng = img.get_coordinates()
            x_x = re.findall(r'\[(-?\d+)\,(-?\d+)\]', srng)
            
            
            x_1 = (int(xydata[1]) - int(x_x[0][0]))
            y_1 = (int(x_x[0][1]) - int(xydata[2]))
            if img.get_barcode() not in mappos.keys():
                mappos[img.get_barcode()] = [x_1,y_1]
            tx = int((20+(x_1*80)+chng_x)*zoom)
            ty = int((45+(y_1*80)+chng_y)*zoom)
            tx1 = int((20+((x_1+1)*80)+chng_x)*zoom)
            ty1 = int((45+((y_1+1)*80)+chng_y)*zoom)
            if((tx<thispos[0] and tx1>thispos[0] and ty<thispos[1] and ty1>thispos[1])
               or
               ((shftprsd== 1) and
                ((tx > prevpos[0] and tx < newpos[0]) and
                (ty >prevpos[1]  and ty < newpos[1]))
                )):
                
                
                running = 1
                if(shftprsd == 1):
                    if i not in selec:
                        selec.append(i)
                        if(lst[i] not in selected_imgs):
                            selected_imgs.append(lst[i])
                    else:
                        selec.remove(i)
                        if(lst[i] in selected_imgs):
                            selected_imgs.remove(lst[i])

                else:
                    
                
                    if(ctrlprsd == 0 and shftprsd == 0):
                        if(len(selec)==1):
                            if(selec[0] == i):
                                selec[0] = []
                                selected_imgs = []
                            else:
                                selec = [i]
                                selected_imgs =[lst[i]]
                                
                        else:
                            selec = [i]
                            selected_imgs =[lst[i]]
                    elif(ctrlprsd == 1 or shftprsd==1):
                                            
                       
                        if i not in selec:
                            selec.append(i)
                            if(lst[i] not in selected_imgs):
                                selected_imgs.append(lst[i])
                        else:
                            selec.remove(i)
                            if(lst[i] in selected_imgs):
                                selected_imgs.remove(lst[i])
                
                
                    
                thispos = (-22225,-22225)   
                found = 1
            #print(selec)    
            if(i in selec):
                running = 1
                
            else:
                running = 0
            img.set_image(qp, x_1, y_1,running)
            
            self.update()
            
            
            
    def mouseDoubleClickEvent(self, e):
    
        global thispos
        global  ctrlprsd
        global shiftact
        global newpos
        global selAll 
        selAll = 0
        self.pressed = e.pos()
        self.handleButton()
        if(ctrlprsd == 1):
            shftprsd = 1
        else:
            shftprsd = 0
        thispos = (self.pressed.x(),self.pressed.y())
        if(shiftact == 1):
            newpos = thispos
            
            shiftact = 0
        self.repaint()
        
    def handleButton(self):
        modifiers = QtGui.QApplication.keyboardModifiers()
        global  ctrlprsd
        global shftprsd
        global shiftact
        if modifiers == QtCore.Qt.ShiftModifier:
            ctrlprsd = 0
            shftprsd = 1
            shiftact = 1
        elif modifiers == QtCore.Qt.ControlModifier:
            ctrlprsd = 1
            shftprsd = 0
            
        else:
            ctrlprsd = 0
            shftprsd = 0
            shiftact = 0
        self.update()
            
    def mousePressEvent(self, e):
        if e.buttons() & QtCore.Qt.LeftButton:
            self.pressed = e.pos()
            self.first = 1 
            self.anchor = self.position        
            self.lastPos = QtCore.QPoint(e.globalX(), e.globalY())
            
            self.update()
            
            
            
        
            
    
    def mouseMoveEvent(self, event):
        
        if event.buttons() & QtCore.Qt.LeftButton:
            """
            (dx, dy) = event.x() - self.pressed.x(), event.y() - self.pressed.y()
            self.position = (self.anchor[0] - dx, self.anchor[1] - dy)
            self.one = 0
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  """
            if(self.pressed):
                dx, dy = event.x() - self.pressed.x(), event.y() - self.pressed.y()
                self.position = (self.anchor[0] - dx, self.anchor[1] - dy)
                self.one = 0
                
                
            
            global chng_y
            global chng_x
            global zoom
            (dx, dy) = (event.globalX()-self.lastPos.x(),
                event.globalY()-self.lastPos.y())
            
            #if(self.once == 0):
            chng_x = -(self.position[0])
            chng_y = -(self.position[1])
            self.ty = chng_y
            self.tx = chng_x
            
            if(zoom < 1 and self.first == 0):
                
                chng_x = (10-(10*zoom))*dx
                chng_y = (10-(10*zoom))*dy
                self.ty = chng_y
                self.tx = chng_x
            
            elif(self.first == 1):
                self.first = 0
                chng_x = self.tx
                chng_y = self.ty
                
                
            
            else:
                pass
                
            
            
            
        self.repaint()
        
       
    
    def mouseReleaseEvent(self,e):
        self.pressed = self.position
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        global chng_y
        global chng_x
        try:
            chng_x = self.tx
            chng_y = self.ty
        except:
            pass
        self.repaint()
     
        
        
    def wheelEvent(self,event):
       
        global zoom
        global chng_x
        global chng_y
        global MAXX
        
        oldscale = zoom
        zoom += event.delta()/1200.0
        if(zoom < 0.1):
            
            self.defaultFun()
        if(zoom > 3.5):
            self.defaultFun()
        if(event.x()<MAXX[0] or event.y() < MAXX[1]):
            chng_x += (zoom-oldscale)*zoom
            chng_y += (zoom-oldscale)*zoom
        if(MAXX[1] < 70):
            chng_x += 200
            chng_y += 200
            print("This feature us to view all squares on the screen!!!")
        """screenpoint = self.mapFromGlobal(QtGui.QCursor.pos())
        print(screenpoint)
        (dx, dy) = (screenpoint.x(), screenpoint.y())
        oldpoint = (screenpoint.x() + self.position[0], screenpoint.y() + self.position[1])
        newpoint = (oldpoint[0] * (zoom),
                    oldpoint[1] * (zoom))
        self.position = (newpoint[0] - dx, newpoint[1] - dy)
        chng_x = (self.position[0])
        chng_y = (self.position[1]) 
        """
            
        self.update()
         
    #Exist Function
    def ExistFun(self):
        global FILENAME
        global SHOWRACK
        global SHOWNORACK
        SHOWRACK = 0 
        SHOWNORACK = 0
        FILENAME = "mapOutput.csv"
        self.repaint()
        
        
    def defaultFun(self):
        global chng_y
        global chng_x
        global zoom
        chng_x = 0
        chng_y = 0
        zoom = 1
        self.position = (20,45)
        self.repaint()
   
    def WithRackFun(self):
        global SHOWRACK
        global SHOWNORACK
        SHOWRACK = 1 
        SHOWNORACK = 0
    
        self.update()
        
    
    def WithoutRackFun(self):
        global SHOWRACK
        global SHOWNORACK
        SHOWRACK = 0 
        SHOWNORACK = 1
        self.update()
    
    def modif_save(self,RESET):
        global save_list
       
        for i in save_list:
            x_x = re.findall(r'\[(-?\d+)\,(-?\d+)\]', i['coordinate'])
            
            x_x = [int(x_x[0][0]),int(x_x[0][1])]
            
           
            
            ###for diRECTIONS#####
            if(self.NORTHD[0] == int(x_x[0]) and self.NORTHD[1] == int(x_x[1])):
                                       
                i['neighbours'][2][0] = RESET
            
            if(self.EASTD[0] == int(x_x[0]) and self.EASTD[1] == int(x_x[1])):
                                       
                i['neighbours'][3][0] = RESET
                
            if(self.WESTD[0] == int(x_x[0]) and self.WESTD[1] == int(x_x[1])):
                                       
                i['neighbours'][1][0] = RESET
            
            if(self.SOUTHD[0] == int(x_x[0]) and self.SOUTHD[1] == int(x_x[1])):
                                       
                i['neighbours'][0][0] = RESET
        
       
               
               
            
            
    def deleteFun(self):
        global selected_imgs
        global lst
        global selec
        global thispos
        global undo_list
        lis = []
        for i in selected_imgs:
            if i in lst:
                
                ###TRACK COORDINATES
                x_x = re.findall(r'\[(-?\d+)\,(-?\d+)\]', i['coordinate'])
                x_1 = int(x_x[0][0])
                y_1 = int(x_x[0][1])
                self.NORTHD = [x_1,(y_1-1)]
                self.SOUTHD = [x_1,(y_1+1)]
                self.EASTD = [(x_1-1),y_1]       
                self.WESTD = [(x_1+1),y_1]
                self.modif_save(0)   
                lst.remove(i)
                
                
                #####           
                
                
                
                if i not in lis:
                    lis.append(i)
        if(len(lis)>0):
            undo_list.insert(0, lis)
        selec = []
        thispos =(-22240,-22240)
        self.update()
    
    def undoFun(self):
        global undo_list
        global lst
        global selec
        global selected_imgs
        global save_list
        if(len(undo_list)>0):
            undos = undo_list.pop(0)
            
            for i in undos:
                if i not in lst:
                    
                    lst.append(i)
                    
                    x_x = re.findall(r'\[(-?\d+)\,(-?\d+)\]', i['coordinate'])
                    x_1 = int(x_x[0][0])
                    y_1 = int(x_x[0][1])
                    self.NORTHD = [x_1,(y_1-1)]
                    self.SOUTHD = [x_1,(y_1+1)]
                    self.EASTD = [(x_1-1),y_1]       
                    self.WESTD = [(x_1+1),y_1]
                    self.modif_save(1)
                    
                    
        if(len(undo_list) == 0):
            selec = []
            selected_imgs = []
            
        self.update()
   
    def saveFun(self,filename=""):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Check in the same folder if you didnt give any filename\n\tAre you sure to Save?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            pass
        else:
            return
        edited = []
        global save_list
        global SAVEFILE
        if(SAVEFILE == ""):
            SAVEFILE = "updatedFile.csv"
        
        if(filename != ""):
            SAVEFILE = filename
        
        
        
        jnew = json.dumps(save_list)
        new_file = open(SAVEFILE,"w")
        new_file.write(jnew)
        new_file.close()
        self.repaint()
    
    def allFun(self):
        global selAll
        if(selAll == 0):
            selAll = 1
        else:
            selAll = 0
        return
    
    def ArrowEffects(self,DIR):
        global SHOWNORACK
        global SHOWRACK
        global ARROWTOGGLE
        if(SHOWRACK == 1):
            for i in selected_imgs:
               
                for t in range(0,len(lst)):
                    if(lst[t] == i):
                        lst[t]['neighbours'][DIR][1] = ARROWTOGGLE
                    
            if(ARROWTOGGLE == 1):
                ARROWTOGGLE = 0
            else:
                ARROWTOGGLE = 1
            
        if(SHOWNORACK == 1):
            for i in selected_imgs:
               
                for t in range(0,len(lst)):
                    if(lst[t] == i):
                        lst[t]['neighbours'][DIR][2] = ARROWTOGGLE
                    
            if(ARROWTOGGLE == 1):
                ARROWTOGGLE = 0
            else:
                ARROWTOGGLE = 1
                
    def create_new(self):
        text1, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter First Coordinate(numbers separated by comma:')
        text2, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter Second Coordinate(numbers separated by comma:')
        
        if ok:
            first = str(text1)
            second = str(text2)
            num1 = re.findall('(\d+)\,(\d+)',first)
            num2 = re.findall('(\d+)\,(\d+)',second)
            fin = [num1[0],num2[0]]
            self.fromnew = CreateNewMap(fin)
            self.newxydata = [self.fromnew.minx,self.fromnew.maxx,self.fromnew.miny,self.fromnew.maxy]
            self.fromnew = self.fromnew.created_list
            
            self.selnew = 1
            self.repaint()
        
    def browserFun(self):
        url, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter the URL:')
        port, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter the Port:')
        stri = r'http://'+str(url)+":"+str(port)+r'/api/map/all?details=true'
        
        r = requests.get(stri)
        self.newxydata = CSV(r.json(),1)
        self.newxydata = self.newxydata.get_max()[:4]
       
        self.fromnew = r.json()
            
        self.selnew = 1
        self.repaint()
    
    def tobrowserFun(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "The will overwrite the current data\nAre you sure to Save?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            pass
        else:
            return
        global save_list
        url, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter the URL:')
        port, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter the Port:')
        stri = r'http://'+str(url)+":"+str(port)+r'/api/map/'
        url = 'http://192.168.1.166:8182/api/map/'
        
        headers = {'Content-Type': 'application/json'}
        
        jnew = json.dumps(save_list)
        r = requests.post(url,jnew,headers=headers)
        print(r)
    
           
            
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    myQExampleScrollArea = Map()
    myQExampleScrollArea.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    
    
