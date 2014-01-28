# Rouse for Coroner 2014

Aggregate the [official election results][data] for the New Orleans 2014 run for Coroner.

[data]: http://electionresults.sos.la.gov/graphical/

# output (subject to wild change)

Demonstrates that we're correctly parsing data from the CSS and RSS feeds. Now that the data is pulled in, we can do whatever we want with it. (We'll probably end up POSTing it to Geoserver using the [requests][req] library.)

[req]: http://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests

    ### CSV Precinct Summary ###
    headers: ['Office', 'Parish', 'Ward', 'Precinct', 'Vincent A. Culotta, Jr. (DEM)', 'Dwight McKenna (DEM)', 'Jeffrey Rouse (DEM)']
    number of precincts: 367
    totals:
    - 0: Vincent A. Culotta, Jr. (DEM)
    - 0: Dwight McKenna (DEM)
    - 0: Jeffrey Rouse (DEM)

    ### RSS Parish Summary ###
    title: Orleans: Coroner (1 to be Elected)
    - 0 votes, 0%, Vincent A. Culotta, Jr. (D)
    - 0 votes, 0%, Dwight McKenna (D)
    - 0 votes, 0%, Jeffrey Rouse (D)
    total votes cast: 0
    0 of 366 precincts reporting

