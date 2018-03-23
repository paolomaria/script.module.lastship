# -*- coding: UTF-8 -*-

"""
    Lastship Add-on (C) 2017
    Credits to Placenta and Covenant; our thanks go to their creators

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Addon Name: lastship
# Addon id: plugin.video.lastship
# Addon Provider: LastShip

import urllib
import os
import json
import zipfile
import xbmc
from xbmc import translatePath
from resources.lib.modules import control
from resources.lib.modules import log_utils
import xbmcgui

## script.module.lastship
REMOTE_MODULE_COMMITS = "https://api.github.com/repos/lastship/script.module.lastship/commits/nightly"
REMOTE_MODULE_DOWNLOADS = "https://github.com/lastship/script.module.lastship/archive/nightly.zip"

## plugin.video.lastship
REMOTE_PLUGIN_COMMITS = "https://api.github.com/repos/lastship/plugin.video.lastship/commits/nightly"
REMOTE_PLUGIN_DOWNLOADS = "https://github.com/lastship/plugin.video.lastship/archive/nightly.zip"

## Filename of the update File.
profilePath = translatePath(control.addon('plugin.video.lastship').getAddonInfo('profile')).decode('utf-8')
LOCAL_PLUGIN_VERSION = os.path.join(profilePath, "plugin_commit_sha")
LOCAL_MODULE_VERSION = os.path.join(profilePath, "module_commit_sha")
ADDON_DIR = os.path.abspath(os.path.join(translatePath(control.addon('plugin.video.lastship').getAddonInfo('path')).decode('utf-8'), '..'))
LOCAL_FILE_NAME_PLUGIN = os.path.join(profilePath, 'update_plugin.zip')
LOCAL_FILE_NAME_MODULE = os.path.join(profilePath, 'update_module.zip')

def scriptmoduleLastship():
    name = 'script.module.lastship'
    path = control.addon(name).getAddonInfo('Path')
    commitXML = _getXmlString(REMOTE_MODULE_COMMITS)
    if commitXML:
        commitUpdate(commitXML, LOCAL_MODULE_VERSION, REMOTE_MODULE_DOWNLOADS, path, "Updating " + name, LOCAL_FILE_NAME_MODULE)
        xbmcgui.Dialog().ok('LastShip', name+ "-Update Erfolgreich.")
    else:
        xbmcgui.Dialog().ok('LastShip', 'Fehler beim ' + name+ "-Update.")

def pluginVideoLastship():
    name = 'plugin.video.lastship'
    path = control.addon(name).getAddonInfo('Path')
    commitXML = _getXmlString(REMOTE_PLUGIN_COMMITS)
    if commitXML:
        commitUpdate(commitXML, LOCAL_PLUGIN_VERSION, REMOTE_PLUGIN_DOWNLOADS, path, "Updating " + name, LOCAL_FILE_NAME_PLUGIN)
        xbmcgui.Dialog().ok('LastShip', name+ "-Update Erfolgreich.")
    else:
        xbmcgui.Dialog().ok('LastShip', 'Fehler beim ' + name+ "-Update.")

def commitUpdate(onlineFile, offlineFile, downloadLink, LocalDir, Title, localFileName):
    try:
        jsData = json.loads(onlineFile)
        if not os.path.exists(offlineFile) or open(offlineFile).read() != jsData['sha']:
            update(LocalDir, downloadLink, Title, localFileName)
            open(offlineFile, 'w').write(jsData['sha'])
    except Exception as e:
        os.remove(offlineFile)
        log_utils.log("RateLimit reached")

def update(LocalDir, REMOTE_PATH, Title, localFileName):

    try:
        from urllib2 import urlopen
        f = urlopen(REMOTE_PATH)

        # Open our local file for writing
        with open(localFileName, "wb") as local_file:
            local_file.write(f.read())
    except:
        log_utils.log("DevUpdate not possible due download error")

    updateFile = zipfile.ZipFile(localFileName)

    removeFilesNotInRepo(updateFile, LocalDir)

    for index, n in enumerate(updateFile.namelist()):
        if n[-1] != "/":
            dest = os.path.join(LocalDir, "/".join(n.split("/")[1:]))
            destdir = os.path.dirname(dest)
            if not os.path.isdir(destdir):
                os.makedirs(destdir)
            data = updateFile.read(n)
            if os.path.exists(dest):
                os.remove(dest)
            f = open(dest, 'wb')
            f.write(data)
            f.close()
    updateFile.close()
    os.remove(localFileName)
    xbmc.executebuiltin("XBMC.UpdateLocalAddons()")

def removeFilesNotInRepo(updateFile, LocalDir):
    ignored_files = ['settings.xml']
    updateFileNameList = [i.split("/")[-1] for i in updateFile.namelist()]

    for root, dirs, files in os.walk(LocalDir):
        if ".git" in root or "pydev" in root or ".idea" in root:
            continue
        else:
            for file in files:
                if file in ignored_files:
                    continue
                if file not in updateFileNameList:
                    os.remove(os.path.join(root, file))

def _getXmlString(xml_url):
    try:
        xmlString = urllib.urlopen(xml_url).read()
        if "sha" in json.loads(xmlString):
            return xmlString
        else:
            log_utils.log("Update-URL incorrect")
    except Exception as e:
        log_utils.log(e)

def updateLastShip():
    try:
        scriptmoduleLastship()
        pluginVideoLastship()
        log_utils.log("DevUpdate Complete")
    except Exception as e:
        log_utils.log(e)
