import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import json
import psutil

CONFIG_FILE = 'mupen64plus_config.json'

PLUGIN_INFO = {
    'mupen64plus-video-glide64mk2': 'Glide64mk2: A very compatible and generally fast plugin, suitable for most games.',
    'mupen64plus-video-rice': 'Rice: An older plugin with good compatibility, but generally slower than Glide64mk2.',
    'mupen64plus-video-gliden64': 'GLideN64: A modern plugin with high compatibility and good performance, but requires a powerful GPU.',
    'mupen64plus-video-angrylion': 'Angrylion: A very accurate plugin with excellent compatibility, but very demanding on the CPU.'
}

class Mupen64PlusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mupen64Plus GUI")
        self.root.geometry("400x300") 
        
        self.rom_path = tk.StringVar()
        self.mupen64plus_path = tk.StringVar()
        self.video_plugin = tk.StringVar()
        self.cheat_codes = tk.StringVar()  
        self.emulator_process = None  
        
        self.load_config()
        
        
        self.create_menus()
        
        
        self.create_widgets()
    
    def create_menus(self):
        menubar = tk.Menu(self.root)
        
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Select ROM", command=self.browse_rom)
        file_menu.add_command(label="Run ROM", command=self.run_rom)
        file_menu.add_command(label="Close ROM", command=self.close_rom)  
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Set Path and Video Plugin", command=self.open_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About Video Plugins", command=self.open_help)
        help_menu.add_command(label="Check Compatibility", command=self.check_compatibility)
        help_menu.add_command(label="Game Controls", command=self.show_game_controls)  
        help_menu.add_command(label="Mupen64Plus Controls", command=self.show_mupen64plus_controls)  # Add Mupen64Plus Controls option
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_widgets(self):
        
        tk.Label(self.root, text="ROM Path:").place(x=20, y=50)
        tk.Entry(self.root, textvariable=self.rom_path, width=40).place(x=100, y=50)
        
        
        tk.Label(self.root, text="Cheat Codes:").place(x=20, y=100)
        self.cheat_codes_entry = tk.Entry(self.root, textvariable=self.cheat_codes, width=40)
        self.cheat_codes_entry.place(x=100, y=100)
        
        
        tk.Button(self.root, text="Run ROM", command=self.run_rom).place(x=20, y=150)
        
        
        tk.Button(self.root, text="Show Cheat List", command=self.show_cheat_list).place(x=120, y=150)

    def browse_rom(self):
        rom_file = filedialog.askopenfilename(
            title="Select ROM",
            filetypes=(("N64 ROMs", "*.n64 *.z64 *.v64"), ("All files", "*.*"))
        )
        if rom_file:
            self.rom_path.set(rom_file)
    
    def run_rom(self):
        rom_path = self.rom_path.get()
        if not rom_path:
            messagebox.showerror("Error", "Please select a ROM file.")
            return
        
        mupen64plus_path = self.mupen64plus_path.get()
        if not mupen64plus_path or not os.path.exists(mupen64plus_path):
            messagebox.showerror("Error", "Please set the Mupen64Plus path in the settings.")
            return
        
        video_plugin = self.video_plugin.get()
        if not video_plugin:
            messagebox.showerror("Error", "Please set the video plugin in the settings.")
            return
        
        cheat_codes = self.cheat_codes.get()  
        command = [mupen64plus_path, '--gfx', video_plugin, '--cheats', cheat_codes, rom_path]  # Pass cheat codes as argument
        try:
            self.emulator_process = subprocess.Popen(command)
        except OSError as e:
            messagebox.showerror("Error", f"Failed to start emulator: {e}")

    def close_rom(self):
        if self.emulator_process:
            self.emulator_process.terminate()
            self.rom_path.set('')  
            self.rom_path.set('')
            self.cheat_codes.set('')  
        else:
            messagebox.showinfo("Info", "Please select a ROM file and then click on 'Run ROM'.")

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Set Path and Video Plugin")
        
        tk.Label(settings_window, text="Mupen64Plus Path:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(settings_window, textvariable=self.mupen64plus_path, width=40).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(settings_window, text="Browse", command=self.browse_mupen64plus).grid(row=0, column=2, padx=5, pady=5)
        
        tk.Label(settings_window, text="Video Plugin:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        video_plugins = list(PLUGIN_INFO.keys())
        video_plugin_menu = ttk.Combobox(settings_window, textvariable=self.video_plugin, values=video_plugins)
        video_plugin_menu.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(settings_window, text="Save", command=lambda: self.save_settings(settings_window)).grid(row=2, column=1, pady=10)
    
    def browse_mupen64plus(self):
        mupen64plus_file = filedialog.askopenfilename(
            title="Select Mupen64Plus Executable",
            filetypes=(("Executable files", "*.exe *.bin"), ("All files", "*.*"))
        )
        if mupen64plus_file:
            self.mupen64plus_path.set(mupen64plus_file)
    
    def save_settings(self, settings_window):
        self.save_config()
        settings_window.destroy()
    
    def open_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("About Video Plugins")
        
        help_text = ""
        for plugin, info in PLUGIN_INFO.items():
            help_text += f"{plugin}:\n{info}\n\n"
        
        tk.Label(help_window, text=help_text, justify=tk.LEFT, padx=10, pady=10).pack()
    
    def check_compatibility(self):
        ram = psutil.virtual_memory().total / (1024 ** 3)  
        recommended_plugin = ""

        if ram >= 8:
            recommended_plugin = 'mupen64plus-video-gliden64'
        elif 4 <= ram < 8:
            recommended_plugin = 'mupen64plus-video-glide64mk2'
        else:
            recommended_plugin = 'mupen64plus-video-rice'
        
        compatibility_message = (
            f"Detected RAM: {ram:.2f} GB\n\n"
            f"Recommended Video Plugin: {recommended_plugin}\n\n"
            f"{PLUGIN_INFO[recommended_plugin]}"
        )
        
        messagebox.showinfo("Compatibility Check", compatibility_message)

    def show_cheat_list(self):
        rom_path = self.rom_path.get()
        if not rom_path:
            messagebox.showerror("Error", "Please select a ROM file.")
            return
        
        mupen64plus_path = self.mupen64plus_path.get()
        if not mupen64plus_path or not os.path.exists(mupen64plus_path):
            messagebox.showerror("Error", "Please set the Mupen64Plus path in the settings.")
            return
        
        command = [mupen64plus_path, '--cheats', 'list', rom_path]
        try:
            cheat_list_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = cheat_list_process.communicate()
            if stderr:
                messagebox.showerror("Error", f"Failed to get cheat list: {stderr.decode()}")
            else:
                cheat_list_window = tk.Toplevel(self.root)
                cheat_list_window.title("Cheat List")
                tk.Label(cheat_list_window, text=stdout.decode(), padx=10, pady=10).pack()

                
                if self.cheat_codes.get():
                    tk.Label(cheat_list_window, text="Cheat Codes:", font=("Arial", 12, "bold")).pack()
                    tk.Label(cheat_list_window, text=self.cheat_codes.get(), padx=10, pady=5).pack()
        except OSError as e:
            messagebox.showerror("Error", f"Failed to get cheat list: {e}")

    def show_game_controls(self):
        game_controls_window = tk.Toplevel(self.root)
        game_controls_window.title("Game Controls")

        
        game_controls_info = """
        Analog Pad: Arrow Keys (left, right, down, up)
        C Up/Left/Down/Right: "I", "J", "K", "L"
        DPad Up/Left/Down/Right: "W", "A", "S", "D"
        Z trigger: "z"
        Left trigger: "x"
        Right trigger: "c"
        Start: "Enter" ("Return")
        A button: "left shift"
        B button: "left control"
        Select Mempack: ","
        Select Rumblepack: "."
        """

        tk.Label(game_controls_window, text=game_controls_info, padx=10, pady=10).pack()

    def show_mupen64plus_controls(self):
        mupen64plus_controls_window = tk.Toplevel(self.root)
        mupen64plus_controls_window.title("Mupen64Plus Controls")

        
        mupen64plus_controls_info = """
        Quit the emulator: Escape Key
        0-9: Select virtual 'slot' for save/load state (F5 and F7) commands
        Reset Emulator: F9 Key
        Slow down emulator by 5%: F10
        Speed up emulator by 5%: F11
        Take screenshot: F12
        Toggle between windowed and fullscreen: Alt+Enter
        Pause on/off: p or P
        Mute or unmute the sound: m or M
        Press "Game Shark" button (only if cheats are enabled): g or G
        Single frame advance while paused: / or ?
        Fast Forward (playback at 250% normal speed while F key is pressed): F
        Decrease volume: [
        Increase volume: ]
        Save State: F5 Key
        Load State: F7 Key
        """

        tk.Label(mupen64plus_controls_window, text=mupen64plus_controls_info, padx=10, pady=10).pack()

    def load_config(self):
        if os.path.isfile(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as file:
                    config = json.load(file)
                    self.mupen64plus_path.set(config.get('mupen64plus_path', ''))
                    self.video_plugin.set(config.get('video_plugin', ''))
            except json.JSONDecodeError:
                
                self.mupen64plus_path.set('')
                self.video_plugin.set('')
    
    def save_config(self):
        config = {
            'mupen64plus_path': self.mupen64plus_path.get(),
            'video_plugin': self.video_plugin.get()
        }
        with open(CONFIG_FILE, 'w') as file:
           
           json.dump(config, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = Mupen64PlusGUI(root)
    root.mainloop()

