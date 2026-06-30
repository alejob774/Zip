import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox

def crear_zips_en_carpeta(carpeta_base: str) -> int:
    """
    Recorre todas las subcarpetas dentro de `carpeta_base` y crea
    un .zip por cada una dentro de una carpeta nueva llamada 'zips'.
    Devuelve cuántos ZIPs se crearon.
    """
    zips_dir = os.path.join(carpeta_base, "zips")
    os.makedirs(zips_dir, exist_ok=True)

    cantidad_zips = 0

    for nombre in os.listdir(carpeta_base):
        ruta_subcarpeta = os.path.join(carpeta_base, nombre)

        # Solo consideramos directorios, y evitamos la propia carpeta 'zips'
        if os.path.isdir(ruta_subcarpeta) and nombre != "zips":
            ruta_zip = os.path.join(zips_dir, f"{nombre}.zip")

            # Creamos/reescribimos el ZIP
            with zipfile.ZipFile(ruta_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
                for raiz, _, archivos in os.walk(ruta_subcarpeta):
                    for archivo in archivos:
                        ruta_archivo = os.path.join(raiz, archivo)
                        # Guardar dentro del ZIP con ruta relativa a la subcarpeta
                        arcname = os.path.relpath(ruta_archivo, ruta_subcarpeta)
                        zipf.write(ruta_archivo, arcname)

            cantidad_zips += 1

    return cantidad_zips

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta base")
    if carpeta:
        ruta_var.set(carpeta)

def ejecutar_compresion():
    carpeta = ruta_var.get().strip()
    if not carpeta:
        messagebox.showwarning("Sin carpeta", "Por favor selecciona una carpeta primero.")
        return

    if not os.path.isdir(carpeta):
        messagebox.showerror("Error", "La ruta seleccionada no es una carpeta válida.")
        return

    try:
        cantidad = crear_zips_en_carpeta(carpeta)
        messagebox.showinfo(
            "Proceso terminado",
            f"Se crearon {cantidad} archivo(s) .zip en la carpeta 'zips'."
        )
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al crear los ZIPs:\n{e}")

if __name__ == "__main__":
    # Ventana principal
    root = tk.Tk()
    root.title("Compresor de carpetas a ZIP")

    # Texto explicativo
    descripcion = (
        "Esta aplicación crea un archivo .zip por cada subcarpeta\n"
        "dentro de la carpeta seleccionada.\n\n"
        "Los archivos .zip se guardarán en una carpeta nueva llamada\n"
        "'zips' dentro de la misma carpeta seleccionada."
    )
    lbl_descripcion = tk.Label(root, text=descripcion, justify="left")
    lbl_descripcion.pack(padx=10, pady=10)

    # Selector de carpeta
    frame_selector = tk.Frame(root)
    frame_selector.pack(padx=10, pady=5, fill="x")

    ruta_var = tk.StringVar()

    entry_ruta = tk.Entry(frame_selector, textvariable=ruta_var, width=50, state="readonly")
    entry_ruta.pack(side="left", expand=True, fill="x", padx=(0, 5))

    btn_browse = tk.Button(frame_selector, text="Seleccionar carpeta...", command=seleccionar_carpeta)
    btn_browse.pack(side="right")

    # Botón para crear los ZIPs
    btn_ejecutar = tk.Button(root, text="Crear ZIPs", command=ejecutar_compresion)
    btn_ejecutar.pack(pady=10)

    # Iniciar loop de la interfaz
    root.mainloop()