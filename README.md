# Moderationsassistent
Der Moderationsassistent ist ein Prototyp, der im Rahmen einer Masterarbeit entwickelt wurde. Er verwendet das Large Language Model Llama-3.1-8B-Instruct und umfasst die folgenden Funktionen:

- Automatische Klassifizierung von Beiträgen in verschiedene Kategorien (Normal, Beleidigung, Rassismus, Sexismus, religiöser Hass, Werbung)
- Extraktion problematischer Textpassagen aus als schädlich eingestuften Beiträgen
# Installation
1. Klone das Repository  
```bash
git clone https://github.com/mundba/Moderationsassistent.git
```
2. Installiere die requirements.txt
```bash
pip install -r requirements.txt
```
3. Lade ein oder mehrere LLMs herunter  
**Meta-Llama-3.1-8B-Instruct-Q6_K.gguf:** https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main  
**Meta-Llama-3-8B-Instruct-abliterated-v3_q6.gguf:** https://huggingface.co/failspy/Meta-Llama-3-8B-Instruct-abliterated-v3-GGUF/tree/main

Hinweis: Der Name des heruntergeladenen LLMs muss mit dem in der `llm_classification.py` übereinstimmen 

4. Lade einen oder mehrere Datensätze herunter  
**RP-Crowd-1.csv:** https://github.com/Dennis1989/RP-Mod-RP-Crowd/tree/main/Dataset/Text-Data  
**gahd.csv:** https://github.com/jagol/gahd  
**GermEval21_TrainData.csv:** https://github.com/germeval2021toxic/SharedTask/tree/main/Data%20Sets  

Hinweis: Der Name des heruntergeladenen Datensatzes muss mit dem in der `import_data.py` übereinstimmen 

# Anwendung  
Die `llm_classification.py` stellt die Main Klasse dieses Projekts dar.  
Durch die Ausführung von `processing_content(content, select_model_index, select_prompt_index)` wird entweder ein Kommentar klassifiziert oder die schädlichen Begriffe extrahiert.  

Setze `select_model_index` auf 0 für das LLM Meta-Llama-3.1-8B-Instruct-Q6_K.gguf  
Setze `select_model_index` auf 1 für das LLM Meta-Llama-3-8B-Instruct-abliterated-v3_q6.gguf  
Setze `select_prompt_index` auf 0 für den Prompt der die Kommentare klassifiziert  
Setze `select_prompt_index` auf 0 für den Prompt der die schädlichen Begriffe aus dem Kommentar extrahiert  

Zur Ausführung der Evaluation mit der Klasse `llm_evaluation_classification.py` muss in der Methode `start_evaluation_identification(comments_per_category, model_index)` die Variable `df` auf den jeweiligen Datensatz, der eingelesen werden soll, geändert werden. Im Code wird derzeit der GAHD Datensatz eingelsen, `df = gahd()`

# Lizenz
MIT License

Copyright (c) 2025 mundba

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
# Autor
mundba
