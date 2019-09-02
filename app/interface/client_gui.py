import tkinter as tk

from threading import Thread
from time import sleep

from app.backend import client


class ChatLogScroll(tk.Frame):
    """A widget that contains a read-only text and a scrollbar for it."""
    text_field = None
    scrollbar = None

    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        self.pack()
        self._create_widgets()

    def _create_widgets(self):
        self.text_field = tk.Text(self)
        self.text_field.configure(state='disabled')
        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.text_field.yview)
        self.text_field.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.text_field.pack(side="left", fill="both", expand=True)

    def insert_message(self, message):
        self.text_field.configure(state='normal')
        self.text_field.insert(tk.END, f'{message}\n')
        self.text_field.configure(state='disabled')


class Login(tk.Frame):
    """Username input frame"""
    username_label = None
    username_field = None
    submit_button = None

    def __init__(self, parent: tk.Tk):
        """Init superclass instance. Init all inner widgets"""
        super().__init__(parent)
        self.pack()
        self._create_widgets()

    def _create_widgets(self):
        self.username_label = tk.Label(self, text='Username', )
        self.username_label.pack(side='top')
        self.username_field = tk.Entry(self)
        self.username_field.bind('<Return>', self._submit)
        self.username_field.pack(side='left')
        self.submit_button = tk.Button(self, text='Submit', command=self._submit)
        self.submit_button.pack(side='bottom')

    def _submit(self):
        """Creates an instance of ChatBox class and destroys all current widgets"""
        username = self.username_field.get()
        if username:
            for widget in self.master.winfo_children():
                widget.destroy()
            ChatBox(self.master, username)
            self.pack_forget()


class ChatBox(tk.Frame):
    """This is main chat widget. It contains chat log and message input field"""
    client_connection = None
    scroll_box = None
    text_input = None
    send_button = None

    def __init__(self, parent: tk.Tk, username: str):
        """Init superclass instance. Delete login widget. Init all inner widgets and init client socket"""
        super().__init__(parent)
        self.pack(side="top", fill="both",)
        self.master.title(username)
        self._create_widgets()
        self._create_client(username)

    def _create_client(self, username):
        """Create instance of client socket"""
        self.client_connection = client.Client(username=username)
        while not self.client_connection.start_client():
            sleep(2)
        else:
            self.scroll_box.insert_message(f'Connected')
            incoming = Thread(target=self._receive_message)
            incoming.daemon = True
            incoming.start()

    def _create_widgets(self):
        self.scroll_box = ChatLogScroll(self)
        self.scroll_box.pack(side="top", fill="both", expand=True)
        message = tk.StringVar()
        self.text_input = tk.Entry(master=self, textvariable=message)
        self.text_input.bind('<Return>', self._post_message)
        self.text_input.pack(side="left", fill='both', expand=True)
        self.send_button = tk.Button(master=self, text='Send', command=self._post_message)
        self.send_button.pack(side="right")

    def _post_message(self, event=None):
        """Send message to the server and add it to chat log"""
        message = self.text_input.get()
        if message != '':
            self.scroll_box.insert_message(f'You: {message}')
            self.client_connection.send_message(message)
            self.text_input.delete(0, 'end')

    def _receive_message(self):
        """Receive a message from the server and add it to chat log"""
        while True:
            if self.client_connection.connection:
                message = self.client_connection.receive_message()
                if message:
                    self.scroll_box.insert_message(message)
                else:
                    exit()
            else:
                exit()


def main():
    root = tk.Tk()
    root.title('Chat')
    root.geometry('300x450')
    root.resizable(width=False, height=False)
    Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()

