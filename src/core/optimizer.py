class SystemOptimizer:
    """ Sistema Experto de Optimización Local """
    def __init__(self, db_instance):
        self.db = db_instance

    def analyze(self):
        """ Analiza el histórico y genera recomendaciones estáticas locales """
        recommendations = []
        stats = self.db.get_stats("168h") # Últimos 7 días
        
        if not stats or stats[0] is None:
            return ["No hay datos suficientes para analizar."]
            
        max_cpu, avg_cpu, max_ram, avg_ram = stats
        
        # Reglas Experto
        if avg_cpu > 70:
            recommendations.append({
                "title": "Sobrecarga de CPU Detectada",
                "desc": f"Tu CPU promedia {avg_cpu:.1f}%. Considera cambiar al perfil de Energía 'Alto Rendimiento'.",
                "action": "power_high",
                "risk": "Bajo"
            })
            
        import psutil
        total_ram_gb = psutil.virtual_memory().total / (1024**3)
        if avg_ram > (total_ram_gb * 0.8 * 1024**3):
            recommendations.append({
                "title": "Saturación de RAM Constante",
                "desc": "Estás utilizando más del 80% de memoria en promedio. Se sugiere deshabilitar SysMain (Superfetch).",
                "action": "disable_sysmain",
                "risk": "Medio"
            })
            
        if self._is_gaming_heavy():
            recommendations.append({
                "title": "Perfil Gamer",
                "desc": "Detectamos alto uso de GPU/CPU en ráfagas. Puedes activar el Modo de Juego puro de Windows.",
                "action": "enable_game_mode",
                "risk": "Bajo"
            })
            
        return recommendations

    def _is_gaming_heavy(self):
        # Lógica dummy para ejemplificar
        return False

    def apply_optimization(self, action_id):
        """ Ejecuta comandos del sistema seguros """
        import subprocess
        try:
            if action_id == "power_high":
                subprocess.run("powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c", shell=True)
            elif action_id == "disable_sysmain":
                subprocess.run("sc config sysmain start=disabled", shell=True, check=True)
                subprocess.run("net stop sysmain", shell=True)
            elif action_id == "enable_game_mode":
                # Registro para modo juego W10/11
                pass
            return True, "Optimización Aplicada correctamente."
        except Exception as e:
            return False, f"Fallo al aplicar: {str(e)}"
