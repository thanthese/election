## Rouse for Coroner 2014

Aggregate the [official election results][data] for the New Orleans 2014 run for Coroner.

[data]: http://electionresults.sos.la.gov/graphical/

The general steps are these:

- Grab the data from the official site (in CSV form).

- Parse it, do some math.

- `POST` the results to a local [geoserver][geo].

- Repeat often.

At the end of the day we should have a real-time (ish) map of precinct results as they come in

[geo]: http://geoserver.org/display/GEOS/Welcome
