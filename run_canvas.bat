@echo off
REM ملف تشغيل Canvas
REM المطور: Saudi Linux (SaudiLinux7@gmail.com)

echo ====================================================
echo تشغيل Canvas - أداة الرسم
echo ====================================================
echo.

REM التحقق من وجود Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [خطأ] لم يتم العثور على Python. الرجاء تثبيت Python 3.6 أو أحدث.
    echo يمكنك تحميل Python من: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM التحقق من وجود ملف Canvas.py
if not exist Canvas.py (
    echo [خطأ] لم يتم العثور على ملف Canvas.py في المجلد الحالي.
    pause
    exit /b 1
)

REM تشغيل التطبيق
echo [جاري] تشغيل Canvas...
python Canvas.py

REM التحقق من نجاح التشغيل
if %ERRORLEVEL% neq 0 (
    echo.
    echo [خطأ] حدث خطأ أثناء تشغيل التطبيق. الرجاء التحقق من تثبيت جميع المتطلبات.
    echo يمكنك تشغيل ملف install_canvas_requirements.bat لتثبيت المتطلبات.
    pause
)