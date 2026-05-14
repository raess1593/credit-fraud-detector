# credit-fraud-detector

Estructura inicial para aprendizaje de modelos:

- `configs/config.yaml`: define `model_active`
- `src/models/models.py`: `get_model()` construye el modelo activo usando YAMLs de parámetros
- `src/main.py`: punto central que llama a `get_model()` y ejecuta entrenamiento
- `src/train.py`: script de entrenamiento reutilizable
- `configs/models/*.yaml`: parámetros configurables por modelo
