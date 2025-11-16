import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import json
import time
from typing import List, Dict, Optional
import locale
import sys

try:
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8') 
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    except locale.Error:
        pass 

BASE_URL = "https://www.kompas.com"
LISTING_URL_PRIMARY = "https://www.kompas.com"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}


def format_date_to_iso(date_obj: Optional[datetime]) -> Optional[str]:
    if isinstance(date_obj, datetime):
        return date_obj.isoformat()
    return None

def clean_date_string(raw_date_str: Optional[str]) -> Optional[str]:
    if not raw_date_str:
        return None

    date_str_clean = raw_date_str.replace("WIB", "").strip()
    
    if '|' in date_str_clean:
        date_str_clean = date_str_clean.split('|')[0].strip()
        
    return date_str_clean + ' 00:00'


def scrape_article_detail(article_url: str) -> tuple[Optional[str], Optional[str]]:
    try:
        response = requests.get(article_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title_tag = soup.find('h1', class_='read__title') or soup.find('h1')
        title = title_tag.text.strip() if title_tag else "Judul Tidak Ditemukan"
        
        content_div = soup.find('div', class_='read__content')
        
        content_paragraphs = [p.text for p in content_div.find_all('p')] if content_div else []
        content = "\n".join(content_paragraphs).strip()
        
        if len(content) < 50:
             content = "Konten terlalu pendek atau selector gagal."
        
        return title, content
        
    except Exception as e:
        print(f"Error scraping detail for {article_url}: {e}")
        return None, None


def crawl_bisnis_com(start_date: Optional[date] = None, end_date: Optional[date] = None, limit: Optional[int] = None) -> List[Dict]:
    articles_list = []
    page = 1
    max_articles_target = 20 
    

    while page == 1: 
        listing_url = LISTING_URL_PRIMARY
        
        try:
            response = requests.get(listing_url, headers=HEADERS, timeout=15)
            
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code}. Stopping.")
                return []
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            article_tags = soup.find_all('a', href=lambda href: href and '/read/' in href)
            
            unique_links = set() 

            if not article_tags:
                break 

            for link_tag in article_tags:
                link_href = link_tag.get('href')
                
                if link_href in unique_links:
                    continue
                unique_links.add(link_href)
                
                date_tag = link_tag.find_next('time') or link_tag.find_next('small')
                raw_date_str = date_tag.text.strip() if date_tag else None

                article_date = None
                
                if raw_date_str:
                    date_str_clean = clean_date_string(raw_date_str)
                    try:
                        dt_object = datetime.strptime(date_str_clean, '%d/%m/%Y %H:%M') 
                        article_date = dt_object.date() 
                    except ValueError:
                        pass
                    
                    if start_date and end_date and article_date:
                        if not (start_date <= article_date <= end_date):
                            continue
                
                full_link = link_href
                
                title, content = scrape_article_detail(full_link)
                
                if title and content and title != "Judul Tidak Ditemukan" and len(content) > 100:
                    articles_list.append({
                        "link": full_link,
                        "judul": title,
                        "isi_artikel": content,
                        "tanggal_terbit": format_date_to_iso(datetime.combine(article_date, datetime.min.time()) if article_date else datetime.now()) 
                    })
                
                if limit and len(articles_list) >= limit:
                    return articles_list
            
            page += 1
            time.sleep(2) 
            
        except requests.exceptions.RequestException as e:
            print(f"Error accessing listing page: {e}")
            break 
            
    return articles_list


def write_to_json(data: List[Dict], filename_prefix: str):
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')

    filename = f"{filename_prefix}_{timestamp_str}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=str) 
        
    print(f"✅ Output written to {filename}")