import platform
from tkinter.messagebox import showerror
import zipfile
import customtkinter as ctk
from tkinter.filedialog import askopenfilenames, asksaveasfilename as asksaveasfile, askdirectory
import customtkinter as _customtkinter
import CTkListbox as _ctklistbox
import screeninfo as _screeninfo
import CTkListbox
import os
from screeninfo import get_monitors
import py7zr

class App(ctk.CTk):
    def __init__(self, title):

        super().__init__()
        self.title(title)

        if platform.system() == 'Darwin':
            monitor = get_monitors()[0]
            self.geometry(f"{monitor.width}x{monitor.height}+0+0")
        else:
            self.state('zoomed')

        self.l_title = Label(self, text='ZippyARC', font=('Monospace', 40))

        self.l_title.pack(pady=20, side=ctk.TOP, anchor='w')

        WhatToDo(self)

        self.mainloop()

class WhatToDo(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('What would you like to do?')
        self.geometry('500x300')
        self.attributes("-topmost", True)
        self.resizable(False, False)

        def start_zip_instance():
            ZipArchiveWindow(self)
        def start_7z_instance():
            SevenZArchiveWindow(self)

        self.create_zip = Button(self, 'Create a ZIP archive...', ('', 13), start_zip_instance, 190, 30)
        self.create_7z = Button(self, 'Create a 7z archive...', ('', 13), start_7z_instance, 190, 30)

        self.create_zip.pack(padx=15, pady=15)
        self.create_7z.pack(padx=15, pady=15)

        self.deiconify()

class ZipArchiveWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        to_archive = []
        compressopt = ['Stored (full size)', 'Deflated (good)', 'Bzip2 (better)', 'LZMA (best)']
        selected_compression = ctk.StringVar(value=compressopt[1])
        self.title('Create a ZIP archive...')
        self.geometry('750x375')
        self.resizable(False, False)
        self.attributes("-topmost", True)

        def folder_to_archive():
            path = askdirectory()
            to_archive.append(path)
            self.to_archive_list.insert('end', path)


        def add_to_archive():
            self.iconify()
            path = askopenfilenames()
            self.deiconify()
            for f in path:
                to_archive.append(f)
                self.to_archive_list.insert('end', f)

        def remove_from_archive():
            self.to_archive_list.delete(self.to_archive_list.curselection())
            to_archive.remove(self.to_archive_list.get(self.to_archive_list.curselection()))

        def make_archive():
            self.iconify()
            to_zip = asksaveasfile(filetypes=[("ZIP files", "*.zip")])
            self.deiconify()
            with zipfile.ZipFile(to_zip, mode='w') as zf:
                for item in to_archive:
                    if os.path.isfile(item):
                        zf.write(item, arcname=os.path.basename(item))
                    elif os.path.isdir(item):
                        for root, dirs, files in os.walk(item):
                            for file in files:
                                full_path = os.path.join(root, file)
                                arcname = os.path.relpath(full_path, os.path.dirname(item))
                                if selected_compression.get() == 'LZMA (best)':
                                    zf.write(full_path, arcname=arcname, compresslevel=zipfile.ZIP_LZMA)
                                elif selected_compression.get() == 'Bzip2 (better)':
                                    zf.write(full_path, arcname=arcname, compresslevel=zipfile.ZIP_BZIP2)
                                elif selected_compression.get() == 'Deflated (good)':
                                    zf.write(full_path, arcname=arcname, compresslevel=zipfile.ZIP_DEFLATED)
                                else:
                                    zf.write(full_path, arcname=arcname, compresslevel=zipfile.ZIP_STORED)

        self.listandbuttons = Frame(self)
        self.addremovebuttons = Frame(self.listandbuttons)
        self.compression = Frame(self.addremovebuttons)
        self.to_archive_list = List(self.listandbuttons, width=400, height=200)
        self.add_to_list_btn = Button(self.addremovebuttons, 'Add file to archive...', ('', 13), add_to_archive, 190, 30)
        self.folder_to_list_btn = Button(self.addremovebuttons, 'Add folder to archive', ('', 13), folder_to_archive, 190, 30)
        self.remove_from_list_btn = Button(self.addremovebuttons, 'Remove from archive...', ('', 13), remove_from_archive, 190, 30)
        self.compression_size = Label(self.compression, 'Compression type:', font=('', 13))
        self.compression_type = Dropdown(self.compression, compressopt, selected_compression)
        self.compress_archive = Button(self.addremovebuttons, 'Compress to...', ('', 13), make_archive, 190, 30)


        self.to_archive_list.pack(side=ctk.LEFT, padx=15, pady=20)
        self.add_to_list_btn.pack(side=ctk.TOP, padx=15, pady=10)
        self.remove_from_list_btn.pack(side=ctk.BOTTOM, padx=15, pady=10)
        self.folder_to_list_btn.pack(side=ctk.BOTTOM, padx=15, pady=10)
        self.addremovebuttons.pack(padx=15, pady=10, side=ctk.RIGHT)
        self.listandbuttons.pack(padx=15, pady=10, side=ctk.LEFT)
        self.compression_size.pack(padx=15, pady=10, side=ctk.TOP)
        self.compression_type.pack(padx=15, pady=10, side=ctk.BOTTOM)
        self.compression.pack(padx=15, pady=10, side=ctk.BOTTOM)
        self.compress_archive.pack(pady=10, side=ctk.BOTTOM)

        self.deiconify()

class SevenZArchiveWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        to_archive = []
        compressopt = ['Copy (full size)', 'LZMA2', 'LZMA', 'Bzip2', 'PPMd']
        compressvol = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        selected_compression = ctk.StringVar(value=compressopt[0])
        selected_compressvol = ctk.StringVar(value=compressvol[7])
        self.title('Create a 7z archive...')
        self.geometry('750x460')
        self.resizable(False, False)
        self.attributes("-topmost", True)

        def folder_to_archive():
            self.iconify()
            self.deiconify()
            path = askdirectory()
            to_archive.append(path)
            self.to_archive_list.insert('end', path)


        def add_to_archive():
            self.iconify()
            path = askopenfilenames()
            self.deiconify()
            for f in path:
                to_archive.append(f)
                self.to_archive_list.insert('end', f)

        def remove_from_archive():
            self.to_archive_list.delete(self.to_archive_list.curselection())
            to_archive.remove(self.to_archive_list.get(self.to_archive_list.curselection()))

        def make_archive():
            self.iconify()
            to_7z = asksaveasfile(filetypes=[("7-Zip file", ("*.7z", "*.7zip"))])
            self.deiconify()

            if not to_7z:
                return

            compress_type = selected_compression.get()
            compress_level = int(selected_compressvol.get())

            if compress_type == 'Copy (full size)':
                filters = [{"id": py7zr.FILTER_COPY}]
            elif compress_type == 'LZMA2':
                filters = [{"id": py7zr.FILTER_LZMA2, "preset": compress_level}]
            elif compress_type == 'LZMA':
                filters = [{"id": py7zr.FILTER_LZMA, "preset": compress_level}]
            elif compress_type == 'Bzip2':
                filters = [{"id": py7zr.FILTER_BZIP2}]
            else:
                filters = [{"id": py7zr.FILTER_PPMD, "preset": compress_level}]

            with py7zr.SevenZipFile(to_7z, mode='w', filters=filters) as zf:
                for item in to_archive:
                    if os.path.isfile(item):
                        zf.write(item, arcname=os.path.basename(item))
                    elif os.path.isdir(item):
                        for root, dirs, files in os.walk(item):
                            for file in files:
                                full_path = os.path.join(root, file)
                                arcnm = os.path.relpath(full_path, os.path.dirname(item))
                                zf.write(full_path, arcname=arcnm)

        self.listandbuttons = Frame(self)
        self.addremovebuttons = Frame(self.listandbuttons)
        self.compression = Frame(self.addremovebuttons)
        self.to_archive_list = List(self.listandbuttons, width=400, height=200)
        self.add_to_list_btn = Button(self.addremovebuttons, 'Add file to archive...', ('', 13), add_to_archive, 190, 30)
        self.folder_to_list_btn = Button(self.addremovebuttons, 'Add folder to archive', ('', 13), folder_to_archive, 190, 30)
        self.remove_from_list_btn = Button(self.addremovebuttons, 'Remove from archive...', ('', 13), remove_from_archive, 190, 30)
        self.compression_size = Label(self.compression, 'Compression type:', ('', 13))
        self.compression_type = Dropdown(self.compression, compressopt, selected_compression)
        self.compression_volume = Label(self.compression, 'Compression level:', ('', 13))
        self.compression_vol = Dropdown(self.compression, compressvol, selected_compressvol)
        self.compress_archive = Button(self.addremovebuttons, 'Compress to...', ('', 13), make_archive, 190, 30)


        self.to_archive_list.pack(side=ctk.LEFT, padx=15, pady=20)
        self.add_to_list_btn.pack(side=ctk.TOP, padx=15, pady=10)
        self.remove_from_list_btn.pack(side=ctk.BOTTOM, padx=15, pady=10)
        self.folder_to_list_btn.pack(side=ctk.BOTTOM, padx=15, pady=10)
        self.addremovebuttons.pack(padx=15, pady=10, side=ctk.RIGHT)
        self.listandbuttons.pack(padx=15, pady=10, side=ctk.LEFT)
        self.compression_size.pack(padx=15, pady=10, side=ctk.TOP)
        self.compression_type.pack(padx=15, pady=10, side=ctk.BOTTOM)
        self.compression_volume.pack(padx=15, pady=10, side=ctk.BOTTOM)
        self.compression_vol.pack(padx=15, pady=10, side=ctk.BOTTOM)
        self.compression.pack(padx=15, pady=10, side=ctk.BOTTOM)
        self.compress_archive.pack(pady=10, side=ctk.BOTTOM)

        self.deiconify()


class Label(ctk.CTkLabel):
    def __init__(self, parent, text, font):
        super().__init__(parent)
        self.configure(text=text, font=font)


class Button(ctk.CTkButton):
    def __init__(self, parent, text, font, cmd, width, height):
        super().__init__(parent)
        self.configure(text=text, font=font, command=cmd, width=width, height=height)

class Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

class List(CTkListbox.CTkListbox):
    def __init__(self, parent, width, height):
        super().__init__(parent)
        self.configure(width=width, height=height)

class Dropdown(ctk.CTkOptionMenu):
    def __init__(self, parent, values, selected_value):
        super().__init__(parent)
        self.configure(values=values, variable=selected_value)

App('ZippyARC v1.0.1 build 1013')