# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Udpegning_kontrol
                                 A QGIS plugin
 husholdning til udpegninger
                              -------------------
        begin                : 2017-03-21
        git sha              : $Format:%H$
        copyright            : (C) 2017 by mafal/sdfe
        email                : mafal@sdfe.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
from osgeo import gdal, osr
import re, os
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from Udpegning_kontrol_dialog import Udpegning_kontrolDialog
import os.path


class Udpegning_kontrol:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Udpegning_kontrol_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = Udpegning_kontrolDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Udpegning_kontrol')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Udpegning_kontrol')
        self.toolbar.setObjectName(u'Udpegning_kontrol')

        QObject.connect(self.dlg.inShapeA, SIGNAL("currentIndexChanged(QString)" ), self.checkA )

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Udpegning_kontrol', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Udpegning_kontrol/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GD_udpegninger'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Udpegning_kontrol'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

 #   def to_unicode(in_string):
 #       if isinstance(in_string, str):
 #           out_string = in_string.decode('utf-8')
 #       elif isinstance(in_string, unicode):
 #           out_string = in_string
 #       else:
 #           raise TypeError('not stringy')
 #       return out_string

    def checkA( self ):
        inputFilNavn = unicode( self.dlg.inShapeA.currentText() )
        canvas = self.iface.mapCanvas()
        allLayers = canvas.layers()

        for i in allLayers:
            if(i.name() == inputFilNavn):
                if i.selectedFeatureCount() != 0:
                    self.dlg.useSelectedA.setCheckState( Qt.Checked )
                else:
                    self.dlg.useSelectedA.setCheckState( Qt.Unchecked )

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        # populate layer list


        mapCanvas = self.iface.mapCanvas()
        lyrs = self.iface.legendInterface().layers()
        lyr_list = []
        for layer in lyrs:
            lyr_list.append(layer.name())
        self.dlg.inShapeA.clear()
        self.dlg.inShapeA.addItems(lyr_list)

        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            inputLayer = unicode(self.dlg.inShapeA.currentText())
            inputFilNavn = self.dlg.inShapeA.currentText()
            canvas = self.iface.mapCanvas()
            allLayers = canvas.layers()
            try:
                count = 0

                for i in allLayers:
                    if (i.name() == inputFilNavn):
                        layer = i
                        geomtype = layer.geometryType()
                        # Check fileformat conformity
                        n = 0
                        features = layer.getFeatures()
                        f = features.next()
                        AttributesList = [c.name() for c in f.fields().toList()]
                        PossibleValues = ['Aar', 'Nummer', 'Kilde','Aktion','OBJ_type','Foretaget']
                        for s in PossibleValues:
                            if s in AttributesList:
                                n = n + 1
                        ld1 = len(AttributesList) - n
                        ld2 = n - len(AttributesList)
                        if ld1 == 0:
                            NameFailCount = 0
                            #QMessageBox.information(None, "status", "File conforms to SDFE standard!")
                        elif len(AttributesList) != n:
                            QMessageBox.information(None, "status","Files is missing some attributes. \n Check that the following fields are pressent in the attributes table header: \n 'Aar', 'Nummer', 'Kilde','Aktion','OBJ_type','Foretaget'")
                            return
                        else:
                            NameFailCount = len(ld1)
                            whatfailed = "The following attributes did not conrform to standard: \n"
                            for x in range(0, NameFailCount):
                                whatfailed = whatfailed + "Value in File:\t \t" + ld2[x] + "\n SDFE Standard:\t" + ld1[x] + "\n \n"
                            QMessageBox.information(None, "status","File does not conforms to SDFE standard! Check aborted \n \n" + whatfailed)
                            return

                        # create virtual layer
                        vl = QgsVectorLayer("Point", "udpegning-check: " + str(inputFilNavn), "memory")
                        pr = vl.dataProvider()
                        commentCount = 0
                        GSDfailCount = 0
                        SUNfailCount = 0
                        TILTfailCount = 0
                        REFfailCount = 0
                        FeatFailCount = 0
                        # vl.startEditing()
                        # add fields
                        pr.addAttributes([QgsField("Aar", QVariant.String),
                                          QgsField("Nummer", QVariant.String),
                                          QgsField("Kilde", QVariant.String),
                                          QgsField("Aktion", QVariant.String),
                                          QgsField("OBJ_type", QVariant.String),
                                          QgsField("Foretaget", QVariant.String)])
                        if self.dlg.useSelectedA.isChecked():
                            selection = layer.selectedFeatures()
                            QMessageBox.information(None, "status", "checking selected features")
                        else:
                            selection = layer.getFeatures()
                            QMessageBox.information(None, "status", "checking all features")

                        # Define features for name-format checker
                        FeatAarFailCount = 0
                        FeatNummerFailCount = 0
                        FeatKildeFailCount = 0
                        FeatAktionFailCount = 0
                        FeatOBJFailCount= 0
                        FeatForetagetFailCount = 0
                        AarString = ''
                        NummerString = ''
                        KildeString = ''
                        AktionString = ''
                        OBJString = ''
                        ForetagetString = ''

                        for feat in selection:
                            #Define pattern for variables
                            PatternAar = re.compile('[0-9]{4}$')
                            PatternNummer1 = re.compile('[1-9]$')
                            PatternNummer2 = re.compile('[0-9]{2,9}$')
                            PatternKilde = re.compile('.{1,20}$')
                            PatternOBJ = re.compile('[a-zA-Z\xe6\xf8\xe5\xc6\xd8\xc5 _]{1,30}$')
                            # check name format
                            NameFormat = 'Not Checked'
                            Aar = feat['Aar']
                            Nummer = feat['Nummer']
                            Kilde = feat['kilde']
                            Aktion = feat['Aktion']
                            OBJ_type = feat['OBJ_type']
                            Foretaget = feat['Foretaget']
                            TempList = ['ny','Ny','NY','ikke tildelt','Ikke tildelt','Ikke Tildelt','IKKE TILDELT','slet','Slet','SLET','aendre geometri','AEndre geometri','AEndre Geometri','AENDRE GEOMETRI']
                            AktionList=[]
                            for i in TempList:
                                s = i.decode('utf-8')
                                if s == 'aendre geometri':
                                    s = u'\xe6ndre geometri'
                                elif s == 'AEndre geometri':
                                    s = u'\xc6ndre geometri'
                                elif s == 'AEndre Geometri':
                                    s = u'\xc6ndre geometri'
                                elif s == 'AENDRE GEOMETRI':
                                    s = u'\xc6NDRE GEOMETRI'
                                AktionList.append(s)


                            if PatternAar.match(str(Aar)):
                                AarString = "Aar - OK"
                            else:
                                AarString = "Aar - Fejl"
                                FeatAarFailCount = FeatAarFailCount + 1

                            if Nummer == '0':
                                NummerString = 'error - Number must not be 0'
                                FeatNummerFailCount = FeatNummerFailCount + 1
                            else:
                                if PatternNummer1.match(str(Nummer)):
                                    NummerString = "Nummer - OK"
                                elif PatternNummer2.match(str(Nummer)):
                                    NummerString = "Nummer - OK"
                                else:
                                    NummerString = "Nummer - Fejl"
                                    FeatNummerFailCount = FeatNummerFailCount + 1


                            if PatternKilde.match(Kilde):
                                KildeString = "Kilde - OK"
                            else:
                                KildeString = "Kilde - Fejl"
                                FeatKildeFailCount = FeatKildeFailCount +1

                            if Aktion in AktionList:
                                AktionString = 'Aktion - OK'
                            else:
                                AktionString = 'Aktion - Fejl'
                                FeatAktionFailCount = FeatAktionFailCount +1

                            if OBJ_type == '':
                                OBJString = 'OBJ_type  - OK'
                            elif PatternOBJ.match(str(OBJ_type)):
                                OBJString = 'OBJ_type - OK'
                            else:
                                OBJString = 'OBJ_type - Fejl'
                                FeatOBJFailCount = FeatOBJFailCount + 1

                            if Foretaget == 'NY':
                                ForetagetString = 'Foretaget  - OK'
                            elif Foretaget == 'ny':
                                ForetagetString = 'Foretaget - OK'
                            elif Foretaget == 'Ny':
                                ForetagetString = 'Foretaget - OK'
                            else:
                                ForetagetString = 'Foretaget - Fejl'
                                FeatForetagetFailCount = FeatForetagetFailCount + 1

                            if str(geomtype) == '0':
                                geom = feat.geometry().centroid()
                                Geometri = geom.asPoint()
                                # add a feature
                                newfeat = QgsFeature()
                                newfeat.setGeometry(QgsGeometry.fromPoint(Geometri))
                            elif str(geomtype) == '1':
                                geom = feat.geometry()
                                Geometri = geom.asPolyline()
                                newfeat = QgsFeature()
                                newfeat.setGeometry(QgsGeometry.fromPolyline(Geometri))
                            elif str(geomtype) == '2':
                                geom = feat.geometry()
                                Geometri = geom.asPolygon()
                                newfeat = QgsFeature()
                                newfeat.setGeometry(QgsGeometry.fromPolygon(Geometri))
                            try:
                                newfeat.setAttributes([AarString,NummerString,KildeString,AktionString,OBJString,ForetagetString])
                            except (RuntimeError, TypeError, NameError, ValueError):
                                QMessageBox.information(None, "General Error", "PPC Format errors found, exiting!")
                                return

                            pr.addFeatures([newfeat])

                            # update layer's extent when new features have been added
                            # because change of extent in provider is not propagated to the layer
                        vl.updateExtents()
                        vl.updateFields()
                        QgsMapLayerRegistry.instance().addMapLayer(vl)

                        rapporten = "Check of: \n" + inputFilNavn + "\n \nThere was found: \n"
                        rapporten = rapporten + str(FeatAarFailCount) + " Fejl i Aar kolonne \n"
                        rapporten = rapporten + str(FeatNummerFailCount) + " Fejl i Nummer kolonne \n"
                        rapporten = rapporten + str(FeatKildeFailCount) + " Fejl i Kilde kolonne \n"
                        rapporten = rapporten + str(FeatAktionFailCount) + " Fejl i Aktion kolonne \n"
                        rapporten = rapporten + str(FeatOBJFailCount) + " Fejl i OBJ_typr kolonne \n"
                        rapporten = rapporten + str(FeatForetagetFailCount) + " Fejl i Foretaget kolonne \n"

                        #if GSDfailCount + SUNfailCount + TILTfailCount + REFfailCount + FeatFailCount == 0:
                        QMessageBox.information(self.iface.mainWindow(), 'Aendrings_udpegning_rapport', rapporten)
                        #else:
                        #    QMessageBox.critical(self.iface.mainWindow(), 'PPC check', rapporten)
                        #self.dlg.close()
                        #return
            #                        QMessageBox.information(None, "status", str(AttributesList))
            except (RuntimeError, TypeError, NameError):  # , ValueError):
                QMessageBox.information(None, "General Error", "General file error V2.1, please check that you have choosen the correct PPC file")
                return