# GlucoCheck — Documentación Técnica

## Arquitectura
Sistema cliente-servidor desacoplado. Frontend en Netlify, Backend en Railway.

## Métricas del modelo
- Accuracy: 81%
- Recall (clase positiva): 83%
- F1-score: 81%
- AUC-ROC: 0.91
- Threshold óptimo: 0.63

## Pipeline ML
1. Descarga dataset Pima Indians
2. EDA y detección de ceros sospechosos
3. Preprocesamiento: imputación por mediana, SMOTE, StandardScaler
4. Entrenamiento: Random Forest vs Regresión Logística
5. Selección por AUC-ROC y serialización de artefactos
