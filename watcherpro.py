import tkinter as tk
from tkinter import messagebox, scrolledtext
import dns.resolver
from concurrent.futures import ThreadPoolExecutor

def get_subdomains(domain, wordlist):
    subdomains = brute_force_subdomains(domain, wordlist)
    resolved_subdomains = resolve_subdomains(subdomains)
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

def display_results(subdomains):
    result_text.delete(1.0, tk.END)  # Clear previous results
    if not subdomains:
        result_text.insert(tk.END, "🚫 No subdomains found.\n")
        return
    for sub in subdomains:
        result_text.insert(tk.END, sub + "\n")

def on_submit():
    domain = domain_entry.get()
    if not domain:  # Check if domain is empty
        messagebox.showerror("Error", "❌ Please enter a valid domain name.")
        return

    # Custom wordlist path
    wordlist = 'wordlist.txt'  # Specify your wordlist file name here

    subdomains = get_subdomains(domain, wordlist)
    display_results(subdomains)

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
root.geometry("500x500")

tk.Label(root, text=ascii_art, font=("Courier", 10), justify=tk.LEFT).pack(pady=10)
tk.Label(root, text="👋 Welcome to WatcherPro!", font=("Arial", 16)).pack(pady=10)
tk.Label(root, text="Enter domain name (e.g., example.com):").pack(pady=5)

domain_entry = tk.Entry(root, width=30)
domain_entry.pack(pady=5)

submit_btn = tk.Button(root, text="Search", command=on_submit)
submit_btn.pack(pady=20)

# Text area for displaying results
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15)
result_text.pack(pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
