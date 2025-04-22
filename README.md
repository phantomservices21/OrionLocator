# OrionLocator

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)  

OrionLocator is a free and open-source tool which takes an IP address and returns tons of data including the precise location. This tool is very easy to install and use!

## Features

- 👉 **Deep IP insights**: Country, region, city, latitude/longitude, UTC offset, timezone name  
- 👉 **Network info**: ISP, organization, autonomous system (AS)
- 👉 **Reverse lookup**: Resolve hostnames to IP and vice versa  
- 👉 **Lightweight** Very few dependencies 
- 👉 **CLI & Launcher**: Use from command line or run with included launcher

> [!WARNING]  
> This software only runs on Windows 10/11 at the moment.

## Prerequisites

- Python 3.6 or newer  
- pip (for installing dependencies)  

## Installation

```bash
# Clone the repo
git clone https://github.com/phantomservices21/OrionLocator.git
cd OrionLocator

# (Optional) Create and activate virtual environment
python3 -m venv venv
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Usage

### Command‑Line Interface

```bash
python -m src/main.py
```

### Launcher

1. Find `Runner.bat` in the root directory of this repository.
2. Run `Runner.bat` as an Administrator.
3. Done!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Crafted with ❤️*  
