# Magic Notepad

> A minimalist, distraction-free text editor with "Magic Formatting" and secure storage.

**Magic Notepad** is a lightweight desktop application built for security professionals and minimalists. It features a **"destructive formatting" engine**—simply type Markdown-like syntax, and watch it instantly transform into rich text. 

Designed with a dark-mode interface perfect for **Kali Linux** and late-night coding sessions.

```text
┌──────────────────────────────────────────────────────────────┐
│  New   Open   Save                  Tip: **bold** blue::text:: │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  This is a minimalist editor.                                │
│                                                              │
│  It supports **bold text** and even custom colors like       │
│  red::WARNING:: or cyan::NOTE::.                             │
│                                                              │
│  (The syntax disappears instantly as you type!)              │
│                                                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```
## Features

**1. Distraction-Free UI:** No complex toolbars or ribbons. Just you and your text.

**2. Magic Formatting:** 
* Type `**bold**` → Instantly becomes bold.
* Type `//italic//` → Instantly becomes italic.
  
**3. Dynamic Colors:** Type `colorname::text::` (e.g., `red::alert::`) to paint words instantly.
  
**4. Secure Storage:** Saves files in strict **JSON format** (`.ntp`). Unlike other Python editors that use pickle, this application does not execute code when opening files, making it safe for sharing.
  
**5. Dark Mode:** Built with a `#2d2d2d` dark theme to match standard Linux terminals.

## Installation

### Linux (Kali / Ubuntu / Debian)
This tool relies on `tkinter`, which is sometimes missing from minimal Linux installs.

**1. Install Dependencies:**

```Bash

sudo apt update
sudo apt install python3-tk
```

**2. Clone the Repository:**

```Bash

git clone [https://github.com/KNIE-91723/magic-notepad.git](https://github.com/KNIE-91723/magic-notepad.git)
cd magic-notepad
```
**3. Run the App:**

```Bash

python3 magic_notepad.py
```
### Windows
1. Ensure you have [Python 3](https://www.python.org/) installed.
2. Download the repository.
3. Double-click `magic_notepad.py.`
   
## Usage Guide

| Feature | Syntax to Type | Example | Notes |
| :--- | :--- | :--- | :--- |
| **Bold Text** | `**text**` | `**Important**` | Text turns bold instantly. |
| **Italic Text** | `//text//` | `//Notes//` | Text slants to the right. |
| **Color Text** | `color::text::` | `red::Error::` | Supports names (red, blue) or hex codes. |
| **New File** | Click "New" | N/A | **Warning:** This clears your current screen. |
| **Save File** | Click "Save" | N/A | Saves as `.ntp` (JSON format). |
| **Open File** | Click "Open" | N/A | Restores text AND colors exactly. |

*Note: The magic triggers when you finish the syntax (e.g., typing the final "::" or "**").*

## Security Note
This application uses a custom `.ntp` file extension. These files are pure JSON.
* **Safe:** You can open `.ntp` files in any text editor to see the raw data.
* **Audit Friendly:** No binary blobs or hidden scripts.

## License
Distributed under the MIT License. See LICENSE for more information.
