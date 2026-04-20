@echo off
REM ─────────────────────────────────────────────────────────────────────────────
REM GlucoCheck — Script de arranque local (Windows)
REM Uso: scripts\start.bat
REM ─────────────────────────────────────────────────────────────────────────────
setlocal EnableDelayedExpansion

set "ROOT_DIR=%~dp0.."
set "VENV_DIR=%ROOT_DIR%\.venv"
set "ARTIFACTS_DIR=%ROOT_DIR%\data\processed"
set "FRONTEND=%ROOT_DIR%\frontend\index.html"
set "PORT=8000"

echo.
echo Iniciando GlucoCheck - Arranque local
echo ======================================
echo.

REM ── 1. Comprobar Python 3.10+ ─────────────────────────────────────────────
echo [1/5] Comprobando Python 3.10+...

set "PYTHON="
for %%P in (python3.12 python3.11 python3.10 python3 python py) do (
  where %%P >/dev/null 2>&1
  if not errorlevel 1 (
    for /f "tokens=*" %%V in ('%%P -c "import sys; print(str(sys.version_info.major) + chr(46) + str(sys.version_info.minor))" 2^>nul') do (
      for /f "tokens=1,2 delims=." %%A in ("%%V") do (
        if %%A==3 if %%B GEQ 10 (
          if not defined PYTHON (
            set "PYTHON=%%P"
            echo   OK - Usando %%P ^(version %%V^)
          )
        )
      )
    )
  )
)

if not defined PYTHON (
  echo   ERROR: No se encontro Python 3.10+.
  echo          Descargalo desde https://www.python.org/downloads/
  pause
  exit /b 1
)

REM ── 2. Entorno virtual ────────────────────────────────────────────────────
echo.
echo [2/5] Preparando entorno virtual...

if not exist "%VENV_DIR%\Scripts\activate.bat" (
  %PYTHON% -m venv "%VENV_DIR%"
  if errorlevel 1 (
    echo   ERROR: No se pudo crear el entorno virtual.
    pause & exit /b 1
  )
  echo   OK - Entorno virtual creado en .venv\
) else (
  echo   OK - Entorno virtual ya existe ^(.venv\^)
)

call "%VENV_DIR%\Scripts\activate.bat"

REM ── 3. Instalar dependencias ──────────────────────────────────────────────
echo.
echo [3/5] Instalando dependencias...

pip install --quiet --upgrade pip
pip install --quiet -r "%ROOT_DIR%\requirements.txt"
if errorlevel 1 (
  echo   ERROR: Fallo al instalar dependencias.
  pause & exit /b 1
)
echo   OK - Dependencias instaladas

REM ── 4. Pipeline de datos (solo si faltan artefactos) ─────────────────────
echo.
echo [4/5] Comprobando artefactos del modelo...

set "ARTIFACTS_OK=1"
if not exist "%ARTIFACTS_DIR%\model.pkl"     set "ARTIFACTS_OK=0"
if not exist "%ARTIFACTS_DIR%\scaler.pkl"    set "ARTIFACTS_OK=0"
if not exist "%ARTIFACTS_DIR%\threshold.txt" set "ARTIFACTS_OK=0"

if "%ARTIFACTS_OK%"=="0" (
  echo   AVISO: Artefactos no encontrados. Ejecutando pipeline...
  echo          Esto puede tardar unos minutos...
  echo.

  pushd "%ROOT_DIR%"

  python -m src.data.download_data
  if errorlevel 1 ( echo   ERROR: Fallo al descargar datos. & pause & exit /b 1 )
  echo   OK - Datos descargados

  python -m src.data.preprocess
  if errorlevel 1 ( echo   ERROR: Fallo en preprocesamiento. & pause & exit /b 1 )
  echo   OK - Preprocesamiento completado

  python -m src.models.train_model
  if errorlevel 1 ( echo   ERROR: Fallo al entrenar el modelo. & pause & exit /b 1 )
  echo   OK - Modelo entrenado

  popd

  if not exist "%ARTIFACTS_DIR%\model.pkl" (
    echo   ERROR: No se genero model.pkl
    pause & exit /b 1
  )
  echo   OK - Artefactos generados correctamente
) else (
  echo   OK - Artefactos ya existen -- omitiendo pipeline
)

REM ── 5. Abrir frontend en el navegador ─────────────────────────────────────
echo.
echo [5/5] Abriendo frontend...

if exist "%FRONTEND%" (
  start "" "%FRONTEND%"
  echo   OK - Frontend abierto en el navegador
) else (
  echo   AVISO: No se encontro frontend\index.html
)

REM ── 6. Arrancar backend ───────────────────────────────────────────────────
echo.
echo -----------------------------------------------
echo   Backend disponible en: http://localhost:%PORT%
echo   Documentacion API:     http://localhost:%PORT%/docs
echo   Pulsa Ctrl+C para detener
echo -----------------------------------------------
echo.

pushd "%ROOT_DIR%"
uvicorn src.api.main:app --host 0.0.0.0 --port %PORT% --reload
popd

endlocal
