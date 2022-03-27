from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import csv
from os.path import exists as fileExists
import sys
import os
import webbrowser
#based window system on https://www.pythonguis.com/tutorials/creating-multiple-windows/
class newPreset(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.startupItems = []
        self.setWindowTitle("Preset Creation")
        
        title = QLabel("Create Preset")
        title.setFont(QFont("Arial",16,QFont.Bold))
        layout.addWidget(title)

        spacer = QLabel("======================")
        layout.addWidget(spacer)

        webLine = QLineEdit()
        layout.addWidget(webLine)

        button1 = QPushButton("Add Website")
        button1.clicked.connect(lambda: self.addWebsite(webLine))
        layout.addWidget(button1)

        spacer = QLabel("======================")
        layout.addWidget(spacer)

        button2 = QPushButton("Add through file explorer")
        button2.clicked.connect(self.addFile)
        layout.addWidget(button2)

        spacer = QLabel("======================")
        layout.addWidget(spacer)

        nameHere = QLabel("Name of Preset")
        layout.addWidget(nameHere)

        nameLine = QLineEdit()
        layout.addWidget(nameLine)

        button3 = QPushButton("Finalize")
        button3.clicked.connect(lambda: self.savePreset(nameLine))
        layout.addWidget(button3)

        self.setLayout(layout)

    def addFile(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)')
        if path != ('', ''):
            item = "FILE:" + str(path[0])
            if item in self.startupItems:
                QMessageBox.about(self,"Warning","You already added that file(will be ignored)")
            else:
                self.startupItems.append(item)
    
    def addWebsite(self, website):
            
        websiteText = website.text().strip()
        if websiteText != "":
            self.startupItems.append("WEB:" + websiteText)
            website.clear()
        else:
            QMessageBox.about(self,"Warning","Website box was left empty")
            

    def savePreset(self, nameLine):
        preset = []
        main = MainWindow()
        fileStarted = False
        if fileExists('startupPresets.csv'):
            fileStarted = True
        name = nameLine.text().strip()
        if name != "":
            if name in main.getPresetsNames():
                QMessageBox.about(self,"Warning","This name of preset has already been taken")
            else:
                if len(self.startupItems) > 1:
                    preset.append(name)
                    for item in self.startupItems:
                        preset.append(item)
                    if fileStarted == False:
                        with open('startupPresets.csv', 'w', newline= "") as csvfile:
                            csvwriter = csv.writer(csvfile)
                            csvwriter.writerow(preset)          
                    else:
                        with open('startupPresets.csv', 'a', newline= "") as csvfile:
                            csvwriter = csv.writer(csvfile)
                            csvwriter.writerow(preset)
                    nameLine.clear()
                    self.hide()
                    self.startupItems = []
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    QMessageBox.about(self,"Warning","There is no websites or files in this preset")
        else:
            QMessageBox.about(self,"Warning","Name of the preset was left empty")
            
    
class editPreset(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.editList()
        self.setLayout(self.layout)
    def editList(self):
        self.clearScreen()
        title = QLabel("Edit Preset")
        title.setFont(QFont("Arial",16,QFont.Bold))
        self.layout.addWidget(title)
        for presetName in MainWindow.getPresetsNames(self):
            presetButton = QPushButton(presetName)
            presetButton.clicked.connect(lambda: self.edit(presetName))
            self.layout.addWidget(presetButton)
    def edit(self,presetName):
        self.initialName = presetName
        initialPreset = MainWindow.getPresetsItems(self,presetName)
        self.finalizedPresetLines = []
        self.clearScreen()
        title = QLabel("Editing: "+ presetName)
        title.setFont(QFont("Arial",16,QFont.Bold))
        self.layout.addWidget(title)

        finalizeButton = QPushButton("Finalize")
        finalizeButton.clicked.connect(lambda: self.finalizeEdit())
        self.layout.addWidget(finalizeButton)

        addFileButton = QPushButton("Add File")
        addFileButton.clicked.connect(lambda: self.addInput("file"))
        self.layout.addWidget(addFileButton)

        addWebButton = QPushButton("Add Website")
        addWebButton.clicked.connect(lambda: self.addInput("web"))
        self.layout.addWidget(addWebButton)

        
        for item in initialPreset:
            line = QLineEdit()
            line.setText(item)
            self.finalizedPresetLines.append(line)
            self.layout.addWidget(line)
        
    def addInput(self,typ):
        if typ == "file":
            line = QLineEdit()
            line.setText("FILE:")
            self.finalizedPresetLines.append(line)
            self.layout.addWidget(line)
        else:
            line = QLineEdit()
            line.setText("WEB:")
            self.finalizedPresetLines.append(line)
            self.layout.addWidget(line)
            
    def clearScreen(self):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()
# checks if it fits the rules and deletes the old plus adds the new to the csv file
    def finalizeEdit(self):
        name = True
        testSucceded = True
        finalPreset = []
        for item in self.finalizedPresetLines:
            item = item.text().strip()
            if name:
                if item == "":
                    QMessageBox.about(self,"Warning","Name of Preset was Left empty")
                    testSucceded = False
                    break
                else:
                    finalPreset.append(item)
                    name = False
            else:
                if item =="" or item == "WEB:" or item == "FILE:":
                    pass
                elif "WEB:" in item or "FILE:" in item:
                    finalPreset.append(item)
                else:
                    QMessageBox.about(self,"Warning","Did not assign a type(WEB: or FILE:)")
                    testSucceded = False
                    break
        if testSucceded and len(finalPreset) > 1:
            deletePreset.delete(self,self.initialName)
            with open('startupPresets.csv', 'a', newline= "") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(finalPreset)
            os.execl(sys.executable, sys.executable, *sys.argv)
            self.clearScreen()
            
            
                
                
                    
        
class deletePreset(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle("Preset Deletion")
        title = QLabel("Delete Preset")
        title.setFont(QFont("Arial",16,QFont.Bold))
        layout.addWidget(title)
        for presetName in MainWindow.getPresetsNames(self):
            presetButton = QPushButton(presetName)
            presetButton.clicked.connect(lambda: self.deleteFinalize(presetName))
            layout.addWidget(presetButton)
        self.setLayout(layout)
    #deletes and refresh
    def deleteFinalize(self,presetName):
        self.delete(presetName)
        os.execl(sys.executable, sys.executable, *sys.argv)
    #dosent have the thing refresh
    def delete(self,presetName):
        presets = []
        with open('startupPresets.csv', 'r') as csvfile:
            for row in csv.reader(csvfile):
                presets.append(row)
        with open('startupPresets.csv', 'w', newline= "") as csvfile:
            writer = csv.writer(csvfile)
            for row in presets:
                if row[0] != presetName:
                    writer.writerow(row)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.newPreset = newPreset()
        self.editPreset = editPreset()
        self.deletePreset = deletePreset()
        self.setWindowTitle("ImprovedStartup")
        l = QVBoxLayout()

        title = QLabel("Select Startup Preset")
        title.setFont(QFont("Arial",16,QFont.Bold))
        l.addWidget(title)

        for presetName in self.getPresetsNames():
            presetButton = QPushButton(presetName)
            presetButton.clicked.connect(lambda: self.startPreset(presetName))
            l.addWidget(presetButton)
        
        button1 = QPushButton("Add a Preset")
        button1.clicked.connect(self.toggle_newPreset)
        l.addWidget(button1)

        button2 = QPushButton("Edit a Preset")
        button2.clicked.connect(self.toggle_editPreset)
        l.addWidget(button2)

        button3 = QPushButton("Delete a Preset")
        button3.clicked.connect(self.toggle_deletePreset)
        l.addWidget(button3)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

#run through preset and check if file or website and open them
    def startPreset(self,presetName):
        preset = self.getPresetsItems(presetName)
        for item in preset:
            if item[0:5] == "FILE:":
                os.startfile(item[5:])
            elif item[0:4] == "WEB:":
                chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
                if "http" in item[4:]:
                    webbrowser.get().open_new_tab(item[4:])
                else:
                    webbrowser.get().open_new_tab("https://"+item[4:])
            else:
                pass
                
        
#gives all items in a preset including the name  
    def getPresetsItems(self,presetName):
        preset = []
        #look for the preset
        with open('startupPresets.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if row[0] == presetName:
                        preset = row
        return preset
# gets all names of presets  
    def getPresetsNames(self):
        presets = []
        if fileExists('startupPresets.csv'):
            with open('startupPresets.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if row[0] != "":
                        presets.append(row[0])
        return presets
#checks if they are open so you dont open another
    def toggle_newPreset(self, checked):
        if self.newPreset.isVisible():
            self.newPreset.hide()

        else:
            self.newPreset.show()

    def toggle_editPreset(self, checked):
        if self.editPreset.isVisible():
            self.editPreset.hide()

        else:
            self.editPreset.show()
            
    def toggle_deletePreset(self, checked):
        if self.deletePreset.isVisible():
            self.deletePreset.hide()

        else:
            self.deletePreset.show()
# create the app and show it
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

