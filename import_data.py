import pandas as pd
import json

# Diese Klasse enthält alle Funktionen zum Einlesen verschiedener Datensätze für die Analyse von Beiträgen und Kommentaren

def input_comments_export2():
    
    with open("comments_export2.json", "r") as f:
        data = json.load(f)

    df = pd.DataFrame(columns=["id", "content"])

    for i in data.keys():

        row = pd.DataFrame({"id": [i], "content": [data[i]["text"]]})
        df = pd.concat([df, row], axis=0, ignore_index=True)
    

    return df


def input_comments_export1():

    with open("comments_export_all.json", "r") as f:
        data = json.load(f)

    df = pd.DataFrame(columns=["id", "content"])

    for i in data:

        if i == None:
            continue

        id = (list(i.keys()))[0]
        content =  i[id]["text"]


        if content is None:
            content = ""

        row = pd.DataFrame({"id": [id], "content": [content]})
        df = pd.concat([df, row], axis=0, ignore_index=True)
    
    return df


def input_RP_Crowd_1():

    df = pd.read_csv("RP-Crowd-1.csv")
    df.rename(columns={"text": "content"}, inplace=True)

    return df

def input_rp_sexism():

    df = pd.read_csv("rp-sexism.csv")
    df.rename(columns={"Sexism Count Crowd": "label"}, inplace=True)
    return df


def input_rp_racism():

    df = pd.read_csv("rp-racism.csv")
    df.rename(columns={"Racism Count Crowd": "label"}, inplace=True)
    return df


def input_rp_insult():

    df = pd.read_csv("rp-insult.csv")
    df.rename(columns={"Insult Count Crowd": "label"}, inplace=True)
    return df


def input_rp_advertisement():

    df = pd.read_csv("rp-advertisement.csv")
    df.rename(columns={"Advertisement Count Crowd": "label"}, inplace=True)
    return df

def input_rp_threat():

    df = pd.read_csv("rp-threat.csv", delimiter=";")
    df.rename(columns={"Threat Count Crowd": "label"}, inplace=True)
    return df

def input_rp_religion():

    df = pd.read_csv("rp religion.CSV", delimiter=";", encoding='latin1')
    return df

def input_rp_phrases():

    df = pd.read_csv("rp-phrases.csv")
    
    return df

def gahd():

    df = pd.read_csv("gahd.csv")
    df.rename(columns={"text": "content"}, inplace=True)
    df.rename(columns={"ghd_id": "id"}, inplace=True)
    df.drop(columns=["round", "split", "contrastive_gahd_id"], inplace=True)

    return df


def GermEval21():

    df = pd.read_csv("GermEval21_TrainData.csv")
    df.rename(columns={"comment_text": "content"}, inplace=True)
    df.rename(columns={"comment_id": "id"}, inplace=True)
    df.rename(columns={"Sub1_Toxic": "label"}, inplace=True)
    df.drop(columns=["Sub2_Engaging", "Sub3_FactClaiming"], inplace=True)
    df['content'] = df['content'].replace(r'@\S+', '', regex=True).str.strip()
    return df


