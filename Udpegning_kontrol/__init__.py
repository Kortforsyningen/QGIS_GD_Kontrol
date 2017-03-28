# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Udpegning_kontrol
                                 A QGIS plugin
 husholdning til udpegninger
                             -------------------
        begin                : 2017-03-21
        copyright            : (C) 2017 by mafal/sdfe
        email                : mafal@sdfe.dk
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Udpegning_kontrol class from file Udpegning_kontrol.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Udpegning_kontrol import Udpegning_kontrol
    return Udpegning_kontrol(iface)
