import requests
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, Toplevel, StringVar
import socket
import threading

class WatcherPro:
    def __init__(self, master):
        self.master = master
        self.master.title("WatcherPro - Version 3.2.1")
        self.subdomains = set()
        self.valid_subdomains = set()  # To store valid subdomains after DNS resolution
        self.loading_label = None  # For loading animation

        # Create GUI components
        self.label = tk.Label(master, text="🔗 Enter your domain (e.g., example.com):", font=("Helvetica", 12))
        self.label.pack(pady=5)

        self.domain_entry = tk.Entry(master, width=30, font=("Helvetica", 12))
        self.domain_entry.pack(pady=5)

        self.search_button = tk.Button(master, text="Search Now", command=self.start_search, bg="#4CAF50", fg="white", borderwidth=0, relief="flat")
        self.search_button.pack(pady=10)

        self.exit_button = tk.Button(master, text="Exit", command=self.master.quit, bg="#FF5733", fg="white", borderwidth=0, relief="flat")
        self.exit_button.pack(pady=5)

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=15, font=("Helvetica", 10))
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(master, text="Save Now", command=self.open_save_dialog, bg="#2196F3", fg="white", borderwidth=0, relief="flat")
        self.save_button.pack(pady=10)

    def start_search(self):
        # Start loading animation
        self.loading_label = tk.Label(self.master, text="🔄 Loading...", font=("Helvetica", 12))
        self.loading_label.pack(pady=5)

        # Start the search in a separate thread to prevent freezing
        search_thread = threading.Thread(target=self.find_subdomains)
        search_thread.start()

    def find_subdomains(self):
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Error", "🚨 Please enter a valid domain!")
            self.loading_label.destroy()  # Remove loading label
            return

        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.text.splitlines()
                for line in data:
                    parts = line.split(',')
                    subdomain = parts[0].strip()
                    if subdomain.endswith(domain):
                        self.subdomains.add(subdomain)

                self.resolve_subdomains()  # Call to resolve subdomains
                self.display_results()
            else:
                messagebox.showerror("Error", f"😱 Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"🚨 Network error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"🚨 Unknown error: {e}")
        finally:
            self.loading_label.destroy()  # Remove loading label

    def resolve_subdomains(self):
        for subdomain in self.subdomains:
            try:
                # Get the IP address of the subdomain
                ip = socket.gethostbyname(subdomain)
                self.valid_subdomains.add(subdomain)  # Add valid subdomain to the set
            except socket.gaierror:
                # If the DNS resolution fails, skip the subdomain
                continue

    def display_results(self):
        ascii_art = r"""
 __    __      _       _                ___           
/ / /\ \ \__ _| |_ ___| |__   ___ _ __ / _ \_ __ ___  
\ \/  \/ / _` | __/ __| '_ \ / _ \ '__/ /_)/ '__/ _ \ 
 \  /\  / (_| | || (__| | | |  __/ | / ___/| | | (_) |
  \/  \/ \__,_|\__\___|_| |_|\___|_| \/    |_|  \___/ 
                                                      
        """
        
        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.result_text.insert(tk.END, ascii_art + "\n")  # Display ASCII art
        self.result_text.insert(tk.END, "🌟 Results:\n\n")  # Add results header
        if self.valid_subdomains:
            for sub in self.valid_subdomains:
                self.result_text.insert(tk.END, f"🌐 {sub}\n")
        else:
            self.result_text.insert(tk.END, "🙅‍♂️ No valid subdomains found.")

    def open_save_dialog(self):
        # Create a new window for saving options
        save_window = Toplevel(self.master)
        save_window.title("Save Options")

        tk.Label(save_window, text="Choose file format:", font=("Helvetica", 12)).pack(pady=5)
        
        file_format_var = StringVar(value='txt')
        tk.Radiobutton(save_window, text="Text (.txt)", variable=file_format_var, value='txt', bg="white").pack(anchor='w')
        tk.Radiobutton(save_window, text="PDF (.pdf)", variable=file_format_var, value='pdf', bg="white").pack(anchor='w')

        tk.Label(save_window, text="Enter filename:", font=("Helvetica", 12)).pack(pady=5)
        filename_entry = tk.Entry(save_window, width=30, font=("Helvetica", 12))
        filename_entry.pack(pady=5)

        # Save button to initiate the saving process
        save_button = tk.Button(save_window, text="Save", command=lambda: self.save_results(filename_entry.get().strip(), file_format_var.get()), bg="#FF9800", fg="white", borderwidth=0, relief="flat")
        save_button.pack(pady=10)

    def save_results(self, filename, file_format):
        if not filename:
            messagebox.showerror("Error", "🚨 Please enter a filename!")
            return

        if file_format == 'txt':
            filename += '.txt'
        elif file_format == 'pdf':
            filename += '.pdf'

        # Create a loading label
        loading_label = tk.Label(self.master, text="🔄 Saving...", font=("Helvetica", 12))
        loading_label.pack(pady=5)

        try:
            if file_format == 'txt':
                with open(filename, 'w') as file:
                    for sub in self.valid_subdomains:
                        file.write(sub + '\n')  # Each subdomain on a new line
            elif file_format == 'pdf':
                # PDF saving logic can be implemented using libraries like fpdf or reportlab
                with open(filename, 'w') as file:
                    file.write("This is a PDF file with valid subdomains:\n")
                    for sub in self.valid_subdomains:
                        file.write(sub + '\n')

            messagebox.showinfo("Success", f"✅ Results saved as: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"🚨 Error while saving file: {e}")
        finally:
            loading_label.destroy()  # Remove loading label

if __name__ == "__main__":
    root = tk.Tk()
    app = WatcherPro(root)

    # Set button styles
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(borderwidth=5, relief="flat", highlightbackground="lightgray", highlightcolor="lightblue", bg="lightblue")

    root.mainloop()
