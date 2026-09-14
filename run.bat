@echo off
setlocal

REM Launch Rolevia from this folder, regardless of where it is double-clicked.
set "PROJECT_DIR=%~dp0"
set "PYTHON_EXE=%PROJECT_DIR%.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo Creating the project virtual environment...
    py -m venv "%PROJECT_DIR%.venv"
    if errorlevel 1 (
        echo.
        echo Could not create the virtual environment. Install Python 3 and try again.
        pause
        exit /b 1
    )
)

"%PYTHON_EXE%" -c "import streamlit, fitz, pandas, sklearn" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages. This may take a moment...
    "%PYTHON_EXE%" -m pip install -r "%PROJECT_DIR%requirements.txt"
    if errorlevel 1 (
        echo.
        echo Dependency installation failed. Check your internet connection and try again.
        pause
        exit /b 1
    )
)

echo Starting Rolevia...
REM Run the server in its own console so this launcher can open the browser.
start "Rolevia Server" /D "%PROJECT_DIR%" "%PYTHON_EXE%" -m streamlit run "%PROJECT_DIR%app.py" --server.port 8501 --server.headless true

REM Give Streamlit a moment to start, then explicitly open the default browser.
timeout /t 3 /nobreak >nul
start "" "http://localhost:8501"

echo Rolevia is opening in your browser at http://localhost:8501
echo To stop the application later, close the "Rolevia Server" window.
timeout /t 2 /nobreak >nul
endlocal
