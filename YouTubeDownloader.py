from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

#Functionality:

#Function for downloading:
def download_video():
    try:
        video_link = entry.get()
        resolution = video_resolution.get()
        if resolution == '' and video_link == '':
            showerror(title='Error', message='Please enter both the video URL and resolution.')
        elif resolution == '':
            showerror(title='Error', message='Please select a video resolution.')
        elif resolution == 'None':
            showerror(title='Error', message='None is an invalid video resolution.\n'\
                    'Please select a valid video resolution.')    
        else:
            try:
                def on_progress(stream, chunk, bytes_remaining):
                    total_size = stream.filesize
                    def get_formatted_size(total_size, factor=1024, suffix='B'):
                        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                            if total_size < factor:
                                return f"{total_size:.2f}{unit}{suffix}"
                            total_size /= factor
                        return f"{total_size:.2f}Y{suffix}"
                    formatted_size = get_formatted_size(total_size)
                    bytes_downloaded = total_size - bytes_remaining
                    percentage_completed = round(bytes_downloaded / total_size * 100)
                    progress_bar['value'] = percentage_completed
                    progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                    root.update()

                video = YouTube(video_link, on_progress_callback=on_progress)
                video.streams.filter(res=resolution).first().download()
                showinfo(title='Download Complete', message='Video has been downloaded successfully.')
                progress_label.config(text='')
                progress_bar['value'] = 0
            except:
                showerror(title='Download Error', message='Failed to download video for this resolution')
                progress_label.config(text='')
                progress_bar['value'] = 0
    except:
        showerror(title='Download Error', message='An error occurred while trying to ' \
                    'download the video\nThe following could ' \
                    'be the causes:\n->Invalid link\n->No internet connection\n'\
                     'Make sure you have stable internet connection and the video link is valid')
        progress_label.config(text='')
        progress_bar['value'] = 0




#Function for searching for available resolutions
def searchResolution():
    video_link = entry.get()
    if video_link == "":
         showerror(title='Error', message='Provide the video link please!')
    else:
        try:
            showinfo(title='Search In Progress', message='Please wait for the resolutions to load')
            video = YouTube(video_link)
            resolutions = []
            for i in video.streams.filter(file_extension='mp4'):
                resolutions.append(i.resolution)
            video_resolution['values'] = resolutions
            showinfo(title='Search Complete', message='Check the Combobox for the available video resolutions')
        except:
            showerror(title='Error', message='An error occurred while searching for video resolutions!\n'\
                'Below might be the causes\n->Unstable internet connection\n->Invalid link')

#Functions to run the above functions as a threads.

def searchThread():
    t1 = threading.Thread(target=searchResolution)
    t1.start()

def downloadThread():
    t2 = threading.Thread(target=download_video)
    t2.start()





#GUI Section Start

#Window Layout
root = ttkb.Window(themename="cyborg")
root.geometry("750x700")
root.title("YouTube Video Downloader")
root.resizable(height=FALSE, width=FALSE)

#Canva for Logo and text.
canvas = Canvas(root, width=400, height=200, bg='black', highlightthickness=0)
canvas.place(anchor='center', relx=0.5, rely=0.1)
logo = PhotoImage(file='logo.png')
canvas.create_text(200,150, fill='#5bc0de', text="YouTube Video Downloader", font=('Helvetica 21 bold'))
canvas.create_image(200,75, image=logo)
canvas.pack()

#Frame Layout
frame = Frame(root, width=500, height=400, highlightbackground ="#5bc0de", highlightthickness=2)
frame.place(anchor='center', relx=0.5, rely=0.6)

#Label
label = ttkb.Label(frame, text="Enter The Video's URL: ", style="primary.TLabel",
                  font=('Helvetica 18 bold'))
label.place(relx=0.22, rely=0.05)

#Entry
entry = ttkb.Entry(frame, style='primary.TEntry', width=60,)
entry.place(relx=0.12, rely=0.15)

#Label for Combobox and Combobox
resolution_label = ttkb.Label(frame, text='Resolution: ', style='primary.TLabel', font=('Helbetica 14 italic'))
resolution_label.place(relx=0.13, rely=0.25)
video_resolution = ttkb.Combobox(frame, style='primary.TCombobox', width=20)
video_resolution.place(relx=0.56, rely=0.25)

#Button to Search for resolutions
search_resolution = ttkb.Button(frame,takefocus=False, text='Search For Available Resolutions',command=searchThread ,style='primary.Outline.TButton')
Style = ttkb.Style()
Style.configure('TButton', font=('Helvetica', 14))
search_resolution.place(relx=0.20, rely=0.36)

#Progress Bar section
progress_label = ttkb.Label(frame, text='', style='primary.TLabel', font=('Helbetica 12 italic'))
progress_label.place(relx=0.22, rely=0.46)
progress_bar = ttkb.Progressbar(frame, style='primary.Horizontal.TProgressbar', length=400)
Style.configure('primary.Horizontal.TProgressbar', thickness=25, bordercolor='#5bc0de', troughcolor='#191919')
progress_bar.place(relx=0.09, rely=0.62)

#Donload Button
download_button = ttkb.Button(frame,takefocus=False, text='Download',style='primary.TButton', command=downloadThread)
download_button.place(relx=0.34, rely=0.75)
Style.configure('primary.TButton', background='#191919', font=('Helvetica', 20))

#GUI Section End




root.mainloop()