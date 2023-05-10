@echo off


REM create and pull data
mkdir ".\data\forests" ".\data\cities" ".\maps" 

REM make that parallel (faster)

if not exist .\data\cities\output.zip (
  start /b curl -L -o .\data\cities\output.zip https://www.insee.fr/fr/statistiques/fichier/6683035/ensemble.zip
)

if not exist .\data\forests\FOR_PUBL_FR.json (
  start /b curl -L -o .\data\forests\FOR_PUBL_FR.json https://www.data.gouv.fr/fr/datasets/r/7b0811ee-9c02-435a-a2e8-440f6a4ffca7
)

if not exist .\data\cities\cities.json (
  start /b curl -L -o .\data\cities\cities.json https://www.data.gouv.fr/fr/datasets/r/521fe6f9-0f7f-4684-bb3f-7d3d88c581bb
)

if not exist .\data\cities\communes.geojson (
  start /b curl -L -o .\data\cities\communes.geojson https://github.com/gregoiredavid/france-geojson/raw/master/communes.geojson
)

echo Sucess
REM wait for all tasks to finish
:wait
timeout /t 1 /nobreak >nul
tasklist | findstr /i "curl" >nul
if errorlevel 1 goto :continue
goto :wait

:continue
REM extract data that needs to be extracted
@REM cd /d ".\data\cities\"
powershell -Command "Expand-Archive -Force -Path '.\data\cities\output.zip' -DestinationPath '.\data\cities\'"
