import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import threading
import subprocess
import requests
import json
from tkinter import ttk
import openai

# Set up OpenAI GPT API credentials
openai.api_key = 'YOUR_API_KEY_HERE'

class LinuxSoftwareScanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Linux Software Scan GPT GUI")
        self.root.configure(bg="#333333")  # Set background color of the root window

        # Set the title color to green
        self.root.option_add('*Dialog.msg.font', 'Helvetica 12 bold')
        self.root.option_add('*Dialog.msg.foreground', 'green')

        # Set font size
        font_size = ("Helvetica", 14)
        
        # Top Widget
        self.top_frame = tk.Frame(self.root, bg='black')
        self.top_frame.grid(row=0, column=0, sticky="ew")

        self.user_label_gpt = tk.Label(self.top_frame, text="You: ", bg='black', fg='green', font=font_size)
        self.user_label_gpt.pack(side=tk.LEFT)

        self.entry_field_gpt = tk.Entry(self.top_frame, bg='black', fg='green', insertbackground='green', font=font_size)
        self.entry_field_gpt.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.entry_field_gpt.bind("<Return>", self.generate_instructions)
        self.entry_field_gpt.bind("<KP_Enter>", self.generate_instructions)

        self.text_area_gpt = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg='black', fg='green', insertbackground='green', font=font_size)
        self.text_area_gpt.grid(row=1, column=0, sticky="nsew")

        self.reply_button_gpt = tk.Button(self.root, text="Reply to Morpheus", command=self.generate_instructions, bg='black', fg='green', font=font_size)
        self.reply_button_gpt.grid(row=2, column=0, pady=10)

        self.clear_button_gpt = tk.Button(self.root, text="Clear GPT Text", command=self.clear_text_gpt, bg='black', fg='green', font=font_size)
        self.clear_button_gpt.grid(row=3, column=0, pady=10)

        # Separator
        self.separator = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.separator.grid(row=6, column=0, sticky="ew", pady=10)

        # Bottom Widget
        self.bottom_frame = tk.Frame(self.root, bg='black')
        self.bottom_frame.grid(row=5, column=0, sticky="ew")

        self.text_area_Scan = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg='black', fg='green', insertbackground='green', font=font_size)
        self.text_area_Scan.grid(row=6, column=0, sticky="nsew")

        # Create a frame for scan controls
        self.scan_controls_frame = tk.Frame(self.root, bg='black')
        self.scan_controls_frame.grid(row=7, column=0, pady=10, sticky="ew")

        # Create the 'Scan for Software' button
        self.run_button_Scan = tk.Button(self.scan_controls_frame, text="Scan for Software", command=self.run_Scan, bg='black', fg='green', font=font_size)
        self.run_button_Scan.grid(row=0, column=0, padx=10)

        # Create the 'Stop Scan' button and initially disable it
        self.stop_button_Scan = tk.Button(self.scan_controls_frame, text="Stop Scan", command=self.stop_scan, bg='black', fg='green', font=font_size, state=tk.DISABLED)
        self.stop_button_Scan.grid(row=0, column=1, padx=10)

        # Create the 'Pause/Resume Scan' button and initially disable it
        self.pause_button_Scan = tk.Button(self.scan_controls_frame, text="Pause/Resume Scan", command=self.pause_resume_scan, bg='black', fg='green', font=font_size, state=tk.DISABLED)
        self.pause_button_Scan.grid(row=0, column=2, padx=10)

        # Create a frame for Clear Scan Text button
        self.clear_button_frame = tk.Frame(self.root, bg='black')
        self.clear_button_frame.grid(row=8, column=0, pady=10, sticky="ew")

        # Create the 'Clear Scan Text' button
        self.clear_button_Scan = tk.Button(self.clear_button_frame, text="Clear Scan Text", command=self.clear_text_scan, bg='black', fg='green', font=font_size)
        self.clear_button_Scan.grid(sticky="ew")

        # Start the instruction process
        self.text_area_gpt.insert(tk.END, 'Morpheus: Hello Neo. How can I help you with Scanning for Software on your Machine?')

        # Center the buttons in the first row
        self.scan_controls_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Center the 'Clear Scan Text' button
        self.clear_button_frame.grid_columnconfigure(0, weight=1)

        # Initialize threading condition
        self.scan_condition = threading.Condition()

        # Initialize control flags
        self.scan_stop = False
        self.scan_pause = False
    
    def stop_scan(self):
        with self.scan_condition:
            self.scan_stop = True
            self.scan_condition.notify_all()  # Resume the thread if it's paused

    def pause_resume_scan(self):
        with self.scan_condition:
            self.scan_pause = not self.scan_pause  # Toggle pause/resume
            self.scan_condition.notify_all()  # Resume the thread if it's paused


        # Configure resizing behavior
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def generate_instructions(self, event=None):
        input_text = self.entry_field_gpt.get()
        self.text_area_gpt.insert(tk.END, f"\nYou: {input_text}\n")
        
        # Start a new thread to generate the instructions.
        threading.Thread(target=self.generate_instructions_thread, args=(input_text,)).start()

    def generate_instructions_thread(self, input_text):
        try:
            messages = [
                {"role": "system", "content": "You are Morpheus, a helpful assistant."},
                {"role": "user", "content": input_text}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=200
            )

            generated_text = response['choices'][0]['message']['content']
            self.text_area_gpt.insert(tk.END, f"Morpheus: {generated_text}\n")
        except Exception as e:
            self.text_area_gpt.insert(tk.END, f"\nMorpheus: Error: {str(e)}\n")

        self.entry_field_gpt.delete(0, tk.END)

    def clear_text_gpt(self):
        self.text_area_gpt.delete(1.0, tk.END)

    def get_installed_packages(self):
        try:
            result = subprocess.run(['dpkg', '--get-selections'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            packages = result.stdout.decode('utf-8').split('\n')
            print(f'Found {len(packages)} packages.')
            return packages
        except Exception as e:
            print(f'Error getting packages: {str(e)}')
            return []
        
        # Add Stop and Pause/Resume buttons
        self.stop_button_Scan = tk.Button(self.root, text="Stop Scan", command=self.stop_scan, bg='black', fg='green', font=font_size, state=tk.DISABLED)
        self.stop_button_Scan.grid(row=8, column=0, pady=10)

        self.pause_button_Scan = tk.Button(self.root, text="Pause/Resume Scan", command=self.pause_resume_scan, bg='black', fg='green', font=font_size, state=tk.DISABLED)
        self.pause_button_Scan.grid(row=9, column=0, pady=10)

        # Initialize control flags and condition object
        self.scan_stop = False
        self.scan_pause = False
        self.scan_condition = threading.Condition()

    def run_Scan(self):
        self.run_button_Scan.config(state=tk.DISABLED)
        self.stop_button_Scan.config(state=tk.NORMAL)
        self.pause_button_Scan.config(state=tk.NORMAL)
        self.clear_text_scan()
        self.text_area_Scan.insert(tk.END, "Scanning in progress...\n")

        threading.Thread(target=self.thread_func).start()

    def thread_func(self):
        packages = self.get_installed_packages()

        for package in packages:
            with self.scan_condition:
                while self.scan_pause:
                    self.scan_condition.wait()  # Pause the thread if paused

            if self.scan_stop:
                break  # Stop the thread

            package = package.split('\t')[0]  # Package name is before the tab character

        # Insert package name into the text area
            self.text_area_Scan.insert(tk.END, f"Scanning package: {package}\n")
            self.text_area_Scan.update_idletasks()

            response = requests.get(f"https://cve.circl.lu/api/search/{package}")
            if response.status_code == 200:
                vulnerabilities = response.json()
                if vulnerabilities:
                    for vulnerability in vulnerabilities['data']:
                        self.text_area_Scan.insert(tk.END, json.dumps(vulnerability) + "\n")
                        self.text_area_Scan.update_idletasks()
                else:
                    self.text_area_Scan.insert(tk.END, f"No vulnerabilities found for package: {package}\n")
                    self.text_area_Scan.update_idletasks()

        self.scan_complete()

    def stop_scan(self):
        with self.scan_condition:
            self.scan_stop = True
            self.scan_pause = False
            self.scan_condition.notify_all()  # Resume the thread if it's paused

    def pause_resume_scan(self):
        with self.scan_condition:
            self.scan_pause = not self.scan_pause  # Toggle pause/resume
            if not self.scan_pause:
                self.scan_condition.notify_all()  # Resume the thread if it's paused

    def scan_complete(self):
        if self.scan_stop:
            self.text_area_Scan.insert(tk.END, "Scan stopped.\n")
        else:
            self.text_area_Scan.insert(tk.END, "Scan complete.\n")

    # Reset control flags and button states
        self.scan_stop = False
        self.scan_pause = False
        self.run_button_Scan.config(state=tk.NORMAL)
        self.stop_button_Scan.config(state=tk.DISABLED)
        self.pause_button_Scan.config(state=tk.DISABLED)

    def clear_text_scan(self):
        self.text_area_Scan.delete(1.0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='black')  # set background color of the root window
    Linux_Software_Scan_GPT_gui = LinuxSoftwareScanGUI(root)
    root.mainloop()