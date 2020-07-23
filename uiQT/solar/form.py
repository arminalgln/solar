# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_solarUI(object):
    def setupUi(self, solarUI):
        solarUI.setObjectName("solarUI")
        solarUI.resize(800, 600)
        self.log = QtWidgets.QTextBrowser(solarUI)
        self.log.setGeometry(QtCore.QRect(10, 451, 771, 141))
        self.log.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.log.setFrameShadow(QtWidgets.QFrame.Plain)
        self.log.setObjectName("log")
        self.listView = QtWidgets.QListView(solarUI)
        self.listView.setGeometry(QtCore.QRect(10, 10, 131, 381))
        self.listView.setObjectName("listView")
        self.listView_2 = QtWidgets.QListView(solarUI)
        self.listView_2.setGeometry(QtCore.QRect(160, 10, 131, 381))
        self.listView_2.setObjectName("listView_2")
        self.forecast = QtWidgets.QPushButton(solarUI)
        self.forecast.setGeometry(QtCore.QRect(62, 410, 191, 28))
        self.forecast.setObjectName("forecast")
        self.Ghi = QtWidgets.QCheckBox(solarUI)
        self.Ghi.setEnabled(True)
        self.Ghi.setGeometry(QtCore.QRect(30, 80, 81, 20))
        self.Ghi.setChecked(False)
        self.Ghi.setTristate(False)
        self.Ghi.setObjectName("Ghi")
        self.Dni = QtWidgets.QCheckBox(solarUI)
        self.Dni.setGeometry(QtCore.QRect(30, 110, 81, 20))
        self.Dni.setObjectName("Dni")
        self.temp = QtWidgets.QCheckBox(solarUI)
        self.temp.setGeometry(QtCore.QRect(30, 140, 81, 20))
        self.temp.setObjectName("temp")
        self.cloud = QtWidgets.QCheckBox(solarUI)
        self.cloud.setGeometry(QtCore.QRect(30, 170, 111, 20))
        self.cloud.setObjectName("cloud")
        self.tabWidget = QtWidgets.QTabWidget(solarUI)
        self.tabWidget.setGeometry(QtCore.QRect(330, 10, 451, 421))
        self.tabWidget.setObjectName("tabWidget")
        self.fview = QtWidgets.QWidget()
        self.fview.setObjectName("fview")
        self.View = QtWidgets.QGraphicsView(self.fview)
        self.View.setGeometry(QtCore.QRect(0, 0, 441, 391))
        self.View.setObjectName("View")
        self.tabWidget.addTab(self.fview, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.days = QtWidgets.QSlider(solarUI)
        self.days.setGeometry(QtCore.QRect(140, 30, 160, 341))
        self.days.setMinimum(1)
        self.days.setMaximum(7)
        self.days.setPageStep(1)
        self.days.setProperty("value", 4)
        self.days.setSliderPosition(4)
        self.days.setTracking(True)
        self.days.setOrientation(QtCore.Qt.Vertical)
        self.days.setInvertedAppearance(False)
        self.days.setInvertedControls(False)
        self.days.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.days.setTickInterval(1)
        self.days.setObjectName("days")

        self.retranslateUi(solarUI)
        self.tabWidget.setCurrentIndex(0)
        self.forecast.clicked.connect(self.View.show)
        QtCore.QMetaObject.connectSlotsByName(solarUI)

    def retranslateUi(self, solarUI):
        _translate = QtCore.QCoreApplication.translate
        solarUI.setWindowTitle(_translate("solarUI", "solarUI"))
        self.forecast.setText(_translate("solarUI", "Forecast"))
        self.Ghi.setText(_translate("solarUI", "Ghi"))
        self.Dni.setText(_translate("solarUI", "Dni"))
        self.temp.setText(_translate("solarUI", "Air temp"))
        self.cloud.setText(_translate("solarUI", "Cloud opacity"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.fview), _translate("solarUI", "Forecast Display"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("solarUI", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    solarUI = QtWidgets.QWidget()
    ui = Ui_solarUI()
    ui.setupUi(solarUI)
    solarUI.show()
    sys.exit(app.exec_())
