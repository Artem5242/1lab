import csv, json
import requests
from bs4 import BeautifulSoup
import datetime

def diсtionary_func(arr):
    dic = { arr[i]:list(k for k in range(i, len(arr)) if arr[i] == arr[k]) for i in range(0,len(arr)) if arr.index(arr[i]) >= i}
    print(dic)

def jaccar_func(first_set, second_set):
    sections_inter = 0
    union = len(first_set) + len(second_set)
    for item in first_set:
        if item in second_set:
            intersections += 1
    print(intersections / (len(first_set) + len(second_set) - intersections))

def Json_to_csv_func():
    jname = "data.json"
    csvname = "result.csv"

    with open(jname, "r") as file:
        MyJSON = json.loads(file.read())

    with open(csvname, "w", newline = "") as file:
        columns = ["item", "country", "year", "sales"]
        writer = csv.DictWriter(file, fieldnames = columns)
        writer.writeheader()
    
        for dict in MyJSON:
            for country, value in dict['sales_by_country'].items():
                for year in value:
                    writer.writerow({"item": dict['item'], "country": country, "year": year, "sales": value[year]})

def currency_func():

    start = datetime.datetime.strptime("01/03/2020", "%d/%m/%Y")
    end = datetime.datetime.strptime("01/07/2020", "%d/%m/%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    
    with open("money.csv", "w", newline = "") as file:
        columns = ["Дата", "Доллар США", "Евро", "Индийская рупия", "Украинская гривна"]
        writer = csv.DictWriter(file, fieldnames = columns)
        writer.writeheader()

        for date in date_generated:
            resp = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date.strftime("%d/%m/%Y"))
            soup = BeautifulSoup(resp.content, "xml")
            writer.writerow({"Дата": date.strftime("%d/%m/%Y"), "Доллар США": float(soup.find("CharCode", text = "USD").find_next_sibling("Value").get_text().replace(',','.')),
            "Евро": float(soup.find("CharCode", text = "EUR").find_next_sibling("Value").get_text().replace(',','.')),
            "Индийская рупия": round(float(soup.find("CharCode", text = "INR").find_next_sibling("Value").get_text().replace(',','.')) / 100, 5),
            "Украинская гривна": round(float(soup.find("CharCode", text = "UAH").find_next_sibling("Value").get_text().replace(',','.')) / 10, 5)})

def main_func():
    arr = input("Enter the array for task 1: ").split(" ")
    dictionary_func(arr)
    first_set = input("Введите первое множество для Жаккара: ").split(" ")
    second_set = input("Введите второе множество для Жаккара: ").split(" ")
    jaccard_func(first_set, second_set)
    currency_func()
    Json_to_csv_func()

main()
