import tkinter as tk
from tkinter import messagebox
import socket
import threading
import asyncio

class Chat(object):
    def __init__(self, name, client):
        super().__init__()
        self.window = tk.Tk()
        self.window.title("Client")
        self.username = name
        self.client = client
        self.topFrame = tk.Frame(self.window)
        self.lblName = tk.Label(self.topFrame, text = "Name:").pack(side=tk.LEFT)
        self.entName = tk.Label(self.topFrame, text = self.username)
        self.entName.pack(side=tk.LEFT)
        #btnConnect.bind('<Button-1>', connect)
        self.topFrame.pack(side=tk.TOP)
        self.displayFrame = tk.Frame(self.window)
        self.lblLine = tk.Label(self.displayFrame, text="*********************************************************************").pack()
        self.scrollBar = tk.Scrollbar(self.displayFrame)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tkDisplay = tk.Text(self.displayFrame, height=20, width=55)
        self.tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.tkDisplay.tag_config("tag_your_message", foreground="blue")
        self.tkDisplay.tag_config("dm", foreground="red")
        self.tkDisplay.tag_config("player", foreground="green")
        self.scrollBar.config(command=self.tkDisplay.yview)
        self.tkDisplay.config(yscrollcommand=self.scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
        self.displayFrame.pack(side=tk.TOP)

        self.bottomFrame = tk.Frame(self.window)
        self.tkMessage = tk.Text(self.bottomFrame, height=2, width=55)
        self.tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
        self.tkMessage.config(highlightbackground="grey")
        self.tkMessage.bind("<Return>", (lambda event: self.getChatMessage(self.tkMessage.get("1.0", tk.END))))
        self.bottomFrame.pack(side=tk.BOTTOM)
        self.tkMessage.config(state=tk.NORMAL)
        self.start()


    def start(self):
        threading._start_new_thread(self.receive_message_from_server, ())
        self.window.mainloop() 
        
    async def start_event_loop(self):
        while True:
            await asyncio.sleep(0.1)

    def receive_message_from_server(self):
        print("started")
        while True:
            message = self.client.recv(65535).decode()   
            from_server = message

            if not from_server: break

            # display message from server on the chat window

            # enable the display area and insert the text and then disable.
            # why? Apparently, tkinter does not allow us insert into a disabled Text widget :(
            texts = self.tkDisplay.get("1.0", tk.END).strip()
            
            if from_server.startswith('DM'):
                text_type = "dm"
            else:
                text_type = "player"

            self.tkDisplay.config(state=tk.NORMAL)
            if len(texts) < 1:
                self.tkDisplay.insert(tk.END, from_server, text_type)
            else:
                self.tkDisplay.insert(tk.END, "\n\n"+ from_server, text_type)

            self.tkDisplay.config(state=tk.DISABLED)
            self.tkDisplay.see(tk.END)

            # print("Server says: " +from_server)

        self.window.destroy()


    def getChatMessage(self, msg):

        msg = msg.replace('\n', '')
        texts = self.tkDisplay.get("1.0", tk.END).strip()

        # enable the display area and insert the text and then disable.
        # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
        self.tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            self.tkDisplay.insert(tk.END, "You: " + msg, "tag_your_message") # no line
        else:
            self.tkDisplay.insert(tk.END, "\n\n" + "You: " + msg, "tag_your_message")

        self.tkDisplay.config(state=tk.DISABLED)
        self.send_message_to_server(msg)
        self.tkDisplay.see(tk.END)
        self.tkMessage.delete('1.0', tk.END)


    def send_message_to_server(self, msg):
        client_msg = str(msg+'\n')
        print(client_msg)
        self.client.send(client_msg.encode())
        if msg == "exit":
            self.client.close()
            self.window.destroy()
        print("Sending message")

    def setName(self, name):
        self.username = name

