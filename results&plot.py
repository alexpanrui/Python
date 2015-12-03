#!/usr/bin/python
# V1, Vsub; I1, Isub; V3, Vd; I3, Id
import numpy as np
import matplotlib as mpl
mpl.use("Qt4Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rcParams
import sys,os,math
from PyQt4.QtGui import (QComboBox, QWidget, QPushButton, QApplication, QFileDialog, QMessageBox, QLabel, QLineEdit)
rcParams.update({'figure.autolayout':True})
filelist = []

class mainUI(QWidget):

    def __init__(self):
        super(mainUI, self).__init__()
        self.btn_browse = QPushButton('Browse',self)
        self.btn_run = QPushButton('Run',self)
        self.lvd_dd = QComboBox(self)
        self.lvsub_dd = QComboBox(self)
        self.lid_dd = QComboBox(self)
        self.lisub_dd = QComboBox(self)
        self.lvd = QLabel('Vd' ,self)
        self.lvsub = QLabel('Vsub', self)
        self.lid = QLabel('Id', self)
        self.lisub = QLabel('Isub', self)
        self.la_vd = QLabel('Step', self)
        self.ln_vd_step = QLineEdit(self)
        self.initUI()

    def initUI(self):
        self.btn_browse.move(60,20)
        self.btn_browse.clicked.connect(self.showFolderDialog)

        self.btn_run.move(60,220)
        self.btn_run.clicked.connect(self.run)
        self.btn_run.setEnabled(False)

        self.lvd.move(38, 64)
        self.lvd_dd.setEditable(True)
        self.lvd_dd.addItems('none x y'.split())
        self.lvd_dd.move(60, 60)

        self.la_vd.move(150, 64)
        self.ln_vd_step.move(180, 60)
        self.ln_vd_step.resize(50,20)

        self.lvsub.move(38, 104)
        self.lvsub_dd.setEditable(True)
        self.lvsub_dd.addItems('none x y'.split())
        self.lvsub_dd.move(60, 100)

        self.lid.move(38, 144)
        self.lid_dd.setEditable(True)
        self.lid_dd.addItems('none x y'.split())
        self.lid_dd.move(60, 140)

        self.lisub.move(38, 184)
        self.lisub_dd.setEditable(True)
        self.lisub_dd.addItems('none x y'.split())
        self.lisub_dd.move(60, 180)

        # self.btn_save = QPushButton('Save', self)
        # self.btn_save.move(60, 100)
        # self.btn_save.clicked.connect(self.save)
        # self.btn_save.setEnabled(False)

        self.setGeometry(300,300,300,260)
        self.setWindowTitle('SnapBack')
        self.show()

    def showFolderDialog(self):
        global filelist
        index = 0
        basex = 60
        basey = 60
        try:
            filelist = QFileDialog.getOpenFileNames(self,'Select Files')
            self.btn_run.setEnabled(True)
            # print(os.path.dirname(os.path.realpath(filelist[0])))
            os.chdir(os.path.dirname(os.path.realpath(filelist[0])))
            # self.chk = QCheckBox('test',self)
            # self.chk.move(basex, basey)
            # self.chk.toggle()
            # self.show()
            # for item in filelist:
            #     basey = basey + (index + 1) * 40
                # self.addchkbox(item, basex, basey)
            # self.update()
            # print(filelist)
        except:
            print(sys.exc_info()[0])

    # def addchkbox(self, item, basex, basey):
    #     base = os.path.basename(item)
    #     l = os.path.splitext(base)[0]
    #     chk = QCheckBox(l,self)
    #     chk.move(basex, basey)
    #     chk.toggle()
        # print(basex)
        # print(basey)

    def run(self):
        global filelist
        # print(filelist)
        # newlist = list(map(self.xtr_plot,filelist))
        if filelist == []:
            QMessageBox.information(self,'Warning', 'Nothing to plot')
            return
        elif self.ln_vd_step.text() == '':
            QMessageBox.information(self, 'Warning', 'Please input step')
            return
        else:
            l_plot = []
            c_plot = []
            if self.lvd_dd.currentText() != 'none':
                l_plot.append('V3')
                c_plot.append(self.lvd_dd.currentText())
            if self.lid_dd.currentText() != 'none':
                l_plot.append('I3')
                c_plot.append(self.lid_dd.currentText())
            if self.lvsub_dd.currentText() != 'none':
                l_plot.append('V1')
                c_plot.append(self.lvsub_dd.currentText())
            if self.lisub_dd.currentText() != 'none':
                l_plot.append('I1')
                c_plot.append(self.lisub_dd.currentText())
            # print(l_plot)
            plt.ion()
            # fig = plt.figure()
            # ax = fig.add_subplot(111)
            # ax.minorticks_on()
            # ax.set_title("Id Vs Vd")
            # ax.set_xlabel('Vd(V)')
            # ax.set_ylabel('Id(A)')
            # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
            # ax.xaxis.set_minor_formatter(mtick.FormatStrFormatter('%.2f'))
            # ax.xaxis.set_minor_locator(mtick.AutoMinorLocator(2))
            # ax.yaxis.set_minor_formatter(mtick.FormatStrFormatter('%.2e'))
            # ax.yaxis.set_minor_locator(mtick.AutoMinorLocator(2))
            #
            # ax.grid(b=True, which='major', color='black', linestyle='-')
            # ax.grid(b=True, which='minor', color='r', linestyle='--')
            # i = 1
            for file in filelist:
                self.xtr_plot(file, l_plot, c_plot)
                # i = i + 1
            # plt.legend()
            # plt.show()
            # print(newlist)
            # self.btn_save.setEnabled(True)
            filelist = []
            return

    def closeEvent(self, QCloseEvent):
        plt.ioff()
        plt.close()
        QApplication.quit()
        sys.exit()

    def xtr_plot(self, item, l_plot, c_plot):
        # print(item)
        data1 = []
        i = 0
        with open(item) as f:
            data = f.read()
        data = data.split('\n')
        # print(data)
        for x in data:
            # if i > 2:
            data1.append(x)
            # i += 1
        i = 0
        while True:
            if '' in data1:
                data1.remove('')
            else:
                break
        del data[:]
        temp = []
        for i in range(0,len(data1)):
            if "NO." in data1[0]:
                temp = data1[0].split('\t')
                del data1[0:2]
                break
            else:
                data1.remove(data1[0])
        x = []
        y = []
        y.append([])
        y.append([])
        for s in l_plot:
            i = temp.index(s)
            # print(i)
            if s == 'V3':
                x = [row.split("\t")[i] for row in data1]
            elif s == 'V1':
                x = [row.split("\t")[i] for row in data1]
            elif s == 'I3':
                y[0] = [row.split("\t")[i] for row in data1]
            elif s == 'I1':
                y[1] = [row.split("\t")[i] for row in data1]
        i = 0

        for s in x:
            s = s.replace("V","")
            s = s.replace(" ","")
            if "f" in s:
                s = s.replace("f","")
                num = float(s)/1000000000000000
            elif "p" in s:
                s = s.replace("p","")
                num = float(s)/1000000000000
            elif "n" in s:
                s = s.replace("n","")
                num = float(s)/1000000000
            elif "u" in s:
                s = s.replace("u","")
                num = float(s)/1000000
            elif "m" in s:
                s = s.replace("m","")
                num = float(s)/1000
            else:
                num = float(s)
            x[i] = num
            i += 1
        # print(x)
        i = 0
        m = 0
        for s in y:
            # print(s)
            if s != []:
                for s1 in s:
                    s1 = s1.replace("A","")
                    s1 = s1.replace(" ","")
                    if "f" in s1:
                        s1 = s1.replace("f","")
                        num = float(s1)/1000000000000000
                    elif "p" in s1:
                        s1 = s1.replace("p","")
                        num = float(s1)/1000000000000
                    elif "n" in s1:
                        s1 = s1.replace("n","")
                        num = float(s1)/1000000000
                    elif "u" in s1:
                        s1 = s1.replace("u","")
                        num = float(s1)/1000000
                    elif "m" in s1:
                        s1 = s1.replace("m","")
                        num = float(s1)/1000
                    else:
                        num = float(s1)
                    y[m][i] = num
                    i += 1
                i = 0
            # print(m)
            # print(y[m])
            m += 1
        i = 0
        m = 0
        base = os.path.basename(item)
        l = os.path.splitext(base)[0]
        l = l.replace('T','')
        w_title = ' '.join(['Vg =', str(int(l)-1),'V'])
        # # print(Vd)
        # # print(Id)
        # print(y[0])
        # print(y[1])
        index = len(x)
        step = int(self.ln_vd_step.text())
        Vsub_step = 100
        cols = 5
        nrows = math.ceil(index/step/5)
        fig, ax = plt.subplots(nrows, cols)
        fig.canvas.set_window_title(w_title)
        ax_row = 0
        ax_col = 0
        max_I = max(y[0])
        if max_I < max(y[1]):
            max_I = max(y[1])
        min_I = min(y[0])
        if min_I > min(y[1]):
            min_I = min(y[0])
        max_V = max(x)
        min_V = min(x)
        Vsub = 0
        while True:
            # ax[ax_row][ax_col] = fig.add_subplot(111)
            # ax[ax_row][ax_col].minorticks_on()
            # ax[ax_row][ax_col].set_title("Id Vs Vd")
            ax[ax_row][ax_col].set_xlabel('Vd(V)')
            ax[ax_row][ax_col].set_ylabel('I(A)')
            ax[ax_row][ax_col].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
            # ax[ax_row][ax_col].xaxis.set_minor_formatter(mtick.FormatStrFormatter('%.2f'))
            # ax[ax_row][ax_col].xaxis.set_minor_locator(mtick.AutoMinorLocator(2))
            # ax[ax_row][ax_col].yaxis.set_minor_formatter(mtick.FormatStrFormatter('%.2e'))
            # ax[ax_row][ax_col].yaxis.set_minor_locator(mtick.AutoMinorLocator(2))

            ax[ax_row][ax_col].grid(b=True, which='major', color='black', linestyle='-')
            # ax[ax_row][ax_col].grid(b=True, which='minor', color='red', linestyle='--')
            m += step
            x_temp = x[i:m]
            ax[ax_row][ax_col].set_autoscale_on(False)
            title = ' '.join(['Vsub=', str(Vsub/1000), 'V'])
            ax[ax_row][ax_col].set_title(title)
            if y[0] != []:
                y_temp = y[0][i:m]
                ax[ax_row][ax_col].plot(x_temp, y_temp, label='Id')
                # ax[ax_row][ax_col].plot(x_temp, y_temp)
                ax[ax_row][ax_col].set_ylim([min_I*1.1, max_I*1.1])
                ax[ax_row][ax_col].set_xlim([min_V, max_V*1.1])
            if y[1] != []:
                y_temp = y[1][i:m]
                ax[ax_row][ax_col].plot(x_temp, y_temp, label='Isub')
                # ax[ax_row][ax_col].plot(x_temp, y_temp)
                ax[ax_row][ax_col].set_ylim([min_I*1.1, max_I*1.1])
                ax[ax_row][ax_col].set_xlim([min_V, max_V*1.1])
            # plt.legend()
            ax[ax_row][ax_col].legend(prop={'size':10})
            plt.show()
            i = m
            ax_col += 1
            Vsub += Vsub_step
            if ax_col >= cols:
                ax_col = 0
                ax_row += 1
            if i >= index:
                break

        # if y[0] != []:
        #     y_temp = y[0][0:211]
        #     ax.plot(x[0:211], y_temp, label=l)
        # if y[1] != []:
        #     y_temp = y[1][0:211]
        #     ax.plot(x[0:211], y_temp, label=l)


    # def save(self):
    #     return
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainUI()
    app.exec_()



