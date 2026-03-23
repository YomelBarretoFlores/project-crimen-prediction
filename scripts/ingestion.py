import os

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


# ── Configuración ──
PROJECT_ID = "my-project-big-data-484021"
DATASET_ID = "raw_data"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "..", "auth", "key.json")

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

# ── Tablas y archivos ──
files_config = {
    "ipc_lima": {
        "path": os.path.join(BASE_DIR, "..", "data", "ipc_lima.csv"),
        "skiprows": 2,
        "names": ["periodo", "indice"],
    },
    "desempleo_lima": {
        "path": os.path.join(BASE_DIR, "..", "data", "desempleo_lima.csv"),
        "skiprows": 2,
        "names": ["periodo", "tasa"],
    },
    "poblacion_inei": {
        "path": os.path.join(BASE_DIR, "..", "data", "poblacion_inei.csv"),
        "skiprows": 0,
        "sep": ";",
    },
    "denuncias_policiales": {
        "path": os.path.join(BASE_DIR, "..", "data", "denuncias_policiales.csv"),
        "skiprows": 0,
        "sep": ",",
    },
}


def upload_to_bigquery(table_name: str, config: dict) -> None:
    file_path = config["path"]
    if not os.path.exists(file_path):
        print(f"⚠️ Archivo no encontrado: {file_path}")
        return

    print(f"🚀 Procesando: {table_name}...")

    encoding = "utf-8-sig" if "poblacion" in table_name else "latin-1"

    try:
        df = pd.read_csv(
            file_path,
            sep=config.get("sep", ","),
            encoding=encoding,
            skiprows=config["skiprows"],
            names=config.get("names", None),
        )
        df.columns = [c.strip() for c in df.columns]

        table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE", autodetect=True
        )

        client.load_table_from_dataframe(df, table_ref, job_config=job_config).result()
        print(f"Tabla '{table_name}' cargada con éxito.\n")

    except Exception as e:
        print(f"Error en {table_name}: {e}\n")


if __name__ == "__main__":
    for table, config in files_config.items():
        upload_to_bigquery(table, config)
    print("🏁 Ingesta finalizada.")
