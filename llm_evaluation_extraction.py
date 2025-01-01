from import_data import *
from llm_classification import processing_content
import pandas as pd
import time

def start_evaluation(comment_count, model_index):
    """
    Führt die Extraktion der schädlichen Begriffe für eine bestimmte Anzahl an Kommentaren durch.
   
    Args:
       comment_count (int): Anzahl der zu analysierenden Kommentare
       model_index (int): Index des zu verwendenden LLM
   
   Returns:
       None: Ergebnisse werden in Excel-Datei gespeichert
   """
    start_time = time.time()
    df = input_rp_phrases()

    result_df = df[['id', 'content']].head(comment_count)
    result_df["phrases"] = ""
    result_df["processing_time"] = 0

    counter = 0

    for index, row in result_df.iterrows():
        print(index)
        content = row["content"]
        print(content)
        result_processing = processing_content(content, model_index, 1)
        result_df.at[index, "phrases"] = result_processing[0]
        result_df.at[index, "processing_time"] = result_processing[1] 

        counter += 1 
        if counter % 10 == 0:
            calculation_evaluation(result_df, counter, start_time)


def calculation_evaluation(result_df, counter, start_time):
    """
    Berechnet Evaluierungsmetriken für die Extraktion der schädlichen Begriffe.
   
    Args:
       result_df (DataFrame): DataFrame mit den Extraktionsergebnissen
       counter (int): Anzahl der bisher verarbeiteten Kommentare
       start_time (float): Startzeitpunkt der Evaluierung
   
    Returns:
       None: Speichert Ergebnisse in einer xlsx Datei
    """
    result_df = result_df.head(counter)

    max_processing_time = result_df["processing_time"].max()
    min_processing_time = result_df["processing_time"].min()
    mean_processing_time = result_df["processing_time"].mean()
    total_processing_time = result_df["processing_time"].sum()


    summary = f"""
                Insgesamt wurden {counter} Kommentare geprüft.\n
                Die Ausführung hat insgesamt {round(total_processing_time, 2)} Sekunden gedauert.\n 
                Im Durchschnitt dauerte die Prüfung {round(mean_processing_time, 2)} Sekunden.\n
                Die kürzeste Prüfung dauerte {min_processing_time} Sekunden und die längste Prüfung dauerte {max_processing_time} Sekunden.\n 
                """
    print(summary)

    result_df.at[0, "summary"] = summary
    result_df.to_excel(f"results/{time.strftime('%H-%M-%S')}_extraction.xlsx", index=False)

    end_time = time.time()
    execution_time = end_time - start_time
    execution_time = round(execution_time, 2)

    print(f"Die Ausführung der Evaluation hat {execution_time} Sekunden gedauert.")

#start_evaluation(100, 1)
