import os
import csv
import pandas as pd
from datetime import datetime
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:
    pass

class DataExporter:
    """ Exportador de métricas a varios formatos """
    
    @staticmethod
    def export_csv(db_instance, filepath):
        try:
            # Opción 1: CSV nativo (Optimizado)
            db_instance._flush_buffer()
            db_instance.cursor.execute("SELECT * FROM metrics_snapshot")
            columns = [desc[0] for desc in db_instance.cursor.description]
            rows = db_instance.cursor.fetchall()
            
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)
                
            # Opción 2: Usar pandas si se requiere procesar/limpiar extra
            # df = pd.DataFrame(rows, columns=columns)
            # df.to_csv(filepath + "_pandas.csv", index=False)
            return True
        except Exception as e:
            print(f"Error Exportando CSV: {e}")
            return False

    @staticmethod
    def export_html(db_instance, filepath):
        try:
            db_instance._flush_buffer()
            db_instance.cursor.execute("SELECT timestamp, cpu_avg, ram_used FROM metrics_snapshot ORDER BY id DESC LIMIT 100")
            rows = db_instance.cursor.fetchall()
            
            html = f"""
            <html>
            <head>
                <title>Reporte Monitor Clay</title>
                <style>
                    body {{ font-family: sans-serif; background: #E2E2EC; padding: 20px; }}
                    div.card {{ background: white; border-radius: 20px; padding: 20px; max-width: 800px; margin: auto; }}
                    table {{ width: 100%; border-collapse: collapse; }}
                    th, td {{ border-bottom: 1px solid #ddd; padding: 10px; text-align: left; }}
                </style>
            </head>
            <body>
            <div class="card">
                <h2>Reporte de Sistema: {datetime.now().strftime("%Y-%m-%d %H:%M")}</h2>
                <table>
                    <tr><th>Timestamp</th><th>CPU %</th><th>RAM (Bytes)</th></tr>
            """
            for r in rows:
                html += f"<tr><td>{r[0]}</td><td>{r[1]:.2f}</td><td>{r[2]}</td></tr>\n"
                
            html += """
                </table>
            </div>
            </body>
            </html>
            """
            with open(filepath, 'w') as f:
                f.write(html)
            return True
        except Exception as e:
            return False

    @staticmethod
    def export_pdf(db_instance, filepath):
        try:
            c = canvas.Canvas(filepath, pagesize=letter)
            c.setFont("Helvetica", 14)
            c.drawString(50, 750, "RESUMEN EJECUTIVO: Monitor de Sistema Local")
            
            stats = db_instance.get_stats("24h")
            if stats and stats[0]:
                c.setFont("Helvetica", 10)
                c.drawString(50, 700, f"Max CPU % (24h): {stats[0]:.2f}%")
                c.drawString(50, 680, f"Avg CPU % (24h): {stats[1]:.2f}%")
                max_ram = stats[2] / (1024**3)
                avg_ram = stats[3] / (1024**3)
                c.drawString(50, 660, f"Max RAM   (24h): {max_ram:.2f} GB")
                c.drawString(50, 640, f"Avg RAM   (24h): {avg_ram:.2f} GB")
            
            c.save()
            return True
        except Exception as e:
            print(f"Reportlab PDF Error: {e}")
            return False
