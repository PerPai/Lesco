import pyttsx3

def speaker(text):
    engine = pyttsx3.init()
    engine.setProperty('lang', 'es')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) # Selecciona la voz española
    engine.setProperty('rate', 150) # Aumenta la velocidad
    engine.setProperty('pitch', 50) # Aumenta el tono
    engine.say(text)
    engine.runAndWait()

