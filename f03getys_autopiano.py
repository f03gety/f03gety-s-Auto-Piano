# source code
import customtkinter as ctk
import keyboard
import pynput
import threading
import time
import webbrowser

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class f03getyAutoPiano:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("f03gety's Auto Piano")
        
        self.root.geometry("650x950")
        
        self.root.attributes("-topmost", True)
        
        self.is_playing = False
        self.current_pos = 0
        self.keyboard_controller = pynput.keyboard.Controller()
        
        self.setup_gui()
        self.setup_hotkeys()
        
    def setup_gui(self):
        title = ctk.CTkLabel(self.root, text="f03gety's Auto Piano", 
                            font=ctk.CTkFont(size=26, weight="bold"))
        title.pack(pady=25)
        
        sheet_label = ctk.CTkLabel(self.root, text="Paste Your Sheet Music Here", 
                                  font=ctk.CTkFont(size=15, weight="bold"))
        sheet_label.pack(anchor="w", padx=35)
        
        self.music_text = ctk.CTkTextbox(self.root, height=320, 
                                        font=ctk.CTkFont(family="Consolas", size=14))
        self.music_text.pack(padx=35, pady=12, fill="x")
        self.music_text.bind("<KeyRelease>", self.on_sheet_changed)
        
        next_label = ctk.CTkLabel(self.root, text="Next Notes", 
                                 font=ctk.CTkFont(size=15, weight="bold"))
        next_label.pack(anchor="w", padx=35, pady=(20,5))
        
        self.next_notes = ctk.CTkTextbox(self.root, height=150, 
                                        font=ctk.CTkFont(family="Consolas", size=14))
        self.next_notes.pack(padx=35, pady=8, fill="x")
        self.next_notes.configure(state="disabled")
        
        self.toggle_btn = ctk.CTkButton(self.root, text="▶ ACTIVATE HOTKEYS", 
                                       font=ctk.CTkFont(size=19, weight="bold"),
                                       height=55, corner_radius=16,
                                       command=self.toggle_play)
        self.toggle_btn.pack(pady=30)
        
        self.status_label = ctk.CTkLabel(self.root, text="Ready - Click Activate to start", 
                                        font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=5)
        
        hotkey_label = ctk.CTkLabel(self.root, text="Hotkeys:   -     =     [     ]", 
                                   font=ctk.CTkFont(size=17, weight="bold"), 
                                   text_color="#ffff00")
        hotkey_label.pack(pady=18)
        
        # Blue clickable GitHub Link
        self.github_link = ctk.CTkButton(self.root, 
                                        text="🔗 Open Source on GitHub",
                                        font=ctk.CTkFont(size=13, weight="bold"),
                                        text_color="#58a6ff",           # GitHub blue
                                        fg_color="transparent",
                                        hover_color="#2b2b2b",
                                        height=35,
                                        command=self.open_github)
        self.github_link.pack(pady=10)
    
    def open_github(self):
        webbrowser.open("https://github.com/f03gety/f03gety-s-Auto-Piano")
    
    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.toggle_btn.configure(text="⏹ STOP", fg_color="#ff4444")
            self.status_label.configure(text="ACTIVATED - Use hotkeys to play", text_color="#00ff88")
            self.current_pos = 0
        else:
            self.toggle_btn.configure(text="▶ ACTIVATE HOTKEYS", fg_color="#3B8ED0")
            self.status_label.configure(text="Stopped", text_color="gray")
    
    def update_next_notes(self):
        text = self.music_text.get("0.0", "end").strip()
        cleaned = text.replace("\n", "").replace(" ", "").replace("/", "")
        
        if self.current_pos >= len(cleaned):
            self.current_pos = 0
        
        remaining = text[self.current_pos:self.current_pos + 110]
        
        self.next_notes.configure(state="normal")
        self.next_notes.delete("0.0", "end")
        self.next_notes.insert("0.0", remaining if remaining else "End of sheet")
        self.next_notes.configure(state="disabled")
    
    def play_next_note(self):
        if not self.is_playing:
            return
            
        text = self.music_text.get("0.0", "end").strip()
        if not text:
            return
            
        cleaned = text.replace("\n", "").replace(" ", "").replace("/", "")
        
        if self.current_pos >= len(cleaned):
            self.current_pos = 0
        
        if cleaned[self.current_pos] == '[':
            end = cleaned.find(']', self.current_pos)
            if end != -1:
                keys = cleaned[self.current_pos + 1:end]
                self.current_pos = end + 1
            else:
                keys = cleaned[self.current_pos]
                self.current_pos += 1
        else:
            keys = cleaned[self.current_pos]
            self.current_pos += 1
        
        try:
            for char in keys:
                self.keyboard_controller.press(char)
                self.keyboard_controller.release(char)
                time.sleep(0.01)
        except:
            pass
        
        self.update_next_notes()
    
    def setup_hotkeys(self):
        def on_hotkey():
            if self.is_playing:
                threading.Thread(target=self.play_next_note, daemon=True).start()
        
        for key in ['-', '=', '[', ']']:
            keyboard.add_hotkey(key, on_hotkey, suppress=True)
    
    def on_sheet_changed(self, event=None):
        if not self.is_playing:
            self.current_pos = 0
            self.update_next_notes()
    
    def run(self):
        self.root.mainloop()
    
    def on_close(self):
        keyboard.unhook_all()
        self.root.destroy()

if __name__ == "__main__":
    app = f03getyAutoPiano()
    app.run()
