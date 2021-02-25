#from tutorial:
# https://realpython.com/python-gui-tkinter/
# http://openbookproject.net/courses/python4fun/tkphone1.html
# https://www.geeksforgeeks.org/gui-chat-application-using-tkinter-in-python/

import AudioClient
import tkinter as tk
from socket import AF_INET, socket, SHUT_RDWR, SOCK_STREAM
from imutils.video import VideoStream
from Login_system import *
from sub_cmd import *
import io
import cv2
import sys
import threading
import os
import sub_cmd
import pub_cmd
import DBInterface

#for video
import numpy as np
import struct
import time
from PIL import Image
from PIL import ImageTk


class GUI:
    def __init__(self, information):

        # Intializing the user info
        self.user_info = information

        # Defining the current path
        self.CURPATH = os.path.dirname(os.path.abspath(__file__))
        

        # Making a GUI window
        self.window = tk.Tk()
        self.video_panel = None #video
        self.window.geometry("1000x550")
        self.window.configure(bg="#4DA8DA")
        
        # Title of GUI

        tk.Label(self.window, text="Night Light Baby Monitor",
                                 font="Helvetica 20 bold", bg="#4DA8DA", fg="#EEFBFB").pack()

        # Accessing the file in this path
        self.path = os.path.join(self.CURPATH, "Information", "night_light_logo.PNG")

        logo = PhotoImage(file = self.path)
        
        tk.Label(self.window, image = logo).pack()

        self.app = tk.Frame(self.window)
        self.app.pack()

        # Showing the action in the main display
        self.lmain = tk.Label(self.app)
        self.lmain.pack()


        # Setting the main display
        self.main_display()

        # Showing The Video Frame
        self.video_frame = tk.Frame(self.window)
        self.video_frame.configure(bg="#4DA8DA")
        self.video_frame.pack()

        # Showing the button in the display
        self.button_frame = tk.Frame(self.window)
        self.button_frame.configure(bg="#4DA8DA")
        self.button_frame.pack()

        self.mute = True
        # Inserting a rounded button for MIC
        self.path = os.path.join(self.CURPATH, "Information", "no_sound.png")
        self.loadimage = tk.PhotoImage(file = self.path)
        self.path = os.path.join(self.CURPATH, "Information", "sound.png")
        self.loadimage2 = tk.PhotoImage(file = self.path)

        # Initializing the notification
        self.getting_user_info()
        if(self.notification_info2 == True):
            self.notification = "On"
        else:
            self.notification = "Off"

        self.video_stream = False

        # Creating buttons
        self.button_a = tk.Button(self.button_frame, text="Watch the baby", font="Helvetica 11 bold",
                                  width=14, height=5, bg="aquamarine", fg="BLACK", command=self.handle_click_video_stream)
        self.button_b = tk.Button(self.button_frame, text="Play lullaby", font="Helvetica 11 bold",
                                  width=14, height=5, bg="aquamarine", fg="BLACK", command=self.handle_click_lullaby)
        self.button_c = tk.Button(self.button_frame, text="Listen To Audio", font="Helvetica 11 bold",
                                  bg="aquamarine", fg="black", image=self.loadimage, compound="bottom", command=self.handle_click_listen)
        self.button_d = tk.Button(self.button_frame, text="Changing Login Info", font="Helvetica 11 bold",
                                  width=18, height=5, bg="aquamarine", fg="BLACK", command=self.handle_click_changing_login_info)
        self.button_e = tk.Button(self.button_frame, text="Open Chat Window", font="Helvetica 11 bold",
                                  width=16, height=5, bg="aquamarine", fg="BLACK", command=self.handle_click_open_chat_window)
        self.button_f = tk.Button(self.button_frame, text="Current Notification" + "\n\n" + self.notification, font="Helvetica 11 bold", 
                                    width=17, height=5, bg="aquamarine", fg="BLACK", command=self.handle_click_notification)
        self.button_g = tk.Button(self.button_frame, text="Quit", font="Helvetica 11 bold",
                                  width=14, height=5, bg="aquamarine", fg="BLACK", command=self.quit_the_program)


        self.button_a.pack(side=tk.LEFT, fill=tk.BOTH)
        self.button_b.pack(side=tk.LEFT, fill=tk.BOTH)
        self.button_c.pack(side=tk.LEFT, fill=tk.BOTH)
        self.button_d.pack(side=tk.LEFT, fill=tk.BOTH)
        self.button_e.pack(side=tk.LEFT, fill=tk.BOTH)
        self.button_f.pack(side=tk.LEFT, fill=tk.BOTH)
        self.button_g.pack(side=tk.LEFT, fill=tk.BOTH)

        self.window.protocol("WM_DELETE_WINDOW", self.quit_the_program)
        self.window.mainloop()  # runs application

    # Event handlers
    def main_display(self):
        # Setting the main display
        try:
            self.txt = open("notification.txt", "r")
            self.txt = self.txt.readline()
        except:
            self.txt = "How can I help you?"
        self.lmain.configure(text=self.txt, justify="center",font="Helvetica 20 bold", bg="#4DA8DA", fg="#EEFBFB")
        self.lmain.after(1000, self.main_display)
	
    def enable_button(self):
        self.button_b.configure(state = tk.NORMAL)
        self.button_d.configure(state = tk.NORMAL)
    
    def handle_click_video_stream(self):
      
        if (self.video_stream == False):
            self.video_stream = True
            self.window.geometry("1000x1550")
            #initialize video client connections
            #use try/except for if server isn't running?
            self.gui_sock = socket()
            #gui_sock.connect(('3.140.200.49',6662)) # connect to Denny's AWS Server's public IP
            self.gui_sock.connect(('18.189.21.182',6662)) # connect to Robert's AWS Server's public IP
            print("Client User listening on port...")
            self.connection = self.gui_sock.makefile('rb')
            print("Client User connected")
            self.video_thread = threading.Thread(target=self.videoLoop,args=())
            self.video_thread.start()
            self.window.wm_title("Video Stream")
        else:
            self.video_stream = False
            self.window.geometry("1000x550")
            self.connection.close()
            self.gui_sock.close()
            
        # self.path = os.path.join(self.CURPATH, "vid_gui_client_latest_user1.py")
        # exec(open(self.path).read())


    def videoLoop(self):
    	# try:
    	# 	while True:
    	# 		self.image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
    	# 		if not self.image_len:
    	# 			print("invalid data from stream ")
    	# 			break
    	# 		print(self.image_len)
    	# 		self.image_stream = io.BytesIO()
    	# 		self.image_stream.write(connection.read(image_len))
    	# 		self.image_stream.seek(0)

    	# 		self.file_bytes = np.asarray(bytearray(self.image_stream.read()),dtype=np.uint8)
    	# 		self.raw_image = cv2.imdecode(self.file_bytes,cv2.IMREAD_COLOR)
    	# 		rgb_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB) #self vs no self?
    	# 		pil_image = Image.fromarray(rgb_frame)
    	# 		pil_image = ImageTk.PhotoImage(pil_image)
    			
    	# 		if self.video_panel is None:
    	# 			self.video_panel = tk.Label(image=pil_image)
    	# 			self.video_panel.image = pil_image
    	# 			self.video_panel.pack(side="left",padx=10, pady=10)
    	# 		else:
    	# 			self.panel.configure(image=image)
    	# 			self.panel.image = image
    	# except:
    	# 	print("Occurred Exception, closing socket")
    	# 	self.connection.close()
    	# 	self.gui_sock.close()
    	# finally:
    	# 	self.connection.close()
    	# 	self.gui_sock.close()
        try:
            while True:
                self.image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                if not self.image_len:
                    print("invalid data from stream ")
                    break
                print(self.image_len)
                self.image_stream = io.BytesIO()
                self.image_stream.write(self.connection.read(self.image_len))
                self.image_stream.seek(0)

                self.file_bytes = np.asarray(bytearray(self.image_stream.read()),dtype=np.uint8)
                self.raw_image = cv2.imdecode(self.file_bytes,cv2.IMREAD_COLOR)
                self.rgb_image = cv2.cvtColor(self.raw_image, cv2.COLOR_BGR2RGB) #self vs no self?
                self.pil_image = Image.fromarray(self.rgb_image)
                self.pil_image = ImageTk.PhotoImage(self.pil_image)
                
                if self.video_panel is None:
                    self.video_panel = tk.Label(image=self.pil_image)
                    self.video_panel.image = self.pil_image
                    self.video_panel.pack(padx=10, pady=10)
                else:
                    self.video_panel.configure(image=self.pil_image)
                    self.video_panel.image = self.pil_image

        except:
            print("Occurred Exception, closing socket")
            self.connection.close()
            self.gui_sock.close()

    def handle_click_lullaby(self):
        self.button_b.configure(state = tk.DISABLED)
        
        self.new_window = tk.Toplevel(self.window)
        self.new_window.configure(bg="#4DA8DA")

        # Making a scroll bar display
        self.scroll_bar = tk.Scrollbar(self.new_window)
        self.option = tk.Listbox(self.new_window, bd=0, bg="#007CC7", fg="#EEFBFB",
                                 font="Helvetica 11 bold", yscrollcommand=self.scroll_bar.set)
        self.inserting_option()
        self.option.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scroll_bar.config(command=self.option.yview)

        self.select = tk.Button(self.new_window, text="Play Song", bd=0, bg="#4DA8DA",
                                fg="BLACK", font="Helvetica 11 bold", command=self.play_sound)
        self.select.pack(fill=tk.BOTH)
        
        self.pause = tk.Button(self.new_window, text="Pause Song", bd=0, bg="#4DA8DA",
                                fg="BLACK", font="Helvetica 11 bold", command= self.pause_sound)
        self.pause.pack(fill=tk.BOTH)

        self.resume = tk.Button(self.new_window, text="Resume Song", bd=0, bg="#4DA8DA",
                                fg="BLACK", font="Helvetica 11 bold", command= self.resume_sound)
        self.resume.pack(fill=tk.BOTH)

        self.stop = tk.Button(self.new_window, text="Stop Song", bd=0, bg="#4DA8DA",
                                fg="BLACK", font="Helvetica 11 bold", command= self.stop_sound)
        self.stop.pack(fill=tk.BOTH)

        self.new_window.protocol("WM_DELETE_WINDOW", self.enable_button)

    def handle_click_listen(self):
        
        if self.mute == True:
            self.button_c.config(image = self.loadimage2)
            # Audio Streaming
            self.audio_conn = AudioClient.AudioClient(write = False)    
            self.audio_conn.write = True
            self.audio_conn.start()
            thread = threading.Thread(target=self.audio_conn.recv)
            thread.start()
            self.mute = False 

        elif self.mute == False:
            self.button_c.config(image = self.loadimage)
            self.audio_conn.write = False 
            self.audio_conn.stop()
            self.mute = True

    def handle_click_changing_login_info(self):
        self.button_d.configure(state = tk.DISABLED)
        
        self.login_screen = tk.Toplevel(self.window)
        self.login_screen.geometry("300x300")
        self.login_screen.configure(bg="#4DA8DA")
        tk.Label(self.login_screen, text = "Please choose either one of these button", bg = "#4DA8DA", fg = "black").pack()
        tk.Label(self.login_screen, text = "", bg = "#4DA8DA").pack()
        tk.Button(self.login_screen, text = "Changing Password", bg = "white", fg= "black", font = "Helvetica 11 bold", command = self.changing_password).pack()
        tk.Label(self.login_screen, text = "", bg = "#4DA8DA").pack()
        tk.Button(self.login_screen, text = "Changing Email", bg = "white", fg= "black", font = "Helvetica 11 bold", command = self.changing_email).pack()

        self.login_screen.protocol("WM_DELETE_WINDOW", self.enable_button)

    def handle_click_open_chat_window(self):
        self.enable_button()
        self.button_e.configure(state = tk.DISABLED)
        
        self.chat_window = tk.Toplevel(self.window)
        self.chat_window.title("Chatter")

        self.messages_frame = tk.Frame(self.chat_window)
        self.my_msg = tk.StringVar()  # For the messages to be sent.
        self.scrollbar = tk.Scrollbar(self.messages_frame)  # To navigate through past messages.
        
        # Following will contain the messages.
        self.msg_list = tk.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side= tk.RIGHT, fill= tk.Y)
        self.msg_list.pack(side= tk.LEFT, fill= tk.BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()


        self.guide = tk.Label(self.chat_window, text = "Type your messages below")
        self.guide.pack()
        self.entry_field = tk.Entry(self.chat_window, textvariable = self.my_msg)
        self.entry_field.bind("<Return>", self.send)
        self.entry_field.pack()
        self.send_button = tk.Button(self.chat_window, text="Send", command = self.send)
        self.send_button.pack()

        self.chat_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        #----Now comes the sockets part----
        HOST = '18.189.21.182'#input('Enter host: ')
        PORT = int (33000)

        self.BUFSIZ = 1024
        ADDR = (HOST, PORT)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)
        self.client_socket.send(self.username_info2.encode("utf8"))
        receive_thread = threading.Thread(target = self.receive)
        receive_thread.start()

    def handle_click_notification(self):
        
        db = DBInterface.DBInterface()
        if(self.notification == "On"):
            self.notification = "Off"
            self.button_f.config(text="Current Notification" + "\n\n" + self.notification)
            pub_cmd.publish(client, "update email")
            db.switch_notification(self.ID_info2, False)
        elif (self.notification == "Off"):
            self.notification = "On"
            self.button_f.config(text="Current Notification" + "\n\n" + self.notification)
            pub_cmd.publish(client, "update email")
            db.switch_notification(self.ID_info2, True)


    def quit_the_program(self):
        if(self.mute == False):
            self.audio_conn.stop()
            self.audio_conn.write = False
        if(self.video_stream == True):
            self.connection.close()
            self.gui_sock.close()
        sys.exit()


    # Some funcions for play song button
    def inserting_option(self):
        self.option.insert(tk.END, "First Lullaby")
        self.option.insert(tk.END, "Second Lullaby")
        self.option.insert(tk.END, "Third Lullaby")
        self.option.insert(tk.END, "Fourth Lullaby")

    def play_sound(self):
        scrollbar_command = self.option.get('active')
        if scrollbar_command == 'First Lullaby':
            pub_cmd.publish(client, "lullaby1.mp3")
        elif scrollbar_command == 'Second Lullaby':
            pub_cmd.publish(client, "lullaby2.mp3")
        elif scrollbar_command == 'Third Lullaby':
            pub_cmd.publish(client, "lullaby3.mp3")
        elif scrollbar_command == 'Fourth Lullaby':
            pub_cmd.publish(client, "lullaby4.mp3")


    def pause_sound(self):
        pub_cmd.publish(client, "pause")

    def resume_sound(self):
        pub_cmd.publish(client, "resume")
    
    def stop_sound(self):
        pub_cmd.publish(client, "pause")

    # Some Functions for Chat Client
    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                self.msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.msg_list.insert(tk.END, self.msg)
            except OSError:  # Possibly client has left the chat.
                break
    
    def send(self, event=None):  # event is passed by binders.
        """Handles sending of messages."""
        self.msg = self.my_msg.get()
        self.my_msg.set("")  # Clears input field.
        self.client_socket.send(bytes(self.msg, "utf8"))
        if self.msg == "quit":
            self.chat_window.destroy()
            self.client_socket.shutdown(SHUT_RDWR)
            self.client_socket.close()

    
    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.button_e.configure(state = tk.NORMAL)
        self.my_msg.set("quit")
        self.send()
    

    # Some functions for changing login info
    def changing_password(self):
        self.password = tk.StringVar()
        self.password2 = tk.StringVar()
        self.password_screen = tk.Toplevel(self.login_screen)
        self.password_screen.geometry("300x300")
        self.password_screen.configure(bg = "white")
        self.password_lable = Label(self.password_screen, text="Current Password * ", bg = "white")
        self.password_lable.pack()
        self.password_entry = Entry(self.password_screen, textvariable=self.password, show='*')
        self.password_entry.pack()
        tk.Label(self.password_screen, text="", bg = "white").pack()
        self.password_lable2 = Label(self.password_screen, text="New Password * ", bg = "white")
        self.password_lable2.pack()
        self.password_entry2 = Entry(self.password_screen, textvariable=self.password2, show='*')
        self.password_entry2.pack()
        tk.Label(self.password_screen, text="" , bg = "white").pack()
        tk.Button(self.password_screen, text="Update", width=10, height=1, bg = "cyan", command = self.register_pass).pack()

        self.info_screen = tk.Frame(self.password_screen)
        self.info_screen.pack()
        self.info_regis = tk.Label(self.info_screen)
        self.info_regis.pack()

    def changing_email(self):
        self.password = tk.StringVar()
        self.email_address = tk.StringVar()
        self.email_screen = tk.Toplevel(self.login_screen)
        self.email_screen.geometry("300x300")
        self.email_screen.configure(bg = "white")
        self.password_lable = Label(self.email_screen, text="Current Password * ", bg = "white")
        self.password_lable.pack()
        self.password_entry = Entry(self.email_screen, textvariable=self.password, show='*')
        self.password_entry.pack()
        tk.Label(self.email_screen, text="", bg = "white").pack()
        self.email_lable = Label(self.email_screen, text="Email Address * ", bg = "white")
        self.email_lable.pack()
        self.email_address_entry = Entry(self.email_screen, textvariable=self.email_address)
        self.email_address_entry.pack()
        tk.Label(self.email_screen, text="" , bg = "white").pack()
        tk.Button(self.email_screen, text="Update", width=10, height=1, bg = "cyan", command = self.register_email).pack()

        self.info_screen = tk.Frame(self.email_screen)
        self.info_screen.pack()
        self.info_regis = tk.Label(self.info_screen)
        self.info_regis.pack()

    def register_pass(self):
        self.password_info = self.password.get()
        self.password_entry.delete(0, END)
        self.password_info2 = self.password2.get()
        self.password_entry2.delete(0, END)

        if(isBlank(self.password_info) or isBlank(self.password_info2)):
            self.empty_filler()
            self.info_regis.configure(text="Failed", justify = "center", bg = "white", fg="green", font=("calibri", 11))
        else:
            db = DBInterface.DBInterface()
            log = db.login(self.username_info2, self.password_info)
            data2 = json.loads(log)
            if(data2["status"] == True):
                db.update_password(self.ID_info2, self.password_info, self.password_info2)
                self.info_regis.configure(text="Success Changing Password", justify = "center", bg = "white", fg="green", font=("calibri", 11))
            else:
                self.info_regis.configure(text="Wrong Current Password", justify = "center", bg = "white", fg="green", font=("calibri", 11))

    
    def register_email(self):
        self.password_info = self.password.get()
        self.password_entry.delete(0, END)
        self.email_info = self.email_address.get()
        self.email_address_entry.delete(0, END)

        if(isBlank(self.email_info) or isBlank(self.password_info)):
            self.empty_filler()
            self.info_regis.configure(text="Failed", justify = "center", bg = "white", fg="green", font=("calibri", 11))
        else:
            db = DBInterface.DBInterface()
            log = db.login(self.username_info2, self.password_info)
            data2 = json.loads(log)
            if(data2["status"] == True):
                db.update_email(self.ID_info2, self.email_info2, self.email_info, self.password_info)
                pub_cmd.publish(client, "update email")
                self.info_regis.configure(text="Success Changing Email", justify = "center", bg = "white", fg="green", font=("calibri", 11))
            else:
                self.info_regis.configure(text="Wrong Current Password", justify = "center", bg = "white", fg="green", font=("calibri", 11))


    def getting_user_info(self):
        self.username_info2 = self.user_info["username"]
        self.email_info2 = self.user_info["email"] 
        self.notification_info2 = self.user_info["notification"]
        self.ID_info2 = self.user_info["id"]
        
    def empty_filler(self):
        self.empty_filler_screen = Toplevel()
        self.empty_filler_screen.title("Error Registration")
        self.empty_filler_screen.geometry("200x100")
        Label(self.empty_filler_screen, text="You have not filled the filler box").pack()
        Button(self.empty_filler_screen, text="OK", bg = "cyan", command= self.delete_empty_filler_screen).pack()

    def delete_empty_filler_screen(self):
        self.empty_filler_screen.destroy()

    def isBlank(self, my_string):
        if my_string and my_string.strip():
            return False
        return True

main_account_screen()
information = get_user_info()
if (verified() == True):
    client = pub_cmd.connect_mqtt()
    sub_client = sub_cmd.connect_mqtt()
    g = GUI(information)

# client = pub_cmd.connect_mqtt()
# sub_client = sub_cmd.connect_mqtt()
# g = GUI("Leondi")
