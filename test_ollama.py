from langchain_ollama import OllamaLLM

# Configuramos el modelo (aquí es donde cambiarás la línea el último día)
model = OllamaLLM(model="llama3.1")

print("--- Iniciando consulta a Ollama ---")
pregunta = "Cuentame un chiste"
respuesta = model.invoke(pregunta)

print(f"\nRespuesta de la IA:\n{respuesta}")