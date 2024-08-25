import customtkinter
from pynput import keyboard
from collections import deque
from threading import Thread
import time
import pyglet


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.sep = ' ' * 2
        # font
        pyglet.font.add_file('fonts/Inter-Regular.ttf')


        self.key_queue = deque(maxlen=5)
        self.title("Keystroke")
        self.geometry("500x150")
        # Frameless
        self.overrideredirect(True)

        # Transparent
        self.wm_attributes("-topmost", True)
        # -------- Transparent ---------
        self.config(bg='white')
        self.wm_attributes("-transparentcolor", "white")
        # ------------------------------

        # Hidden in taskbar
        self.wm_attributes("-toolwindow", True)

        self.button = customtkinter.CTkButton(self, text="Close", command=self.button_callback, bg_color="blue")
        # self.button.pack()
        self.label = customtkinter.CTkLabel(self, fg_color="black", text='', font=(
            'Inter', 40), text_color='#eee', corner_radius=10, padx=10, pady=10)
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        t = Thread(target=self.auto_pop)
        t.daemon = True  # the thread t will be terminated when the main thread ends.
        t.start()

    def button_callback(self):
        print("Close the windows")
        self.destroy()

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
            self.key_queue.append(key.char.upper())
        except AttributeError:
            print('special key {0} pressed'.format(key.name))
            self.key_queue.append(key.name.title().split('_')[0])
        except Exception as e:
            print(repr(e))
        finally:
            self.label.configure(text=self.sep.join(list(self.key_queue)))

    def auto_pop(self):
        while True:
            if len(self.key_queue):
                self.label.pack()
                self.key_queue.popleft()
                time.sleep(1)
                self.label.configure(text=self.sep.join(list(self.key_queue)))
            else:
                self.label.pack_forget()


if __name__ == '__main__':
    app = App()
    app.mainloop()
