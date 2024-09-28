import requests
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import socket

class WatcherPro:
    def __init__(self, master):
        self.master = master
        self.master.title("WatcherPro - Version 3.2.1")
        self.subdomains = set()
        self.valid_subdomains = set()  # To store valid subdomains after DNS resolution

        # Create GUI components
        self.label = tk.Label(master, text="🔗 Enter your domain (e.g., example.com):")
        self.label.pack(pady=5)

        self.domain_entry = tk.Entry(master, width=30)
        self.domain_entry.pack(pady=5)

        self.search_button = tk.Button(master, text="Search Now", command=self.find_subdomains)
        self.search_button.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=15)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(master, text="Save Now", command=self.save_results)
        self.save_button.pack(pady=10)

    def find_subdomains(self):
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Error", "🚨 Please enter a valid domain!")
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
        if self.valid_subdomains:
            for sub in self.valid_subdomains:
                self.result_text.insert(tk.END, f"🌐 {sub}\n")
        else:
            self.result_text.insert(tk.END, "🙅‍♂️ No valid subdomains found.")

    def save_results(self):
        if not self.valid_subdomains:
            messagebox.showwarning("No Results", "🙅‍♂️ No subdomains to save!")
            return

        file_format = simpledialog.askstring("File Format", "Choose file format (txt/pdf):").strip().lower()
        if file_format not in ['txt', 'pdf']:
            messagebox.showerror("Error", "🚨 Invalid file format selected!")
            return

        filename = simpledialog.askstring("Save File", "Enter filename:")
        if not filename:
            messagebox.showerror("Error", "🚨 Please enter a filename!")
            return

        if file_format == 'txt':
            filename += '.txt'
        elif file_format == 'pdf':
            filename += '.pdf'

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

if __name__ == "__main__":
    root = tk.Tk()
    app = WatcherPro(root)
    root.mainloop()
