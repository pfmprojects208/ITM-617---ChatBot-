from pypdf import PdfReader

def extraer_primeras_palabras(ruta_pdf, limite_palabras=500):
    try:
        # 1. Cargar el archivo PDF
        reader = PdfReader(ruta_pdf)
        texto_completo = ""
        
        print(f"--- Analizando: {ruta_pdf} ---")
        print(f"Total de páginas: {len(reader.pages)}")

        # 2. Recorrer las páginas y extraer texto
        for i, pagina in enumerate(reader.pages):
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + " "
            
            # Si ya tenemos suficientes palabras, paramos de leer páginas
            if len(texto_completo.split()) >= limite_palabras:
                break

        # 3. Procesar las palabras
        palabras = texto_completo.split()
        resultado = " ".join(palabras[:limite_palabras])
        
        print(f"--- Primeras {len(palabras[:limite_palabras])} palabras extraídas ---\n")
        print(resultado)
        print("\n--- Fin de la extracción ---")

    except Exception as e:
        print(f"Error al leer el PDF: {e}")

if __name__ == "__main__":
    # IMPORTANTE: Cambia 'prueba.pdf' por el nombre de un PDF que tengas en la misma carpeta
    archivo_de_prueba = "Unknown.pdf" 
    extraer_primeras_palabras(archivo_de_prueba)