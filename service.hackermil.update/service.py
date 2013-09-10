import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os, urllib, urllib2, re
import time

ADDON = xbmcaddon.Addon()
sys.path.append(xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'), 'resources')))

from addon.common.net   import Net as net
from ga import GA
import downloader
import extract

art = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'), 'resources', 'art'))



xbmc.log('hackermil HackedTV Updater')
current_version = ADDON.getSetting('current_version')
OLC_url = 'http://bitbucket.org/jas0npc_13/jas0npc-repo/raw/master/hackTest/hackedtvVersion.xml'
newVersion = re.findall('hackedtv\sversion=\"(.+?)\"', net().http_GET(OLC_url).content)[0]
GA('None', 'CV: %s NV: %s'%(current_version, newVersion))
xbmc.log('Currently Installed: %s Latest Version Available: %s'%(current_version, newVersion))

if newVersion > current_version:
    xbmc.executebuiltin("XBMC.Notification([COLOR aqua]HackedTV Information[/COLOR],[COLOR aqua]An Update Has Been Found And Will Be Downloaded And Installed[/COLOR],7000,"+os.path.join(art, 'hms.png')+")")
    
    GA("None", "NOTFICatION")
    GA('NOTIF', '12345')
    print 'bigger'
