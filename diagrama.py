import sqlite3
from PyQt5 import uic, QtWidgets

def showTasks():
    diagramDataBase = sqlite3.connect('diagramDataBase.db')
    cursor = diagramDataBase.cursor()
    cursor.execute('create table if not exists tasks (id integer primary key, taskDescription text, importancy integer, urgency integer, status text)')
    
    cursor.execute('select taskDescription from tasks where importancy = 1 and urgency = 2 and status = "Not done"')
    for i in cursor.fetchall():
        diagramFrame.list1.addItem(i[0])
    
    cursor.execute('select taskDescription from tasks where importancy = 1 and urgency = 1 and status = "Not done"')
    for i in cursor.fetchall():
        diagramFrame.list2.addItem(i[0])
    
    cursor.execute('select taskDescription from tasks where importancy = 2 and urgency = 1 and status = "Not done"')
    for i in cursor.fetchall():
        diagramFrame.list3.addItem(i[0])

    cursor.execute('select taskDescription from tasks where importancy = 2 and urgency = 2 and status = "Not done"')
    for i in cursor.fetchall():
        diagramFrame.list4.addItem(i[0])

    diagramDataBase.close()

def refreshLists():
    diagramFrame.list1.clear()
    diagramFrame.list2.clear()
    diagramFrame.list3.clear()
    diagramFrame.list4.clear()
    showTasks()

def saveTask():
    diagramDataBase = sqlite3.connect('diagramDataBase.db')
    cursor = diagramDataBase.cursor()

    taskDescription = str(newTaskWindow.lineEdit.text())
    importancy = str(newTaskWindow.comboBox.currentIndex())
    urgency = str(newTaskWindow.comboBox_2.currentIndex())
    task = (taskDescription, importancy, urgency)
    cursor.execute('insert into tasks (taskDescription, importancy, urgency, status) values (?,?,?,"Not done")', task)

    diagramDataBase.commit()
    diagramDataBase.close()
    
    refreshLists()
    newTaskWindow.close()

def concludeTask():
    diagramDataBase = sqlite3.connect('diagramDataBase.db')
    cursor = diagramDataBase.cursor()

    list1= diagramFrame.list1.selectedItems()
    list2= diagramFrame.list2.selectedItems()  
    list3= diagramFrame.list3.selectedItems()  
    list4= diagramFrame.list4.selectedItems()    

    for item in list1:
       diagramFrame.list1.takeItem(diagramFrame.list1.row(item))
       cursor.execute('update tasks set status = "Done" where taskDescription = ?', (item.text(),))
       diagramDataBase.commit()
    for item in list2:
       diagramFrame.list2.takeItem(diagramFrame.list2.row(item))
       cursor.execute('update tasks set status = "Done" where taskDescription = ?', (item.text(),))
       diagramDataBase.commit()
    for item in list3:
       diagramFrame.list3.takeItem(diagramFrame.list3.row(item))
       cursor.execute('update tasks set status = "Done" where taskDescription = ?', (item.text(),))
       diagramDataBase.commit()
    for item in list4:
       diagramFrame.list4.takeItem(diagramFrame.list4.row(item))
       cursor.execute('update tasks set status = "Done" where taskDescription = ?', (item.text(),))
       diagramDataBase.commit()

    diagramDataBase.close()



app = QtWidgets.QApplication([])
diagramFrame = uic.loadUi('diagramFrame.ui')
newTaskWindow = uic.loadUi('newTask.ui')

diagramFrame.newTask.clicked.connect(newTaskWindow.show)
diagramFrame.endTask.clicked.connect(lambda: concludeTask())


newTaskWindow.inserir.clicked.connect(lambda: saveTask())
newTaskWindow.cancelar.clicked.connect(lambda: newTaskWindow.close())

diagramFrame.show()
showTasks()
app.exec()
