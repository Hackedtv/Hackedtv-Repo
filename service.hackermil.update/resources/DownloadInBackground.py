import sys, os, time
import urllib
import xbmc, xbmcgui, xbmcaddon
from traceback import print_exc
from addon.common.net   import Net as net
from ga import *

addon_id = 'service.hackermil.update'
ADDON = xbmcaddon.Addon(id=addon_id)
#addon = Addon(addon_id)

class StopDownloading(Exception): 
    def __init__(self, value): 
        self.value = value 
    def __str__(self): 
        return repr(self.value)


UpdateUrl = (sys.argv[1])
downloadPath = (sys.argv[2])
UpdateName = (sys.argv[3])
NotifyPercent = int(10)
print 'Setting NotifyPercent every : ' + str(NotifyPercent)
print UpdateUrl
   
DeleteIncomplete = 'true'
art = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'), 'resources', 'art'))
NotifyPercents = range(0, 100 + NotifyPercent, NotifyPercent)
start_time = time.time()

DownloadFile=os.path.join(downloadPath, UpdateName)

print '----------'
print DownloadFile

def Notification(currentPercent):
    if currentPercent in NotifyPercents:
        try: del NotifyPercents[NotifyPercents.index(currentPercent)]
        except: 
            print 'Could not clean Notified percents .....'
            pass
        icon_file =os.path.join(art, 'hackedtv.png')
        print '        Download progress...' + str(currentPercent)+'% for file ' + UpdateName
        xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i,%s)" % ( 'Download Progress - ' + str(currentPercent)+'%', UpdateName, 5000,os.path.join(art, 'hackedtv.png') ) )

def progress(numblocks, blocksize, filesize, start_time):    
    try:        
        percent = min(numblocks * blocksize * 100 / filesize, 100)
        Notification(percent)
    except:
        print_exc()

try:
    urllib.urlretrieve(UpdateUrl, DownloadFile, lambda nb, bs, fs: progress(nb, bs, fs, start_time))
    open(DownloadFile,'a').write('{name="%s",destination="%s"}'%(UpdateName,downloadPath))
except:
    if DeleteIncomplete == 'true':
        while os.path.exists(DownloadFile):
            try: 
                os.remove(DownloadFile) 
                break 
            except: 
                pass

    dialog = xbmcgui.Dialog()
    dialog.ok('Error in download', 'There was an error downloading file ' + UpdateName)
