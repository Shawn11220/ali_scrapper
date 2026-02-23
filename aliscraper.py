import csv
from playwright.sync_api import sync_playwright

def scrape(category):
    query = category.replace(" ", "+")
    url = f"https://www.aliexpress.com/w/wholesale-{query}.html?SearchText={query}&sortType=total_tranpro_desc"

    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        page.goto(url, timeout=60000)

        page.wait_for_selector("a.search-card-item")

        cards = page.query_selector_all("a.search-card-item")

        for card in cards:

            href = card.get_attribute("href")
            if not href:
                continue

            product_url = "https:" + href.split("?")[0]

            price_el = card.query_selector(".l0_lm")
            rating_el = card.query_selector(".l0_km")
            sold_el = card.query_selector(".l0_kk")

            price = price_el.inner_text() if price_el else ""
            rating = rating_el.inner_text() if rating_el else ""
            sold = sold_el.inner_text() if sold_el else ""

            data.append([product_url, rating, price, sold])

        browser.close()

    return data


def save_csv(rows):
    with open("products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "rating", "price", "sold"])
        writer.writerows(rows)


if __name__ == "__main__":
    category = input("Enter category: ").strip()
    results = scrape(category)
    save_csv(results)
    print(f"Saved {len(results)} products to products.csv")