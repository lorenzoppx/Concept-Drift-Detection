## Part-1-Extract-Data

This part is for collect the data of social networks from Postgres Relational Database of my organization.
This script .ps1 run in Power Shell.
Need only change your string connection at <string-connection>.

<br>
```
& psql <string-connection> -c @"
\copy (select * from ""Post"" p INNER JOIN ""_SubthemePosts"" s ON p.id = s.""A"" INNER JOIN ""Subtheme"" sub ON s.""B"" = sub.""id"" WHERE sub.""themeId"" IN ('66f66240-04a6-4e66-b6bf-1f5b96a8d659', '81c318e3-be77-440a-87dd-21fe9e5fc67e','8109cbac-c756-47bc-a1bc-96498d8d0401','5b981962-a0ca-48fc-b04d-c364eda5fb0a') AND p.time between DATE '2025-04-01' - interval '1 days' and DATE '2025-05-31' + interval '1 days' and p.""socialNetwork"" = 'X' and embedding_openclip_text is not null) TO 'output_vacinal_abril_maio_test.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8');
"@
```
<br>

For run the script:
```
./collect_material_sample.ps1
```