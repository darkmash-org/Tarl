#################################################################
"""
Part of Tarl Project ~ Darkmash

This file contains code which works in bg doing all real stuff..
"""
#################################################################


try:
    from rich import print
except:
    pass
import time
import os


def install_req():
    try:
        os.system("pip install numpy opencv-python pyautogui pynput pyaudio wave moviepy rich")
    except:
        try:
            os.system("pip3 install numpy opencv-python pyautogui pynput pyaudio wave moviepy rich")
        except:
            print("[red]  [-] Couldnt install required Libs.. \n[/red]")
            quit()

    print("\n\n[dark_orange3]  [/] If you saw some error regarding installation of any modules please try to install your self..[\dark_orange3]")


print("[green]  [+] Installing required libs...\n [/green]")


#install_req()


from moviepy.editor import *
from pynput import keyboard
from pynput import mouse
import numpy as np
import pyautogui
import threading
import pyaudio
import utils
import wave
import cv2




class TarlCore:
    """
    out_file - filename

    fps - int

    area - (x , y , w , h)

    keyboard_captions -  F/T , gives caption 
    for what ever is being done with keyboard..

    mouse_icon - Location to the image ,  A icon 
    for your mouse..

    show_mouse - F/T ,If you want to hide the 
    pointer..

    audio_in -  T/F ,If to record your audio from 
    mic..

    
    bgm - Location to your bgm file, To add bgm to 
    your recording..
    """
    def __init__(self , out_file , fps = 60 ,  area = (), keyboard_captions = False , show_mouse = False ,  mouse_icon = None ,  audio_in = False , bgm = None):


        if area == ():
            self.area = (0,0,pyautogui.size()[0],pyautogui.size()[1])

        self.STOP_ALL = False
        self.FOUND_KEYS = {}
        self.CUR_KEY = ""
        self.mouse_x = 0
        self.mouse_y = 0
       
        self.out_file = out_file
        self.fps = fps 
        self.keyboard_captions = keyboard_captions
        self.show_mouse = show_mouse
        self.mouse_icon = mouse_icon

        if self.mouse_icon == None:
            self.mouse_icon = "mouse_pointer.png" 

        try: 
            self.mouse_pointer = cv2.imread(self.mouse_icon,-1)
        except:
            print("\n[red]  [-] Mouse pointer - icon not found , switching to default one.. [/red]")
            self.mouse_pointer = cv2.imread("mouse_pointer.png",-1)

        self.mouse_pointer  = cv2.cvtColor(self.mouse_pointer , cv2.COLOR_BGRA2RGBA)


        self.audio_in = audio_in
        self.audio_out = False
        self.bgm = bgm

        # define the codec
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        
        self.key_listener = keyboard.Listener(
        on_press = self.on_press,
        on_release = self.on_release)
        
        self.key_listener.start()
        
        self.mouse_listener = mouse.Listener(
         on_move = self.on_move,
        on_click = self.on_click,
        on_scroll = self.on_scroll)

        self.mouse_listener.start()


    def record_screen(self):
        
        # create the video write object
        out = cv2.VideoWriter(f"{self.out_file}.avi", self.fourcc, self.fps, (self.area[2],self.area[3]))
        
        delay = 1/self.fps
        
        print("[green]  [+] Starting to record screen..[/green]")
        
        if self.audio_in:
            threading.Thread(target=self.audio_recording_mic).start()
        
        while not self.STOP_ALL:
            # make a screenshot
            img = pyautogui.screenshot()
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            if self.keyboard_captions == True and  self.CUR_KEY != "":
                overlay = self.make_key_image(self.CUR_KEY)
                

                # load resized image as grayscale
                img = overlay
                print(img.shape)
                h, w , z= list(img.shape)

                # load background image as grayscale
                back = frame
                hh, ww , z= back.shape

                # compute xoff and yoff for placement of upper left corner of resized image
                yoff = round((hh-h)/2)
                xoff = round((ww-w)/2)

                # use numpy indexing to place the resized image in the center of background image
                result = back.copy()
                
                result[yoff:yoff+h, xoff:xoff+w] = img
                
                frame = result
                self.CUR_KEY = ""
            
            if self.show_mouse == True:
                h = self.mouse_pointer.shape[0]
                w = self.mouse_pointer.shape[1]
                frame[self.mouse_y:self.mouse_y+h, self.mouse_x:self.mouse_x+w] = self.mouse_pointer

            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)


            out.write(frame)
        
        print("[green]  [+] Stoping with no error..  [/green]")
        
        # make sure everything is closed when exited
        cv2.destroyAllWindows()
        out.release()
        self.combine_all()

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
            self.CUR_KEY = f"Presd {key.char}"
        except AttributeError:
            self.CUR_KEY = f"Presd {key}"
            print('special key {0} pressed'.format(key))

    def on_release(self, key):
        print('{0} released'.format(key))
        
        self.CUR_KEY = f"Reld {key}"

        if key == keyboard.Key.esc:
            self.STOP_ALL = True 
            # Stop listener
            return False

    def on_move(self, x, y):
        print('Pointer moved to {0}'.format((x, y)))
        self.mouse_x = x
        self.mouse_y = y

    def on_click(self , x, y, button, pressed):
        print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))

    def on_scroll(self , x, y, dx, dy):
        print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))
        self.scroll = True

    def make_key_image(self, key):	
        try:
            return self.FOUND_KEYS[key]
        
        except:
            # path
            path = "a.png"
	
            # Reading an image in default mode
            image = cv2.imread(path,1)
	
            # font
            font = cv2.FONT_HERSHEY_SIMPLEX

            # org
            org = (round(image.shape[1]/2-len(str(key))/2), round(image.shape[0]/2-len(str(key))/2))
            org = (50,round(image.shape[0]/2))
            print(org)
            # fontScale
            fontScale = 1

            # Blue color in BGR
            color = (0, 0, 0)

            # Line thickness of 2 px
            thickness = 3 

            # Using cv2.putText() method
            image = cv2.putText(image, key, org, font,fontScale, color, thickness, cv2.LINE_AA)

            self.FOUND_KEYS[key] = image
            
            return image

    def audio_recording_mic(self):


        # the file name output you want to record into
        filename = "recorded_in.wav"
        # set the chunk size of 1024 samples
        chunk = 1024
        # sample format
        FORMAT = pyaudio.paInt16
        # mono, change to 2 if you want stereo
        channels = 1
        # 44100 samples per second
        sample_rate = 44100
        record_seconds = 5
        # initialize PyAudio object
        p = pyaudio.PyAudio()
        # open stream object as input & output
        stream = p.open(format=FORMAT,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)
        frames = []
        
        print("[green]  [+] Recording audio - in... [/green]")

        while not self.STOP_ALL:
            data = stream.read(chunk)
            frames.append(data)

        print("\n[green]  [+] Finished recording audio. [green]")
        # stop and close stream
        stream.stop_stream()
        stream.close()
        # terminate pyaudio object
        p.terminate()
        # save audio file
        # open the file in 'write bytes' mode
        wf = wave.open(filename, "wb")
        # set the channels
        wf.setnchannels(channels)
        # set the sample format
        wf.setsampwidth(p.get_sample_size(FORMAT))
        # set the sample rate
        wf.setframerate(sample_rate)
        # write the frames as bytes
        wf.writeframes(b"".join(frames))
        # close the file
        wf.close()

    def combine_all(self):
        
        print("\n[green]  [+] Combining.. [/green]")

        # loading video
        clip = VideoFileClip(f"{self.out_file}.avi")
        
        if self.audio_in:
            try:

                # loading audio file
                audioclip_a = AudioFileClip("recorded_in.wav")
                clip = clip.set_audio(audioclip_a)
            except:

                print("[red]  [-] There was some error, regarding audio-in..[/red]")

            try:
                os.remove("recorded_in.wav")
            except:
                pass


        if self.audio_out:
            try:
                # loading audio file
                audioclip_b = AudioFileClip("recorded_out.wav")
                if audio_in:
                        audioclip_b = CompositeAudioClip([video_clip.audio, audio_clip])

                clip = clip.set_audio(audioclip_b)

            except:

                print("[red]  [-] There was some error, regarding audio-out..[/red]")

            try:
                os.remove("recorded_out.wav")

            except:
                pass
        
        if self.bgm != None:
            try:
                # loading audio file
                audioclip_c = AudioFileClip(self.bgm)
                if audio_in or audio_out:
                    
                    audioclip_c = audioclip_c.volumex(-3)
                    
                    audioclip_c = CompositeAudioClip([video_clip.audio, audio_clip])

                clip = clip.set_audio(audioclip_c)

            except:

                print("[red]  [-] There was some error, regarding bgm..[/red]")


        clip.write_videofile(f"{self.out_file}.mp4")
