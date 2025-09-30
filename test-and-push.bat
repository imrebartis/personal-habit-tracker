@echo off
echo Running tests...
python -m unittest tests.test_unit tests.test_integration
if %errorlevel% neq 0 (
    echo Tests failed. Not pushing.
    exit /b 1
)
echo All tests passed. Pushing to origin...
git push