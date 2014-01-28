# data source: http://electionresults.sos.la.gov/graphical/

import csv
import urllib2

resultsUrls = {
    "csvPrecinct": "http://lasos.blob.core.windows.net/graphical-prod/20140201/csv/ByPrecinct_47474.csv",
    "csvParish": "http://lasos.blob.core.windows.net/graphical-prod/20140201/csv/ByParish_47474.csv",
    "rssParish": "http://lasos.blob.core.windows.net/graphical-prod/rss/02012014_Parish.xml",
    "rssComplete": "http://lasos.blob.core.windows.net/graphical-prod/rss/02012014_RSS.xml"
}

def printCsvSummary():
    urlFile = urllib2.urlopen(resultsUrls["csvPrecinct"])
    csvIter = csv.reader(urlFile)

    headers = csvIter.next()
    rows = list(csvIter)

    print "### CSV Precinct Summary ###"
    print "headers: " + str(headers)
    print "number of precincts: " + str(len(rows))

    print "totals:"
    for i in [4, 5, 6]:
        print "- " + str(sum([int(r[i]) for r in rows])) + ": " + headers[i]

printCsvSummary()

