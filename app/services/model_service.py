from app.common.utils import cargar_modelo, convertir_a_python
import pandas as pd
import numpy as np
import io
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report,
    mean_squared_error, r2_score
)
from sklearn.base import RegressorMixin

class ModelService:
    def __init__(self, model_path, excel_path, input_fields, target_field, metadata):
        self.model = cargar_modelo(model_path)
        self.excel_path = excel_path
        self.input_fields = input_fields
        self.target_field = target_field
        self.metadata = metadata

        self._cached_df = None
        self._cached_stats = None
        self._cached_metricas = None
        self._cached_info = None

    def _load_dataset(self):
        if self._cached_df is None:
            self._cached_df = pd.read_csv(self.excel_path)
            self._cached_stats = self._precompute_field_statistics()

    def _precompute_field_statistics(self):
        stats = {}
        for field in self.input_fields:
            if field in self._cached_df.columns:
                column = self._cached_df[field].dropna()

                if column.empty:
                    stats[field] = None
                elif pd.api.types.is_numeric_dtype(column):
                    stats[field] = column.mean()
                else:
                    stats[field] = column.mode().iloc[0] if not column.mode().empty else None
            else:
                stats[field] = None
        return stats

    def predecir(self, data: dict):
        self._load_dataset()
        return self._predecir_optimized(data)
    
    def _predecir_optimized(self, datos_input: dict) -> dict:
        datos_completos = {}

        for campo in self.input_fields:
            valor = datos_input.get(campo)
            if valor is not None:
                datos_completos[campo] = valor
            else:
                datos_completos[campo] = self._cached_stats.get(campo)

        entrada = pd.DataFrame([datos_completos], columns=self.input_fields)
        pred = self.model.predict(entrada)

        resultado = pred.tolist() if isinstance(pred, np.ndarray) else pred

        return {
            "prediccion": resultado[0]
        }

    def obtener_info(self):
        self._load_dataset()
        if self._cached_info is None:
            self._cached_info = self._compute_info()
        return self._cached_info

    def _compute_info(self):
        buffer = io.StringIO()
        self._cached_df.info(buf=buffer)

        return {
            "metadata": {
                **self.metadata,
                "ultima_actualizacion": datetime.fromtimestamp(
                    os.path.getmtime(self.excel_path)
                ).isoformat()
            },
            "dataset": {
                "columnas": self._cached_df.columns.tolist(),
                "primeras_filas": self._cached_df.head(5).to_dict(orient="records"),
                "estadisticas": self._cached_df.describe().to_dict(),
                "info": buffer.getvalue()
            }
        }

    def obtener_metricas(self):
        self._load_dataset()
        if self._cached_metricas is None:
            self._cached_metricas = self._compute_metricas()
        return self._cached_metricas

    def _compute_metricas(self):
        X = self._cached_df[self.input_fields]
        y = self._cached_df[self.target_field]
        y_pred = self.model.predict(X)

        ejemplos = [
            {
                "input": X.iloc[i].to_dict(),
                "real": y.iloc[i],
                "predicho": y_pred[i]
            }
            for i in range(min(10, len(X)))
        ]
        
        if isinstance(self.model, RandomForestClassifier):
            return {
                "tipo": "clasificacion",
                "accuracy": float(accuracy_score(y, y_pred)),
                "reporte": convertir_a_python(classification_report(y, y_pred, output_dict=True)),
                "ejemplos": convertir_a_python(ejemplos)
            }

        elif isinstance(self.model, RegressorMixin):
            return {
                "tipo_modelo": "regresión",
                "rmse": float(np.sqrt(mean_squared_error(y, y_pred))),
                "r2_score": float(r2_score(y, y_pred)),
                "ejemplos": [
                    {
                        "input": convertir_a_python(X.iloc[i].to_dict()),
                        "real": float(y.iloc[i]),
                        "predicho": float(y_pred[i])
                    }
                    for i in range(min(10, len(X)))
                ]
            }

        else:
            raise ValueError("Tipo de modelo no soportado. Se esperaba un modelo de clasificación o regresión.")