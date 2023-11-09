import random
import sys
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image
from moviepy.editor import VideoFileClip
import imageio
from shutil import copyfile
import subprocess
import os
import tempfile
import shutil
from pydub import AudioSegment
import pyfbx
from pyfbx import *

Spezma_Vers = "Alpha-1.0"

class Boot:
    state = 0

    choose_file = None
    cnv_file = None
    dwn_file = None

    @staticmethod
    def make_can(canvas):
        canvas.pack()
        Boot.create_gradient_background(canvas)

    @staticmethod
    def create_gradient_background(canvas):
        width = 720
        height = 480
        num_steps = 10

        for i in range(num_steps):
            factor = i * 5
            gradient_color = f'#{i * 10:02X}{i * 10:02X}{i * 10:02X}'
            if i == num_steps - 1:
                gradient_color = "#808080"
            canvas.create_rectangle(factor, factor, width - factor, height - factor, fill=gradient_color, outline="")

    @staticmethod
    def select_file():
        global file, ext, sp
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if file_path:
            file = file_path
            ext = file_path.split(".")[-1]
        sp = Spezma(file, ext)

    def download_card(self, root, ddv):

        def on_dropdown_change(*args):
            selected_file = ddv.get()
            self.selected_file_label.config(text=f"Selected File Type: {selected_file}")

        # Attach a callback function to monitor changes in the dropdown selection
        ddv.trace_add("write", on_dropdown_change)
        sp.desired_ext = ddv

        txt = open(f"{sp.ft}_exts.txt", "r")
        txt = txt.read().split("\n")

        self.dwn_file = tk.Button(root, text="Download File", bg="gray", bd=2, font=("Times New Roman", 20),
                                  command=sp.convert_file)
        self.dwn_file.place(x=360, y=240 - 25, width=200, height=50)

        self.choose_file = tk.OptionMenu(root, ddv, *txt)
        self.choose_file.place(x=160, y=240 - 25, width=100, height=50)

        self.selected_file_label = tk.Label(root, text="", bg="gray", font=("Times New Roman", 16))
        self.selected_file_label.place(x=100, y=300, height=30)
        self.selected_file_label.config(text=f"Selected File Type: {ddv.get()}")

    async def open(self):

        root = tk.Tk()
        root.title("Spezma")

        dropdown_var = tk.StringVar()

        canvas = tk.Canvas(root, width=720, height=480)

        self.state = Spezma.get_state()

        imp_file = tk.Button(root, text="Import File", bg="gray", bd=2, font=("Times New Roman", 20),
                             command=self.select_file)
        imp_file.place(x=360 - 100, y=240 - 25, width=200, height=50)

        def update_gui():
            # print(self.state)
            # print(type(self.imp_file))

            if not self.state:
                pass
            elif self.state:
                Boot.download_card(self, root, dropdown_var)
                imp_file.destroy()
                imp_file.pack_forget()
            root.after(500, update_gui)

        Boot.make_can(canvas)
        update_gui()

        root.mainloop()


