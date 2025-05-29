import requests
import pandas as pd
from datetime import date

# Columnas que te interesan
values = ["id", "name", "nameDistrict", "nameDepartment", "attributes"]
prices = ["price_hour", "price_part_time", "price_daily", "latitude", "longitude"]

# Crear DataFrame vacío
df = pd.DataFrame(columns=values + prices)

def parse_json_to_dataframe(list_web, df_entrada):
    for card in list_web:
        result = {}
        for variable in values:
            try:
                if variable == "attributes":
                    for price in prices:
                        result[price] = card.get(variable, {}).get(price)
                else:
                    result[variable] = card.get(variable)
            except Exception as e:
                print(f"Error al procesar '{variable}': {e}")
                continue
        df_entrada = pd.concat([df_entrada, pd.DataFrame([result])], ignore_index=True)
    return df_entrada

def read_api():
    all_cards = []
    url = "https://api.smileandgo.pe/1.0/directory"
    offset = 0
    limit = 100  # puedes ajustar este valor

    while True:
        params = {
            "district": "",
            "province": "",
            "price_range": "",
            "seed": 5673,
            "offset": offset,
            "limit": limit,
            "mode": "rent"
        }

        headers = {
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code != 200:
                break

            data = response.json()
            items = data.get("list", [])

            if not items:
                break

            all_cards.extend(items)
            offset += limit
        except Exception as e:
            print(f"Error en la solicitud: {e}")
            break

    return all_cards

def save_csv(base):
    base.to_csv(f"Data/data_consultorios_{date.today()}.csv", sep = ',', quotechar = '"', index = False)

# Ejecutar todo
cards_list = read_api()
base = parse_json_to_dataframe(cards_list, df)
base["date_updated"] = date.today()
print(base.head())
save_csv(base)
