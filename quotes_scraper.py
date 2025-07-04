# 📦 Import necessary libraries
import requests                    # To make HTTP requests (open the webpage)
from bs4 import BeautifulSoup      # To parse HTML content
import pandas as pd                # To save data in CSV format
import os
os.startfile("quotes.csv")

# 🔗 Define the base URL (notice the {} — it will be filled with page numbers)
url = "http://quotes.toscrape.com/page/{}/"

# 📋 Create an empty list to store all scraped quote data
all_quotes = []

# 🔁 Loop through first 5 pages of the site
for page in range(1, 6):
    # 🛜 Send a GET request to the current page
    res = requests.get(url.format(page))
    
    # ⚠️ If request fails (e.g., site is down), skip to next page
    if res.status_code != 200:
        print(f"Failed to load page {page}")
        continue

    # 🧠 Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(res.text, "html.parser")
    
    # 🔍 Find all quote blocks (inside <div class="quote">)
    quotes = soup.find_all("div", class_="quote")

    # 🔁 Loop through each quote block and extract data
    for quote in quotes:
        # ✏️ Get the quote text
        text = quote.find("span", class_="text").get_text(strip=True)
        
        # 🧑‍🎓 Get the author
        author = quote.find("small", class_="author").get_text(strip=True)
        
        # 🏷️ Get all tags (they're inside <a class="tag">)
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
        
        # 📦 Store the data in dictionary format
        all_quotes.append({
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags)
        })

# 💾 Convert all data to a DataFrame (table-like) and save to CSV
df = pd.DataFrame(all_quotes)
df.to_csv("quotes.csv", index=False)

print("✅ Scraping complete! Data saved to quotes.csv")
for quote in all_quotes[:5]:
    print(quote)
