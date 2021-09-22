"""Dieses Modul beinhaltet einige Funktionen zur Erstellung von Diagrammen.
Dieses wird für das beiliegende Skript zur Datenanalyse benötigt und sorgt mit Kapselung dafür, dass der
eigentliche Prozess der Analyse im Vordergrund steht"""
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.patches as mpatches
import joblib


def heatmap(datensätze, Größe, Datensatz_namen):
    """ Plottet jeweils eine Heatmap/ Korrelationsmatrix des Datensatzes
    Argumente
        datensätze: Liste der Datensätze aus denen eine Korrelationsmatrix erstellt werden soll
        Größe (Tupel): Größe der auszuwerfenden Heatmap
        Datensatz_namen (lst): Liste der Datensatz Namen zur späteren Benennung (als str())
    Output
        heatmaps: werden in aktuellem Arbeitsverzeichnis (working directory) gespeichert"""
    datensatz_string = Datensatz_namen
    for datensatz, i in zip(datensätze, datensatz_string):
        file_name = "heatmap_" + i + ".svg"
        header_name = "Korrelationsmatrix_" + i
        mask = np.zeros_like(datensatz.corr())
        mask[np.triu_indices_from(mask)] = True
        with sns.axes_style("white"):
            f, ax = plt.subplots(figsize=Größe)
            ax = sns.heatmap(
                datensatz.corr(),
                mask=mask,
                annot=True,
                vmax=1,
                square=True).set_title(
                header_name,
                fontsize=30)
        f.savefig(file_name, bbox_inches='tight', format='svg')


def Kuchendiagramm(Daten, Größe, Farbe1, Farbe2, Labels,
                   angle, titel, name, kontur, Position):
    """ Funktion zum Erstellen eines Kuchendiagramms und automatischer Ablage
    Argumente
        Daten: Liste der Achsen (x, y Daten)
        Größe (Tupel): Größe des Diagramms
        Farbe 1: Farbe der Flächen (cmap kompatibel)
        Farbe 2: Farbe der hervorzuhebenden Fläche (falls vorhanden)
        Labels (Liste): Beschriftungen
        angle: Winkel des Diagramms
        titel: Titel des Diagramms
        name (.svg): Dateiname des Diagramms
        kontur (tupel): Wie sehr Fläche hervorgehoben werden soll (0, falls nicht)
        Position (int): Position der Fläche die hervorgehoben werden soll
    Output
        Kuchendiagramm
    """
    fig, ax = plt.subplots(figsize=Größe)
    cmap = plt.get_cmap(Farbe1)
    colors = list(cmap(np.linspace(0.45, 0.85, len(Daten))))
    # hervorzuhebende Farbe
    colors[Position] = Farbe2
    # Kuchendiagramm
    patches, texts, pcts = ax.pie(
        Daten, labels=Labels, autopct='%.1f%%',
        wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},
        textprops={'size': 'x-large'},
        startangle=angle,
        colors=colors,
        # Teile highlighten.
        explode=kontur)

    for i, patch in enumerate(patches):
        texts[i].set_color(patch.get_facecolor())
    plt.setp(pcts, color='white')
    plt.setp(texts, fontweight=600)
    ax.set_title(titel, fontsize=18)
    plt.tight_layout()
    fig.savefig(name, bbox_inches='tight', format='svg')


