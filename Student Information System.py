##NOTE THAT THE PROGRAM MUST ONLY BE CLOSED BY CLICKING
##THE EXIT BUTTON IN THE HOME WINDOW TO AVOID A LOSS OF DATA
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime

class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
    def hasLeftChild(self):
        return self.leftChild
    def hasRightChild(self):
        return self.rightChild
    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self
    def isRightChild(self):
        return self.parent and self.parent.rightChild == self
    def isRoot(self):
        return not self.parent
    def isLeaf(self):
        return not (self.rightChild or self.leftChild)
    def hasAnyChildren(self):
        return self.rightChild or self.leftChild
    def hasBothChildrent(self):
        return self.leftChild and self.rightChild
    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.righChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self,key,val):
        if self.root:
            self._put(key,val,self.root)
        else:
            self.root = TreeNode(key,val)
        self.size = self.size + 1

    def _put(self,key,val,currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                   self._put(key,val,currentNode.leftChild)
            else:
                   currentNode.leftChild = TreeNode(key,val,parent=currentNode)
        else:
            if currentNode.hasRightChild():
                   self._put(key,val,currentNode.rightChild)
            else:
                   currentNode.rightChild = TreeNode(key,val,parent=currentNode)


#The two following functions are meant to do an inorder traversal of  an instance of the binary
#of the BinarySearchTree class which store's student objects using their name properties
#for keys.
#This inorder traversal  method  takes a file as a parameter 
#It writes the name and id attributes of each student node it visits to a line of the file
#in the following format ID;name
#The entries are in alphabetical order as far as names(LastName FirstName) are  concerned

                   
    def inorderToFile(self, file):
        try:
            
            myFile = open(file, "w")
            self._inorderToFile(myFile, self.root)
            myFile.close()
        except:
            pass
        
        
    def _inorderToFile(self, file, treeNode):
        #if tree node has a leftChild, do an inorder traversal of its
        #left subtree
        if treeNode.leftChild:
            self._inorderToFile(file,treeNode.leftChild)
        #then visit the node itself and write the id and name of the Student object
        # it holds to the file
        file.write(treeNode.payload.values[0]+";"+treeNode.key + "\n")
        #if tree node has a rightChild, do an inorder traversal of its
        #right subtree
        if treeNode.rightChild:
            self._inorderToFile(file, treeNode.rightChild)

    def __setitem__(self,k,v):
       self.put(k,v)

    def get(self,key):
       if self.root:
           res = self._get(key,self.root)
           if res:
                  return res.payload
           else:
                  return None
       else:
           return None

    def _get(self,key,currentNode):
       if not currentNode:
           return None
       elif currentNode.key == key:
           return currentNode
       elif key < currentNode.key:
           return self._get(key,currentNode.leftChild)
       else:
           return self._get(key,currentNode.rightChild)

    def __getitem__(self,key):
       return self.get(key)

    def __contains__(self,key):
       if self._get(key,self.root):
           return True
       else:
           return False

    def delete(self,key):
      if self.size > 1:
         nodeToRemove = self._get(key,self.root)
         if nodeToRemove:
             self.remove(nodeToRemove)
             self.size = self.size-1
         else:
             raise KeyError('Error, key not in tree')
      elif self.size == 1 and self.root.key == key:
         self.root = None
         self.size = self.size - 1
      else:
         raise KeyError('Error, key not in tree')

    def __delitem__(self,key):
       self.delete(key)

    def spliceOut(self):
       if self.isLeaf():
           if self.isLeftChild():
                  self.parent.leftChild = None
           else:
                  self.parent.rightChild = None
       elif self.hasAnyChildren():
           if self.hasLeftChild():
                  if self.isLeftChild():
                     self.parent.leftChild = self.leftChild
                  else:
                     self.parent.rightChild = self.leftChild
                  self.leftChild.parent = self.parent
           else:
                  if self.isLeftChild():
                     self.parent.leftChild = self.rightChild
                  else:
                     self.parent.rightChild = self.rightChild
                  self.rightChild.parent = self.parent

    def findSuccessor(self):
      succ = None
      if self.hasRightChild():
          succ = self.rightChild.findMin()
      else:
          if self.parent:
                 if self.isLeftChild():
                     succ = self.parent
                 else:
                     self.parent.rightChild = None
                     succ = self.parent.findSuccessor()
                     self.parent.rightChild = self
      return succ

    def findMin(self):
      current = self
      while current.hasLeftChild():
          current = current.leftChild
      return current

    def remove(self,currentNode):
         if currentNode.isLeaf(): #leaf
           if currentNode == currentNode.parent.leftChild:
               currentNode.parent.leftChild = None
           else:
               currentNode.parent.rightChild = None
         elif currentNode.hasBothChildren(): #interior
           succ = currentNode.findSuccessor()
           succ.spliceOut()
           currentNode.key = succ.key
           currentNode.payload = succ.payload

         else: # this node has one child
           if currentNode.hasLeftChild():
             if currentNode.isLeftChild():
                 currentNode.leftChild.parent = currentNode.parent
                 currentNode.parent.leftChild = currentNode.leftChild
             elif currentNode.isRightChild():
                 currentNode.leftChild.parent = currentNode.parent
                 currentNode.parent.rightChild = currentNode.leftChild
             else:
                 currentNode.replaceNodeData(currentNode.leftChild.key,
                                    currentNode.leftChild.payload,
                                    currentNode.leftChild.leftChild,
                                    currentNode.leftChild.rightChild)
           else:
             if currentNode.isLeftChild():
                 currentNode.rightChild.parent = currentNode.parent
                 currentNode.parent.leftChild = currentNode.rightChild
             elif currentNode.isRightChild():
                 currentNode.rightChild.parent = currentNode.parent
                 currentNode.parent.rightChild = currentNode.rightChild
             else:
                 currentNode.replaceNodeData(currentNode.rightChild.key,
                                    currentNode.rightChild.payload,
                                    currentNode.rightChild.leftChild,
                                    currentNode.rightChild.rightChild)




class HashTable:
    def __init__(self, size, counts):
        self.size = size
        self.slots = [None] * self.size
        self.data = [None] * self.size
        self.counts = counts


    def get(self,key):
      startslot = self.hashfunction(key,len(self.slots))

      data = None
      stop = False
      found = False
      position = startslot
      while self.slots[position] != None and  \
                           not found and not stop:
         if self.slots[position] == key:
           found = True
           data = self.data[position]
         else:
           position=self.rehash(position,len(self.slots))
           if position == startslot:
               stop = True
      return data

    def __getitem__(self,key):
        return self.get(key)

    def __setitem__(self,key,data):
        self.put(key,data)

      

    def isPrime(self, num):
        isPrime = True
        divisor = 3
        while divisor < num and isPrime:
            if num % divisor == 0:
                isPrime = False
            divisor += 2
        return isPrime

    def nextPrime(self, num):
        current = 2 * num + 1
        while not self.isPrime(current):
            current += 2
        return current
    
    def rehashAll(self):
        newMap = HashTable(self.nextPrime(self.size), self.counts)
        for ind in range(len(self.slots)):
            if self.slots[ind] != None:
                newMap.put(self.slots[ind], self.data[ind])
        self = newMap
                

    def put(self, key, data):
        loadFactor = self.counts / len(self.slots)
        if loadFactor > 0.5:
            self.rehashAll()
            self._put(key, data)
        else:
            self._put(key, data)
                           

    def _put(self,key,data):
        self.counts += 1
        hashvalue = self.hashfunction(key,len(self.slots))
        
        if self.slots[hashvalue] == None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = data
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue] = data  #replace
            else:
                nextslot = self.rehash(hashvalue,len(self.slots))
                while self.slots[nextslot] != None and \
                      self.slots[nextslot] != key:
                    nextslot = self.rehash(nextslot,len(self.slots))

                if self.slots[nextslot] == None:
                    self.slots[nextslot]=key
                    self.data[nextslot]=data
                else:
                    self.data[nextslot] = data #replace

    def hashfunction(self,key,size):
            return int(key)%size

    def rehash(self,oldhash,size):
            return (oldhash+1)%size










