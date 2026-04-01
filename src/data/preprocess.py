import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

RAW_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "diabetes_raw.csv"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
REPORT_PATH = Path(__file__).resolve().parents[2] / "docs" / "preprocessing_report.txt"

SUSPICIOUS_ZERO_COLS = ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]
PREDICTORS = ["pregnancies", "glucose", "blood_pressure", "skin_thickness",
              "insulin", "bmi", "diabetes_pedigree", "age"]


def section(title):
    print(f"\n{'=' * 60}\n  {title}\n{'=' * 60}")


def main():
    report_lines = ["REPORTE PREPROCESAMIENTO — GlucoCheck", "=" * 60, ""]

    try:
        # 1. CARGA
        section("1. CARGA")
        df = pd.read_csv(RAW_PATH)
        print(f"  Dataset cargado: {df.shape}")
        report_lines += ["=== CARGA ===", f"Shape original: {df.shape}", ""]

        # 2. TRATAMIENTO DE VALORES CERO SOSPECHOSOS
        section("2. IMPUTACION DE CEROS SOSPECHOSOS")
        imputed_counts = {}
        for col in SUSPICIOUS_ZERO_COLS:
            n_zeros = (df[col] == 0).sum()
            imputed_counts[col] = n_zeros
            df[col] = df[col].replace(0, np.nan)
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"  {col:<20} {n_zeros:>4} ceros imputados con mediana={median_val:.2f}")

        imputed_lines = [f"  {col:<20} {n} ceros imputados" for col, n in imputed_counts.items()]
        report_lines += ["=== IMPUTACION ==="] + imputed_lines + [""]

        # 3. SEPARAR FEATURES Y TARGET
        X = df[PREDICTORS]
        y = df["outcome"]

        dist_before = y.value_counts().sort_index()
        print(f"\n  Distribucion antes de SMOTE:\n"
              f"    No diabetes (0): {dist_before[0]}\n"
              f"    Diabetes    (1): {dist_before[1]}")

        # 4. SMOTE
        section("3. SMOTE — BALANCEO DE CLASES")
        smote = SMOTE(random_state=42)
        X_res, y_res = smote.fit_resample(X, y)

        dist_after = pd.Series(y_res).value_counts().sort_index()
        print(f"  Distribucion despues de SMOTE:\n"
              f"    No diabetes (0): {dist_after[0]}\n"
              f"    Diabetes    (1): {dist_after[1]}")
        print(f"  Total muestras: {len(X_res)}")

        report_lines += [
            "=== BALANCEO DE CLASES (SMOTE) ===",
            f"Antes  — No diabetes: {dist_before[0]}, Diabetes: {dist_before[1]}",
            f"Despues — No diabetes: {dist_after[0]}, Diabetes: {dist_after[1]}",
            ""
        ]

        # 5. NORMALIZACION
        section("4. NORMALIZACION — StandardScaler")
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_res)
        X_scaled_df = pd.DataFrame(X_scaled, columns=PREDICTORS)

        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        scaler_path = PROCESSED_DIR / "scaler.pkl"
        joblib.dump(scaler, scaler_path)
        print(f"  Scaler guardado en: {scaler_path}")
        report_lines += ["=== NORMALIZACION ===", f"Scaler guardado en: {scaler_path}", ""]

        # 6. PARTICION
        section("5. PARTICION TRAIN/TEST (80/20)")
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled_df, y_res, test_size=0.2, random_state=42, stratify=y_res
        )

        X_train.to_csv(PROCESSED_DIR / "X_train.csv", index=False)
        X_test.to_csv(PROCESSED_DIR / "X_test.csv", index=False)
        y_train.to_csv(PROCESSED_DIR / "y_train.csv", index=False)
        y_test.to_csv(PROCESSED_DIR / "y_test.csv", index=False)

        print(f"  X_train: {X_train.shape}  |  y_train: {y_train.shape}")
        print(f"  X_test:  {X_test.shape}  |  y_test:  {y_test.shape}")
        print(f"  Archivos guardados en: {PROCESSED_DIR}")

        report_lines += [
            "=== PARTICION ===",
            f"X_train: {X_train.shape}, y_train: {y_train.shape}",
            f"X_test:  {X_test.shape},  y_test:  {y_test.shape}",
            ""
        ]

        # GUARDAR REPORTE
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(str(l) for l in report_lines))
        print(f"\n  Reporte guardado en: {REPORT_PATH}")

    except FileNotFoundError:
        print(f"Error: no se encontro {RAW_PATH}")
        print("Ejecuta primero: python src/data/download_data.py")
        raise
    except Exception as e:
        print(f"Error durante el preprocesamiento: {e}")
        raise


if __name__ == "__main__":
    main()
