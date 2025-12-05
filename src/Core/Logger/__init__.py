import threading
import queue
from datetime import datetime


from .enum import COLORS as ANSI


class Logger:
    """Singleton logger with separate thread"""

    _instance = None
    _lock = threading.Lock()

    COLORS: dict[str, str] = ANSI

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.queue = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self._log_worker, daemon=True)
        self.thread.start()

    def _log_worker(self):
        """Worker que procesa logs en un thread separado"""
        while self.running:
            try:
                log_item = self.queue.get(timeout=0.1)
                if log_item is None:
                    break

                level, message, color = log_item
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                formatted = (
                    f"{self.COLORS['GRAY']}[{timestamp}]{self.COLORS['RESET']} "
                    f"{color}[{level}]{self.COLORS['RESET']} {message}"
                )

                print(formatted)
                self.queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error en logger: {e}")

    @staticmethod
    def log(message):
        instance = Logger()
        instance.queue.put(("LOG", message, instance.COLORS["WHITE"]))

    @staticmethod
    def info(message):
        instance = Logger()
        instance.queue.put(("INFO", message, instance.COLORS["BLUE"]))

    @staticmethod
    def success(message):
        instance = Logger()
        instance.queue.put(("SUCCESS", message, instance.COLORS["GREEN"]))

    @staticmethod
    def warning(message):
        instance = Logger()
        instance.queue.put(("WARNING", message, instance.COLORS["YELLOW"]))

    @staticmethod
    def error(message):
        instance = Logger()
        instance.queue.put(("ERROR", message, instance.COLORS["RED"]))

    @staticmethod
    def start(message):
        instance = Logger()
        instance.queue.put(("START", message, instance.COLORS["GREEN"]))

    @staticmethod
    def shutdown():
        instance = Logger()
        instance.queue.put(None)
        instance.running = False
        instance.thread.join(timeout=2)