class Student:
    def __init__(self,ID, surname, firstName, otherNames, gender, day, month, year, major, Class, currentYear ):
        self.keys = ["ID Number", "Surname", "First Name","Other Names", "Gender", "Day", "Month", "Year", "Major","Class",
                     "Current Year"]
        self.values=[ID, surname, firstName, otherNames, gender, day, month, year, major, Class, currentYear ]
    

    def writeToFile(self):
        file = open(self.values[0]+".txt", "w")
        for i in range(len(self.keys)):
            file.write(self.keys[i] + ";" + self.values[i]+"\n")
        file.close()

    def calcAge(self):
        return None

    def tell_age(self,day, month,year):
        dict_={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,
               "October":10,"November":11,"December":12}
        date_of_birth=datetime.date(int(year), dict_[month], int(day))

        age_year,age_day=date_of_birth.year,date_of_birth.day
        today_date=datetime.datetime.today()

        current_month,current_day=today_date.month,today_date.day
        your_age=today_date.year-age_year 

        if current_month<date_of_birth.month:
            return your_age-1
            
        else:
            if current_month==date_of_birth.month and current_day<date_of_birth.day:
                return your_age-1
            else:
                return your_age



    def dispData(self):
        self.titleFont=("Papyrus",30,"bold")
        self.widgetFont=("Papyrus",20)
        self.background="tan"
        self.foreground="black"
        self.stickyVal="NE"+"SW"
        self.pady=5
        self.padx=5
        self.entryRelief="sunken"
        self.butRelief="raised"
        self.entryBd=10
        wini = Tk()
        wini.rowconfigure(0,weight=1)
        wini.columnconfigure(0,weight=1)
        winiF=Frame(wini,bg="black")
        winiF.grid(row=0, column=0, sticky=self.stickyVal)
        winiF.rowconfigure(0,weight=1)
        winiF.columnconfigure(0,weight=1)
        winRow=0
        
        self.classTitleLab=Label(winiF,text="Student's Information" ,fg=self.foreground,bg=self.background,
                             font=self.titleFont)
        self.classTitleLab.grid(row=winRow, column=0,columnspan=4,sticky=self.stickyVal)
        winRow+=1
        age = self.tell_age(self.values[5], self.values[6],self.values[7])
        dob = self.values[6] + " " + self.values[5] + ", " + self.values[7]
        keyList = ["ID Number:", "Surname:", "First Name:","Other Names:", "Gender:", "Date of Birth:", "Major:","Class:", "Age:"]
        valList = [self.values[0], self.values[1], self.values[2], self.values[3], self.values[4], dob, self.values[8], self.values[9], age]
        ind = 0
        while winRow<5:
            col = 0
            Label(winiF,text=keyList[ind],fg=self.foreground, bg=self.background, font=self.widgetFont).grid(row=winRow,
                                                                                                             column=col,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            col +=1
            Label(winiF,text=valList[ind],fg=self.foreground, bg=self.background, font=self.widgetFont).grid(row=winRow,
                                                                                                             column=col,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            col +=1
            ind +=1
            
            Label(winiF,text=keyList[ind],fg=self.foreground, bg=self.background, font=self.widgetFont).grid(row=winRow,
                                                                                                             column=col,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            col +=1
            Label(winiF,text=valList[ind],fg=self.foreground, bg=self.background, font=self.widgetFont).grid(row=winRow,
                                                                                                             column=col,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            
            ind += 1
            winRow += 1
        Label(winiF,text=keyList[8],fg=self.foreground, bg=self.background, font=self.widgetFont).grid(row=winRow,
                                                                                                             column=0,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
        Label(winiF,text=valList[8],fg=self.foreground, bg=self.background, font=self.widgetFont).grid(row=winRow,
                                                                                                             column=1,sticky=self.stickyVal,padx=self.padx,pady=self.pady)

        finalBut=Button(winiF,text="Ok",command=wini.destroy,
                               bg=self.background, fg=self.foreground,font=self.widgetFont,relief=self.butRelief)
        finalBut.grid(row=winRow,column=2,columnspan=2,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            
            
        

       
class Class:
    def __init__(self, year):
        self.classList = []
        self.yearList = ["year1", "year2", "year3", "year4"]
        self.classFile = self.yearList[year] + ".txt"
        self.yearHash = HashTable(117,0)
        self.yearBinTree = BinarySearchTree()


    def writeToFile(self):
        self.yearBinTree.inorderToFile(self.classFile)


    def appendToFile(self, studID, name):
        file=open(self.classFile, "a")
        file.write(studID+";"+ name+"\n")
        file.close()
        
        
# This method is to called  whenever an instance of the InfoSystem created. It goes through a particular class' list and uses each
#entry to create a student object. These student objects are placed in the binary tree for storing that particular class' student
#objects
    def load(self):
        try:
            #open class' file
            #Each line has the following format: ID;name
            file = open(self.classFile, "r")
            for aline in file:
                entry = aline.split(";")
                #extract id
                studID = entry[0]
                #open student's file
                studFile = open(studID+".txt", "r")
                #create an empty list to contain all parameters needed to create a student object
                studDataList = []
                for aline in studFile:
                    studDataList.append(aline.split(";")[1].strip())
                studObj = Student(studDataList[0], studDataList[1], studDataList[2], studDataList[3], studDataList[4],
                                  studDataList[5], studDataList[6], studDataList[7], studDataList[8], studDataList[9], studDataList[10] )
                #place student object in the class' hash table using its id
                self.yearHash.put(int(studDataList[0]), studObj)
                #place student object in the class' binary search tree
                self.yearBinTree[studDataList[1] + " " + studDataList[2]] = studObj
                self.classList.append(studDataList[1] + " " + studDataList[2])
            
        except FileNotFoundError:
            print("error")
           
class StudButton:
    def __init__(self, application, window, name, yearNum, row):
        self.application = application
        self.window = window
        self.name = name
        self.yearNum = yearNum
        self.row = row
        self.button = Button(self.window, text = self.name,
                             command = self.dispStud,
                             font = self.application.widgetFont, fg = self.application.foreground,
                             bg = self.application.background, relief = self.application.butRelief)
        
        self.button.grid(row=self.row, column = 0, sticky = self.application.stickyVal,
                         padx = self.application.padx, pady = self.application.pady)


    def dispStud(self):
        if self.yearNum == 1:
            studObj = self.application.year1.yearBinTree[self.name]
        elif self.yearNum == 2:
            studObj =self.application.year2.yearBinTree[self.name]
        elif self.yearNum == 3:
            studObj =self.application.year3.yearBinTree[self.name]
        elif self.yearNum == 4:
            studObj =self.application.year4.yearBinTree[self.name]
        studObj.dispData()
            
    

class InfoSystem(Tk):
    def __init__(self):
        super().__init__()
        self.year1 = Class(0)
        self.year2 = Class(1)
        self.year3 = Class(2)
        self.year4 = Class(3)
        self.year1.load()
        self.year2.load()
        self.year3.load()
        self.year4.load()
        
        self.majorList=[]
        self.titleFont=("Papyrus",30,"bold")
        self.widgetFont=("Papyrus",20)
        self.background="tan"
        self.foreground="black"
        self.frame=Frame(self,bg="silver")
        self.stickyVal="E"+"W"
        self.pady=5
        self.padx=5
        
        self.frame.grid(sticky='NE'+'SW')
        self.entryRelief="sunken"
        self.butRelief="raised"
        self.entryBd=10
        self.columnconfigure(0, weight = 1)
        self.title=Label(self.frame,text="Student Information System",font=self.titleFont,fg=self.foreground,bg=self.background,
                         bd=5,relief='flat')
        self.title.grid(row=0, sticky="E"+"W")
        self.addStud=Button(self.frame,text="Add Student",command=self.studAdd,font=self.widgetFont,
                             fg=self.foreground,bg=self.background,relief=self.butRelief)
        self.addStud.grid(row=1,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
        self.addMajor=Button(self.frame,text="Add Major",command=self.addMajor,font=self.widgetFont,
                             fg=self.foreground,bg=self.background,relief=self.butRelief)
        self.addMajor.grid(row=2,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
        self.records=Button(self.frame,text="Records",command=self.records,font=self.widgetFont,
                             fg=self.foreground,bg=self.background,relief=self.butRelief)
        self.records.grid(row=3,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
        self.exit=Button(self.frame,text="Exit",command=self.Exit,font=self.widgetFont,
                             fg=self.foreground,bg=self.background,relief=self.butRelief)
        self.exit.grid(row=4,sticky=self.stickyVal,padx=self.padx,pady=self.pady)

         
    def studAdd(self):
        try:
            self.majorList = []
            self.majorFile = open("major.txt","r")
            for aline in self.majorFile:
                self.majorList.append(aline)
            self.majorFile.close()
            self.studWin=Tk()
            self.studWin.rowconfigure(0,weight=1)
            self.studWin.columnconfigure(0,weight=1)
            self.studWinF=Frame(self.studWin,bg=self.background)
            self.studWinF.grid(row=0, column=0, sticky="NE"+"SW")
            winRow=0

            self.stitleLab=Label(self.studWinF,text="Add a Student",fg=self.foreground,bg=self.background,
                                 font=self.titleFont)
            self.stitleLab.grid(row=winRow,column=0,columnspan=4,sticky=self.stickyVal)
            winRow+=1


            self.ssurnameLab=Label(self.studWinF,text='Surname:',fg=self.foreground, bg=self.background,
                              font=self.widgetFont)
            self.ssurnameLab.grid(row=winRow,column=2,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            self.ssurnameEnt=Entry(self.studWinF,font=self.widgetFont,relief=self.entryRelief,bd=self.entryBd)
            self.ssurnameEnt.grid(row=winRow,column=3,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            self.sIDLab=Label(self.studWinF, text='Student ID#:', fg=self.foreground, bg=self.background,
                              font=self.widgetFont)
            self.sIDLab.grid(row=winRow,column=0,sticky=self.stickyVal,padx=self.padx)
            self.sIDEnt=Entry(self.studWinF,font=self.widgetFont,relief=self.entryRelief,bd=self.entryBd)
            self.sIDEnt.grid(row=winRow,column=1,sticky=self.stickyVal,padx=self.padx)
            winRow+=1


            self.sotherNameLab=Label(self.studWinF,text="Other Names:",fg=self.foreground, bg=self.background,
                              font=self.widgetFont)
            self.sotherNameLab.grid(row=winRow,column=2,sticky=self.stickyVal,padx=self.padx)
            self.sotherNameEnt=Entry(self.studWinF,font=self.widgetFont,relief=self.entryRelief,bd=self.entryBd)
            self.sotherNameEnt.grid(row=winRow,column=3,columnspan=2,sticky=self.stickyVal,padx=self.padx)
            self.sfirstNameLab=Label(self.studWinF,text='First Name:',fg=self.foreground, bg=self.background,
                              font=self.widgetFont)
            self.sfirstNameLab.grid(row=winRow,column=0,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            self.sfirstNameEnt=Entry(self.studWinF,font=self.widgetFont,relief=self.entryRelief,bd=self.entryBd)
            self.sfirstNameEnt.grid(row=winRow,column=1,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            winRow+=1
            
            genderList = ["Female", "Male"]
            self.sgenderFrame=LabelFrame(self.studWinF,bg=self.background,text="Gender",font=('papyrus',20,'bold'),
                                        fg=self.foreground)
            self.sgenderFrame.grid(row=winRow,column=0,padx=self.padx,pady=self.pady,sticky=self.stickyVal)
            self.sgenderFrame.columnconfigure(0, weight=1)
            self.genderOptMen=ttk.Combobox(self.sgenderFrame, values=genderList)
            self.genderOptMen.grid(sticky=self.stickyVal)

            classList = ["year1", "year2","year3","year4"]
            self.classFrame=LabelFrame(self.studWinF,bg=self.background,text="Class",font=('papyrus',20,'bold'),
                                        fg=self.foreground)
            self.classFrame.grid(row=winRow,column=1,padx=self.padx,pady=self.pady,sticky=self.stickyVal)
            self.classFrame.columnconfigure(0, weight=1)
            self.classOptMen=ttk.Combobox(self.classFrame, values=classList)
            self.classOptMen.grid(sticky=self.stickyVal)

            

            #creating label widget for country of origin of student
            self.curYearLab=Label(self.studWinF, text="Current year:", font=self.widgetFont, fg=self.foreground,
                                  bg=self.background)
            self.curYearLab.grid(row=winRow, column=2,sticky=self.stickyVal)
            #creating label widget for country of origin of student
            self.curYearEnt=Entry(self.studWinF, font=self.widgetFont, relief=self.entryRelief, bd=self.entryBd)
            self.curYearEnt.grid(row=winRow,column=3, sticky=self.stickyVal)
            #increasing row variable
            winRow+=1

            #creating Label frame widget to contain date of birth
            self.sbirthDateFrame=LabelFrame(self.studWinF,text="Date of Birth",font=('papyrus',20,'bold'),
                                            fg=self.foreground,bg=self.background)
            self.sbirthDateFrame.grid(row=winRow,column=0,columnspan=3,sticky=self.stickyVal,padx=self.padx,
                                     pady=self.pady)
            
            for i in range(3):
                self.sbirthDateFrame.columnconfigure(i,weight=1)
            #creating options list for day of birth
            dayList=[]
            for i in range(1,32):
                dayList.append(str(i))
            #creating options list for month of birth
            monthList=['January','February','March','April','May','June','July','August','September',
                       'October','November','December']
            #creating options list for year of birth
            yearList=[]
            for i in range(1970,2050):
                yearList.append(str(i))
            self.dayVar=StringVar()
            self.monthVar=StringVar()
            self.yearVar=StringVar()

            #creating label frame and combobox for day of birth
            dayLabFrame=LabelFrame(self.sbirthDateFrame, text="Day", font=self.widgetFont, fg=self.foreground,
                                    bg=self.background)
            dayLabFrame.grid(row=0,column=0,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            dayLabFrame.columnconfigure(0,weight=1)

            self.dayOptMen=ttk.Combobox(dayLabFrame, textvariable=self.dayVar,values=dayList)
            self.dayOptMen.grid(sticky=self.stickyVal)

            #creating label frame and combobox for month of birth
            monthLabFrame=LabelFrame(self.sbirthDateFrame, text="Month", font=self.widgetFont, fg=self.foreground,
                                    bg=self.background)
            monthLabFrame.grid(row=0,column=1,sticky=self.stickyVal,pady=self.pady)

            monthLabFrame.columnconfigure(0,weight=1)

            self.monthOptMen=ttk.Combobox(monthLabFrame,textvariable=self.monthVar,values=monthList)
            self.monthOptMen.grid(sticky=self.stickyVal)

            #creating label frame and combobox for year of birth
            yearLabFrame=LabelFrame(self.sbirthDateFrame,text="Year", font=self.widgetFont, fg=self.foreground,
                                    bg=self.background)
            yearLabFrame.grid(row=0,column=2,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
            yearLabFrame.columnconfigure(0,weight=1)
            

            self.yearOptMen=ttk.Combobox(yearLabFrame,textvariable=self.yearVar,values=yearList)
            self.yearOptMen.grid(sticky=self.stickyVal)
            

            theMajorFile = open("major.txt","r")
            majorList = []
            for aline in theMajorFile:
                majorList.append(aline)
            self.majorFrame=LabelFrame(self.studWinF,bg=self.background,text="Major",font=('papyrus',20,'bold'),
                                        fg=self.foreground)
            self.majorFrame.grid(row=winRow,column=3,padx=self.padx,pady=self.pady,sticky=self.stickyVal)
            self.majorFrame.columnconfigure(0, weight=1)
            self.majorOptMen=ttk.Combobox(self.majorFrame, values=majorList)
            self.majorOptMen.grid(sticky=self.stickyVal)
            winRow+=1

            #creating  that saves a students data and brings up another window  to add another student
            completeBut=Button(self.studWinF,text="Add Student",command=self.addStudent,
                               bg=self.background, fg=self.foreground,font=self.widgetFont,relief=self.butRelief)
            completeBut.grid(row=winRow,column=3,sticky=self.stickyVal)

        

            for i in range(winRow+1):
                self.studWinF.rowconfigure(i,weight=1)
            for i in range(4):
                self.studWinF.columnconfigure(i,weight=1)

        except FileNotFoundError:
            messagebox.showinfo("No major", "It seems you will have to add some majors before you can proceed")

#The following function  retrieves all pieces of student information entered in
#the graphical interface for entering a students information(created by the
#studAdd method).  
    def addStudent(self):
         #assign text in each text box and combobox to a variable
        ID=self.sIDEnt.get()
        surname = self.ssurnameEnt.get()
        firstName = self.sfirstNameEnt.get()
        otherNames = self.sotherNameEnt.get()
        gender = self.genderOptMen.get()
        day = self.dayOptMen.get()
        month = self.monthOptMen.get()
        year = self.yearOptMen.get()
        major = self.majorOptMen.get().strip()
        Class = self.classOptMen.get()
        currentYear  =self.curYearEnt.get()
 #Use the retrieved student information to create a student object       
        studObj = Student(ID, surname, firstName, otherNames, gender, day, month, year, major, Class, currentYear)
        #create key(name) that will be used to place the student object into the
        #binary search tree of the class to which it belongs
        name = surname + " " + firstName
        #Let student object write its data to file named in the following
        #format "id.txt" where id is the id attribute of the student object
        studObj.writeToFile()
        #Depending on whether the student is in his first, second, third
        #or fourth year, add it to the corrrect binary search tree and hash table
        if studObj.values[9] == "year1":
            self.year1.yearHash.put(studObj.values[0], studObj)
            self.year1.yearBinTree.put(name, studObj)
            self.year1.appendToFile(ID, name)
            self.year1.classList.append(name)
        elif studObj.values[9] == "year2":
            self.year2.yearHash.put(studObj.values[0], studObj)
            self.year2.yearBinTree.put(name, studObj)
            self.year2.appendToFile(ID,name)
            self.year2.classList.append(name)
        elif studObj.values[9] == "year3":
            self.year3.yearHash.put(studObj.values[0], studObj)
            self.year3.yearBinTree.put(name, studObj)
            self.year3.appendToFile(ID,name)
            self.year3.classList.append(name)
        elif studObj.values[9] == "year4":
            self.year4.yearHash.put(studObj.values[0], studObj)
            self.year4.yearBinTree.put(name, studObj)
            self.year4.appendToFile(ID,name)
            self.year4.classList.append(name)
        #close window into which student information has been entered
        self.studWin.destroy()
        #create another window into which new information can be entered
        self.studAdd()
        


    def Exit(self):
        self.year1.writeToFile()
        self.year2.writeToFile()
        self.year3.writeToFile()
        self.year4.writeToFile()
        self.destroy()
                              

    def addMajor(self):
        self.win = Tk()
        self.win.rowconfigure(0,weight=1)
        self.win.columnconfigure(0,weight=1)
        self.winF=Frame(self.win,bg=self.background)
        self.winF.grid(row=0, column=0, sticky=self.stickyVal)
        winRow=0

        self.majorTitle=Label(self.winF,text="Add a Major",fg=self.foreground,bg=self.background,
                             font=self.titleFont)
        self.majorTitle.grid(row=winRow,column=0,columnspan=2,sticky=self.stickyVal)
        winRow+=1

        self.majorLab=Label(self.winF,text='Major Name:',fg=self.foreground, bg=self.background,
                          font=self.widgetFont)
        self.majorLab.grid(row=winRow,column=0,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
        self.majorEnt=Entry(self.winF,font=self.widgetFont,relief=self.entryRelief,bd=self.entryBd)
        self.majorEnt.grid(row=winRow,column=1,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
        winRow+=1

        addBut=Button(self.winF,text="Add Major", command=self.AddMajor,
                               bg=self.background, fg=self.foreground, font=self.widgetFont, relief=self.butRelief)
        addBut.grid(row=winRow, column=0, sticky=self.stickyVal, columnspan=2)


        
    def AddMajor(self):
        self.majorList.append(self.majorEnt.get())
        file = open("major.txt", "w")
        for i in self.majorList:
            file.write(i+"\n")
        file.close()
        self.win.destroy()  


        
    def dispStudData(self, studObj):
        win = Tk()
        winF=Frame(self.win,bg=self.background)
        winF.grid(row=0, column=0, sticky=self.stickyVal)
        win.rowconfigure(0, weight = 1)
        win.columnconfigure(0, weight = 1)
        titleLab=Label(self.winF,text="Student's Information",fg=self.foreground,bg=self.background,
                             font=self.titleFont)
        titleLab.grid(row=0,column=0,columnspan=2,sticky=self.stickyVal)
        for i in range(len(studObj.keys)):
            Label(winF, text = studObj.keys[i], fg=self.foreground, bg=self.background,
                  font=self.widgetFont) .grid(row=i+1, column=0, sticky=self.stickyVal)
            Label(winF, text = studObj.values[i], fg=self.foreground, bg=self.background,
                  font=self.widgetFont) .grid(row=i+1, column=0, sticky=self.stickyVal)



    def records(self):
        self.recWin = Tk()
        self.recWin.rowconfigure(0,weight=1)
        self.recWin.columnconfigure(0,weight=1)
        self.recWinF=Frame(self.recWin,bg=self.background)
        self.recWinF.grid(row=0, column=0, sticky=self.stickyVal)
        self.recWinF.rowconfigure(0,weight=1)
        self.recWinF.columnconfigure(0,weight=1)
        
        winRow=0
        self.recordsTitleLab=Label(self.recWinF,text="Records",fg=self.foreground,bg=self.background,
                             font=self.titleFont)
        self.recordsTitleLab.grid(row=winRow, column=0,sticky=self.stickyVal)
        winRow+=1
        
        self.y1=Button(self.recWinF,text="year1",command=lambda:self.year(1),font=self.widgetFont,
                             fg=self.foreground,bg=self.background,relief=self.butRelief)
        self.y1.grid(row=winRow,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
        winRow+=1
        
        self.y2=Button(self.recWinF,text="year2",command=lambda:self.year(2),font=self.widgetFont,
                             fg=self.foreground,bg=self.background,relief=self.butRelief)
        self.y2.grid(row=winRow,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
        winRow+=1
        
        self.y3=Button(self.recWinF,text="year3",command=lambda:self.year(3),font=self.widgetFont,
                             fg=self.foreground,bg=self.background,relief=self.butRelief)
        self.y3.grid(row=winRow,sticky=self.stickyVal,padx=self.padx,pady=self.pady)
        winRow+=1
        
        self.y4=Button(self.recWinF, text="year4", command=lambda:self.year(4),font=self.widgetFont,
                             fg=self.foreground,bg=self.background,relief=self.butRelief)
        self.y4.grid(row=winRow,sticky=self.stickyVal,padx=self.padx,pady=self.pady)



    def year(self, n):
        wini = Tk()
        wini.rowconfigure(0,weight=1)
        wini.columnconfigure(0,weight=1)
        winiF=Frame(wini,bg=self.background)
        winiF.grid(row=0, column=0, sticky=self.stickyVal)
        winiF.rowconfigure(0,weight=1)
        winiF.columnconfigure(0,weight=1)
        winRow=0 
        
        self.classTitleLab=Label(winiF,text="Search year "+str(n),fg=self.foreground,bg=self.background,
                             font=self.titleFont)
        self.classTitleLab.grid(row=winRow, column=0,columnspan=2,sticky=self.stickyVal)
        winRow+=1

        self.searchEnt=Entry(winiF,font=self.widgetFont,relief=self.entryRelief,bd=self.entryBd)
        self.searchEnt.grid(row=winRow,column=0,columnspan = 2, sticky=self.stickyVal,padx=self.padx,pady=self.pady)
        winRow+=1

        searchBut =Button(winiF,text="Search",command=lambda:self.search(n),font=self.widgetFont,
                             fg=self.foreground,bg=self.background,relief=self.butRelief)
        searchBut.grid(row=winRow, column = 1, sticky=self.stickyVal, padx=self.padx, pady=self.pady)
        winRow+=1 

        viewClass =Button(winiF,text="View Year "+str(n)+" Class List",command=lambda:self.viewClass(n),font=self.widgetFont,
                             fg=self.foreground,bg=self.background,relief=self.butRelief)
        viewClass.grid(row=winRow, column = 0, columnspan=2, sticky=self.stickyVal, padx=self.padx, pady=self.pady)


    def search(self, n):
        key = self.searchEnt.get()
        if n==1:
            studObj =self.year1.yearBinTree[key]
        elif n==2:
            studObj =self.year2.yearBinTree[key]
        elif n==3:
            studObj =self.year3.yearBinTree[key]
        else:
            studObj =self.year4.yearBinTree[key]
        studObj.dispData()


    def viewClass(self, n):
        wini = Tk()
        wini.rowconfigure(0,weight=1)
        wini.columnconfigure(0,weight=1)
        winiF=Frame(wini,bg=self.background)
        winiF.grid(row=0, column=0, sticky=self.stickyVal)
        winiF.rowconfigure(0,weight=1)
        winiF.columnconfigure(0,weight=1)
        winRow=0 
        
        self.classTitleLab=Label(winiF,text="View Class Information",fg=self.foreground,bg=self.background,
                             font=self.titleFont)
        self.classTitleLab.grid(row=winRow, column=0,sticky=self.stickyVal)
        winRow+=1
        if n == 1:
            ourList = self.year1.classList
        elif n== 2:
            ourList = self.year2.classList
        elif n == 3:
            ourList = self.year3.classList
        elif n == 4:
            ourList = self.year4.classList
        for i in range(len(ourList)):
            StudButton( self, winiF, ourList[i], n, winRow+i)
            winRow += 1
            
            
        



application = InfoSystem()

