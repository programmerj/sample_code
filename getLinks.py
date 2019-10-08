import time
from time import sleep
from urllib.request import Request, urlopen  # Python 3
from bs4 import BeautifulSoup
import settingsLogging

# curFileId = "20180513"
# curFileId = "20180531"
# curFileId = "20180613"
# curFileId = "20180720"
curFileId = "20180824"

logger = settingsLogging.setupLogger( "info_" + curFileId + ".log", "other_" + curFileId + ".log", "my logger test" )

loadedList = [ ]
fileLinks = open( "siteLinks_" + curFileId + ".csv", "rb" )
curOutIndex = int( time.time() )
fileNamePrefix = "downloadLinks_" + curFileId + "_"
fileHtmlLinks = open( fileNamePrefix + str( curOutIndex ) + ".html", "w" )

curNumProcessedFiles = 0
curNumProcessedFilesGood = 0

for line in fileLinks:
    lineTmp = line.decode( 'utf8' ).strip( " \t\n\r" )
    loadedList.append( lineTmp )

    resLink = ""
    html = ""
    try:
        q = Request( lineTmp )
        q.add_header( "User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0" )
        q.add_header( "Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" )
        html = urlopen( q ).read()
    except Exception as ex:
        resLink = "error1"
        logger.error( lineTmp + "\t" + resLink + "\t" + str( ex ) )
    sleep( 0.01 )

    if resLink != "error1":
        bsObj = BeautifulSoup( html, "html.parser" )
        item = bsObj.find( "a", { "id": "download-btn" } )
        if item is not None:
            resLink = item[ "href" ]
            fileHtmlLinks.write( '<a href="' + resLink + '">' + lineTmp + "</a>" + " " )
            fileHtmlLinks.write( "\n" )
            curNumProcessedFilesGood += 1
        else:
            resLink = "error2"
            logger.error( lineTmp + "\t" + resLink )

    logger.info( lineTmp + "\t" + resLink )

    curNumProcessedFiles += 1
    if (curNumProcessedFiles % 10) == 0:
        logger.info( "sleep" + "\t" + "sleep" )
        sleep( 0.10 )
    if (curNumProcessedFilesGood % 50) == 0:
        fileHtmlLinks.close()
        curOutIndex += 1
        fileHtmlLinks = open( fileNamePrefix + str( curOutIndex ) + ".html", "w" )

print( "loadedList: ", loadedList )
fileLinks.close()
fileHtmlLinks.close()
