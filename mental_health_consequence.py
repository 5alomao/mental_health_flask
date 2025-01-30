# -*- coding: utf-8 -*-
"""mental_health_consequence.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Fe1BhhRxsRXVilqxu80-CGyXHNT9MdjW
"""

from sklearn.model_selection import train_test_split
#precisão
from sklearn.metrics import accuracy_score
#alg de árvore de decisão
from sklearn import tree
#manipulação de dados
import pandas as pd

import gspread
csv_url = 'https://docs.google.com/spreadsheets/d/18nu7AeQjKycz_b3PQ826PvJiaitNKRBvJ3xREcraJIg/export?format=csv&id=18nu7AeQjKycz_b3PQ826PvJiaitNKRBvJ3xREcraJIg'
df = pd.read_csv(csv_url)
# df.head()

mental_health_replace = {
  'No': 0,
  'Yes': 1,
  'Maybe': 2
}

work_interfere_replace = {
  'Often': 0,
  'Sometimes': 1,
  'Rarely': 2,
  'Never': 3,
  'NA': 4,
 }

remote_work_replace = {
  'No': 0,
  'Yes': 1,
}

family_history_replace = {
  'No': 0,
  'Yes': 1,
}

df['family_history_cod'] = df['family_history'].replace(family_history_replace)
df['work_interfere_cod'] = df['work_interfere'].replace(work_interfere_replace)
df['remote_work_cod'] = df['remote_work'].replace(remote_work_replace)
df['mental_health_cod'] = df['mental_health_consequence'].replace(mental_health_replace)

df = pd.get_dummies(df, drop_first=True)

df = df.drop(columns=['family_history_Yes','mental_health_consequence_Yes','work_interfere_Sometimes','work_interfere_Rarely', 'mental_health_consequence_No', 'work_interfere_Often', 'remote_work_Yes'])
df

X = df.drop(columns=['mental_health_cod'])
y = df['mental_health_cod']
features = X;
X = X.values
y = y.values

print(X[0])
print(y[0])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(X_train)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)

preditos = clf.predict(X_test)
print("Real:", y_test)
print("Predito:", preditos)

acuracia = accuracy_score(y_test, preditos)
print("Acurácia:", acuracia)

def input_data():
    try:
        # Using __builtins__.input to access the original input function
        age = float(__builtins__.input("Digite a idade: "))  # Idade deve ser float
        print("[0] - Não\n[1] - Sim")
        family_history = int(__builtins__.input("Possui histórico familiar? "))  # Deve ser int
        print("[0] - Muitas vezes\n[1] - Às vezes\n[2] - Raramente\n[3] - Nunca\n[4] - NA")
        work_interfere = int(__builtins__.input("Interfere na vida profissional? "))  # Deve ser int
        print("[0] - Não\n[1] - Sim")
        remote_work = int(__builtins__.input("Trabalha de forma remota? "))  # Deve ser int
        return [[age, family_history, work_interfere, remote_work]]
    except ValueError:
        print("Valor inválido, tente novamente.")
        return None

# Lista de possíveis previsões
list_mental_health = ['Não', 'Sim', 'Talvez']

# Capturar entrada do usuário
user_input = input_data()

# Se a entrada for válida, fazer a previsão
if user_input is not None:
    predito = clf.predict(user_input)  # Passando a entrada como lista dentro de outra lista
    print("O indivíduo pode sofrer consequências na saúde mental no ambiente de trabalho:", list_mental_health[predito[0]])

import pickle
pickle.dump(clf, open('model.pkl', 'wb'))

# Salvar a lista de saídas (nomes das classes) em um arquivo names.pkl
pickle.dump(list_mental_health, open('names.pkl', 'wb'))