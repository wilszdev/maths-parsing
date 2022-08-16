@echo off
pushd %~dp0\..\
call vendor\bin\premake5.exe vs2022
popd

:: pause on error
if %errorlevel% NEQ 0 (pause)
