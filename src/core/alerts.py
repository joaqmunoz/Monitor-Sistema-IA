import os
import smtplib
from email.message import EmailMessage
import psutil
from PySide6.QtWidgets import QMessageBox

class AlertEngine:
    """ Motor de evaluación de reglas offline """
    def __init__(self, config=None):
        self.config = config or {
            'alerts': [
                {
                    'name': 'CPU Overload',
                    'condition': 'metrics.get("cpu").get("percent") > 90',
                    'action': 'notify',
                    'message': '¡Uso de CPU crítico!',
                    'enabled': True
                }
            ]
        }
        self.history = {}

    def check_rules(self, current_metrics):
        """ Evaluacion segura usando eval con diccionario restringido """
        context = {"metrics": current_metrics}
        for rule in self.config.get('alerts', []):
            if not rule.get('enabled', False):
                continue
            
            try:
                # Se utiliza eval limitando el scope al diccionario metrics
                if eval(rule['condition'], {"__builtins__": {}}, context):
                    self.trigger_alert(rule)
            except Exception as e:
                print(f"Error parseando regla {rule['name']}: {e}")

    def trigger_alert(self, rule):
        action = rule.get('action')
        name = rule['name']
        
        # Rate Limiting: No repetir la misma alerta más de una vez por minuto
        import time
        last_triggered = self.history.get(name, 0)
        if time.time() - last_triggered < 60:
            return
            
        self.history[name] = time.time()
        
        msg = rule.get('message', f'Alerta: {name}')
        print(f"⚠️ DISPARANDO ALERTA: {msg} (Acción: {action})")
        
        if action == 'notify':
            self.show_notification(msg)
        elif action == 'kill_process':
            proc_name = rule.get('process_name', '')
            self.kill_process_by_name(proc_name)
        elif action == 'run_program':
            os.system(f"start {rule.get('path', '')}")

    def show_notification(self, message):
        """ Native Windows Notification """
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast("Monitor de Sistema", message, duration=5, threaded=True)
        except ImportError:
            # Fallback en caso de no tener win10toast
            print(f"NOTIFICACIÓN: {message}")

    def kill_process_by_name(self, name):
        """ Elimina procesos problemáticos """
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() == name.lower():
                    proc.kill()
                    print(f"✅ Proceso {name} eliminado por alerta")
            except:
                pass
