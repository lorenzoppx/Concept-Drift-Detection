#!ps1

# Script ps1 for collect data from Labic's DB

# Command for execute ps1:
# powershell -ExecutionPolicy Bypass -File collect_material.ps1

###################################
#   Collect data from Labic MMA   #
###################################

# Janeiro e fevereiro - Train
& psql <string-connection> -c @"
\copy (select * from ""Post"" p INNER JOIN ""_SubthemePosts"" s ON p.id = s.""A"" INNER JOIN ""Subtheme"" sub ON s.""B"" = sub.""id"" WHERE sub.""themeId"" IN ('d8b03074-29ce-4604-8491-30e5536dc49b', '702f2236-ba9f-4015-a2ca-fef108d4e7b6','7fe7c27a-c456-4ce3-a52b-26ca991e9a64','837a32ed-4ac9-4fb8-924d-440aa3e2a778') AND p.time between DATE '2025-01-01' - interval '1 days' and DATE '2025-02-28' + interval '1 days' and p.""socialNetwork"" = 'X' and embedding_openclip_text is not null) TO 'output_mma_jan_fev_train.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8');
"@
# Março - Validation
& psql <string-connection> -c @"
\copy (select * from ""Post"" p INNER JOIN ""_SubthemePosts"" s ON p.id = s.""A"" INNER JOIN ""Subtheme"" sub ON s.""B"" = sub.""id"" WHERE sub.""themeId"" IN ('d8b03074-29ce-4604-8491-30e5536dc49b', '702f2236-ba9f-4015-a2ca-fef108d4e7b6','7fe7c27a-c456-4ce3-a52b-26ca991e9a64','837a32ed-4ac9-4fb8-924d-440aa3e2a778') AND p.time between DATE '2025-03-01' - interval '1 days' and DATE '2025-03-31' + interval '1 days' and p.""socialNetwork"" = 'X' and embedding_openclip_text is not null) TO 'output_mma_mar_val.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8');
"@
# Abril e Maio - Test
& psql <string-connection> -c @"
\copy (select * from ""Post"" p INNER JOIN ""_SubthemePosts"" s ON p.id = s.""A"" INNER JOIN ""Subtheme"" sub ON s.""B"" = sub.""id"" WHERE sub.""themeId"" IN ('d8b03074-29ce-4604-8491-30e5536dc49b', '702f2236-ba9f-4015-a2ca-fef108d4e7b6','7fe7c27a-c456-4ce3-a52b-26ca991e9a64','837a32ed-4ac9-4fb8-924d-440aa3e2a778') AND p.time between DATE '2025-04-01' - interval '1 days' and DATE '2025-05-31' + interval '1 days' and p.""socialNetwork"" = 'X' and embedding_openclip_text is not null) TO 'output_mma_abril_maio_test.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8');
"@

###################################
# Collect data from Labic Vacinal #
###################################

# Janeiro e fevereiro - Train
& psql <string-connection> -c @"
\copy (select * from ""Post"" p INNER JOIN ""_SubthemePosts"" s ON p.id = s.""A"" INNER JOIN ""Subtheme"" sub ON s.""B"" = sub.""id"" WHERE sub.""themeId"" IN ('66f66240-04a6-4e66-b6bf-1f5b96a8d659', '81c318e3-be77-440a-87dd-21fe9e5fc67e','8109cbac-c756-47bc-a1bc-96498d8d0401','5b981962-a0ca-48fc-b04d-c364eda5fb0a') AND p.time between DATE '2025-01-01' - interval '1 days' and DATE '2025-02-28' + interval '1 days' and p.""socialNetwork"" = 'X' and embedding_openclip_text is not null) TO 'output_vacinal_jan_fev_train.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8');
"@

# Março - Validation
& psql <string-connection> -c @"
\copy (select * from ""Post"" p INNER JOIN ""_SubthemePosts"" s ON p.id = s.""A"" INNER JOIN ""Subtheme"" sub ON s.""B"" = sub.""id"" WHERE sub.""themeId"" IN ('66f66240-04a6-4e66-b6bf-1f5b96a8d659', '81c318e3-be77-440a-87dd-21fe9e5fc67e','8109cbac-c756-47bc-a1bc-96498d8d0401','5b981962-a0ca-48fc-b04d-c364eda5fb0a') AND p.time between DATE '2025-03-01' - interval '1 days' and DATE '2025-03-31' + interval '1 days' and p.""socialNetwork"" = 'X' and embedding_openclip_text is not null) TO 'output_vacinal_mar_val.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8');
"@

# Abril e Maio - Test
& psql <string-connection> -c @"
\copy (select * from ""Post"" p INNER JOIN ""_SubthemePosts"" s ON p.id = s.""A"" INNER JOIN ""Subtheme"" sub ON s.""B"" = sub.""id"" WHERE sub.""themeId"" IN ('66f66240-04a6-4e66-b6bf-1f5b96a8d659', '81c318e3-be77-440a-87dd-21fe9e5fc67e','8109cbac-c756-47bc-a1bc-96498d8d0401','5b981962-a0ca-48fc-b04d-c364eda5fb0a') AND p.time between DATE '2025-04-01' - interval '1 days' and DATE '2025-05-31' + interval '1 days' and p.""socialNetwork"" = 'X' and embedding_openclip_text is not null) TO 'output_vacinal_abril_maio_test.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8');
"@