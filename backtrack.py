import sys
from datetime import datetime, date
from crawler_core import crawl_bisnis_com, write_to_json
import os

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python backtrack.py <start_date> <end_date>")
        print("Date format: YYYY-MM-DD")
        sys.exit(1)

    start_date_str = sys.argv[1]
    end_date_str = sys.argv[2]

    try:
        START_DATE = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        END_DATE = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)
        
    print(f"--- Starting Backtrack Mode: {start_date_str} to {end_date_str} ---")
    
    articles = crawl_bisnis_com(start_date=START_DATE, end_date=END_DATE)
    
    if articles:
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_prefix = f"backtrack_output_{timestamp_str}"
        write_to_json(articles, filename_prefix)
    else:
        print("No articles found in the specified date range.")