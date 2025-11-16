import time
import schedule
from datetime import datetime
from crawler_core import crawl_bisnis_com, write_to_json

SCRAPE_INTERVAL_SECONDS = 900 

def job_function():
    current_time = datetime.now()
    print(f"--- Running Standard Mode at {current_time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    latest_articles = crawl_bisnis_com(limit=10) 
    
    if latest_articles:
        filename_prefix = f"standard_output_{current_time.strftime('%Y%m%d_%H%M%S')}"
        write_to_json(latest_articles, filename_prefix)
    else:
        print("No new articles found.")

if __name__ == "__main__":
    job_function() 
    schedule.every(SCRAPE_INTERVAL_SECONDS).seconds.do(job_function)
    print(f"Crawler started. Running every {SCRAPE_INTERVAL_SECONDS} seconds. Press Ctrl+C to stop.")

    while True:
        schedule.run_pending()
        time.sleep(1)