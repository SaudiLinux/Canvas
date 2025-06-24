#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Setup - برنامج تثبيت Canvas
تم تطويره بواسطة: Saudi Linux
البريد الإلكتروني: SaudiLinux7@gmail.com
'''

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import shutil
import json
import platform
import winreg
from datetime import datetime

class SetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Setup - تثبيت Canvas")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # تعيين الأيقونة إذا كانت موجودة
        try:
            self.root.iconbitmap("setup_icon.ico")
        except:
            pass
        
        # متغيرات التثبيت
        self.install_dir = os.path.expanduser("~\\Canvas")
        self.create_desktop_shortcut = tk.BooleanVar(value=True)
        self.create_start_menu_shortcut = tk.BooleanVar(value=True)
        self.current_step = 0
        self.total_steps = 4
        
        # إنشاء واجهة المستخدم
        self.create_ui()
    
    def create_ui(self):
        # إطار رئيسي
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # العنوان
        title_frame = tk.Frame(main_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(title_frame, text="تثبيت Canvas", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="برنامج الرسم البسيط", font=("Arial", 10), bg="#f0f0f0")
        subtitle_label.pack()
        
        # خط فاصل
        separator = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=10)
        
        # إطار المحتوى
        self.content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # إطار الأزرار
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)
        
        # أزرار التنقل
        self.back_button = ttk.Button(button_frame, text="رجوع", command=self.go_back, state=tk.DISABLED)
        self.back_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = ttk.Button(button_frame, text="التالي", command=self.go_next)
        self.next_button.pack(side=tk.RIGHT, padx=5)
        
        self.cancel_button = ttk.Button(button_frame, text="إلغاء", command=self.cancel_setup)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # شريط التقدم
        progress_frame = tk.Frame(main_frame, bg="#f0f0f0")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X)
        
        self.progress_label = tk.Label(progress_frame, text="الخطوة 1 من 4", bg="#f0f0f0")
        self.progress_label.pack(anchor=tk.E)
        
        # عرض الخطوة الأولى
        self.show_welcome_step()
    
    def show_welcome_step(self):
        # مسح المحتوى السابق
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # عنوان الترحيب
        welcome_label = tk.Label(self.content_frame, text="مرحباً بك في معالج تثبيت Canvas", font=("Arial", 12, "bold"), bg="#f0f0f0")
        welcome_label.pack(pady=10)
        
        # نص الترحيب
        welcome_text = """سيقوم هذا المعالج بتثبيت برنامج Canvas على جهازك.

Canvas هو برنامج رسم بسيط يتيح لك إنشاء رسومات وتصميمات بسهولة.

انقر على 'التالي' للاستمرار أو 'إلغاء' للخروج من المعالج."""
        
        text_box = tk.Text(self.content_frame, wrap=tk.WORD, height=10, width=50)
        text_box.insert(tk.END, welcome_text)
        text_box.configure(state="disabled", font=("Arial", 10), bg="#f5f5f5")
        text_box.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # معلومات المطور
        developer_label = tk.Label(self.content_frame, text="تم تطويره بواسطة: Saudi Linux", font=("Arial", 8), bg="#f0f0f0")
        developer_label.pack()
        
        email_label = tk.Label(self.content_frame, text="البريد الإلكتروني: SaudiLinux7@gmail.com", font=("Arial", 8), bg="#f0f0f0")
        email_label.pack()
        
        # تحديث الخطوة الحالية
        self.current_step = 1
        self.update_progress()
    
    def show_license_step(self):
        # مسح المحتوى السابق
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # عنوان الترخيص
        license_label = tk.Label(self.content_frame, text="اتفاقية الترخيص", font=("Arial", 12, "bold"), bg="#f0f0f0")
        license_label.pack(pady=10)
        
        # نص الترخيص
        license_text = """اتفاقية ترخيص المستخدم النهائي (EULA)

يرجى قراءة اتفاقية الترخيص التالية بعناية قبل استخدام برنامج Canvas. باستخدامك للبرنامج، فإنك توافق على الالتزام بشروط هذه الاتفاقية.

1. منح الترخيص
يمنحك هذا الترخيص الحق غير الحصري وغير القابل للتحويل لاستخدام البرنامج على جهاز كمبيوتر واحد.

2. قيود الاستخدام
لا يجوز لك نسخ أو تعديل أو دمج أو ترجمة أو إعادة هندسة أو تفكيك أو إنشاء أعمال مشتقة من البرنامج.

3. حقوق الملكية
يحتفظ المطور بجميع حقوق الملكية والملكية الفكرية في البرنامج.

4. إخلاء المسؤولية
يتم توفير البرنامج "كما هو" دون أي ضمانات من أي نوع، صريحة أو ضمنية.

5. تحديد المسؤولية
لن يكون المطور مسؤولاً عن أي أضرار مباشرة أو غير مباشرة أو عرضية أو خاصة أو تبعية ناتجة عن استخدام البرنامج.

6. الإنهاء
ينتهي هذا الترخيص تلقائيًا إذا انتهكت أي من شروطه. عند الإنهاء، يجب عليك التوقف عن استخدام البرنامج وإتلاف جميع نسخه.

7. القانون الحاكم
تخضع هذه الاتفاقية لقوانين المملكة العربية السعودية وتفسر وفقًا لها.

بالنقر على "أوافق"، فإنك تقر بأنك قد قرأت وفهمت وتوافق على الالتزام بشروط هذه الاتفاقية."""
        
        text_box = tk.Text(self.content_frame, wrap=tk.WORD, height=10, width=50)
        text_box.insert(tk.END, license_text)
        text_box.configure(state="disabled", font=("Arial", 10), bg="#f5f5f5")
        text_box.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # خيار الموافقة
        self.accept_license = tk.BooleanVar(value=False)
        accept_checkbox = ttk.Checkbutton(self.content_frame, text="أوافق على شروط الترخيص", variable=self.accept_license, command=self.update_next_button)
        accept_checkbox.pack(anchor=tk.W, pady=5)
        
        # تعطيل زر التالي حتى يتم قبول الترخيص
        self.next_button.config(state=tk.DISABLED)
        
        # تحديث الخطوة الحالية
        self.current_step = 2
        self.update_progress()
    
    def show_install_options_step(self):
        # مسح المحتوى السابق
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # عنوان خيارات التثبيت
        options_label = tk.Label(self.content_frame, text="خيارات التثبيت", font=("Arial", 12, "bold"), bg="#f0f0f0")
        options_label.pack(pady=10)
        
        # إطار مسار التثبيت
        path_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        path_frame.pack(fill=tk.X, pady=10)
        
        path_label = tk.Label(path_frame, text="مسار التثبيت:", bg="#f0f0f0")
        path_label.pack(side=tk.LEFT, padx=5)
        
        self.path_entry = ttk.Entry(path_frame, width=40)
        self.path_entry.insert(0, self.install_dir)
        self.path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(path_frame, text="استعراض...", command=self.browse_install_dir)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # إطار الاختصارات
        shortcuts_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        shortcuts_frame.pack(fill=tk.X, pady=10)
        
        desktop_checkbox = ttk.Checkbutton(shortcuts_frame, text="إنشاء اختصار على سطح المكتب", variable=self.create_desktop_shortcut)
        desktop_checkbox.pack(anchor=tk.W, pady=5)
        
        startmenu_checkbox = ttk.Checkbutton(shortcuts_frame, text="إنشاء اختصار في قائمة ابدأ", variable=self.create_start_menu_shortcut)
        startmenu_checkbox.pack(anchor=tk.W, pady=5)
        
        # معلومات المساحة المطلوبة
        space_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        space_frame.pack(fill=tk.X, pady=10)
        
        space_label = tk.Label(space_frame, text="المساحة المطلوبة: 5.2 ميجابايت", bg="#f0f0f0")
        space_label.pack(anchor=tk.W)
        
        # تحديث الخطوة الحالية
        self.current_step = 3
        self.update_progress()
    
    def show_installing_step(self):
        # مسح المحتوى السابق
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # عنوان التثبيت
        installing_label = tk.Label(self.content_frame, text="جاري التثبيت...", font=("Arial", 12, "bold"), bg="#f0f0f0")
        installing_label.pack(pady=10)
        
        # إطار التقدم
        progress_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        progress_frame.pack(fill=tk.X, pady=20)
        
        self.install_progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.install_progress.pack(fill=tk.X, padx=20)
        
        self.install_status = tk.Label(progress_frame, text="جاري التحضير للتثبيت...", bg="#f0f0f0")
        self.install_status.pack(pady=5)
        
        # تعطيل أزرار التنقل أثناء التثبيت
        self.back_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        
        # تحديث الخطوة الحالية
        self.current_step = 4
        self.update_progress()
        
        # بدء عملية التثبيت
        self.root.after(500, self.perform_installation)
    
    def show_finish_step(self):
        # مسح المحتوى السابق
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # عنوان الانتهاء
        finish_label = tk.Label(self.content_frame, text="اكتمل التثبيت", font=("Arial", 12, "bold"), bg="#f0f0f0")
        finish_label.pack(pady=10)
        
        # رسالة الانتهاء
        finish_text = """تم تثبيت برنامج Canvas بنجاح على جهازك.

يمكنك الآن بدء استخدام البرنامج من خلال النقر على أيقونة Canvas على سطح المكتب أو من قائمة ابدأ.

شكراً لاختيارك برنامج Canvas!"""
        
        text_box = tk.Text(self.content_frame, wrap=tk.WORD, height=8, width=50)
        text_box.insert(tk.END, finish_text)
        text_box.configure(state="disabled", font=("Arial", 10), bg="#f5f5f5")
        text_box.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # خيار تشغيل البرنامج
        self.run_after_install = tk.BooleanVar(value=True)
        run_checkbox = ttk.Checkbutton(self.content_frame, text="تشغيل Canvas الآن", variable=self.run_after_install)
        run_checkbox.pack(anchor=tk.W, pady=5)
        
        # تغيير أزرار التنقل
        self.back_button.config(state=tk.DISABLED)
        self.next_button.config(text="إنهاء", command=self.finish_setup)
        self.cancel_button.config(state=tk.DISABLED)
    
    def go_back(self):
        if self.current_step == 2:
            self.show_welcome_step()
        elif self.current_step == 3:
            self.show_license_step()
        elif self.current_step == 4:
            self.show_install_options_step()
    
    def go_next(self):
        if self.current_step == 1:
            self.show_license_step()
        elif self.current_step == 2:
            self.show_install_options_step()
        elif self.current_step == 3:
            self.show_installing_step()
        elif self.current_step == 4:
            self.show_finish_step()
    
    def cancel_setup(self):
        if messagebox.askyesno("إلغاء التثبيت", "هل أنت متأكد من إلغاء عملية التثبيت؟"):
            self.root.destroy()
    
    def update_progress(self):
        # تحديث شريط التقدم وعنوان الخطوة
        progress_value = (self.current_step / self.total_steps) * 100
        self.progress_bar["value"] = progress_value
        self.progress_label.config(text=f"الخطوة {self.current_step} من {self.total_steps}")
        
        # تحديث حالة أزرار التنقل
        if self.current_step > 1:
            self.back_button.config(state=tk.NORMAL)
        else:
            self.back_button.config(state=tk.DISABLED)
    
    def update_next_button(self):
        # تحديث حالة زر التالي بناءً على قبول الترخيص
        if self.accept_license.get():
            self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)
    
    def browse_install_dir(self):
        # اختيار مسار التثبيت
        directory = tk.filedialog.askdirectory(initialdir=self.install_dir)
        if directory:
            self.install_dir = directory
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, self.install_dir)
    
    def perform_installation(self):
        # الحصول على مسار التثبيت من حقل الإدخال
        self.install_dir = self.path_entry.get()
        
        # التأكد من وجود المسار
        if not os.path.exists(self.install_dir):
            try:
                os.makedirs(self.install_dir)
            except Exception as e:
                messagebox.showerror("خطأ", f"لا يمكن إنشاء مسار التثبيت: {str(e)}")
                self.show_install_options_step()
                return
        
        # محاكاة خطوات التثبيت
        installation_steps = [
            ("إنشاء مجلدات البرنامج...", 10),
            ("نسخ ملفات البرنامج...", 30),
            ("تكوين الإعدادات...", 20),
            ("إنشاء الاختصارات...", 20),
            ("تسجيل البرنامج...", 10),
            ("تنظيف الملفات المؤقتة...", 10)
        ]
        
        total_progress = 0
        
        # تنفيذ خطوات التثبيت
        for step_text, step_progress in installation_steps:
            # تحديث حالة التثبيت
            self.install_status.config(text=step_text)
            
            # محاكاة التقدم
            for i in range(step_progress):
                total_progress += 1
                self.install_progress["value"] = total_progress
                self.root.update()
                self.root.after(50)  # تأخير لمحاكاة العمل
            
            # تنفيذ الخطوة الفعلية
            if "إنشاء مجلدات" in step_text:
                self.create_program_folders()
            elif "نسخ ملفات" in step_text:
                self.copy_program_files()
            elif "تكوين الإعدادات" in step_text:
                self.configure_settings()
            elif "إنشاء الاختصارات" in step_text:
                self.create_shortcuts()
            elif "تسجيل البرنامج" in step_text:
                self.register_program()
        
        # الانتقال إلى خطوة الانتهاء
        self.show_finish_step()
    
    def create_program_folders(self):
        # إنشاء المجلدات اللازمة
        try:
            os.makedirs(os.path.join(self.install_dir, "data"), exist_ok=True)
            os.makedirs(os.path.join(self.install_dir, "templates"), exist_ok=True)
            os.makedirs(os.path.join(self.install_dir, "temp"), exist_ok=True)
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن إنشاء مجلدات البرنامج: {str(e)}")
    
    def copy_program_files(self):
        # نسخ ملفات البرنامج
        try:
            # نسخ ملف Canvas.py إلى مجلد التثبيت
            script_dir = os.path.dirname(os.path.abspath(__file__))
            canvas_path = os.path.join(script_dir, "Canvas.py")
            
            if os.path.exists(canvas_path):
                shutil.copy2(canvas_path, os.path.join(self.install_dir, "Canvas.py"))
            
            # إنشاء ملف تشغيل للويندوز
            with open(os.path.join(self.install_dir, "Canvas.bat"), "w") as f:
                f.write(f'@echo off\n"python.exe" "{os.path.join(self.install_dir, "Canvas.py")}"\npause')
            
            # إنشاء ملف تكوين
            config = {
                "version": "1.0",
                "install_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "install_path": self.install_dir,
                "user": os.getenv("USERNAME"),
                "system": platform.system() + " " + platform.release()
            }
            
            with open(os.path.join(self.install_dir, "config.json"), "w") as f:
                json.dump(config, f, indent=4)
            
            # إنشاء ملفات قوالب
            with open(os.path.join(self.install_dir, "templates", "blank.canvas"), "w") as f:
                template = {
                    "postscript": "",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "version": "1.0"
                }
                json.dump(template, f, indent=4)
        
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن نسخ ملفات البرنامج: {str(e)}")
    
    def configure_settings(self):
        # تكوين إعدادات البرنامج
        try:
            # إنشاء ملف الإعدادات
            settings = {
                "theme": "default",
                "language": "ar",
                "autosave": True,
                "autosave_interval": 5,
                "recent_files": [],
                "default_pen_color": "#000000",
                "default_pen_size": 2,
                "default_eraser_size": 10
            }
            
            with open(os.path.join(self.install_dir, "settings.json"), "w") as f:
                json.dump(settings, f, indent=4)
        
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن تكوين إعدادات البرنامج: {str(e)}")
    
    def create_shortcuts(self):
        # إنشاء الاختصارات
        try:
            # مسار ملف التشغيل
            exe_path = os.path.join(self.install_dir, "Canvas.bat")
            
            # اختصار سطح المكتب
            if self.create_desktop_shortcut.get():
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                self.create_shortcut(exe_path, os.path.join(desktop_path, "Canvas.lnk"), "Canvas - أداة الرسم")
            
            # اختصار قائمة ابدأ
            if self.create_start_menu_shortcut.get():
                start_menu_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs")
                canvas_folder = os.path.join(start_menu_path, "Canvas")
                
                if not os.path.exists(canvas_folder):
                    os.makedirs(canvas_folder)
                
                self.create_shortcut(exe_path, os.path.join(canvas_folder, "Canvas.lnk"), "Canvas - أداة الرسم")
                self.create_shortcut(self.install_dir, os.path.join(canvas_folder, "مجلد Canvas.lnk"), "مجلد Canvas")
        
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن إنشاء الاختصارات: {str(e)}")
    
    def create_shortcut(self, target_path, shortcut_path, description):
        # إنشاء اختصار في نظام ويندوز
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = target_path
            shortcut.Description = description
            shortcut.WorkingDirectory = os.path.dirname(target_path)
            shortcut.save()
        except ImportError:
            # إذا لم تكن مكتبة win32com متوفرة، نستخدم طريقة بديلة
            with open(shortcut_path, "w") as f:
                f.write(f"[InternetShortcut]\nURL=file:///{target_path.replace('/', '\\')}\n")
    
    def register_program(self):
        # تسجيل البرنامج في نظام التشغيل
        try:
            # تسجيل امتداد الملف .canvas
            if platform.system() == "Windows":
                try:
                    # فتح مفتاح التسجيل لامتداد الملف
                    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\.canvas")
                    winreg.SetValue(key, "", winreg.REG_SZ, "Canvas.Document")
                    winreg.CloseKey(key)
                    
                    # إنشاء مفتاح نوع الملف
                    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\Canvas.Document")
                    winreg.SetValue(key, "", winreg.REG_SZ, "Canvas Document")
                    winreg.CloseKey(key)
                    
                    # إنشاء مفتاح أمر الفتح
                    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\Canvas.Document\\shell\\open\\command")
                    winreg.SetValue(key, "", winreg.REG_SZ, f'"{os.path.join(self.install_dir, "Canvas.bat")}" "%1"')
                    winreg.CloseKey(key)
                except Exception as e:
                    # تجاهل أخطاء التسجيل
                    pass
        
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن تسجيل البرنامج: {str(e)}")
    
    def finish_setup(self):
        # إنهاء عملية التثبيت
        if self.run_after_install.get():
            # تشغيل البرنامج
            try:
                if platform.system() == "Windows":
                    os.startfile(os.path.join(self.install_dir, "Canvas.bat"))
                else:
                    subprocess.Popen(["python", os.path.join(self.install_dir, "Canvas.py")])
            except Exception as e:
                messagebox.showerror("خطأ", f"لا يمكن تشغيل البرنامج: {str(e)}")
        
        # إغلاق المعالج
        self.root.destroy()


def main():
    root = tk.Tk()
    app = SetupApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()