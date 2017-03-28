# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Udpegning_kontrol_dialog_base.ui'
#
# Created: Tue Mar 28 15:28:34 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Udpegning_kontrolDialogBase(object):
    def setupUi(self, Udpegning_kontrolDialogBase):
        Udpegning_kontrolDialogBase.setObjectName(_fromUtf8("Udpegning_kontrolDialogBase"))
        Udpegning_kontrolDialogBase.resize(391, 185)
        self.button_box = QtGui.QDialogButtonBox(Udpegning_kontrolDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 130, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.groupBox = QtGui.QGroupBox(Udpegning_kontrolDialogBase)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 371, 91))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.inShapeA = QtGui.QComboBox(self.groupBox)
        self.inShapeA.setGeometry(QtCore.QRect(20, 20, 331, 22))
        self.inShapeA.setObjectName(_fromUtf8("inShapeA"))
        self.useSelectedA = QtGui.QCheckBox(self.groupBox)
        self.useSelectedA.setGeometry(QtCore.QRect(30, 60, 181, 17))
        self.useSelectedA.setObjectName(_fromUtf8("useSelectedA"))

        self.retranslateUi(Udpegning_kontrolDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), Udpegning_kontrolDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), Udpegning_kontrolDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(Udpegning_kontrolDialogBase)

    def retranslateUi(self, Udpegning_kontrolDialogBase):
        Udpegning_kontrolDialogBase.setWindowTitle(_translate("Udpegning_kontrolDialogBase", "Udpegning_kontrol", None))
        self.groupBox.setTitle(_translate("Udpegning_kontrolDialogBase", "Layer", None))
        self.useSelectedA.setText(_translate("Udpegning_kontrolDialogBase", "Use only selected features", None))

