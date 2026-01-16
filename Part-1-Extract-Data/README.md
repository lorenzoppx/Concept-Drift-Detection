## Part-1-Extract-Data

This part is for collect the data of social networks from Postgres Relational Database of my organization.
This script .ps1 run in Power Shell.
Need only change your string connection at <string-connection>.
```
& psql <string-connection> -c @"
\copy (select * from ""Post"" p INNER JOIN ""_SubthemePosts"" s ON p.id = s.""A"") TO 'output.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8');
"@
```
For run the script, open a PowerShell and put:
```
./collect_material_sample.ps1
```
