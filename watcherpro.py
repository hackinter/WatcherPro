import tkinter as tk
from tkinter import messagebox
import dns.resolver
from concurrent.futures import ThreadPoolExecutor

def get_subdomains(domain, wordlist):
    messagebox.showinfo("Loading", "🔍 Searching for subdomains, please wait...")
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
    except Exception as e:
        print(f"Error resolving {subdomain}: {e}")  # Debugging line
        return subdomain, None

def save_results(domain, subdomains, file_type):
    file_name = f"{domain}.{file_type}"
    if file_type == 'pdf':
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for sub in subdomains:
            pdf.cell(200, 10, sub, ln=True)
        pdf.output(file_name)
    else:
        with open(file_name, "w") as file:
            for sub in subdomains:
                file.write(sub + "\n")
    messagebox.showinfo("Success", f"🎉 Results saved: {file_name}!")

def on_submit():
    domain = domain_entry.get()
    file_type = file_type_var.get()
    
    if file_type not in ['txt', 'pdf']:
        messagebox.showerror("Error", "❌ Please select a valid file type (txt or pdf).")
        return

    # Custom wordlist path
    wordlist = 'wordlist.txt'  # Specify your wordlist file name here

    subdomains = get_subdomains(domain, wordlist)
    if not subdomains:
        messagebox.showwarning("No Results", "🚫 No subdomains found.")
        return

    save_results(domain, subdomains, file_type)

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
