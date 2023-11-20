import os
from tkinter import Tk
from tkinter import Entry
from tkinter import Label
from tkinter import Button
from tkinter import PhotoImage
from tkinter import Frame
from tkinter import Canvas
from tkinter import Scrollbar
from pytube import Playlist,YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip


is_mp3 = True

line_spacing = 20

BG_COLOR = "#181818"
FG_COLOR = "white"
ADD_COLOR_1 = "#242424"
ADD_COLOR_2 = "#ffaab6"
ADD_COLOR_3 = "#1F1F1F"

root = Tk()

mp3 = PhotoImage(file = "mp3.png")
mp4 = PhotoImage(file = "mp4.png")

is_mp3_button = Button(root)
download_button = Button(root)

label_greeting = Label(root)

input_link = Entry(root)

output_frame = Frame(root)

output_canvas = Canvas(output_frame)

output_scrollbar = Scrollbar(output_frame)


def remove_special_char(text):
    temp = text
    spec_chars = [",",";",":",".","'",'"',"#","%","&","{","}","\\","/","*","?","<",">","@","!","$","+","=","`"]

    for c in spec_chars:
        temp = temp.replace(c,"")

    return temp

def check_link():
    if "playlist" in input_link.get():
        download_playlist()
    else:
        download_video()

def switch_format():
    global is_mp3

    if is_mp3:
        is_mp3_button.config(image = mp4)
        is_mp3 = False
    else:
        is_mp3_button.config(image = mp3)
        is_mp3 = True


def download_video():
    link = input_link.get()
    if link == "":
        return
    
    global line_spacing
    
    yt = YouTube(link)
    yt_name = remove_special_char(yt.title)

    vid_path = yt.streams.filter(only_audio=False, 
                              progressive=True, 
                              file_extension="mp4").order_by('resolution').desc().first().download(output_path="exports",
                                                                                                   skip_existing=True)
    if is_mp3:
        video_file = vid_path
        audio_file = vid_path.replace(".mp4",".mp3")

        vid_clip = VideoFileClip(video_file)
        
        audio_clip = vid_clip.audio
        audio_clip.write_audiofile(audio_file,verbose=False,logger=None)

        audio_clip.close()
        vid_clip.close()

        os.remove(video_file)


    msg = f"'{yt_name}' has been downloaded."
    output_canvas.create_text(5,line_spacing,text=msg,fill=ADD_COLOR_2,anchor="w")
    line_spacing += 20
    root.update()

def download_playlist():
    link = input_link.get()
    if link == "":
        return
    
    global line_spacing
    
    p = Playlist(link)
    p_name = remove_special_char(p.title)

    path = f"exports\\{p_name}"

    for video in p.videos:
        vid_path = video.streams.filter(only_audio=False, 
                                   progressive=True, 
                                   file_extension="mp4").order_by('resolution').desc().first().download(output_path=path,
                                                                                                        skip_existing=True)
        
        i = vid_path.find(p_name)+1
        v_name = vid_path[i+len(p_name):]
        vid_name = v_name.replace(".mp4","")

        if is_mp3:
            video_file = f"exports\\{p_name}\\{vid_name}.mp4"
            audio_file = f"exports\\{p_name}\\{vid_name}.mp3"

            vid_clip = VideoFileClip(video_file)
            
            audio_clip = vid_clip.audio
            audio_clip.write_audiofile(audio_file,verbose=False,logger=None)

            audio_clip.close()
            vid_clip.close()

            os.remove(f"exports\\{p_name}\\{vid_name}.mp4")
        
        
        msg = f"'{vid_name}' has been downloaded."
        output_canvas.create_text(5,line_spacing,text=msg,fill=ADD_COLOR_2,anchor="w")
        line_spacing += 20
        root.update()
        
        
    msg = f"\nPlaylist '{p_name}' has been completely downloaded.\n"
    output_canvas.create_text(5,line_spacing,text=msg,fill=ADD_COLOR_2,anchor="w")
    line_spacing += 20
    msg = "---------------------------"*3 +">"
    output_canvas.create_text(5,line_spacing,text=msg,fill=ADD_COLOR_2,anchor="w")
    line_spacing += 20


def configure_attributes():
    root.geometry("500x500")
    root.title("YT Downloader")
    root.iconbitmap("ytd_icon.ico")
    root.config(background=BG_COLOR)
    # next line removes default window around app (cant close unless press Alt + F4)
    #root.overrideredirect(True)

    is_mp3_button.config(command = switch_format,
                         image = mp3,
                         borderwidth=0,
                         background=BG_COLOR,
                         activebackground=BG_COLOR)
    
    download_button.config(text="DOWNLOAD", 
                           command=check_link,
                           padx=10,
                           pady=5,
                           background="lightblue")
    
    
    label_greeting.config(text="YOUTUBE DOWNLOADER\n\nPaste the link below and click ' DOWNLOAD '",
                          font=("Arial",10),
                          pady=20,
                          background=BG_COLOR,
                          foreground=FG_COLOR)
    
    input_link.config(font=("Arial",8),
                      width=60,
                      background=ADD_COLOR_3,
                      foreground=FG_COLOR)

    output_frame.config(width=400,
                        height=100,
                        bd=1,
                        background=BG_COLOR,
                        pady=20)
    
    output_canvas.config(bg=ADD_COLOR_1,
                         width=500,
                         height=100,
                         scrollregion=(0,0,500,1000),
                         yscrollcommand=output_scrollbar.set)
    
    output_scrollbar.config(orient="vertical",
                            command=output_canvas.yview)
    
def pack_elements():
    label_greeting.pack()
    input_link.pack()
    is_mp3_button.pack(pady = 50)
    download_button.pack()

    output_frame.pack(expand=True,fill="both")
    output_scrollbar.pack(side="right",fill="y")
    output_canvas.pack(side="left", fill="both",expand=True)




if __name__ == '__main__':
    configure_attributes()
    pack_elements()

    root.mainloop()
    