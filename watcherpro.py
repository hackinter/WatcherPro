import requests
import os
from tkinter import *
from tkinter import filedialog, messagebox
import threading
import time

class WatcherPro:
    def __init__(self, master):
        self.master = master
        self.master.title("WatcherPro")
        self.master.geometry("600x500")
        self.master.configure(bg="#f0f0f0")  # Light gray background
        self.subdomains = set()
        self.version = "1.1.0"

        # Powered by HACKINTER credit label (top-right corner)
        self.credit_label = Label(master, text="Powered by HACKINTER", font=("Helvetica", 10, "italic"), 
                                  fg="gray", bg="#f0f0f0", anchor="e")
        self.credit_label.pack(side=TOP, anchor=NE, padx=10, pady=5)  # Positioned at the top-right corner

        # Label for domain input
        self.label = Label(master, text="🔗 Enter target domain (e.g., example.com)", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
        self.label.pack(pady=10)

        # Entry for domain input with rounded corners
        self.domain_entry = Entry(master, width=40, font=("Helvetica", 12), bd=2, relief="groove")
        self.domain_entry.pack(pady=10)

        # Button frame for top and bottom rows
        self.button_frame_top = Frame(master, bg="#f0f0f0")
        self.button_frame_top.pack(pady=10)
        
        self.button_frame_bottom = Frame(master, bg="#f0f0f0")
        self.button_frame_bottom.pack(pady=10)

        # Style for buttons
        button_style = {
            "bg": "#007BFF",  # Blue background
            "fg": "white",    # White text
            "font": ("Helvetica", 10, "bold"),
            "activebackground": "#0056b3",  # Darker blue on hover
            "relief": "raised",
            "borderwidth": 2,
            "width": 12
        }

        # Top row buttons: Search, Copy, Save
        self.search_button = Button(self.button_frame_top, text="🔍 Search", command=self.start_search, **button_style)
        self.search_button.grid(row=0, column=0, padx=20)

        self.copy_button = Button(self.button_frame_top, text="📋 Copy", command=self.copy_results, **button_style)
        self.copy_button.grid(row=0, column=1, padx=20)

        self.save_button = Button(self.button_frame_top, text="💾 Save", command=self.save_results, **button_style)
        self.save_button.grid(row=0, column=2, padx=20)

        # Spacer row to create a gap between the two rows
        self.button_frame_top.grid_rowconfigure(1, minsize=20)

        # Bottom row buttons: Clear, Exit (Centered under top row)
        self.clear_button = Button(self.button_frame_bottom, text="🧹 Clear", command=self.clear_input, **button_style)
        self.clear_button.grid(row=2, column=0, padx=20, pady=5)

        self.exit_button = Button(self.button_frame_bottom, text="❌ Exit", command=self.master.quit, **button_style)
        self.exit_button.grid(row=2, column=1, padx=20, pady=5)

        # Loading animation label with new color
        self.loading_label = Label(master, text="", font=("Helvetica", 14, "bold"), fg="black", bg="#f0f0f0")  # Black color
        self.loading_label.pack(pady=5)

        # Results count label with a new color and style
        self.results_label = Label(master, text="", font=("Helvetica", 12, "bold"), fg="black", bg="#f0f0f0")  # Black color
        self.results_label.pack(pady=5)

        # Text box to display results
        self.result_box = Text(master, height=15, width=70, font=("Helvetica", 12), bd=2, relief="groove", bg="#ffffff")
        self.result_box.pack(pady=10)

    def start_search(self):
        self.result_box.delete(1.0, END)  # Clear text box
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showwarning("Input Error", "Please enter a valid domain!")
            return

        self.loading_label.config(text="Loading...")  # Show loading text
        self.results_label.config(text="")  # Clear result count
        self.subdomains.clear()  # Clear previous results
        threading.Thread(target=self.find_subdomains, args=(domain,)).start()  # Start search in a new thread

    def find_subdomains(self, domain):
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        loading_steps = 100  # Total loading steps
        for i in range(loading_steps):
            time.sleep(0.05)  # Simulate loading time
            self.loading_label.config(text=f"Loading... {i + 1}/{loading_steps}")  # Update loading text

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.text.splitlines()
                for line in data:
                    parts = line.split(',')
                    subdomain = parts[0].strip()
                    if subdomain.endswith(domain):
                        self.subdomains.add(subdomain)

                self.display_results()
            else:
                messagebox.showerror("Error", f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unknown error: {e}")

    def display_results(self):
        self.loading_label.config(text="")  # Clear loading label
        self.results_label.config(text=f"Results found: {len(self.subdomains)}")  # Show result count
        self.result_box.delete(1.0, END)  # Clear text box
        if self.subdomains:
            for sub in self.subdomains:
                # Making results bold and larger
                self.result_box.insert(END, f"🌐 {sub}\n", "bold")  # Insert subdomain with tag
        else:
            self.result_box.insert(END, "🙅‍♂️ No subdomains found.\n")

        # Configure tag for bold text
        self.result_box.tag_configure("bold", font=("Helvetica", 12, "bold"))  # Increased font size for bold

    def copy_results(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.result_box.get(1.0, END))
        messagebox.showinfo("Copy Successful", "Results copied to clipboard!")

    def save_results(self):
        if not self.subdomains:
            messagebox.showwarning("Save Error", "No subdomains to save!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                         filetypes=[("Text files", "*.txt"), 
                                                    ("Config files", "*.conf")]))
        if not file_path:
            return  # User cancelled the save dialog

        try:
            with open(file_path, 'w') as file:
                for sub in self.subdomains:
                    file.write(sub + '\n')

            messagebox.showinfo("Save Successful", f"Results saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error while saving file: {e}")

    def clear_input(self):
        self.domain_entry.delete(0, END)
        self.result_box.delete(1.0, END)
        self.results_label.config(text="")
        self.loading_label.config(text="")

# Usage example
if __name__ == "__main__":
    root = Tk()
    app = SubChecker(root)
    root.mainloop()
