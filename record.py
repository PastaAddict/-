import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import time
p=np.pi

def record(seconds,fs):
    data = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished

    return np.array([i[0] for i in data])

def hamming(n,L=64):
    return 0.5-0.5*np.cos(2*p*(n+1)/(L+1))

def create_blocks(data,L,Nfft):
    W_n=np.fromiter(map(hamming,np.linspace(0,L-1,L)),float)

    blocks=[data[(i*L)//4:L+(i*L)//4] for i in range(1+(len(data)-L)//(L//4)) ]
    blocks_fft=[np.abs(np.fft.fft(i*W_n,Nfft)) for i in blocks]
    M=max([max(i) for i in blocks_fft])
    blocks_fft=[i/M for i in blocks_fft]
    blocks_fft=[[i[j] for i in blocks_fft] for j in range(Nfft)]
    
    return blocks_fft[Nfft//2:]

def max_freq(data,samplerate,L,Nfft):
    sound=np.transpose(create_blocks(data,L,Nfft))
    return [np.argmax(i) for i in sound]

def plotSound(data,fs,block,nfft):
    fig, axs = plt.subplots(3, sharex=True)
    fig.set_figheight(15)
    fig.set_figwidth(15)
    t=np.linspace(0,len(data)/fs,len(data))#αντιστοιχηση δειγματων στο χρονο
    
##    axs[0].xlabel('Time(s)')
##    axs[0].ylabel('Amplitude(V)')
    axs[0].plot(t,data,color='g')

    axs[1].imshow(create_blocks(data,block,nfft),cmap='Spectral', extent = [ 0 , len(data)/fs, 0 , fs//2], aspect='auto' )
##    axs[1].colorbar()
##    axs[1].ylabel('Frequency [Hz]')
##    axs[1].xlabel('Time [sec]')
    maxFreq=max_freq(data,fs,block,nfft)
    n=np.linspace(0,len(data)/fs,len(maxFreq))
    axs[2].plot(n,maxFreq)

    fig.show()
    
'''gui'''
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QProgressBar, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot



            
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'recorder'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 500
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.l1 = QLabel(self)
        self.l1.setText("Seconds")
        self.l1.move(20, 15)

        self.l2 = QLabel(self)
        self.l2.setText("Samplerate")
        self.l2.move(20, 45)

        self.l3 = QLabel(self)
        self.l3.setText("Block Size")
        self.l3.move(20, 75)

        self.l4 = QLabel(self)
        self.l4.setText("FFT Size")
        self.l4.move(20, 105)

        self.l5 = QLabel(self)
        self.l5.move(80, 150)
    
        # Create textbox
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(100, 20)
        self.textbox1.resize(50,25)

        # Create textbox
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(100, 50)
        self.textbox2.resize(50,25)

        # Create textbox
        self.textbox3 = QLineEdit(self)
        self.textbox3.move(100, 80)
        self.textbox3.resize(50,25)

        # Create textbox
        self.textbox4 = QLineEdit(self)
        self.textbox4.move(100, 110)
        self.textbox4.resize(50,25)

        
        # Create a button in the window
        
        self.button = QPushButton('REC', self)
        self.button.setGeometry(200, 150, 50, 50)
        self.button.move(20,140)
        self.button.setStyleSheet("border-radius : 25; border : 2px solid red") 
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    def on_click(self):

        seconds = int(self.textbox1.text())
        fs = int(self.textbox2.text())
        block = int(self.textbox3.text())
        nfft = int(self.textbox4.text())

        data = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished

        sound=np.array([i[0] for i in data])

        
        
        plotSound(sound,fs,block,nfft)


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
