import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "diabetes_raw.csv"
REPORT_PATH = Path(__file__).resolve().parents[2] / "docs" / "eda_report.txt"

SUSPICIOUS_ZERO_COLS = ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]
PREDICTORS = ["pregnancies", "glucose", "blood_pressure", "skin_thickness",
              "insulin", "bmi", "diabetes_pedigree", "age"]


def section(title):
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"  {title}")
    print(separator)


def analyze(df):
    lines = []

    # 1. INFORMACIÓN GENERAL
    section("1. INFORMACIÓN GENERAL")
    info = f"Shape: {df.shape}\n\nTipos de datos:\n{df.dtypes}"
    print(info)
    lines += ["=== INFORMACIÓN GENERAL ===", info, ""]

    # 2. VARIABLE OBJETIVO
    section("2. VARIABLE OBJETIVO")
    counts = df["outcome"].value_counts().sort_index()
    pcts = df["outcome"].value_counts(normalize=True).sort_index() * 100
    target_lines = []
    for label, name in [(0, "No diabetes"), (1, "Diabetes")]:
        line = f"  {label} ({name}): {counts[label]} registros ({pcts[label]:.1f}%)"
        print(line)
        target_lines.append(line)
    ratio = counts[0] / counts[1]
    balance_msg = f"\n  Ratio mayoritaria/minoritaria: {ratio:.2f}:1"
    balance_msg += " -> Desbalance moderado" if ratio > 1.5 else " -> Clases balanceadas"
    print(balance_msg)
    lines += ["=== VARIABLE OBJETIVO ==="] + target_lines + [balance_msg, ""]

    # 3. VALORES CERO SOSPECHOSOS
    section("3. VALORES CERO SOSPECHOSOS")
    zero_lines = []
    for col in SUSPICIOUS_ZERO_COLS:
        n_zeros = (df[col] == 0).sum()
        pct = n_zeros / len(df) * 100
        line = f"  {col:<20} {n_zeros:>4} ceros  ({pct:.1f}%)"
        print(line)
        zero_lines.append(line)
    lines += ["=== VALORES CERO SOSPECHOSOS ==="] + zero_lines + [""]

    # 4. ESTADÍSTICAS POR CLASE
    section("4. MEDIA DE VARIABLES POR CLASE (outcome)")
    stats = df.groupby("outcome")[PREDICTORS].mean().round(2)
    stats.index = stats.index.map({0: "No diabetes (0)", 1: "Diabetes (1)"})
    stats_str = stats.to_string()
    print(stats_str)
    lines += ["=== MEDIA POR CLASE ===", stats_str, ""]

    # 5. CORRELACIONES CON OUTCOME
    section("5. CORRELACIÓN CON OUTCOME (mayor a menor)")
    corr = df[PREDICTORS].corrwith(df["outcome"]).sort_values(ascending=False)
    corr_lines = []
    for col, val in corr.items():
        line = f"  {col:<20} {val:+.4f}"
        print(line)
        corr_lines.append(line)
    lines += ["=== CORRELACIÓN CON OUTCOME ==="] + corr_lines + [""]

    return lines


def save_report(lines):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("REPORTE EDA — GlucoCheck\n")
        f.write("=" * 60 + "\n\n")
        f.write("\n".join(str(l) for l in lines))
    print(f"\nReporte guardado en: {REPORT_PATH}")


def main():
    try:
        df = pd.read_csv(DATA_PATH)
        lines = analyze(df)
        save_report(lines)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo {DATA_PATH}")
        print("Ejecuta primero: python src/data/download_data.py")
        raise
    except Exception as e:
        print(f"Error durante el análisis: {e}")
        raise


if __name__ == "__main__":
    main()
