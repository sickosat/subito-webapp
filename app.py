from flask import Flask, render_template, request, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

def scrape_subito(marka, tip, lokacija, godiste, cena_min, cena_max, kilometraza_max):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    query = f"{marka}+{tip}"
    url = f"https://www.subito.it/annunci-{lokacija}/vendita/moto-scooter/?q={query}&from={godiste}"
    if cena_min:
        url += f"&priceMin={cena_min}"
    if cena_max:
        url += f"&priceMax={cena_max}"

    driver.get(url)
    time.sleep(3)

    oglasi = driver.find_elements(By.CSS_SELECTOR, "a.AdCardAd_cardLink__zU5EX")[:25]

    with open("rezultati.txt", "w", encoding="utf-8") as f:
        for oglas in oglasi:
            naslov = oglas.text.strip()
            link = oglas.get_attribute("href")
            f.write(f"{naslov}\n{link}\n\n")

    driver.quit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        marka = request.form["marka"]
        tip = request.form["tip"]
        lokacija = request.form["lokacija"]
        godiste = request.form["godiste"]
        cena_min = request.form.get("cena_min")
        cena_max = request.form.get("cena_max")
        kilometraza_max = request.form.get("kilometraza_max")

        scrape_subito(marka, tip, lokacija, godiste, cena_min, cena_max, kilometraza_max)
        return send_file("rezultati.txt", as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
