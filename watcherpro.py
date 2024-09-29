import requests
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import socket
import threading

class WatcherPro:
    def __init__(self, master):
        self.master = master
        self.master.title("WatcherPro - Version 1.0.1")
        self.subdomains = set()
        self.valid_subdomains = set()
        self.loading_label = None
        self.is_running = False

        # Create GUI components
        self.label = tk.Label(master, text="🔗 Enter your domain (e.g., example.com):", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.domain_entry = tk.Entry(master, width=30, font=("Helvetica", 14), bd=2, relief="solid")
        self.domain_entry.pack(pady=10)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=5)

        self.search_button = tk.Button(button_frame, text="🔍 Search Now", command=self.start_search, bg="white", fg="black", borderwidth=0, relief="flat")
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_frame, text="⏹ Stop", command=self.stop_search, bg="white", fg="black", borderwidth=0, relief="flat")
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame, text="🧹 Clear", command=self.clear_results, bg="white", fg="black", borderwidth=0, relief="flat")
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(button_frame, text="❌ Exit", command=self.master.quit, bg="white", fg="black", borderwidth=0, relief="flat")
        self.exit_button.pack(side=tk.LEFT, padx=5)

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=15, font=("Helvetica", 12), bd=2, relief="solid")
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(master, text="💾 Save Now", command=self.save_results, bg="white", fg="black", borderwidth=0, relief="flat")
        self.save_button.pack(pady=10)

    def start_search(self):
        if self.is_running:
            messagebox.showwarning("Warning", "🔄 A search is already in progress!")
            return

        self.loading_label = tk.Label(self.master, text="🔄 Loading...", font=("Helvetica", 14))
        self.loading_label.pack(pady=5)

        self.is_running = True
        search_thread = threading.Thread(target=self.find_subdomains)
        search_thread.start()

    def stop_search(self):
        if self.is_running:
            self.is_running = False
            messagebox.showinfo("Stopped", "⏹ The search has been stopped.")
            if self.loading_label:
                self.loading_label.destroy()

    def clear_results(self):
        self.subdomains.clear()
        self.valid_subdomains.clear()
        self.domain_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        if self.loading_label:
            self.loading_label.destroy()
        self.is_running = False

    def find_subdomains(self):
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Error", "🚨 Please enter a valid domain!")
            if self.loading_label:
                self.loading_label.destroy()
            self.is_running = False
            return

        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.text.splitlines()
                for line in data:
                    if not self.is_running:
                        break
                    parts = line.split(',')
                    subdomain = parts[0].strip()
                    if subdomain.endswith(domain):
                        self.subdomains.add(subdomain)

                self.resolve_subdomains()
                self.display_results()
            else:
                messagebox.showerror("Error", f"😱 Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"🚨 Network error: {e}")
        finally:
            if self.loading_label:
                self.loading_label.destroy()
            self.is_running = False

    def resolve_subdomains(self):
        for subdomain in self.subdomains:
            if not self.is_running:
                break
            try:
                ip = socket.gethostbyname(subdomain)
                self.valid_subdomains.add(subdomain)
            except socket.gaierror:
                continue

    def display_results(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "WatcherPro Results:\n\n")  # Added title here
        if self.valid_subdomains:
            self.result_text.insert(tk.END, f"🔍 Found {len(self.valid_subdomains)} valid subdomains:\n\n")
            for sub in self.valid_subdomains:
                self.result_text.insert(tk.END, f"🌐 {sub}\n")
        else:
            self.result_text.insert(tk.END, "🙅‍♂️ No valid subdomains found.")

    def save_results(self):
        if not self.valid_subdomains:
            messagebox.showwarning("No Results", "🙅‍♂️ No subdomains to save!")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                  filetypes=[("Text Files", "*.txt")])
        if filename:
            try:
                with open(filename, 'w') as file:
                    for sub in self.valid_subdomains:
                        file.write(f"{sub}\n")
                
                messagebox.showinfo("Success", f"✅ Results saved as: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"🚨 Error while saving file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatcherPro(root)
    root.mainloop()
