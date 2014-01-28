import csv
import urllib2
import feedparser
import bs4

resultsUrls = {
    "csvPrecinct": "http://lasos.blob.core.windows.net/graphical-prod/20140201/csv/ByPrecinct_47474.csv",
    "csvParish": "http://lasos.blob.core.windows.net/graphical-prod/20140201/csv/ByParish_47474.csv",
    "rssParish": "http://lasos.blob.core.windows.net/graphical-prod/rss/02012014_Parish.xml",
    "rssComplete": "http://lasos.blob.core.windows.net/graphical-prod/rss/02012014_RSS.xml"
}


def print_cvs_precinct_summary():
    url_file = urllib2.urlopen(resultsUrls["csvPrecinct"])
    cvs_iter = csv.reader(url_file)

    headers = cvs_iter.next()
    rows = list(cvs_iter)

    print "### CSV Precinct Summary ###"
    print "headers: " + str(headers)
    print "number of precincts: " + str(len(rows))
    print "totals:"
    candidates_cols = [4, 5, 6]
    for i in candidates_cols:
        print "- " + str(sum([int(r[i]) for r in rows])) + ": " + headers[i]


def print_rss_summary():
    feed = feedparser.parse(resultsUrls["rssParish"])
    coroner_item = feed.entries[2]

    soup = bs4.BeautifulSoup(coroner_item.summary)
    names_row = soup.table.find_all('tr')[0].find_all('td')
    totals_row = soup.table.find_all('tr')[2].find_all('td')

    print "### RSS Parish Summary ###"
    print "title: " + coroner_item.title
    for i in [1, 2, 3]:
        votes = int(totals_row[i * 2 - 1].text)
        percentage = totals_row[i * 2].text
        name = names_row[i].text
        print "- {} votes, {}, {}".format(votes, percentage, name)

    print "total votes cast: {}".format(int(totals_row[7].text))
    print totals_row[8].text


print_cvs_precinct_summary()
print
print_rss_summary()