def Balkendiagramm(Farbe1, Farbe2, column_names1, column_names2,
                   dataframe, Größe, Anzahl_ticks, Werte1, Werte2,
                   titel, x_label, y_label, Legende, name):
    """ Funktion zum Erstellen eines spezifischen Balkendiagramms, das im Arbeitsverzeichnis
    gespeichert wird

    Argumente
        Farbe1 (str): Farbe des ersten Balkens
        Farbe2 (str): Farbe des zweiten Balkens
        column_names1 (Liste): Spaltennamen, die gemappt werden sollen
        column_names2 (Liste): Spaltennamen, die dargestellt werden sollen
        dataframe: Datensatz
        Größe (Tupel): Größe des Diagramms
        Anzahl_ticks (int): Anzahl der Ticks
        Werte1 (Liste): Liste der ersten darzustellenden Einheiten
        Werte2 (Liste): Liste der zweiten darzustellenden Einheiten
        titel (str): Titel
        x_label (str): Bezeichnung der x-Achse
        y_label (str): Bezeichnung der y-Achse
        Legende (Liste mit str): Legende des Diagramms
        name (.svg): Name zur Bezeichnung der abzuspeichernden Datei
    Output
        Balkendiagramm
        """
    col_list = list(dataframe.columns.values)
    colors = []
    for i in range((Anzahl_ticks - 1)):
        if 'sachbezogen' in column_names1[i]:
            colors.append(Farbe1)
        elif 'sachfremd' in column_names1[i]:
            colors.append(Farbe1)
    # Dictionary für Farben - Spalten - Mapping
    d2cb = dict(zip(col_list[:15], colors))

    colors = []
    for i in range((Anzahl_ticks - 1)):
        if 'sachbezogen' in column_names1[i]:
            colors.append(Farbe2)
        elif 'sachfremd' in column_names1[i]:
            colors.append(Farbe2)
    # Dictionary für Farben - Spalten - Mapping
    d2cd = dict(zip(col_list[:15], colors))

    x = np.arange(Anzahl_ticks)
    figure = plt.figure(figsize=Größe)
    ax = plt.subplot(111)
    ax.bar(x, Werte1, color=[d2cd.get(x, Farbe2)
           for x in col_list], width=0.4, edgecolor="k")
    ax.bar(x + 0.4, Werte2, color=[d2cb.get(x, Farbe1)
           for x in col_list], width=0.4, edgecolor="k")
    plt.xticks(x, column_names2)
    plt.title(titel, fontsize=30)
    plt.xlabel(x_label, fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    plt.legend(Legende, fontsize=20)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax.set_axisbelow(True)
    plt.show()
    figure.savefig(name, bbox_inches='tight', format='svg')


def descr_stat(dataset_list):
    """ Funktion für das Ausgeben deskriptiver Statistik
    Argumente:
        dataset_list (lst): Benötigt eine Liste der zu beschreibenden Datensätze
    """
    list = []
    for i, j in zip(dataset_list, range(len(dataset_list))):
        count = 1
        count += j
        print('\n Deskriptive Statistik für Datensatz ' + str(count))
        list.append(i.describe())
        print('\n')
        print(list, sep="\n")
        list.pop()


def preprocessing(Datensatz, filtered, col_loc, first=' ',
                  second=' ', third=' ', fourth=' '):
    """Vorbereiten für grafische Funktionen mit
    2 gefilterten Ausprägungen, wobei der bedingte Mittelwert berechnet wird
    Argumente
        Datensatz: Datensatz dem die vorzubereitenden Daten entspringen
        filtered (str): Spalte, nach der zu Filtern ist
        array1: die ersten gemittelten Werte
        second (int): wo mit Slicing schluss ist
        col_loc (var): df.columns[x] mit x als Positionsangabe der Spaltenbezeichnungen im Datensatz
    Output:
        gemittelte Werte als Variablen sowie Spaltenbezeichnungen dieser
    """
    means = Datensatz.groupby(filtered).mean()
    fst_array = means.iloc[slice(first, second), slice(third, fourth)].values
    fst_array_1d = fst_array.flatten()
    snd_array = means.iloc[:first, :second].values
    snd_array_1d = snd_array.flatten()
    Spalten = list(col_loc)
    return fst_array_1d, snd_array_1d, Spalten

def dictionary(list1, list2, name):
    """Funktion zum Erstellen eines Dictionarys. Mappt die beiden
    Listen spaltenweise
    Argumente
    list1 (lst): Enthält die Key values
    list2 (lst): Enthält die Werte der Keys
    name (str): Name des Dictionarys
    Output: Dictionary
    """
    dictionary = {}
    for key in list1:
        for value in list2:
            dictionary[key] = value
            list2.remove(value)
            break
    print(name, end = '\n')
    print(dictionary, end = '\n\n\n\n')
