import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk
from pandastable import Table

# Parámetros
num_replicas = 50
dias_simulacion = 25
media_produccion = 30
desviacion_produccion = 5
demanda_diaria = 15
stock_inicial = 12

resultados_replicas = []
primer_repl_data = []

for replica in range(num_replicas):
    aleatorios = np.random.rand(dias_simulacion)
    produccion_diaria = np.round(stats.norm.ppf(aleatorios, loc=media_produccion, scale=desviacion_produccion)).astype(int)

    stock_actual = stock_inicial
    no_abastece = 0
    datos_replica = []

    for dia in range(dias_simulacion):
        if dia == 4:
            stock_actual = stock_actual + 10 + produccion_diaria[dia] - demanda_diaria
        else:
            stock_actual = stock_actual + produccion_diaria[dia] - demanda_diaria

        if stock_actual < 0:
            stock_actual = 0
            no_abastece += 1

        datos_replica.append([
            dia + 1,
            round(aleatorios[dia], 5),  # Redondear aleatorio a 5 decimales
            int(produccion_diaria[dia]),
            int(stock_actual),
            1 if stock_actual == 0 else 0
        ])

    resultados_replicas.append(no_abastece)

    if replica == 0:
        primer_repl_data = datos_replica

# DataFrame con resultados de las réplicas
df_resultados = pd.DataFrame({
    "Réplica": np.arange(1, num_replicas + 1),
    "Días sin abastecimiento": resultados_replicas
})
# Convertir la columna "Réplica" a cadena con formato entero para su visualización
df_resultados["Réplica"] = df_resultados["Réplica"].apply(lambda x: f"{x:d}")

promedio_dias_sin_abastecimiento = np.mean(resultados_replicas)

# DataFrame con datos de la primera réplica
df_primera_replica = pd.DataFrame(primer_repl_data, columns=[
    "Día", "Aleatorio", "Producción", "Stock Final", "¿No se Abastece?"
])
# Formatear "Aleatorio" para mostrar hasta 5 decimales
df_primera_replica["Aleatorio"] = df_primera_replica["Aleatorio"].apply(lambda x: f"{x:.5f}")

# ----------- Gráfico de evolución de la primera réplica -----------
plt.figure(figsize=(10, 5))
sns.lineplot(x=df_primera_replica["Día"], y=df_primera_replica["Stock Final"], marker="o", label="Stock Final")
sns.lineplot(x=df_primera_replica["Día"], y=df_primera_replica["Producción"], marker="o", label="Producción Diaria")
plt.axhline(y=demanda_diaria, color='r', linestyle='--', label="Demanda Fija (15)")
plt.xlabel("Día")
plt.ylabel("Cantidad")
plt.title("Evolución del Stock y Producción en la Primera Réplica")
plt.legend()
plt.tight_layout()
plt.show()

# ----------- Interfaz gráfica (GUI) con tkinter y pandastable -----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resultados de la Simulación")
        self.geometry("900x500")

        tab_control = ttk.Notebook(self)
        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab1, text="50 Réplicas")
        tab_control.add(tab2, text="1° Réplica Detalle")
        tab_control.pack(expand=1, fill="both")

        # Tabla de réplicas
        self.table1 = Table(tab1, dataframe=df_resultados, showtoolbar=True, showstatusbar=True)
        self.table1.show()

        # Tabla de la primera réplica
        self.table2 = Table(tab2, dataframe=df_primera_replica, showtoolbar=True, showstatusbar=True)
        self.table2.show()

if __name__ == "__main__":
    print(f"Promedio de días sin abastecimiento: {promedio_dias_sin_abastecimiento:.2f}")
    app = App()
    app.mainloop()
