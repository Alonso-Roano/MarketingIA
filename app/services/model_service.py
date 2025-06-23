from app.common.utils import cargar_modelo, predecir_instancia, obtener_info_dataset, calcular_metricas

class ModelService:
    def __init__(self, model_path, excel_path, input_fields, target_field, metadata):
        self.model = cargar_modelo(model_path)
        self.excel_path = excel_path
        self.input_fields = input_fields
        self.target_field = target_field
        self.metadata = metadata

    def predecir(self, data: dict):
        return predecir_instancia(self.model, data, self.excel_path, self.input_fields)

    def obtener_info(self):
        return obtener_info_dataset(self.excel_path, self.metadata)

    def obtener_metricas(self):
        return calcular_metricas(self.model, self.excel_path, self.input_fields, self.target_field)