class Spezma:

    @staticmethod
    def change_state():
        Boot.state = Boot.state + 1

    @staticmethod
    def get_state() -> int:
        return Boot.state

    file = None
    ext = "."
    desired_ext = ""
    FINAL_FILE = None
    ft = ""
    exit_stat = 0

    def __init__(self, cv_file, cv_ext):
        self.file, self.ext = cv_file, "." + cv_ext
        self.ft = self.classify_file()
        self.change_state()
        self.desired_ext = tk.StringVar()
        # print("Finished file processing")

    def classify_file(self) -> str:
        types = ["IMAGE", "VIDEO", "AUDIO", "DOCUMENT", "OBJECT"]
        for cfy in types:
            spec_exts = open(f"{cfy}_exts.txt", "r")
            files = spec_exts.read()
            if cfy.__eq__("IMAGE"):
                files = files[10::]
                # print(files)
            if self.ext in files:
                return cfy

    def convert_file(self):
        ID = random.randint(0, 9132019)
        file = self.file
        initial_ext = self.ext
        desired_ext = self.desired_ext.get()
        if self.ft.__eq__("IMAGE"):
            # print("converting image")
            self.image_convert(ID, file, initial_ext, desired_ext)
        elif self.ft.__eq__("VIDEO"):
            # print("converting video")
            self.video_convert(ID, file, initial_ext, desired_ext)
        elif self.ft.__eq__("AUDIO"):
            # print("converting audio")
            self.audio_convert(ID, file, initial_ext, desired_ext)
        elif self.ft.__eq__("DOCUMENT"):
            # print("converting document")
            self.document_convert(ID, file, initial_ext, desired_ext)
        elif self.ft.__eq__("OBJECT"):
            # print("converting object")
            # self.object_convert(ID, file, initial_ext, desired_ext)
            self.call_bluff()
        else:
            self.call_bluff()

    def image_convert(self, ID, file, initial_ext, desired_ext):
        if desired_ext.__eq__(".mp4"):
            output_video_filename = f'SpezmaID{ID}-{initial_ext[1:]}2{desired_ext[1:]}{desired_ext}'
            downloads_folder = os.path.expanduser('~') + '/Downloads'
            output_video_path = os.path.join(downloads_folder, output_video_filename)
            if os.path.exists(file):
                image = cv2.imread(file)
                height, width, layers = image.shape
                duration = 5
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(output_video_path, fourcc, 1.0 / duration, (width, height))
                for _ in range(int(duration * 25)):
                    video_writer.write(image)
                video_writer.release()
                return
        elif desired_ext.__eq__("MAKE_TRANSPARENCY"):
            try:
                with Image.open(file) as img:
                    img = img.convert("RGBA")
                    image_data = list(img.getdata())
                    new_image_data = []
                    white_color = (255, 255, 255)
                    transparency_threshold = 230
                    for pixel in image_data:
                        r, g, b, a = pixel
                        if r == 255 and g == 255 and b == 255:
                            a = 0
                        elif r >= transparency_threshold and g >= transparency_threshold and b >= transparency_threshold:
                            a = 0
                        new_image_data.append((r, g, b, a))
                    img.putdata(new_image_data)
                    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                    new_file_name = f'SpezmaID{ID}-{initial_ext[1:]}2TRANSPARENT_ADDON.png'
                    save_path = os.path.join(downloads_folder, new_file_name)
                    img.save(save_path)
                    self.conversion_status()
                    return
            except Exception as e_pil:
                self.conversion_status(False, e_pil)
        try:
            with Image.open(file) as img:
                downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                new_file_name = f'SpezmaID{ID}-{initial_ext[1:]}2{desired_ext[1:]}{desired_ext}'
                save_path = os.path.join(downloads_folder, new_file_name)
                img.save(save_path)
                self.conversion_status()
        except Exception as e_pil:
            try:
                with imageio.get_reader(file, format=initial_ext[1:]) as reader:
                    images = [im for im in reader]
                    if images:
                        save_path = os.path.join(os.path.expanduser("~"), "Downloads", new_file_name)
                        imageio.imsave(save_path, images[0], format=desired_ext[1:])
                    else:
                        self.conversion_status(False)
            except Exception as e_io:
                self.conversion_status(False, e_io)

    def video_convert(self, ID, file, initial_ext, desired_ext):
        input_file_path = file
        output_file_path = os.path.join(os.path.expanduser("~"), "Downloads", f"SpezmaID{ID}-{initial_ext[1:]}2{desired_ext[1:]}{desired_ext}")
        if not input_file_path.lower().endswith(initial_ext.lower()):
            self.conversion_status(False, "Failure to read file")
        try:
            clip = VideoFileClip(input_file_path)
            codec = Spezma.get_codec(desired_ext)
            clip.write_videofile(output_file_path, codec=codec)
            clip.close()
        except Exception as e:
            self.conversion_status(False, e)

    @staticmethod
    def get_codec(desired_ext):
        codec_mapping = {
            "avi": "Xvid",
            "mp4": "libx264",
            "mov": "libx264",
            "mkv": "libx264",
            "wmv": "wmv2",
            "flv": "libx264",
            "mpeg": "mpeg2video",
            "webm": "libvpx",
            "3gp": "h263",
            "asf": "wmv2",
            "m2ts": "libx264",
            "mpg": "mpeg2video",
            "ts": "libx264",
            "m4v": "libx264",
            "ogg": "libtheora",
            "rm": "rv40",
            "rmvb": "rv40",
            "vob": "mpeg2video",
            "dat": "mpeg1video",
            "divx": "mpeg4",
            "xvid": "mpeg4",
            "mts": "libx264",
            "ogv": "libtheora",
            "swf": "libx264",
            "avchd": "libx264",
            "dv": "dvvideo",
            "mpv": "mpeg1video",
            "mpv2": "mpeg2video",
            "mpe": "mpeg2video"
        }

        # Use the specified codec or default to libx264
        return codec_mapping.get(desired_ext, "libx264")

    def audio_convert(self, ID, file, initial_ext, desired_ext):
        output_filename = f'SpezmaID{ID}-{initial_ext[1:]}2{desired_ext[1:]}{desired_ext}'
        input_file = file
        output_file = os.path.join(os.path.expanduser('~'), 'Downloads', output_filename)
        try:
            command = ['ffmpeg', '-i', input_file, output_file]
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            # print(f'Conversion complete using ffmpeg. Output file: {output_file}')
            self.conversion_status()
        except subprocess.CalledProcessError as e:
            try:
                audio = AudioSegment.from_file(input_file, format=initial_ext)
                audio.export(output_file, format=desired_ext)
                # print(f'Conversion complete using pydub. Output file: {output_file}')
                self.conversion_status()
            except Exception as e:
                # print(f'Error converting audio using pydub: {e}')
                self.conversion_status(False, e)

    def document_convert(self, ID, file, initial_ext, desired_ext):
        source_file = os.path.abspath(file)
        if not os.path.exists(source_file):
            self.conversion_status(False, f"Failure to find existing path: {source_file}")
        output_filename = f"SpezmaID{ID}-{initial_ext[1:]}2{desired_ext[1:]}{desired_ext}"
        user_downloads_folder = os.path.expanduser("~/Downloads")
        destination_file = os.path.join(user_downloads_folder, output_filename)
        try:
            shutil.copyfile(source_file, destination_file)
            self.conversion_status()
        except Exception as e:
            self.conversion_status(False, e)

    def object_convert(self, ID, file, initial_ext, desired_ext):
        #output_filename = f'SpezmaID{ID}-{initial_ext[1:]}2{desired_ext[1:]}{desired_ext}'
        #input_file = file
        #output_file = os.path.join(os.path.expanduser('~'), 'Downloads', output_filename)
        #scene = pyfbx.Scene()
        pass

    def call_bluff(self):
        newroot = tk.Tk()
        newroot.title("Excess Implementation Required")
        newroot.geometry("360x244")
        lab = tk.Label(newroot, text=f"File type format '{self.ext}' unsupported \nor unimplemented for Spezma Version: {Spezma_Vers}")
        lab.pack()
        newroot.mainloop()

    def conversion_status(self, success=True, exception=None):
        status = "Success" if success else "Fail"
        self.exit_stat = not success
        newroot = tk.Tk()
        newroot.title(f"Conversion {status}")
        newroot.geometry("360x244")
        lab = tk.Label(newroot,
                       text=f"Conversion of {self.file}\nfrom {self.ext} to {self.desired_ext}: {status}\n\n"
                            f"Excess notes/errors: {exception}")
        lab.pack()
        exit_button = tk.Button(newroot, text="Exit Spezma", command=self.exit_spezma)
        exit_button.pack()
        newroot.mainloop()

    def exit_spezma(self):
        sys.exit(self.exit_stat)
