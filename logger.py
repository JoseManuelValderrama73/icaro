"""
Sistema de logging para ejecuciones de finetuning y testing.
"""

import os
import json
from datetime import datetime
from pathlib import Path


class ExecutionLogger:
    """
    Clase para gestionar el logging de ejecuciones de finetuning y testing.
    
    Estructura de logs:
    logs/
        finetuning/
            {model}/
                {dataset}/
                    execution_YYYYMMDD_HHMMSS.log
        testing/
            {model}/
                {dataset}/
                    execution_YYYYMMDD_HHMMSS.log
    """
    
    def __init__(self, execution_type: str, model: str, dataset: str, settings: dict):
        """
        Inicializa el logger para una ejecución.
        
        :param execution_type: Tipo de ejecución ('finetuning' o 'testing')
        :param model: Nombre del modelo
        :param dataset: Nombre del dataset
        :param settings: Configuración utilizada para la ejecución
        """
        self.execution_type = execution_type
        self.model = model.split('/')[-1]  # Obtener solo el nombre del modelo
        self.dataset = dataset
        self.settings = settings
        
        # Generar timestamp para el nombre del archivo
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Crear la ruta del archivo de log
        self.log_dir = self._get_log_dir()
        self.log_file = os.path.join(self.log_dir, f"execution_{self.timestamp}.log")
        
        # Crear directorio si no existe
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Inicializar el archivo de log con la configuración
        self._init_log_file()
    
    def _get_log_dir(self) -> str:
        """
        Genera la ruta del directorio de logs.
        
        :return: Ruta del directorio de logs
        """
        return os.path.join("logs", self.execution_type, self.model, self.dataset)
    
    def _init_log_file(self):
        """
        Inicializa el archivo de log con información de la ejecución y configuración.
        """
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"EXECUTION LOG - {self.execution_type.upper()}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {self.model}\n")
            f.write(f"Dataset: {self.dataset}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("SETTINGS:\n")
            f.write("-" * 80 + "\n")
            f.write(json.dumps(self.settings, indent=4, ensure_ascii=False))
            f.write("\n" + "-" * 80 + "\n\n")
            
            f.write("EXECUTION LOG:\n")
            f.write("-" * 80 + "\n")
    
    def log(self, class_name: str, message: str):
        """
        Registra una entrada en el log.
        
        :param class_name: Nombre de la clase o componente que genera el log
        :param message: Mensaje a registrar
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{class_name}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        # También imprimir en consola
        print(log_entry.strip())
    
    def log_error(self, class_name: str, error: Exception):
        """
        Registra un error en el log.
        
        :param class_name: Nombre de la clase o componente que genera el error
        :param error: Excepción capturada
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{class_name}] ERROR: {type(error).__name__}: {str(error)}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        print(log_entry.strip())
    
    def log_step(self, class_name: str, step: str, status: str = "STARTED"):
        """
        Registra el inicio o finalización de un paso específico.
        
        :param class_name: Nombre de la clase o componente
        :param step: Nombre del paso
        :param status: Estado del paso ('STARTED', 'COMPLETED', 'FAILED')
        """
        message = f"{status}: {step}"
        self.log(class_name, message)
    
    def log_metrics(self, class_name: str, metrics: dict):
        """
        Registra métricas de evaluación.
        
        :param class_name: Nombre de la clase o componente
        :param metrics: Diccionario con las métricas
        """
        metrics_str = ", ".join([f"{k}={v}" for k, v in metrics.items()])
        self.log(class_name, f"Metrics: {metrics_str}")
    
    def finalize(self, class_name: str, status: str = "SUCCESS"):
        """
        Finaliza el log con un estado final.
        
        :param class_name: Nombre de la clase o componente
        :param status: Estado final ('SUCCESS', 'FAILED')
        """
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("-" * 80 + "\n")
            f.write(f"EXECUTION {status}\n")
            f.write(f"End timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
        
        self.log(class_name, f"Execution finished with status: {status}")
        print(f"\nLog file saved at: {self.log_file}")


def finetuning_log_path(model: str, dataset: str) -> str:
    """
    Genera la ruta del directorio de logs para finetuning.
    Similar a model_save_path pero para logs de finetuning.
    
    :param model: Nombre del modelo
    :param dataset: Nombre del dataset
    :return: Ruta del directorio de logs
    """
    return os.path.join("logs", "finetuning", model.split('/')[-1], dataset)


def testing_log_path(model: str, dataset: str) -> str:
    """
    Genera la ruta del directorio de logs para testing.
    Similar a model_save_path pero para logs de testing.
    
    :param model: Nombre del modelo
    :param dataset: Nombre del dataset
    :return: Ruta del directorio de logs
    """
    return os.path.join("logs", "testing", model.split('/')[-1], dataset)
