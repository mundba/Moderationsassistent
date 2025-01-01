from import_data import *
from llm_classification import processing_content
import pandas as pd
import time


def start_evaluation_identification(comments_per_category, model_index):
    """ 
   Führt die Evaluierung durch, indem eine bestimmte Anzahl von Kommentaren klassifiziert wird.
   
   Args:
       comments_per_category (int): Anzahl der Kommentare pro Kategorie (schädlich/nicht schädlich)
       model_index (int): Index des zu verwendenden Modells
       
   Returns:
       None: Ergebnisse werden an die calculation_evaluation() Funktion weitergeleitet
   """
    
    start_time = time.time()
    df = gahd()

    number_toxic_comments = comments_per_category
    number_non_toxic_comments = comments_per_category
    number_comments = number_toxic_comments + number_non_toxic_comments

    label_1_df = df[df["label"] == 1.0].head(number_toxic_comments)
    label_0_df = df[df["label"] == 0.0].head(number_non_toxic_comments)

    result_df = pd.DataFrame()
    for i in range(len(label_1_df)):
        result_df = pd.concat([result_df, label_1_df.iloc[[i]], label_0_df.iloc[[i]]], ignore_index=True)

    result_df["category"] = ""
    result_df["processing_time"] = 0


    for index, row in result_df.iterrows():
        print(index)
        content = row["content"]
        print(content)
        result_processing = processing_content(content, model_index, 0) 
        result_df.at[index, "category"] = result_processing[0]
        result_df.at[index, "processing_time"] = result_processing[1]
        
    print("------------------Ende der Klassifizierung-----------------")
    calculation_evaluation(result_df, number_comments, start_time)

def calculation_evaluation(result_df, number_comments, start_time):
    """
   Berechnet Evaluierungsmetriken für die Klassifizierung.
   
   Args:
       result_df (DataFrame): DataFrame mit den Klassifizierungsergebnissen
       number_comments (int): Gesamtanzahl der klassifizierten Kommentare 
       start_time (float): Startzeitpunkt der Evaluierung
       
   Returns:
       None: Speichert die Ergebnisse als Excel Datei
   """
    
    number_toxic_comments = number_comments/2
    number_non_toxic_comments = number_comments/2
    
    max_processing_time = result_df["processing_time"].max()
    min_processing_time = result_df["processing_time"].min()
    mean_processing_time = result_df["processing_time"].mean()
    total_processing_time = result_df["processing_time"].sum()

    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for index, row in result_df.iterrows():
        if row["label"] == 0 and row["category"].strip().lower() == "normal":
            TN += 1 
        if row["label"] == 0 and row["category"].strip().lower() != "normal":
            FP += 1 
        if row["label"] == 1 and row["category"].strip().lower() == "normal":
            FN += 1
        if row["label"] == 1 and row["category"].strip().lower() != "normal":
            TP += 1
    
    precision =  TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (TP + TN) / (TP + TN + FP + FN)

    summary = f"""
                Insgesamt wurden {number_comments} Kommentare klassifiziert.\n
                Die Ausführung hat insgesamt {round(total_processing_time, 2)} Sekunden gedauert.\n 
                Im Durchschnitt dauerte die Klassifizierung {round(mean_processing_time, 2)} Sekunden.\n
                Die kürzeste Klassifizierung dauerte {min_processing_time} Sekunden und die längste Klassifizierung dauerte {max_processing_time} Sekunden.\n 
                {TP} von {int(number_toxic_comments)} schädliche Kommentare wurden tatsächlich vom System als schädlich erkannt.\n
                {TN} von {int(number_non_toxic_comments)} normalen Kommentare wurden tatsächlich als nicht schädlich erkannt.\n
                {FP} normale Kommentare wurden fälschlich als schädlich eingestuft.\n
                {FN} schädliche Kommentare wurden fälschlich als nicht schädlich eingestuft.\n
                Precision: Von allen als schädliche identifizierten Kommentaren waren {round(precision * 100, 2)}% wirklich schädlich.\n
                Recall: Von allen schädlichen Kommentaren wurden {round(recall * 100, 2)}% erkannt.\n
                F1-Score: Wenn etwas als schädlich markiert wurde ist das zu {round(f1_score * 100, 2)}% richtig.\n
                Accuracy: {round(accuracy * 100, 2)}% der Klassifikationen waren korrekt.\n
                """
    print(summary)

    result_df.at[0, "summary"] = summary
    result_df.to_excel(f"results/{time.strftime('%H-%M-%S')}_classified.xlsx", index=False)

    end_time = time.time()
    execution_time = end_time - start_time
    execution_time = round(execution_time, 2)

    print(f"Die Ausführung der Evaluation hat {execution_time} Sekunden gedauert.")

#start_evaluation_identification(5, 0)


 
