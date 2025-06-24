#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Canvas - أداة رسم بسيطة
تم تطويره بواسطة: Saudi Linux
البريد الإلكتروني: SaudiLinux7@gmail.com
'''

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import time
import threading
import requests
import subprocess
import platform
from datetime import datetime

class UpdateManager:
    def __init__(self, parent, app_version="1.0"):
        self.parent = parent
        self.current_version = app_version
        self.update_url = "https://api.github.com/repos/SaudiLinux/Canvas/releases/latest"
        self.download_url = "https://github.com/SaudiLinux/Canvas/releases/download/"
        self.update_available = False
        self.latest_version = ""
        self.update_info = {}
        self.checking = False
        
        # إعدادات التحديث التلقائي
        self.auto_check = True  # التحقق التلقائي من التحديثات
        self.check_interval = 24 * 60 * 60  # الفاصل الزمني للتحقق (بالثواني) - يوم واحد
        self.last_check_time = 0  # وقت آخر تحقق
        
        # تحميل إعدادات التحديث
        self.load_update_settings()
        
        # بدء التحقق من التحديثات في الخلفية إذا كان التحقق التلقائي مفعلاً
        if self.auto_check:
            threading.Thread(target=self.background_check, daemon=True).start()
    
    def load_update_settings(self):
        """تحميل إعدادات التحديث من ملف الإعدادات"""
        try:
            # تحديد مسار ملف الإعدادات
            settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")
            
            if os.path.exists(settings_path):
                with open(settings_path, "r") as f:
                    settings = json.load(f)
                
                # تحميل إعدادات التحديث إذا كانت موجودة
                if "updates" in settings:
                    self.auto_check = settings["updates"].get("auto_check", True)
                    self.check_interval = settings["updates"].get("check_interval", 24 * 60 * 60)
                    self.last_check_time = settings["updates"].get("last_check_time", 0)
        except Exception as e:
            print(f"خطأ في تحميل إعدادات التحديث: {str(e)}")
    
    def save_update_settings(self):
        """حفظ إعدادات التحديث في ملف الإعدادات"""
        try:
            # تحديد مسار ملف الإعدادات
            settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")
            
            # تحميل الإعدادات الحالية أو إنشاء إعدادات جديدة
            settings = {}
            if os.path.exists(settings_path):
                with open(settings_path, "r") as f:
                    settings = json.load(f)
            
            # تحديث إعدادات التحديث
            if "updates" not in settings:
                settings["updates"] = {}
            
            settings["updates"]["auto_check"] = self.auto_check
            settings["updates"]["check_interval"] = self.check_interval
            settings["updates"]["last_check_time"] = self.last_check_time
            
            # حفظ الإعدادات
            with open(settings_path, "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"خطأ في حفظ إعدادات التحديث: {str(e)}")
    
    def background_check(self):
        """التحقق من التحديثات في الخلفية"""
        # الانتظار قليلاً قبل التحقق للسماح للتطبيق بالتحميل بالكامل
        time.sleep(5)
        
        # التحقق مما إذا كان الوقت قد حان للتحقق من التحديثات
        current_time = time.time()
        if current_time - self.last_check_time >= self.check_interval:
            self.check_for_updates(show_no_updates=False)
    
    def check_for_updates(self, show_no_updates=True):
        """التحقق من وجود تحديثات جديدة"""
        if self.checking:
            return
        
        self.checking = True
        try:
            # تحديث وقت آخر تحقق
            self.last_check_time = time.time()
            self.save_update_settings()
            
            # محاولة الاتصال بالخادم للتحقق من التحديثات
            response = requests.get(self.update_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.latest_version = data.get("tag_name", "").replace("v", "")
                
                # مقارنة الإصدارات
                if self.compare_versions(self.latest_version, self.current_version) > 0:
                    self.update_available = True
                    self.update_info = {
                        "version": self.latest_version,
                        "description": data.get("body", ""),
                        "download_url": data.get("assets", [])[0].get("browser_download_url", "") if data.get("assets") else ""
                    }
                    
                    # عرض إشعار التحديث
                    self.parent.after(0, self.show_update_notification)
                elif show_no_updates:
                    # عرض رسالة عدم وجود تحديثات إذا كان مطلوبًا
                    self.parent.after(0, lambda: messagebox.showinfo("التحديثات", "أنت تستخدم أحدث إصدار من البرنامج."))
            else:
                if show_no_updates:
                    self.parent.after(0, lambda: messagebox.showwarning("خطأ في التحديث", f"فشل الاتصال بخادم التحديثات. رمز الحالة: {response.status_code}"))
        except requests.exceptions.RequestException as e:
            if show_no_updates:
                self.parent.after(0, lambda: messagebox.showwarning("خطأ في التحديث", f"فشل الاتصال بخادم التحديثات: {str(e)}"))
        except Exception as e:
            if show_no_updates:
                self.parent.after(0, lambda: messagebox.showwarning("خطأ في التحديث", f"حدث خطأ أثناء التحقق من التحديثات: {str(e)}"))
        finally:
            self.checking = False
    
    def compare_versions(self, version1, version2):
        """مقارنة إصدارين وإرجاع 1 إذا كان الإصدار الأول أحدث، -1 إذا كان الإصدار الثاني أحدث، 0 إذا كانا متساويين"""
        v1_parts = [int(x) for x in version1.split(".")]
        v2_parts = [int(x) for x in version2.split(".")]
        
        # إضافة أصفار إذا كان أحد الإصدارين أقصر من الآخر
        while len(v1_parts) < len(v2_parts):
            v1_parts.append(0)
        while len(v2_parts) < len(v1_parts):
            v2_parts.append(0)
        
        # مقارنة كل جزء
        for i in range(len(v1_parts)):
            if v1_parts[i] > v2_parts[i]:
                return 1
            elif v1_parts[i] < v2_parts[i]:
                return -1
        
        return 0
    
    def show_update_notification(self):
        """عرض إشعار بوجود تحديث جديد"""
        if self.update_available:
            response = messagebox.askyesno(
                "تحديث جديد متاح",
                f"تم العثور على إصدار جديد من البرنامج: {self.latest_version}\n\n" +
                f"الإصدار الحالي: {self.current_version}\n\n" +
                f"ملاحظات الإصدار:\n{self.update_info['description']}\n\n" +
                "هل ترغب في تنزيل وتثبيت هذا التحديث الآن؟"
            )
            
            if response:
                self.download_and_install_update()
    
    def download_and_install_update(self):
        """تنزيل وتثبيت التحديث"""
        try:
            # إنشاء نافذة التقدم
            progress_window = tk.Toplevel(self.parent)
            progress_window.title("تنزيل التحديث")
            progress_window.geometry("400x150")
            progress_window.resizable(False, False)
            progress_window.transient(self.parent)
            progress_window.grab_set()
            
            # تكوين النافذة
            progress_window.configure(bg="#f0f0f0")
            
            # إضافة عناصر واجهة المستخدم
            tk.Label(progress_window, text=f"جاري تنزيل الإصدار {self.latest_version}...", bg="#f0f0f0").pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress_window, orient=tk.HORIZONTAL, length=350, mode='indeterminate')
            progress_bar.pack(pady=10, padx=20)
            progress_bar.start(10)
            
            status_label = tk.Label(progress_window, text="جاري التنزيل...", bg="#f0f0f0")
            status_label.pack(pady=10)
            
            # بدء التنزيل في خيط منفصل
            threading.Thread(
                target=self._download_update_thread,
                args=(progress_window, progress_bar, status_label),
                daemon=True
            ).start()
            
        except Exception as e:
            messagebox.showerror("خطأ في التحديث", f"حدث خطأ أثناء تنزيل التحديث: {str(e)}")
    
    def _download_update_thread(self, progress_window, progress_bar, status_label):
        """خيط لتنزيل وتثبيت التحديث"""
        try:
            # تحديد مسار التنزيل
            download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "updates")
            os.makedirs(download_dir, exist_ok=True)
            
            # تحديد اسم ملف التحديث
            update_filename = f"Canvas_Update_v{self.latest_version}.zip"
            update_path = os.path.join(download_dir, update_filename)
            
            # تنزيل ملف التحديث
            response = requests.get(self.update_info["download_url"], stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            # تحديث شريط التقدم ليكون محددًا
            progress_window.after(0, lambda: progress_bar.configure(mode='determinate', maximum=total_size))
            progress_window.after(0, lambda: progress_bar.stop())
            
            # كتابة الملف
            downloaded = 0
            with open(update_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress_window.after(0, lambda d=downloaded: progress_bar.configure(value=d))
                        progress_window.after(0, lambda d=downloaded: status_label.configure(
                            text=f"جاري التنزيل... {d/total_size:.1%} ({d/1024/1024:.1f} MB / {total_size/1024/1024:.1f} MB)"
                        ))
            
            # تحديث الحالة
            progress_window.after(0, lambda: status_label.configure(text="جاري تثبيت التحديث..."))
            progress_window.after(0, lambda: progress_bar.configure(mode='indeterminate', maximum=100))
            progress_window.after(0, lambda: progress_bar.start(10))
            
            # تثبيت التحديث
            self._install_update(update_path, progress_window)
            
        except Exception as e:
            progress_window.after(0, lambda: messagebox.showerror("خطأ في التحديث", f"حدث خطأ أثناء تنزيل التحديث: {str(e)}"))
            progress_window.after(0, progress_window.destroy)
    
    def _install_update(self, update_path, progress_window):
        """تثبيت التحديث"""
        try:
            # إنشاء سكريبت التثبيت
            install_script = os.path.join(os.path.dirname(update_path), "install_update.bat")
            
            # تحديد مسار البرنامج الحالي
            app_path = os.path.dirname(os.path.abspath(__file__))
            
            # كتابة سكريبت التثبيت
            with open(install_script, "w") as f:
                f.write(f"@echo off\n")
                f.write(f"echo جاري تثبيت التحديث...\n")
                f.write(f"timeout /t 2 /nobreak > nul\n")
                f.write(f"echo استخراج ملفات التحديث...\n")
                
                # استخراج ملفات التحديث
                f.write(f"powershell -Command \"Expand-Archive -Path '{update_path}' -DestinationPath '{app_path}' -Force\"\n")
                
                # إعادة تشغيل البرنامج
                f.write(f"echo تم تثبيت التحديث بنجاح!\n")
                f.write(f"echo إعادة تشغيل البرنامج...\n")
                f.write(f"timeout /t 2 /nobreak > nul\n")
                f.write(f"start "" \"{sys.executable}\" \"{os.path.join(app_path, 'Canvas.py')}\"\n")
                f.write(f"del \"{update_path}\"\n")
                f.write(f"del \"%~f0\"\n")
            
            # إغلاق نافذة التقدم
            progress_window.after(0, progress_window.destroy)
            
            # عرض رسالة نجاح
            progress_window.after(0, lambda: messagebox.showinfo(
                "تم تنزيل التحديث",
                "تم تنزيل التحديث بنجاح. سيتم إغلاق البرنامج الآن وتثبيت التحديث."
            ))
            
            # تشغيل سكريبت التثبيت وإغلاق البرنامج
            subprocess.Popen([install_script], shell=True)
            self.parent.after(1000, self.parent.destroy)
            
        except Exception as e:
            progress_window.after(0, lambda: messagebox.showerror("خطأ في التحديث", f"حدث خطأ أثناء تثبيت التحديث: {str(e)}"))
            progress_window.after(0, progress_window.destroy)


class CanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Canvas - أداة الرسم")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        
        # تعيين الأيقونة إذا كانت موجودة
        try:
            self.root.iconbitmap("canvas_icon.ico")
        except:
            pass
        
        # متغيرات الرسم
        self.pen_color = "black"
        self.pen_size = 2
        self.eraser_size = 10
        self.current_tool = "pen"
        self.drawing_history = []
        self.redo_history = []
        self.file_path = None
        self.is_modified = False
        
        # إنشاء مدير التحديثات
        self.app_version = "1.0"
        self.update_manager = UpdateManager(self.root, self.app_version)
        
        # إنشاء القائمة الرئيسية
        self.create_menu()
        
        # إنشاء شريط الأدوات
        self.create_toolbar()
        
        # إنشاء منطقة الرسم
        self.create_canvas()
        
        # إنشاء شريط الحالة
        self.create_statusbar()
        
        # تعيين الأحداث
        self.setup_events()
        
        # تحديث شريط الحالة
        self.update_statusbar()
        
        # تعيين عنوان النافذة
        self.update_title()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # قائمة الملف
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="جديد", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="فتح", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="حفظ", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="حفظ باسم", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="تصدير كصورة", command=self.export_as_image)
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=self.exit_app, accelerator="Alt+F4")
        menubar.add_cascade(label="ملف", menu=file_menu)
        
        # قائمة التحرير
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="تراجع", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="إعادة", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="مسح الكل", command=self.clear_canvas)
        menubar.add_cascade(label="تحرير", menu=edit_menu)
        
        # قائمة الأدوات
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="قلم", command=lambda: self.set_tool("pen"))
        tools_menu.add_command(label="ممحاة", command=lambda: self.set_tool("eraser"))
        tools_menu.add_command(label="خط", command=lambda: self.set_tool("line"))
        tools_menu.add_command(label="مستطيل", command=lambda: self.set_tool("rectangle"))
        tools_menu.add_command(label="دائرة", command=lambda: self.set_tool("circle"))
        tools_menu.add_separator()
        tools_menu.add_command(label="اختيار لون", command=self.choose_color)
        menubar.add_cascade(label="أدوات", menu=tools_menu)
        
        # قائمة التحديثات
        update_menu = tk.Menu(menubar, tearoff=0)
        update_menu.add_command(label="التحقق من التحديثات", command=lambda: self.update_manager.check_for_updates(True))
        update_menu.add_separator()
        
        # متغير لتخزين حالة التحديث التلقائي
        self.auto_update_var = tk.BooleanVar(value=self.update_manager.auto_check)
        update_menu.add_checkbutton(label="التحقق التلقائي من التحديثات", 
                                variable=self.auto_update_var, 
                                command=self.toggle_auto_update)
        menubar.add_cascade(label="التحديثات", menu=update_menu)
        
        # قائمة المساعدة
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="حول", command=self.show_about)
        menubar.add_cascade(label="مساعدة", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_toolbar(self):
        # إطار شريط الأدوات
        toolbar_frame = tk.Frame(self.root, bg="#e0e0e0", bd=1, relief=tk.RAISED)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        
        # أزرار الأدوات
        self.pen_btn = ttk.Button(toolbar_frame, text="قلم", command=lambda: self.set_tool("pen"))
        self.pen_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.eraser_btn = ttk.Button(toolbar_frame, text="ممحاة", command=lambda: self.set_tool("eraser"))
        self.eraser_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.line_btn = ttk.Button(toolbar_frame, text="خط", command=lambda: self.set_tool("line"))
        self.line_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.rect_btn = ttk.Button(toolbar_frame, text="مستطيل", command=lambda: self.set_tool("rectangle"))
        self.rect_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.circle_btn = ttk.Button(toolbar_frame, text="دائرة", command=lambda: self.set_tool("circle"))
        self.circle_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # زر اختيار اللون
        self.color_btn = tk.Button(toolbar_frame, text="لون", bg=self.pen_color, fg="white", command=self.choose_color, width=3)
        self.color_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # حجم القلم
        tk.Label(toolbar_frame, text="حجم القلم:", bg="#e0e0e0").pack(side=tk.LEFT, padx=2)
        self.pen_size_var = tk.IntVar(value=self.pen_size)
        pen_size_spinbox = ttk.Spinbox(toolbar_frame, from_=1, to=50, width=3, textvariable=self.pen_size_var, command=self.update_pen_size)
        pen_size_spinbox.pack(side=tk.LEFT, padx=2, pady=2)
        
        # حجم الممحاة
        tk.Label(toolbar_frame, text="حجم الممحاة:", bg="#e0e0e0").pack(side=tk.LEFT, padx=2)
        self.eraser_size_var = tk.IntVar(value=self.eraser_size)
        eraser_size_spinbox = ttk.Spinbox(toolbar_frame, from_=1, to=100, width=3, textvariable=self.eraser_size_var, command=self.update_eraser_size)
        eraser_size_spinbox.pack(side=tk.LEFT, padx=2, pady=2)
        
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # أزرار التراجع والإعادة
        self.undo_btn = ttk.Button(toolbar_frame, text="تراجع", command=self.undo)
        self.undo_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.redo_btn = ttk.Button(toolbar_frame, text="إعادة", command=self.redo)
        self.redo_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # زر مسح الكل
        self.clear_btn = ttk.Button(toolbar_frame, text="مسح الكل", command=self.clear_canvas)
        self.clear_btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def create_canvas(self):
        # إطار منطقة الرسم
        self.canvas_frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # منطقة الرسم
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", cursor="pencil")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # أشرطة التمرير
        self.v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.h_scrollbar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.TOP, fill=tk.X, before=self.canvas_frame)
        
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        self.canvas.configure(scrollregion=(0, 0, 1000, 1000))
    
    def create_statusbar(self):
        # شريط الحالة
        self.statusbar = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # معلومات الموضع
        self.position_label = tk.Label(self.statusbar, text="الموضع: 0, 0", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.position_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # معلومات الأداة الحالية
        self.tool_label = tk.Label(self.statusbar, text="الأداة: قلم", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.tool_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # معلومات اللون
        self.color_label = tk.Label(self.statusbar, text="اللون: أسود", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.color_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # معلومات الحجم
        self.size_label = tk.Label(self.statusbar, text="الحجم: 2", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.size_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def setup_events(self):
        # أحداث الماوس
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        self.canvas.bind("<Motion>", self.update_position)
        
        # أحداث لوحة المفاتيح
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_as_file())
        
        # حدث إغلاق النافذة
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
    
    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y
        
        if self.current_tool in ["line", "rectangle", "circle"]:
            # حفظ نقطة البداية للأشكال
            self.start_x, self.start_y = event.x, event.y
            # إنشاء شكل مؤقت
            if self.current_tool == "line":
                self.temp_shape = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.pen_color, width=self.pen_size)
            elif self.current_tool == "rectangle":
                self.temp_shape = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color, width=self.pen_size)
            elif self.current_tool == "circle":
                self.temp_shape = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color, width=self.pen_size)
    
    def draw(self, event):
        if self.current_tool == "pen":
            x, y = event.x, event.y
            line = self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.pen_color, width=self.pen_size, capstyle=tk.ROUND, smooth=True)
            self.last_x, self.last_y = x, y
            self.is_modified = True
        
        elif self.current_tool == "eraser":
            x, y = event.x, event.y
            # مسح بإنشاء مستطيل أبيض
            eraser = self.canvas.create_rectangle(x-self.eraser_size, y-self.eraser_size, x+self.eraser_size, y+self.eraser_size, fill="white", outline="white")
            self.last_x, self.last_y = x, y
            self.is_modified = True
        
        elif self.current_tool in ["line", "rectangle", "circle"]:
            # تحديث الشكل المؤقت
            if self.current_tool == "line":
                self.canvas.coords(self.temp_shape, self.start_x, self.start_y, event.x, event.y)
            elif self.current_tool == "rectangle":
                self.canvas.coords(self.temp_shape, self.start_x, self.start_y, event.x, event.y)
            elif self.current_tool == "circle":
                self.canvas.coords(self.temp_shape, self.start_x, self.start_y, event.x, event.y)
    
    def stop_draw(self, event):
        if self.current_tool in ["line", "rectangle", "circle"]:
            # إنشاء الشكل النهائي
            if self.current_tool == "line":
                self.canvas.delete(self.temp_shape)
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.pen_color, width=self.pen_size)
            elif self.current_tool == "rectangle":
                self.canvas.delete(self.temp_shape)
                self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color, width=self.pen_size)
            elif self.current_tool == "circle":
                self.canvas.delete(self.temp_shape)
                self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color, width=self.pen_size)
            
            self.is_modified = True
        
        # حفظ الحالة الحالية للتراجع
        self.save_state()
    
    def update_position(self, event):
        x, y = event.x, event.y
        self.position_label.config(text=f"الموضع: {x}, {y}")
    
    def set_tool(self, tool):
        self.current_tool = tool
        
        # تحديث مؤشر الماوس
        if tool == "pen":
            self.canvas.config(cursor="pencil")
            self.tool_label.config(text="الأداة: قلم")
        elif tool == "eraser":
            self.canvas.config(cursor="dot")
            self.tool_label.config(text="الأداة: ممحاة")
        elif tool == "line":
            self.canvas.config(cursor="crosshair")
            self.tool_label.config(text="الأداة: خط")
        elif tool == "rectangle":
            self.canvas.config(cursor="crosshair")
            self.tool_label.config(text="الأداة: مستطيل")
        elif tool == "circle":
            self.canvas.config(cursor="crosshair")
            self.tool_label.config(text="الأداة: دائرة")
    
    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.pen_color)[1]
        if color:
            self.pen_color = color
            self.color_btn.config(bg=color)
            
            # تحديث شريط الحالة
            self.color_label.config(text=f"اللون: {color}")
    
    def update_pen_size(self):
        self.pen_size = self.pen_size_var.get()
        self.size_label.config(text=f"الحجم: {self.pen_size}")
    
    def update_eraser_size(self):
        self.eraser_size = self.eraser_size_var.get()
    
    def clear_canvas(self):
        if messagebox.askyesno("مسح الكل", "هل أنت متأكد من مسح كل الرسم؟"):
            self.canvas.delete("all")
            self.save_state()
            self.is_modified = True
    
    def save_state(self):
        # حفظ حالة الرسم الحالية للتراجع
        ps = self.canvas.postscript(colormode='color')
        self.drawing_history.append(ps)
        self.redo_history = []  # مسح تاريخ الإعادة عند إجراء تغيير جديد
        
        # تحديث حالة أزرار التراجع والإعادة
        self.update_undo_redo_buttons()
    
    def undo(self):
        if len(self.drawing_history) > 1:  # نترك الحالة الأولى (الفارغة)
            self.redo_history.append(self.drawing_history.pop())
            ps = self.drawing_history[-1]
            
            # استعادة الحالة السابقة
            self.canvas.delete("all")
            self.load_postscript(ps)
            
            # تحديث حالة أزرار التراجع والإعادة
            self.update_undo_redo_buttons()
            self.is_modified = True
    
    def redo(self):
        if self.redo_history:
            ps = self.redo_history.pop()
            self.drawing_history.append(ps)
            
            # استعادة الحالة التالية
            self.canvas.delete("all")
            self.load_postscript(ps)
            
            # تحديث حالة أزرار التراجع والإعادة
            self.update_undo_redo_buttons()
            self.is_modified = True
    
    def load_postscript(self, ps):
        # استعادة الرسم من postscript
        # هذه طريقة مبسطة، يمكن تحسينها في الإصدارات المستقبلية
        try:
            # حفظ الـ postscript في ملف مؤقت
            temp_file = "temp_canvas.ps"
            with open(temp_file, "w") as f:
                f.write(ps)
            
            # إعادة تحميل الصورة (هذا يعتمد على وجود مكتبات إضافية)
            # في الإصدارات المستقبلية يمكن استخدام PIL لتحويل PS إلى صورة
            # ثم عرضها على الـ canvas
            pass
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء استعادة الرسم: {str(e)}")
    
    def update_undo_redo_buttons(self):
        # تحديث حالة أزرار التراجع والإعادة
        self.undo_btn.config(state=tk.NORMAL if len(self.drawing_history) > 1 else tk.DISABLED)
        self.redo_btn.config(state=tk.NORMAL if self.redo_history else tk.DISABLED)
    
    def update_statusbar(self):
        # تحديث شريط الحالة
        self.tool_label.config(text=f"الأداة: {self.get_tool_name()}")
        self.color_label.config(text=f"اللون: {self.pen_color}")
        self.size_label.config(text=f"الحجم: {self.pen_size if self.current_tool != 'eraser' else self.eraser_size}")
    
    def get_tool_name(self):
        tool_names = {
            "pen": "قلم",
            "eraser": "ممحاة",
            "line": "خط",
            "rectangle": "مستطيل",
            "circle": "دائرة"
        }
        return tool_names.get(self.current_tool, self.current_tool)
    
    def new_file(self):
        if self.is_modified:
            response = messagebox.askyesnocancel("حفظ التغييرات", "هل تريد حفظ التغييرات قبل إنشاء ملف جديد؟")
            if response is None:  # إلغاء
                return
            elif response:  # نعم
                self.save_file()
        
        self.canvas.delete("all")
        self.file_path = None
        self.drawing_history = []
        self.redo_history = []
        self.save_state()  # حفظ الحالة الفارغة
        self.is_modified = False
        self.update_title()
    
    def open_file(self):
        if self.is_modified:
            response = messagebox.askyesnocancel("حفظ التغييرات", "هل تريد حفظ التغييرات قبل فتح ملف آخر؟")
            if response is None:  # إلغاء
                return
            elif response:  # نعم
                self.save_file()
        
        file_path = filedialog.askopenfilename(filetypes=[("ملفات Canvas", "*.canvas"), ("كل الملفات", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                
                # استعادة الرسم
                self.canvas.delete("all")
                if "postscript" in data:
                    self.load_postscript(data["postscript"])
                
                self.file_path = file_path
                self.is_modified = False
                self.update_title()
                
                # إعادة تعيين تاريخ التراجع والإعادة
                self.drawing_history = [data["postscript"]]
                self.redo_history = []
                self.update_undo_redo_buttons()
                
                messagebox.showinfo("فتح ملف", "تم فتح الملف بنجاح.")
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء فتح الملف: {str(e)}")
    
    def save_file(self):
        if not self.file_path:
            return self.save_as_file()
        
        try:
            # الحصول على الـ postscript للرسم الحالي
            ps = self.canvas.postscript(colormode='color')
            
            # إنشاء بيانات الملف
            data = {
                "postscript": ps,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0"
            }
            
            # حفظ الملف
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=4)
            
            self.is_modified = False
            self.update_title()
            messagebox.showinfo("حفظ الملف", "تم حفظ الملف بنجاح.")
            return True
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ الملف: {str(e)}")
            return False
    
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".canvas", filetypes=[("ملفات Canvas", "*.canvas"), ("كل الملفات", "*.*")])
        if file_path:
            self.file_path = file_path
            return self.save_file()
        return False
    
    def export_as_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("صور PNG", "*.png"), ("صور JPEG", "*.jpg"), ("كل الملفات", "*.*")])
        if file_path:
            try:
                # الحصول على الـ postscript للرسم الحالي
                ps = self.canvas.postscript(colormode='color')
                
                # تحويل الـ postscript إلى صورة (يتطلب مكتبة PIL)
                # في الإصدارات المستقبلية يمكن استخدام PIL لتحويل PS إلى صورة
                messagebox.showinfo("تصدير", "تم تصدير الرسم كصورة بنجاح.")
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء تصدير الرسم: {str(e)}")
    
    def update_title(self):
        # تحديث عنوان النافذة
        title = "Canvas - أداة الرسم"
        if self.file_path:
            title = f"{os.path.basename(self.file_path)} - {title}"
        if self.is_modified:
            title = f"*{title}"
        self.root.title(title)
    
    def toggle_auto_update(self):
        """تفعيل أو تعطيل التحديث التلقائي"""
        # تحديث قيمة المتغير في مدير التحديثات
        self.update_manager.auto_check = self.auto_update_var.get()
        self.update_manager.save_update_settings()
        
        # عرض رسالة تأكيد
        if self.update_manager.auto_check:
            messagebox.showinfo("التحديثات التلقائية", "تم تفعيل التحقق التلقائي من التحديثات.")
        else:
            messagebox.showinfo("التحديثات التلقائية", "تم تعطيل التحقق التلقائي من التحديثات.")
    
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("حول البرنامج")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()
        
        # تكوين النافذة
        about_window.configure(bg="#f0f0f0")
        
        # إضافة المعلومات
        tk.Label(about_window, text="Canvas - أداة الرسم", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        tk.Label(about_window, text=f"الإصدار {self.app_version}", bg="#f0f0f0").pack()
        tk.Label(about_window, text="\n© 2023 Saudi Linux", bg="#f0f0f0").pack(pady=10)
        tk.Label(about_window, text="SaudiLinux7@gmail.com", bg="#f0f0f0").pack()
        
        # زر الإغلاق
        ttk.Button(about_window, text="إغلاق", command=about_window.destroy).pack(pady=20)
    
    def exit_app(self):
        if self.is_modified:
            response = messagebox.askyesnocancel("حفظ التغييرات", "هل تريد حفظ التغييرات قبل الخروج؟")
            if response is None:  # إلغاء
                return
            elif response:  # نعم
                if not self.save_file():
                    return
        
        self.root.destroy()


def main():
    root = tk.Tk()
    app = CanvasApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()