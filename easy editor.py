#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel, QApplication,  QHBoxLayout, QVBoxLayout, QListWidget
import os 
from PyQt5.QtCore import Qt
from PIL import Image
from PyQt5.QtGui import QPixmap 
from PIL.ImageFilter import SHARPEN

app = QApplication([])
win = QWidget()
win.resize(700, 400)
win.setWindowTitle('Easy Editor')

# создание виджетов

btn_dir = QPushButton('Папка') 
list_file = QListWidget()
lb_image = QLabel('Картинка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('ч/б')
btn_save = QPushButton('сохранить')
btn_reset = QPushButton('сбросить фильтры')

# размещение виджетов

line1 = QVBoxLayout()
line1.addWidget(btn_dir)
line1.addWidget(list_file)

line2 = QHBoxLayout()
line2.addWidget(btn_left)
line2.addWidget(btn_right)
line2.addWidget(btn_mirror)
line2.addWidget(btn_sharp)
line2.addWidget(btn_bw)
line2.addWidget(btn_save)
line2.addWidget(btn_reset)

line3 = QVBoxLayout()
line3.addWidget(lb_image)
line3.addLayout(line2)

line4 = QHBoxLayout()
line4.addLayout(line1)
line4.addLayout(line3)
win.setLayout(line4) 

#функции
workdir = ''#путь до папки 
def chooseWorkdir():
    global workdir 
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result  

def showFilenameList():
    chooseWorkdir()
    ext = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', 'dav']
    files = os.listdir(workdir)
    rusult = filter(files, ext)
    list_file.clear 
    for f in rusult:
        list_file.addItem(f) 
btn_dir.clicked.connect(showFilenameList)
# работа с картинками 
class ImageProcessor():
    def __init__ (self):
        self.image = None
        self.filename = None
        self.save_dir = 'Modified/'
    def loadImage(self, filename):
        self.filename = filename 
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = lb_image.width(), lb_image.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pixmap)
        lb_image.setVisible(True)
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.rotate(270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def saveall(self):
        filter_ = 'PNG файлы(*.png);;JPEG файлы (*.jpg *.jpeg)' 
        file_path, ok = QFileDialog.getSaveFileName(filter=filter_)
        self.image.save(file_path)
        ext = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', 'dav']
        files = os.listdir(workdir)
        rusult = filter(files, ext)
        list_file.clear 
        for f in rusult:
            list_file.addItem(f)     

    def dropFilter(self):
        image_path = os.path.join(workdir, self.filename) 
        self.showImage(image_path)
        self.image = Image.open(image_path) 



workimage = ImageProcessor()

def showChosenImage():
    if list_file.currentRow() >= 0:
        filename = list_file.currentItem().text() 
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)
list_file.currentItemChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_save.clicked.connect(workimage.saveall)
btn_reset.clicked.connect(workimage.dropFilter)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharpen)
  

win.show()
app.exec()
