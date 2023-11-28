import requests
from .eventsClass import Event

class listener_class:
    def __init__(self, url: str):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.url : str = url
        self.data = None

    def get_data(self):
        req = requests.get(url=self.url, headers=self.headers)
        self.data = req.json()
        data_collection = []
        # Извлечение данных из Cells
        for item in self.data["Items"]:
            # event_item = self.data["Items"][0]
            event_cells = item["Cells"]

            # Извлечение каждой переменной
            subekt_rossiyskoy_federatsii = event_cells["SUBEKT_ROSSIYSKOY_FEDERATSII"]
            munitsipalnoe_obrazovanie = event_cells["MUNITSIPALNOE_OBRAZOVANIE"]
            nazvanie_meropriyatiya = event_cells["NAZVANIE_MEROPRIYATIYA"]
            data_nachala = event_cells["DATA_NACHALA"]
            data_okonchaniya = event_cells["DATA_OKONCHANIYA"]
            adres_provedeniya = event_cells["ADRES_PROVEDENIYA"]
            koordinaty_wgs_84_dolgota = event_cells["KOORDINATY_WGS_84_DOLGOTA_"]
            koordinaty_wgs_84_shirota = event_cells["KOORDINATY_WGS_84_SHIROTA"]


            data_collection.append(Event(
                object=subekt_rossiyskoy_federatsii,
                municipality=munitsipalnoe_obrazovanie,
                event_name=nazvanie_meropriyatiya,
                event_address=adres_provedeniya,
                event_date=f"{data_nachala} - {data_okonchaniya}",
            ))

        return data_collection