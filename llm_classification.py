from llama_cpp import Llama
import time


def select_prompt(selected_prompt, content):
    """
    Wählt einen vordefinierten Prompt für die Klassifizierung aus.
   
    Args:
       selected_prompt (int): Index des ausgewählten Prompts
       content (str): Der zu analysierende Kommentar
       
    Returns:
       str: Der mit dem Kommentar gefüllte Prompt
   """
    prompt_list = [
        f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>

        Du bist ein Moderationsassistent auf einer digitalen Bürgerbeteiligungsplatform.
        Deine Aufgabe ist es Hate-Speech in den Kommentaren zu erkennen und zu Klassifizieren. Verwende eine der folgenden vordefinierten Kategorien zur Einordnung:

        Beleidigungen
        Rassismus
        Sexismus
        Extremismus
        Religiöser Hass
        Werbung

        Falls der Kommentar kein Hate-Speech enthält Klassifiziere ihn als:
        Normal

        Du darfst ausschließlich nur mit den ermittelten Kategorie antworten. Verwende nicht "Kategorie:" in deiner Antwort. Gebe keine weiteren Erklärungen oder Anmerkungen zu deiner Antwort.

        ####
        Hier sind ein paar Beispiele:
        ---
        Kommentar: "Du bist ein kompletter Vollidiot und hast keine Ahnung von dem, was du redest! Halt endlich die Klappe!"
        Kategorie: Beleidigung
        ---
        Kommentar: "Ich würde mir wünschen und dass alle Türken in ihr Heimatland gehen."
        Kategorie: Rassismus
        ---
        Kommentar: "Frauen wie du gehören nicht an den Verhandlungstisch, sondern in die Küche!"
        Kategorie: Sexismus
        ---
        Kommentar: "Wir sollten alle nicht-westlichen Länder bombardieren, um die Welt zu 'befreien'!"
        Kategorie: Extremismus
        ---
        Kommentar: "Der Koran ist ein Buch des Teufels und alle Moslems sind von Satan besessen!"
        Kategorie: Religiöser Hass
        ---
        Kommentar: "Tolle Initiative! Bin gespannt auf die Website: https://www.besuch-mich.de/"
        Kategorie: Werbung
        ---
        ####
        <|eot_id|><|start_header_id|>user<|end_header_id|>

        Kommentar: "{content}"

        <|eot_id|><|start_header_id|>assistant<|end_header_id|> 
        """,
        f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        Du bist ein Moderationsassistent auf einer digitalen Bürgerbeteiligungsplatform. Deine Aufgabe ist es Hate Speech und toxische Ausdrücke in Kommentaren zu identifizieren.
        
        Identifiziere:
        1. Aggressive, Diskriminierende Aussagen bezüglich:
        - Herkunft
        - Religion
        - Geschlecht
        - Sexueller Orientierung
        - politischer Einstellung
        - sozialer Status
        2. Beleidigungen und Herabwürdigungen
        3. Extremistische oder radikale Äußerungen 

        Antwortformat:
        - Gib ausschließlich die identifizierten Wörter zurück
        - Trenne mehrere Wörer mit einem Komma
        - Behalte die originale Schreibweise bei
        - Keine zusätzlichen Erklärungen oder Kennzeichnungen
        
        ####
        Beispiele:
        ---
        Input: "Du bist ein kompletter Vollidiot und hast keine Ahnung von dem, was du redest! Halt endlich die Klappe"
        Output: Vollidiot, Halt, endlich, die, Klappe
        ---
        Input: "Wir brauchen keine Ausländer in unserem Land"
        Output: Ausländer
        ---
        Input: "Frauen wie du gehören nicht an den Verhandlungstisch, sondern in die Küche!"
        Output: in, die, Küche
        ---
        Input: "Wir sollten alle nicht-westlichen Länder bombardieren, um die Welt zu 'befreien'!"
        Output: bombardieren, Welt, zu, befreien
        ---
        Input: "Der Koran ist ein Buch des Teufels und alle Moslems sind von Satan besessen!"
        Output: Buch, des, Teufels, von, Satan, besessen
        ---
        ####
        <|eot_id|><|start_header_id|>user<|end_header_id|>

        Kommentar: "{content}"

        <|eot_id|><|start_header_id|>assistant<|end_header_id|> 
        """
    ]
    return prompt_list[selected_prompt]

def select_model(selected_model):
    """
    Wählt ein vorhandenes LLM aus.
   
    Args:
       selected_model (int): Index des ausgewählten Modells
       
    Returns:
       str: Der Dateiname des ausgewählten Modells
   """
    model_list = [
        "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf", # 0
        "Meta-Llama-3-8B-Instruct-abliterated-v3_q6.gguf" #1
    ]
    return model_list[selected_model]


def processing_content(content, select_model_index, select_prompt_index):
    """
    Verarbeitet einen Kommentar mit dem ausgewählten Modell und Prompt.
    
    Args:
        content (str): Der zu analysierende Kommentar
        select_model_index (int): Index des zu verwendenden Modells
        select_prompt_index (int): Index des zu verwendenden Prompts
        
    Returns:
        tuple: (Klassifizierungsergebnis, Verarbeitungszeit in Sekunden)
    """
    start_time = time.time()

    model_path = select_model(select_model_index)
    prompt = select_prompt(select_prompt_index, content)

    llm = Llama(
        model_path = model_path,
        n_gpu_layers = -1, # Ändere auf 1, falls die Hardwarebeschleunigung im System akitviert ist
        n_ctx = 4096 # Maximale Anzahl an Tokens die ein Modell einlesen kann
        
    )

    output = llm(
        prompt,
        max_tokens = 64, # Maximale Länge der Antwort des Modells
        echo = False # Verhindert, dass der Prompt nochmal in der Antwort wiedergegeben wird
        
    )

    result = output["choices"][0]["text"] # Extrahiere die Antwort
    print(result)
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time = round(execution_time, 2)
    print(f"Die Ausführung hat {execution_time} Sekunden gedauert.")
    print(f"Verwendetes Modell: {model_path}")

    return result, execution_time
