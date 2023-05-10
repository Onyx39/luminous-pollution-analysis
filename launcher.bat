

mkdir logs

call .venv\Scripts\activate.bat

echo Pulling data...

call src\pull-data.bat

echo Processing forests and cities...

REM Start the first process
start "" /B cmd /C "python -m src.map_creation.process_forest_dataset > logs\process_forest_dataset.log"

REM Start the second process
start "" /B cmd /C "python -m src.map_creation.process_cities > logs\process_cities.log "

REM Wait for both processes to finish
:WAIT
timeout /T 1 >nul
tasklist | find /i "python" >nul
if not errorlevel 1 goto WAIT

echo Downloading forests and cities images...

REM Start the first process
start "" /B cmd /C "python -m src.ndvi_luminance.download_city_images > logs\download_city_images.log"

REM Start the second process
start "" /B cmd /C "python -m src.ndvi_luminance.download_forets_images > logs\download_forets_images.log "

REM Wait for both processes to finish
:WAIT
timeout /T 1 >nul
tasklist | find /i "python" >nul
if not errorlevel 1 goto WAIT

echo Processing images...

python -m src.ndvi_luminance.process_maps > logs\process_maps.log

echo Creating the map...

python -m src.map_creation.full_map_creation > logs\full_map_creation.log
