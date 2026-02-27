import customtkinter as ctk
from textblob import TextBlob
from collections import Counter
import re
import pyperclip  # You might need to run: pip install pyperclip

# Set the modern theme and appearance
ctk.set_appearance_mode("Dark")  # Start in Dark mode
ctk.set_default_color_theme("green")

class SpellCorrectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("✨ Modern Spell Checker & Corrector")
        
        # 1. Responsive Size Logic
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Adjust dimensions to be safe for most screen resolutions
        self.app_width = min(1100, int(screen_width * 0.9))
        self.app_height = min(700, int(screen_height * 0.8)) 
        
        # Center and set geometry
        self.center_window()
        
        # Set a lower minimum size to ensure it fits on smaller laptops
        self.minsize(850, 550)

        # Color variables that change with theme
        self.text_color = "black"
        self.bg_color = "white"
        self.frame_bg = "#F0F0F0"
        self.border_color = "#4ECDC4"
        
        # Create a 2x3 grid layout
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.grid_rowconfigure(2, weight=1)

        # Title Label - Row 0
        self.title_label = ctk.CTkLabel(self, text="✨ AI-Powered Spell Checker",
                                        font=ctk.CTkFont(size=22, weight="bold"),
                                        text_color="#4ECDC4")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(15, 5))

        # Subtitle Label - Row 1
        self.subtitle_label = ctk.CTkLabel(self, text="Type your text and get instant spelling corrections",
                                        font=ctk.CTkFont(size=13), text_color="#FF6B6B")
        self.subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 15))

        # --- Input Text Area ---
        self.input_frame = ctk.CTkFrame(self, fg_color=self.frame_bg, border_color=self.border_color, border_width=2)
        self.input_frame.grid(row=2, column=0, padx=(15, 5), pady=10, sticky="nsew")
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_label = ctk.CTkLabel(self.input_frame, text="📝 Input Text:", 
                                      font=ctk.CTkFont(weight="bold", size=15),
                                      text_color="#4ECDC4")
        self.input_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.input_text = ctk.CTkTextbox(self.input_frame, font=("Arial", 13), wrap="word", 
                                       border_width=1, border_color=self.border_color, 
                                       fg_color="white", text_color="black")
        self.input_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        self.placeholder_text = "Enter your text here...\n\nYour text will be magically corrected!"
        self.input_text.insert("1.0", self.placeholder_text)
        self.input_text.configure(text_color="gray60")
        
        self.input_text.bind("<FocusIn>", self.on_input_focus_in)
        self.input_text.bind("<FocusOut>", self.on_input_focus_out)
        self.input_text.bind("<KeyPress>", self.on_input_key_press)
        self.placeholder_active = True

        # --- Output Text Area ---
        self.output_frame = ctk.CTkFrame(self, fg_color=self.frame_bg, border_color="#45B7D1", border_width=2)
        self.output_frame.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")
        self.output_frame.grid_rowconfigure(1, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        self.output_label = ctk.CTkLabel(self.output_frame, text="✅ Corrected Text:", 
                                       font=ctk.CTkFont(weight="bold", size=15),
                                       text_color="#45B7D1")
        self.output_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.output_text = ctk.CTkTextbox(self.output_frame, font=("Arial", 13), wrap="word", 
                                        border_width=1, border_color="#45B7D1", 
                                        fg_color="white", text_color="black",
                                        state="disabled")
        self.output_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Copy to Clipboard Button inside Output Frame
        self.copy_button = ctk.CTkButton(self.output_frame, text="📋 Copy Text", command=self.copy_to_clipboard,
                                        height=28, width=100, font=ctk.CTkFont(size=12),
                                        fg_color="#45B7D1", hover_color="#3da1ba")
        self.copy_button.grid(row=2, column=0, pady=(0, 10))

        # --- Summary Panel ---
        self.summary_frame = ctk.CTkFrame(self, fg_color=self.frame_bg, border_color="#FF6B6B", border_width=2)
        self.summary_frame.grid(row=2, column=2, padx=(5, 15), pady=10, sticky="nsew")
        self.summary_frame.grid_rowconfigure(1, weight=1)
        self.summary_frame.grid_columnconfigure(0, weight=1)

        self.summary_label = ctk.CTkLabel(self.summary_frame, text="📊 Summary", 
                                        font=ctk.CTkFont(weight="bold", size=15),
                                        text_color="#FF6B6B")
        self.summary_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.summary_text = ctk.CTkTextbox(self.summary_frame, font=("Arial", 12), wrap="word", 
                                         border_width=1, border_color="#FF6B6B", 
                                         fg_color="white", text_color="black",
                                         state="disabled")
        self.summary_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # --- Bottom Button Frame ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, columnspan=3, pady=15, sticky="")
        
        self.clear_button = ctk.CTkButton(self.button_frame, text="🗑️ Clear All", command=self.clear_text,
                                        height=40, fg_color="#FF6B6B", hover_color="#FF4757")
        self.clear_button.grid(row=0, column=0, padx=10)

        self.correct_button = ctk.CTkButton(self.button_frame, text="✨ Correct Spelling", command=self.correct_spelling,
                                            height=40, width=200, font=ctk.CTkFont(weight="bold"),
                                            fg_color="#4ECDC4", hover_color="#45B7D1")
        self.correct_button.grid(row=0, column=1, padx=10)

        self.theme_switch = ctk.CTkSwitch(self.button_frame, text="🌙 Dark Mode", command=self.switch_theme)
        self.theme_switch.grid(row=0, column=2, padx=10)
        self.theme_switch.select()

        # Status Bar
        self.status_bar = ctk.CTkLabel(self, text="✅ Ready!", text_color="#45B7D1", font=ctk.CTkFont(size=11))
        self.status_bar.grid(row=4, column=0, columnspan=3, pady=(0, 5), sticky="ew")
        
        self.update_theme_colors()

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.app_width // 2)
        y = (self.winfo_screenheight() // 2) - (self.app_height // 2)
        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")

    def copy_to_clipboard(self):
        corrected_text = self.output_text.get("1.0", "end-1c")
        if corrected_text and corrected_text != "Your corrected text will appear here...":
            pyperclip.copy(corrected_text)
            self.status_bar.configure(text="📋 Text copied to clipboard!")
        else:
            self.status_bar.configure(text="❌ Nothing to copy.")

    def update_theme_colors(self):
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            self.frame_bg = "#F0F0F0"
            self.input_text.configure(fg_color="white", text_color="black")
            self.output_text.configure(fg_color="white", text_color="black")
            self.summary_text.configure(fg_color="white", text_color="black")
        else:
            self.frame_bg = "#2B2D42"
            self.input_text.configure(fg_color="#1E1E2E", text_color="white")
            self.output_text.configure(fg_color="#1E1E2E", text_color="white")
            self.summary_text.configure(fg_color="#1E1E2E", text_color="white")
        
        self.input_frame.configure(fg_color=self.frame_bg)
        self.output_frame.configure(fg_color=self.frame_bg)
        self.summary_frame.configure(fg_color=self.frame_bg)

    def on_input_focus_in(self, event):
        if self.placeholder_active:
            self.input_text.delete("1.0", "end")
            self.input_text.configure(text_color="black" if ctk.get_appearance_mode() == "Light" else "white")
            self.placeholder_active = False

    def on_input_focus_out(self, event):
        if not self.input_text.get("1.0", "end-1c").strip():
            self.input_text.insert("1.0", self.placeholder_text)
            self.input_text.configure(text_color="gray60")
            self.placeholder_active = True

    def on_input_key_press(self, event):
        if self.placeholder_active:
            self.on_input_focus_in(None)

    def correct_spelling(self):
        try:
            self.status_bar.configure(text="⏳ Analyzing...")
            self.update_idletasks()
            original_text = "" if self.placeholder_active else self.input_text.get("1.0", "end-1c")

            if not original_text.strip():
                self.status_bar.configure(text="❌ No text found.")
                return

            blob = TextBlob(original_text)
            corrected_text = str(blob.correct())
            
            orig_words = re.findall(r'\b\w+\b', original_text.lower())
            corr_words = re.findall(r'\b\w+\b', corrected_text.lower())
            errors = sum(1 for o, c in zip(orig_words, corr_words) if o != c)

            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", corrected_text)
            self.output_text.configure(state="disabled")

            self.summary_text.configure(state="normal")
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("1.0", f"Total Words: {len(orig_words)}\nErrors Corrected: {errors}")
            self.summary_text.configure(state="disabled")

            self.status_bar.configure(text=f"✅ Done! Corrected {errors} words.")
        except Exception as e:
            self.status_bar.configure(text=f"❌ Error: {str(e)}")

    def clear_text(self):
        self.input_text.delete("1.0", "end")
        self.on_input_focus_out(None)
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", "end")
        self.summary_text.configure(state="disabled")
        self.status_bar.configure(text="✅ Ready!")

    def switch_theme(self):
        new_mode = "Light" if ctk.get_appearance_mode() == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.theme_switch.configure(text="☀️ Light Mode" if new_mode == "Light" else "🌙 Dark Mode")
        self.update_theme_colors()

if __name__ == "__main__":
    app = SpellCorrectorApp()
    app.mainloop()