# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!

import importlib
import solarforecast
solarforecast = importlib.reload(solarforecast)
from solarforecast import FileInf
from solarforecast import SolcastHistorical
from solarforecast import SolcastDataForecast
from solarforecast import EtapData
import os  #access files and so on
import matplotlib
import matplotlib.pyplot as plt
from solarforecast import SolarF
import numpy as np
import keras
import pandas as pd
import datetime
import time
from time import sleep
import schedule
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
        self.temp.setObjectName("AirTemp")
        self.temp.setText("AirTemp")
        self.cloud = QtWidgets.QCheckBox(solarUI)
        self.cloud.setGeometry(QtCore.QRect(30, 170, 111, 20))
        self.cloud.setObjectName("CloudOpacity")
        self.cloud.setText("CloudOpacity")
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
        self.forecast.clicked.connect(self.get_forecast)
        QtCore.QMetaObject.connectSlotsByName(solarUI)
        app.processEvents()

    def __define_features(self):
        features = []
        app.processEvents()
        for i in self.__dict__:
            temp = self.__dict__[i]
            if isinstance(temp, QtWidgets.QCheckBox):
                if temp.isChecked():
                    if temp.text() == 'Air temp':
                        temp.setText('AirTemp')
                    if temp.text() == 'Cloud opacity':
                        temp.setText('CloudOpacity')
                    features.append(temp.text())
        return features

    def __load_whole_data(self):
        etap_power = EtapData(0.8)
        train_times = etap_power.train_data.keys()
        test_times = etap_power.test_data.keys()
        # historical data from solcast
        dst = 'data/solcast_etap_historical.csv'
        hist = SolcastHistorical(dst, train_times, test_times)
        return etap_power ,hist

    def __train_test_by_features(self, selected_features, hist, etap_power):

        train_features = []
        train_label = []
        for i in hist.train.keys():
            selected_data = hist.train[i][selected_features]
            train_features.append(selected_data.values)
            train_label.append(etap_power.train_data[i]['Avg'].values)

        train_features = np.array(train_features)
        train_label = np.array(train_label)

        test_features = []
        test_label = []
        for i in hist.test.keys():
            selected_data = hist.test[i][selected_features]
            test_features.append(selected_data.values)
            test_label.append(etap_power.test_data[i]['Avg'].values)

        test_features = np.array(test_features)
        test_label = np.array(test_label)
        # max min normalization
        powermax = np.max(train_label)
        powermin = np.min(train_label)

        feature_max = train_features.max(axis=(1, 0))
        feature_min = train_features.min(axis=(1, 0))

        ##normalize
        x_train = (train_features - feature_min) / (feature_max - feature_min)
        x_test = (test_features - feature_min) / (feature_max - feature_min)

        y_train = (train_label - powermin) / (powermax - powermin)
        y_test = (test_label - powermin) / (powermax - powermin)

        return x_train, x_test, y_train, y_test


    def get_forecast(self):
        selected_features = self.__define_features()
        etap_power, hist = self.__load_whole_data()
        print(selected_features)
        feature_numbers = len(selected_features)
        resolution = 24
        x_train, x_test, y_train, y_test = self.__train_test_by_features(selected_features, hist, etap_power)
        solar_forecaster = SolarF(feature_numbers, resolution)

        solar_forecaster.opt_ls_mtr(optimizer='adam',
                                    loss='mse',
                                    metric='mse')

        solar_forecaster.train(x_train, y_train, batch=1, epoch=1)
        # evaluation on train set
        solar_forecaster.solar_eval(x_train, y_train)
        # #evaluation on dev set

        solar_forecaster.solar_eval(x_train, y_train)
        # solar_forecaster.solar_eval(x_dev, y_dev)
        solar_forecaster.solar_eval(x_test, y_test)

        print(solar_forecaster.model.summary())
        # solar_forecaster.model.save('models/' + sc)






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
    app.aboutToQuit.connect(app.deleteLater)
    solarUI = QtWidgets.QWidget()
    ui = Ui_solarUI()
    ui.setupUi(solarUI)
    solarUI.show()
    QtWidgets.QApplication.setQuitOnLastWindowClosed(True)
    app.exec_()
    app.quit()

