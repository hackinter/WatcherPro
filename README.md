```markdown
# WatcherPro - Subdomain Finder

![version](https://img.shields.io/badge/version-3.0.0-brightgreen.svg)
![status](https://img.shields.io/badge/status-active-success.svg)
![license](https://img.shields.io/badge/license-MIT-blue.svg)

WatcherPro is a powerful and user-friendly subdomain finder tool designed to help users discover and enumerate subdomains for any domain. It supports multiple features like brute-forcing, DNS resolution, and saving results in TXT or PDF formats. Built with simplicity in mind, the tool comes with a sleek GUI and is optimized for Gen-Z users.

## Features

- **Domain Input Option**: Easy-to-use domain entry interface.
- **Brute Forcing**: Search for subdomains using custom wordlists.
- **DNS Resolution**: Verify DNS records for the found subdomains.
- **API Integration**: Collect subdomains using popular APIs like VirusTotal, Shodan, etc.
- **Wordlist Support**: Load custom wordlists to expand subdomain search.
- **Passive Scanning**: Discover subdomains from online databases without brute-forcing.
- **Output Formatting**: Save results in TXT, PDF, CSV, or JSON formats.
- **Multithreading Support**: Fast subdomain scanning using multi-threading.
- **HTTPS Support**: Works with both HTTP and HTTPS protocols.
- **Unresolved Subdomain Filtering**: Filter out subdomains that don’t resolve.

## Getting Started

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/hackinter/WatcherPro.git
    cd WatcherPro
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. Run the tool:
    ```bash
    python watcherpro.py
    ```

2. Enter the domain name (e.g., `example.com`).
3. Select the output format (`TXT` or `PDF`).
4. Wait for the subdomains to be discovered and saved.

### Screenshots

#### GUI Interface:
![GUI](https://example.com/screenshot.png)

### Version History

| Version | Description                                            | Release Date |
|---------|--------------------------------------------------------|--------------|
| ![v3.0.0](https://img.shields.io/badge/version-3.0.0-brightgreen.svg) | Added multithreading and passive scanning features  | September 2024 |
| ![v2.5.0](https://img.shields.io/badge/version-2.5.0-yellow.svg) | Improved DNS resolution and output formatting       | August 2024    |
| ![v2.0.0](https://img.shields.io/badge/version-2.0.0-orange.svg) | Added API integration for subdomain enumeration     | July 2024      |
| ![v1.0.0](https://img.shields.io/badge/version-1.0.0-red.svg)    | Initial release with brute forcing and GUI interface| June 2024      |

### License

![license](https://img.shields.io/badge/license-MIT-blue.svg)  
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contributions

Feel free to open an issue or submit a pull request if you have any suggestions for improvements or features!

---

Happy hacking! 😊
```
