import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report, roc_curve
)
from sklearn.model_selection import cross_val_score

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
REPORT_PATH = Path(__file__).resolve().parents[2] / "docs" / "model_report.txt"


def section(title):
    print(f"\n{'=' * 60}\n  {title}\n{'=' * 60}")


def evaluate(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    recall_1 = recall_score(y_test, y_pred, pos_label=1)
    recall_0 = recall_score(y_test, y_pred, pos_label=0)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred, target_names=["No diabetes", "Diabetes"])

    print(f"\n  Accuracy:       {acc:.4f}")
    print(f"  Sensibilidad:   {recall_1:.4f}  (recall clase 1 - Diabetes)")
    print(f"  Especificidad:  {recall_0:.4f}  (recall clase 0 - No diabetes)")
    print(f"  F1-score:       {f1:.4f}")
    print(f"  AUC-ROC:        {auc:.4f}")
    print(f"\n  Matriz de confusion:\n{cm}")
    print(f"\n  Classification report:\n{cr}")

    return {
        "name": name, "model": model, "y_prob": y_prob,
        "accuracy": acc, "sensitivity": recall_1, "specificity": recall_0,
        "f1": f1, "auc": auc, "cm": cm, "cr": cr
    }


def cross_validate(name, model, X_train, y_train):
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc")
    print(f"  {name}: AUC media={scores.mean():.4f} (+/- {scores.std():.4f})")
    return scores


def optimal_threshold(y_test, y_prob):
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    # Maximizar TPR (sensibilidad) minimizando FPR (falsos negativos)
    optimal_idx = np.argmax(tpr - fpr)
    return float(thresholds[optimal_idx]), float(tpr[optimal_idx]), float(fpr[optimal_idx])


def main():
    report_lines = ["REPORTE MODELO — GlucoCheck", "=" * 60, ""]

    try:
        # 1. CARGA
        section("1. CARGA DE DATOS")
        X_train = pd.read_csv(PROCESSED_DIR / "X_train.csv")
        X_test  = pd.read_csv(PROCESSED_DIR / "X_test.csv")
        y_train = pd.read_csv(PROCESSED_DIR / "y_train.csv").squeeze()
        y_test  = pd.read_csv(PROCESSED_DIR / "y_test.csv").squeeze()
        print(f"  X_train: {X_train.shape} | X_test: {X_test.shape}")

        # 2. ENTRENAMIENTO
        section("2. ENTRENAMIENTO DE MODELOS")
        rf = RandomForestClassifier(random_state=42)
        lr = LogisticRegression(random_state=42, max_iter=1000)
        rf.fit(X_train, y_train)
        lr.fit(X_train, y_train)
        print("  RandomForest y LogisticRegression entrenados.")

        # 3. EVALUACION
        section("3. EVALUACION — Random Forest")
        rf_metrics = evaluate("Random Forest", rf, X_test, y_test)

        section("3. EVALUACION — Logistic Regression")
        lr_metrics = evaluate("Logistic Regression", lr, X_test, y_test)

        report_lines += [
            "=== RANDOM FOREST ===",
            f"Accuracy:      {rf_metrics['accuracy']:.4f}",
            f"Sensibilidad:  {rf_metrics['sensitivity']:.4f}",
            f"Especificidad: {rf_metrics['specificity']:.4f}",
            f"F1-score:      {rf_metrics['f1']:.4f}",
            f"AUC-ROC:       {rf_metrics['auc']:.4f}",
            f"Matriz de confusion:\n{rf_metrics['cm']}",
            f"Classification report:\n{rf_metrics['cr']}", "",
            "=== LOGISTIC REGRESSION ===",
            f"Accuracy:      {lr_metrics['accuracy']:.4f}",
            f"Sensibilidad:  {lr_metrics['sensitivity']:.4f}",
            f"Especificidad: {lr_metrics['specificity']:.4f}",
            f"F1-score:      {lr_metrics['f1']:.4f}",
            f"AUC-ROC:       {lr_metrics['auc']:.4f}",
            f"Matriz de confusion:\n{lr_metrics['cm']}",
            f"Classification report:\n{lr_metrics['cr']}", "",
        ]

        # 4. VALIDACION CRUZADA
        section("4. VALIDACION CRUZADA (cv=5, AUC-ROC)")
        rf_cv = cross_validate("Random Forest", rf, X_train, y_train)
        lr_cv = cross_validate("Logistic Regression", lr, X_train, y_train)

        report_lines += [
            "=== VALIDACION CRUZADA ===",
            f"Random Forest      — media: {rf_cv.mean():.4f}, std: {rf_cv.std():.4f}",
            f"Logistic Regression — media: {lr_cv.mean():.4f}, std: {lr_cv.std():.4f}",
            ""
        ]

        # 5. SELECCION DEL MEJOR MODELO
        section("5. SELECCION DEL MEJOR MODELO")
        best = rf_metrics if rf_metrics["auc"] >= lr_metrics["auc"] else lr_metrics
        other = lr_metrics if best["name"] == "Random Forest" else rf_metrics

        justification = (
            f"Modelo seleccionado: {best['name']}\n"
            f"  AUC-ROC: {best['auc']:.4f} vs {other['auc']:.4f} ({other['name']})\n"
            f"  Mayor AUC indica mejor capacidad discriminativa general.\n"
            f"  Sensibilidad: {best['sensitivity']:.4f} (minimiza falsos negativos — critico en diagnostico medico)"
        )
        print(f"\n{justification}")

        report_lines += ["=== MODELO SELECCIONADO ===", justification, ""]

        # 6. SERIALIZACION
        section("6. SERIALIZACION")
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        model_path = PROCESSED_DIR / "model.pkl"
        joblib.dump(best["model"], model_path)
        print(f"  Modelo guardado en: {model_path}")

        params = best["model"].get_params()
        params_str = "\n".join(f"    {k}: {v}" for k, v in params.items())
        print(f"  Parametros del modelo ganador:\n{params_str}")
        report_lines += [
            "=== PARAMETROS DEL MODELO GANADOR ===",
            params_str, ""
        ]

        # 7. UMBRAL OPTIMO
        section("7. UMBRAL OPTIMO (curva ROC)")
        threshold, tpr_val, fpr_val = optimal_threshold(y_test, best["y_prob"])
        threshold_msg = (
            f"  Umbral optimo:  {threshold:.4f}\n"
            f"  Sensibilidad:   {tpr_val:.4f}\n"
            f"  1-Especificidad: {fpr_val:.4f}\n"
            f"  (Maximiza TPR - FPR para reducir falsos negativos)"
        )
        print(threshold_msg)

        threshold_path = PROCESSED_DIR / "threshold.txt"
        with open(threshold_path, "w") as f:
            f.write(str(threshold))
        print(f"  Umbral guardado en: {threshold_path}")

        report_lines += ["=== UMBRAL OPTIMO ===", threshold_msg, ""]

        # GUARDAR REPORTE
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(str(l) for l in report_lines))
        print(f"\n  Reporte guardado en: {REPORT_PATH}")

    except FileNotFoundError as e:
        print(f"Error: archivo no encontrado — {e}")
        print("Ejecuta primero: python src/data/preprocess.py")
        raise
    except Exception as e:
        print(f"Error durante el entrenamiento: {e}")
        raise


if __name__ == "__main__":
    main()
