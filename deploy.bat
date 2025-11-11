@echo off
echo ============================================
echo GitHub Deployment Helper for CCAV1.0
echo ============================================
echo.

echo Checking git status...
git status
echo.

echo Adding all required files...
git add -f app_block_groups.py
git add -f educational_desert_index_bg.py
git add -f competition_ingest.py
git add -f school_ingest.py
git add -f requirements.txt
git add -f philadelphia_block_groups.geojson
git add -f demographics_block_groups.csv
git add -f current_students.csv
git add -f competition_schools.csv
git add -f census_schools.csv
git add -f .gitignore
git add -f README.md
echo.

echo Current git status:
git status
echo.

echo Committing changes...
git commit -m "Add all required files for Streamlit Cloud deployment"
echo.

echo Pushing to GitHub...
git push origin feature-growth-opportunity-2025
echo.

echo ============================================
echo Deployment files pushed!
echo.
echo Next steps:
echo 1. Visit: https://github.com/lavielehr92/CCAV1.0
echo 2. Verify files are uploaded
echo 3. Create Pull Request: feature-growth-opportunity-2025 -^> main
echo 4. Deploy on Streamlit Cloud
echo ============================================
pause
