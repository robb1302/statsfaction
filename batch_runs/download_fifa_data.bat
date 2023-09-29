@echo off
setlocal

rem Pfad zur virtuellen Umgebung anpassen
set VENV_PATH=C:\Users\Robert\Documents\Projekte\dev\statsfaction\.venv

rem Aktivieren Sie die virtuelle Umgebung
call "%VENV_PATH%\Scripts\activate"

rem Führen Sie Ihren Befehl innerhalb der virtuellen Umgebung aus
rem Zum Beispiel, Python-Skript ausführen:

py .\scripts\sport_analytics\run_crawler_fifa_players.py --fifa_versions 18
py .\scripts\sport_analytics\run_crawler_fifa_attributes.py --fifa_versions 18
py .\scripts\sport_analytics\merge_crawled_fifa_data.py --fifa_versions 18

rem Deaktivieren Sie die virtuelle Umgebung, wenn Sie fertig sind
call "%VENV_PATH%\Scripts\deactivate"

rem Batch-Datei beenden
exit /b 0



