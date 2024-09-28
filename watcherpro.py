import tkinter as tk
from tkinter import messagebox, scrolledtext
import dns.resolver
from concurrent.futures import ThreadPoolExecutor
import requests

def get_subdomains(domain, wordlist):
    loading_window = create_loading_window()
    subdomains = brute_force_subdomains(domain, wordlist)
    resolved_subdomains = resolve_subdomains(subdomains)
    loading_window.destroy()
    return resolved_subdomains

def brute_force_subdomains(domain, wordlist):
    subdomains = []
    try:
        with open(wordlist, 'r') as file:
            for line in file:
                subdomain = f"{line.strip()}.{domain}"
                subdomains.append(subdomain)
    except FileNotFoundError:
        messagebox.showerror("Error", "❌ Wordlist file not found. Please check the file path.")
    return subdomains

def resolve_subdomains(subdomains):
    results = []
    with ThreadPoolExecutor() as executor:
        resolved = executor.map(resolve_subdomain, subdomains)
        for subdomain, ip in resolved:
            if ip:
                results.append(subdomain)
    return results

def resolve_subdomain(subdomain):
    try:
        result = dns.resolver.resolve(subdomain, 'A')
        return subdomain, [str(ip) for ip in result]
    except Exception:
        return subdomain, None

def save_results(domain, subdomains, file_type):
    if not subdomains:
        messagebox.showwarning("No Results", "🚫 No subdomains found.")
        return

    file_name = f"{domain}.{file_type}"
    with open(file_name, "w") as file:
        for sub in subdomains:
            file.write(sub + "\n")
    messagebox.showinfo("Success", f"🎉 Results saved: {file_name}!")

def display_results(subdomains):
    result_window = tk.Toplevel(root)
    result_window.title("Results")
    result_window.geometry("400x300")
    
    text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD)
    text_area.pack(expand=True, fill='both')
    
    for sub in subdomains:
        text_area.insert(tk.END, sub + "\n")
    text_area.configure(state='disabled')  # Make the text area read-only

def on_submit():
    domain = domain_entry.get()
    file_type = file_type_var.get()

    # Custom wordlist path
    wordlist = 'wordlist.txt'  # Specify your wordlist file name here

    subdomains = get_subdomains(domain, wordlist)
    if subdomains:
        display_results(subdomains)  # Show results in a new window
        save_results(domain, subdomains, file_type)

def create_loading_window():
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading")
    loading_window.geometry("300x100")
    tk.Label(loading_window, text="🔍 Searching for subdomains, please wait...", font=("Arial", 12)).pack(pady=20)
    return loading_window

# ASCII Art Header
ascii_art = r"""
 __    __      _       _                ___           
/ / /\ \ \__ _| |_ ___| |__   ___ _ __ / _ \_ __ ___  
\ \/  \/ / _` | __/ __| '_ \ / _ \ '__/ /_)/ '__/ _ \ 
 \  /\  / (_| | || (__| | | |  __/ | / ___/| | | (_) |
  \/  \/ \__,_|\__\___|_| |_|\___|_| \/    |_|  \___/ 
                                                      
"""

# Tkinter GUI
root = tk.Tk()
root.title("WatcherPro - Version 3.2.1")  # Updated version
root.geometry("400x400")

tk.Label(root, text=ascii_art, font=("Courier", 10), justify=tk.LEFT).pack(pady=10)
tk.Label(root, text="👋 Welcome to WatcherPro!", font=("Arial", 16)).pack(pady=10)
tk.Label(root, text="Enter domain name (e.g., example.com):").pack(pady=5)

domain_entry = tk.Entry(root, width=30)
domain_entry.pack(pady=5)

file_type_var = tk.StringVar(value='txt')
tk.Radiobutton(root, text='TXT', variable=file_type_var, value='txt').pack(anchor=tk.W)
tk.Radiobutton(root, text='PDF', variable=file_type_var, value='pdf').pack(anchor=tk.W)

submit_btn = tk.Button(root, text="Search", command=on_submit)
submit_btn.pack(pady=20)

root.mainloop()
