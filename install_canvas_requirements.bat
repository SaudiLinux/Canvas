@echo off
REM ملف تثبيت متطلبات Canvas
REM المطور: Saudi Linux (SaudiLinux7@gmail.com)

echo ====================================================
echo تثبيت متطلبات Canvas
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

REM عرض إصدار Python
echo [معلومات] إصدار Python المثبت:
python --version
echo.

REM تحديث pip
echo [جاري] تحديث مدير الحزم pip...
python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    echo [تحذير] فشل تحديث pip. جاري المتابعة...
) else (
    echo [تم] تحديث pip بنجاح.
)
echo.

REM تثبيت المتطلبات
echo [جاري] تثبيت المكتبات المطلوبة...
python -m pip install -r requirements_canvas.txt
if %ERRORLEVEL% neq 0 (
    echo [خطأ] فشل تثبيت بعض المكتبات. راجع الرسائل أعلاه للتفاصيل.
    pause
    exit /b 1
) else (
    echo [تم] تثبيت جميع المكتبات بنجاح.
)
echo.

echo ====================================================
echo تم تثبيت جميع متطلبات Canvas بنجاح!
echo يمكنك الآن تشغيل Canvas.py أو استخدام Setup.py للتثبيت.
echo ====================================================

pause