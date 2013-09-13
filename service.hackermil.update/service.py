import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os, urllib, urllib2, re
import time

ADDON = xbmcaddon.Addon(id='service.hackermil.update')
sys.path.append(xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'), 'resources')))

from addon.common.net   import Net as net
from ga import *
import downloader
import extract

art = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'), 'resources', 'art'))
baseUrl = 'https://drive.google.com/folderview?id=0B7glCX3gJUKIMW5HQ1Y4bWxQY3c&usp=sharing'
downloadUrl = 'https://docs.google.com/uc?export=download&id='
downloadPath = xbmc.translatePath(os.path.join('special://home/addons','packages'))
SettingsPath = xbmc.translatePath(os.path.join('special://home/userdata','HackedTvSettings.xml'))

f = open (SettingsPath,'r')
HackedTvSettings = f.read()
f.close()
print HackedTvSettings


html = net().http_GET(baseUrl).content
r = re.findall(r'id=\"entry\-(.+?)\"\stabindex=\"\d\"\saria\-label=\"Name\:\s(.+?)\,', html, re.I|re.M|re.DOTALL)
for Gid, name in r:#Gid = google file id
    if name == 'updateUrl.xml':
        TUUrl = re.findall(r'\<url\>(.+?)\<\/url\>', net().http_GET(downloadUrl+Gid).content, re.I)[0]
        UpdateUrl = re.findall(r'action="(.+?)"', net().http_GET(TUUrl).content, re.I)[0]
        UpdateName ='hackedtvupdater.zip'
        print '++++++++++++++++++'+UpdateUrl
    if name == 'hackedtvVersion.xml':NewVersionUrl=downloadUrl+Gid
    if name == 'changelog.txt':ChangeLogUrl=downloadUrl+Gid
    

print ChangeLogUrl
print NewVersionUrl
print UpdateUrl

def QuietDownload(url, dest,originalName, videoname):
    print 'QD: %s %s %s %s'%(url, dest, originalName, videoname)
    script = os.path.join( ADDON.getAddonInfo('path'), 'resources', "DownloadInBackground.py" )
    xbmc.executebuiltin( "RunScript(%s, %s, %s, %s)" % ( script, UpdateUrl, downloadPath, UpdateName))
    return True

class TextBox:
    # constants
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__(self, *args, **kwargs):
        xbmc.executebuiltin("ActivateWindow(%d)" % ( self.WINDOW, ))
        self.win = xbmcgui.Window(self.WINDOW)
        xbmc.sleep(1000)
        self.setControls()

    def setControls(self):
        heading = "[COLOR aqua]HackedTV Change Log Information[/COLOR]"
        self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
        text = re.findall(r'<start>(.+?)<end>', net().http_GET(ChangeLogUrl).content, re.I|re.M|re.DOTALL)[0]
        self.win.getControl(self.CONTROL_TEXTBOX).setText(text)


#f = open(HackedTvSettings)
#f.read()
CurrrentVersion = re.findall(r'<hackedtvversion>(\d+)</hackedtvversion>', HackedTvSettings, re.I)
#f.close()

print CurrrentVersion
LatestVersion = re.findall('hackedtv\sversion=\"(.+?)\"', net().http_GET(NewVersionUrl).content)[0]
print CurrrentVersion
print LatestVersion

if LatestVersion > CurrrentVersion:
    xbmc.log('hackermil HackedTV Updater')
    xbmc.log('Currently Installed: %s Latest Version Available: %s'%(CurrrentVersion, LatestVersion))
    xbmc.executebuiltin("XBMC.Notification([COLOR aqua]HackedTV Information[/COLOR],[COLOR aqua]An Update Has Been Found And Will Be Downloaded And Installed[/COLOR],7000,"+os.path.join(art, 'hms.png')+")")
    GA('TEST', 'CV: %s NV: %s'%(CurrrentVersion, LatestVersion))
    xbmc.sleep(4000)
    TextBox()
    downloadFile = os.path.join(downloadPath, UpdateName)
    try: os.remove(downloadFile)
    except:pass
    GA('TEST', 'DISPLAY CHANGELOG')
    print 'DL PATH: '+str(downloadPath)
    print 'DF path: '+str(downloadFile)
    QuietDownload(UpdateUrl, downloadPath, UpdateName, UpdateName)







#xbmc.log('hackermil HackedTV Updater')
#
#OLC_url = 'http://bitbucket.org/jas0npc_13/jas0npc-repo/raw/master/hackTest/hackedtvVersion.xml'
#newVersion = re.findall('hackedtv\sversion=\"(.+?)\"', net().http_GET(OLC_url).content)[0]
#GA('None', 'CV: %s NV: %s'%(current_version, newVersion))
#xbmc.log('Currently Installed: %s Latest Version Available: %s'%(current_version, newVersion))
#
#if newVersion > current_version:
#    xbmc.executebuiltin("XBMC.Notification([COLOR aqua]HackedTV Information[/COLOR],[COLOR aqua]An Update Has Been Found And Will Be Downloaded And Installed[/COLOR],7000,"+os.path.join(art, 'hms.png')+")")
    
#    GA("None", "NOTFICatION")
#    GA('NOTIF', '12345')
#    print 'bigger'
