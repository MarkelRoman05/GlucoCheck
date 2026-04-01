import pandas as pd
from pathlib import Path

URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

COLUMNS = [
    "pregnancies", "glucose", "blood_pressure", "skin_thickness",
    "insulin", "bmi", "diabetes_pedigree", "age", "outcome"
]

OUTPUT_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "diabetes_raw.csv"


def download_data():
    try:
        print("Descargando dataset...")
        df = pd.read_csv(URL, header=None, names=COLUMNS)

        print(f"\nShape: {df.shape}")
        print(f"\nPrimeras 5 filas:\n{df.head()}")
        print(f"\nTipos de datos:\n{df.dtypes}")
        print(f"\nEstadísticas descriptivas:\n{df.describe()}")

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUTPUT_PATH, index=False)

        print(f"\nDataset guardado en: {OUTPUT_PATH}")

    except Exception as e:
        print(f"Error al descargar o procesar el dataset: {e}")
        raise


if __name__ == "__main__":
    download_data()
