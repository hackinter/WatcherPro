---

# WatcherPro - Subdomain Finder

WatcherPro is a powerful and user-friendly subdomain finder tool, designed to help users discover active subdomains for a given domain using brute forcing, DNS resolution, and API integrations. It supports output formats such as TXT and PDF.

## Features

1. **Domain Input Option**: Simple interface to enter the target domain.
2. **Brute Forcing**: Uses a custom wordlist to find potential subdomains.
3. **DNS Resolution**: Verifies DNS records of found subdomains.
4. **API Integration**: Collect subdomains from popular APIs (e.g., VirusTotal, Shodan).
5. **Wordlist Support**: Ability to use custom wordlists for subdomain discovery.
6. **Passive Scanning**: Finds subdomains from online databases.
7. **Output Formatting**: Export results in CSV, JSON, or TXT format.
8. **Multi-threading**: Fast subdomain scanning with multi-thread support.
9. **HTTPS Support**: Works for both HTTP and HTTPS protocols.
10. **Subdomain Filtering**: Filter out unresolved or invalid subdomains.

---

## Installation

Follow these steps to install WatcherPro on your system:

### Prerequisites

1. **Python 3.x**: Ensure you have Python 3 installed on your machine.
2. **pip**: Ensure `pip` is installed to manage Python packages.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Clone the Repository

```bash
git clone https://github.com/hackinter/WatcherPro.git
cd WatcherPro
```

### Setup Instructions

If you are using a custom wordlist for brute-forcing subdomains, place the wordlist file in the project directory or specify the path in the code.

---

## Usage

To run WatcherPro, follow these instructions:

### GUI Mode (Recommended)

1. Run the Python script:
   ```bash
   python watcherpro_gui.py
   ```

2. A graphical interface will appear. Input the target domain (e.g., `example.com`), choose your output file type (TXT or PDF), and press "Search."

3. Once the subdomains are discovered, results will be saved in the selected file format (e.g., `example.txt` or `example.pdf`).

### Command-Line Mode (Advanced Users)

1. Open the terminal and navigate to the WatcherPro directory.

2. Run the following command with the desired domain and wordlist (if needed):
   ```bash
   python watcherpro.py -d example.com -w wordlist.txt
   ```

3. The output will be displayed on the terminal and saved in the specified format.

---

## Version History

- **v3.0.0**: Initial public release with GUI support and basic subdomain discovery features.
- **v2.0.0**: Added multi-threading, custom wordlist support, and enhanced DNS resolution.
- **v1.0.0**: Basic command-line subdomain finder with TXT output support.

---

## Policies & Warnings

- **Legal Notice**: This tool is intended for educational purposes only. It should only be used to test your own domains or those for which you have explicit permission. Unauthorized use may violate legal and ethical guidelines.
  
- **Usage Policy**: WatcherPro comes with no warranty or liability for misuse. Ensure you comply with local laws when using this tool. The developers are not responsible for any consequences resulting from illegal use.
  
- **API Limitations**: Be aware that API services like VirusTotal and Shodan may have rate limits, and you might need API keys to access their services.
  
- **Ethical Usage**: Please ensure you have permission before scanning any domain. Unauthorized domain scanning may be considered illegal in many jurisdictions.

---

## Contributions

If you would like to contribute to the WatcherPro project, feel free to submit issues or pull requests on our [GitHub repository](https://github.com/hackinter/WatcherPro).

---

## License

This project is licensed under the **HACKINTER License 2024**. For more details, refer to the `LICENSE` file in the repository.

---

