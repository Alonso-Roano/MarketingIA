from enum import Enum

class ModeloTipo(str, Enum):
    linear_regression = "linear_regression"
    random_forest = "random_forest"
    random_forest_regressor = "random_forest_regressor"
