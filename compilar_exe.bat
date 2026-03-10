@echo off
title Compilador - Notas de Enfermeria

echo.
echo =====================================================
echo   COMPILADOR - Sistema de Notas de Enfermeria
echo   Generando ejecutable para Windows...
echo =====================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    pause
    exit /b 1
)
echo [OK] Python detectado.

echo.
echo [1/4] Instalando PyInstaller...
pip install pyinstaller --quiet --upgrade
if errorlevel 1 (
    echo [ERROR] No se pudo instalar PyInstaller.
    pause
    exit /b 1
)
echo [OK] PyInstaller listo.

echo.
echo [2/4] Verificando dependencias...
pip install PyQt5 --quiet
echo [OK] Dependencias verificadas.

echo.
echo [3/4] Limpiando archivos anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "NotasEnfermeria.spec" del /q "NotasEnfermeria.spec"
echo [OK] Limpieza completa.

echo.
echo [4/4] Compilando ejecutable (puede tardar 2-3 minutos)...
echo       Por favor espera sin cerrar esta ventana...
echo.

pyinstaller --onedir --windowed --name "NotasEnfermeria" --add-data "datos;datos" --add-data "plantillas;plantillas" --hidden-import "PyQt5.sip" --hidden-import "PyQt5.QtWidgets" --hidden-import "PyQt5.QtCore" --hidden-import "PyQt5.QtGui" --hidden-import "modelos" --hidden-import "controladores" --hidden-import "servicios" --hidden-import "utilidades" --hidden-import "vistas" --collect-all PyQt5 --noconfirm main.py

if errorlevel 1 (
    echo.
    echo [ERROR] La compilacion fallo. Revisa los mensajes arriba.
    pause
    exit /b 1
)

echo.
echo [OK] Copiando archivos de datos...
if not exist "dist\NotasEnfermeria\datos" mkdir "dist\NotasEnfermeria\datos"
copy /y "datos\estadisticas_uso.json" "dist\NotasEnfermeria\datos\" >nul 2>&1
if not exist "dist\NotasEnfermeria\notas_generadas" mkdir "dist\NotasEnfermeria\notas_generadas"

echo.
echo =====================================================
echo   COMPILACION EXITOSA
echo =====================================================
echo.
echo   Aplicacion lista en: dist\NotasEnfermeria\
echo.
echo   Para el pendrive: copia TODA esa carpeta.
echo =====================================================
echo.

explorer "dist\NotasEnfermeria"
pause
