SELECT DISTINCT id, url FROM urls WHERE scrape_status<>'DONE' AND shop='{SHOP}';