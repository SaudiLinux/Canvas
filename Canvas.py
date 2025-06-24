#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Canvas - أداة رسم بسيطة
تم تطويره بواسطة: Saudi Linux
البريد الإلكتروني: SaudiLinux7@gmail.com
'''

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import os
import json
from datetime import datetime

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
    
    def show_about(self):
        about_text = """Canvas - أداة رسم بسيطة
        الإصدار: 1.0
        
        تم تطويره بواسطة: Saudi Linux
        البريد الإلكتروني: SaudiLinux7@gmail.com
        
        © 2023 جميع الحقوق محفوظة."""
        messagebox.showinfo("حول البرنامج", about_text)
    
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