# Static Site Generator

A lightweight and minimal Static Site Generator (SSG) that converts Markdown files into a static website ready for GitHub Pages.
It’s simple, fast, and perfect for learning how static sites work under the hood.

> Repo: [phanatcha/static-sites](https://github.com/phanatcha/static-sites)
> Demo (GitHub Pages): https://phanatcha.github.io/static-sites/

---

## 🧠 What is a Static Site Generator?

A **static site generator** takes raw content (e.g., Markdown + images) and compiles it into a static website (HTML/CSS/JS). Static sites are fast, secure, and simple to host—ideal for **blogs, portfolios, landing pages, and documentation**.

---

## 🧩 Static vs Dynamic Sites

* **Static**: Prebuilt pages. No logins, comments, or user data. Super fast + secure.
* **Dynamic**: Server/database powered. Needed for uploads, accounts, comments, saved preferences.

---

## ⚙️ Features

* 📝 Converts Markdown (.md) into clean, semantic HTML
* 🎨 Uses a single template.html for consistent styling
* 📁 Automatically builds multiple index.html files
* 🚀 Fully compatible with GitHub Pages

---

## 🛠️ How It Works

1. The generator reads your Markdown files (e.g. `index.md`)
2. It converts Markdown to HTML
3. It injects that HTML into `template.html`
4. It writes the result as `index.html` inside a `docs/` folder

---

## 📁 Code Structure

```
static-sites/
├── README.md
├── build.sh
├── content
│   ├── blog
│   ├── contact
│   └── index.md
├── docs
│   ├── blog
│   ├── contact
│   ├── images
│   ├── index.css
│   └── index.html
├── main.sh
├── src
│   ├── __pycache__
│   ├── copystatic.py
│   ├── gencontent.py
│   ├── htmlnode.py
│   ├── inline_markdown.py
│   ├── main.py
│   ├── markdown_blocks.py
│   ├── test_gencontent.py
│   ├── test_htmlnode.py
│   ├── test_inline_markdown.py
│   ├── test_markdown_blocks.py
│   ├── test_textnode.py
│   └── textnode.py
├── static
│   ├── images
│   └── index.css
├── template.html
└── test.sh

```

---

## 🚀 Usage

> Requires **Python 3.10+**

### 1. Clone the project

```bash
git clone https://github.com/phanatcha/static-sites.git
cd static-sites
```

### 2. Run the generator

```bash
python gencontent.py
```

This will read your Markdown files from `content/` and build HTML files in `docs/`.

### 3. Open in browser

```bash
open docs/index.html
```

Or on Windows:

```bash
start docs/index.html
```

---

## 🌐 Hosting on GitHub Pages

1. Push your repo to GitHub
2. In **Settings → Pages**, choose:
   * **Source:** `main` branch
   * **Folder:** `/docs` *(or `/dist`, if that’s where your files build)*
3. Save — your site will appear at
   `https://<your-username>.github.io/static-sites`

---