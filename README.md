This is a scraper for [active emergency incidents in Houston](http://cohweb.houstontx.gov/ActiveIncidents/Combined.aspx). I wrote this code a long time ago and it's been doing its thing quietly via cron ever since. You won't be surprised to learn that there have been a lot of dumpster fires in 2020.

```sql
SELECT UPPER(incident_type) AS description, COUNT(*) AS count FROM report WHERE call_time LIKE '%/%/2020 %:%' AND description LIKE '%FIRE%' GROUP BY description ORDER BY count DESC LIMIT 10;
FIRE EVENT|20815
CAR FIRE|3394
APARTMENT FIRE|3055
TRASH FIRE|2964
HOUSE ON FIRE|2148
BUILDING FIRE|1528
DUMPSTER ON FIRE|1160
GRASS FIRE|1010
CHECK FOR FIRE|422
TREE ON FIRE|406
```
