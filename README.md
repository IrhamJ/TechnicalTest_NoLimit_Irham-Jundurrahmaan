# Modular Web Crawler Solution (Kompas.com)

This project implements a modular Python web crawler to retrieve article data from Kompas.com, supporting two modes of operation as required by the technical assessment.

## 1. Project Architecture and Functionality

### 1.1 Core Components and Modularity

The solution uses a modular design to ensure code reuse, separating core logic from execution entrypoints.

| File | Role | Function |
| :--- | :--- | :--- |
| **`crawler_core.py`** | Core Module | Contains reusable functions for **HTTP requests, HTML parsing, date cleaning, and detail scraping**. This module is shared by both modes. |
| **`backtrack.py`** | Entrypoint 1 | Executes the **Backtrack Mode** (historical filtering). |
| **`standard.py`** | Entrypoint 2 | Executes the **Standard Mode** (long running process via `schedule`). |

### 1.2 Execution Instructions

1.  **Install Dependencies:** Ensure your virtual environment is active, then install required libraries:
    `pip install requests beautifulsoup4 schedule`
2.  **Run Backtrack Mode (Date Range):**
    * **Purpose:** Scrape articles published within the specified date range.
    * **Execution:** `python backtrack.py YYYY-MM-DD YYYY-MM-DD`
    * **Output:** `backtrack_output_<timestamp>.json`
3.  **Run Standard Mode (Long Running):**
    * **Purpose:** Continuously monitor and scrape the latest articles (limit 10 per run).
    * **Execution:** `python standard.py` (Use Ctrl+C to stop the process).
    * **Output:** `standard_output_<timestamp>.json`

***

## 2. Technical and Design

### 2.1  Source Switch From Bisnis.com to Kompas.com

The core logic was initially developed for Bisnis.com. However, due to persistent **Status Code 404** errors and presumed **JavaScript rendering** of the listing content which unable to processed by BeautifulSoup, the initial target was abandoned.

* **Rational:** Standard Python libraries (`requests` and `BeautifulSoup`) cannot render JavaScript-loaded content, which is required for dynamic sites like Bisnis.com. Switching to the structurally **stable index URL of Kompas.com** successfully proved the robustness and accuracy of the core Python logic.

### 2.2 Core Logic: Date Filtering and Output

* **Distinction:** The code successfully separates the role of the **Crawler** (navigating pages/links) and the **Scraper** (extracting detail content).
* **Backtrack Logic :** The `crawl_bisnis_com` function converts the input date range and the scraped date string into **pure Python `date` objects**. This ensures accurate comparison and filtering regardless of time zone variations.
* **Output:** The final JSON output adheres to the required format, with `tanggal terbit` stored in **ISO 8601 format**.
