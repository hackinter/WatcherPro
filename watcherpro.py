import requests
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
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
        self.label = tk.Label(master, text="🔗 Enter your domain (e.g., example.com):", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.domain_entry = tk.Entry(master, width=30, font=("Helvetica", 14), bd=2, relief="solid")
        self.domain_entry.pack(pady=10)

        self.search_button = tk.Button(master, text="🔍 Search Now", command=self.start_search, bg="#4CAF50", fg="white", borderwidth=0, relief="flat")
        self.search_button.pack(pady=10, padx=20)

        self.exit_button = tk.Button(master, text="❌ Exit", command=self.master.quit, bg="#F44336", fg="white", borderwidth=0, relief="flat")
        self.exit_button.pack(pady=5, padx=20)

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=15, font=("Helvetica", 12), bd=2, relief="solid")
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(master, text="💾 Save Now", command=self.save_results, bg="#2196F3", fg="white", borderwidth=0, relief="flat")
        self.save_button.pack(pady=10, padx=20)

    def start_search(self):
        # Start loading animation
        self.loading_label = tk.Label(self.master, text="🔄 Loading...", font=("Helvetica", 14))
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
        if self.valid_subdomains:
            for sub in self.valid_subdomains:
                self.result_text.insert(tk.END, f"🌐 {sub}\n")
        else:
            self.result_text.insert(tk.END, "🙅‍♂️ No valid subdomains found.")

    def save_results(self):
        if not self.valid_subdomains:
            messagebox.showwarning("No Results", "🙅‍♂️ No subdomains to save!")
            return

        save_window = tk.Toplevel(self.master)
        save_window.title("Save Results")

        tk.Label(save_window, text="Choose file format (txt/pdf):", font=("Helvetica", 12)).pack(pady=5)
        file_format = tk.StringVar(value='txt')

        tk.Radiobutton(save_window, text="Text File (.txt)", variable=file_format, value='txt').pack(anchor='w')
        tk.Radiobutton(save_window, text="PDF File (.pdf)", variable=file_format, value='pdf').pack(anchor='w')

        tk.Label(save_window, text="Enter filename:", font=("Helvetica", 12)).pack(pady=5)
        filename_entry = tk.Entry(save_window, width=30, font=("Helvetica", 12), bd=2, relief="solid")
        filename_entry.pack(pady=5)

        def save_file():
            filename = filename_entry.get().strip()
            if not filename:
                messagebox.showerror("Error", "🚨 Please enter a filename!")
                return

            if file_format.get() == 'txt':
                filename += '.txt'
            elif file_format.get() == 'pdf':
                filename += '.pdf'

            try:
                if file_format.get() == 'txt':
                    with open(filename, 'w') as file:
                        for sub in self.valid_subdomains:
                            file.write(sub + '\n')  # Each subdomain on a new line
                elif file_format.get() == 'pdf':
                    # PDF saving logic can be implemented using libraries like fpdf or reportlab
                    with open(filename, 'w') as file:
                        file.write("This is a PDF file with valid subdomains:\n")
                        for sub in self.valid_subdomains:
                            file.write(sub + '\n')

                messagebox.showinfo("Success", f"✅ Results saved as: {filename}")
                save_window.destroy()  # Close the save window
            except Exception as e:
                messagebox.showerror("Error", f"🚨 Error while saving file: {e}")

        save_button = tk.Button(save_window, text="Save", command=save_file, bg="#4CAF50", fg="white", borderwidth=0, relief="flat")
        save_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = WatcherPro(root)
    root.mainloop()
