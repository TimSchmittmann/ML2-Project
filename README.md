# ML2-Project
Holger Heidrich am 25.10.18 18:27 Uhr

Name of Group: GodPutASmileUponYourFace 

Contact Person: Tim Schmittmann (Tim.Schmittmann@gmx.de) 

Members: Tim Schmittmann, Sebastian Riechert, Suraka Al Baradan 

Type of Problem: Classification, Sentiment Analysis 

Problem Description: 
Problem1: 
Sentiment Analysis mit Emojis als Label. Verwendung von "klassischen" ML-Ansätzen logistische Regression und Random Forest. Erstellung des Datasets. Datenvorverarbeitungsschritte wie parsing, Labelsetzen, Codierung der Tweets beispielsweise mit Bag of Words. Modeltuning. 

Dataset: 
Tweets, die über Twitter-API ausgelesen werden. Es werden nur deutsche Tweets die Emojis enthalten abgerufen. Die Emojis werden aus den Tweets-Korpus entfernt und als Labels für die Klassifikation genutzt. Hierbei dienen die Emojis als Repräsentationen von Emotionen. Dieser Ansatz wurde gewählt, da es über diesen Parsing-Ansatz einfach ist, ein großes Trainingsset zu erstellen und die Emojis ein recht breites Spektrum möglicher Emotionen abdecken. Es handelt sich somit um eine Multilabel-Klassifikation. Mithilfe der Twitter-API darf man pro 15 Minuten maximal 45.000 Tweets abrufen, weswegen das Sammeln der Daten Schrittweise geschehen muss. Die Finale Größe der Trainings- und Testdaten wird über empirisches Testen bestimmt, abhängig davon wie schnell die gewählten Modelle auf den Datenmengen lernen können. 

Problem2: 
Deep Learning Ansätze, die inherent mit sequentieller Struktur von natürlicher Sprache umgehen können (bspw. LSTM, TransformerNetwork, ...) auf gleiches Dataset anwenden. Entwickeln einer App, die Inferenz für trainierte Modelle auf eigener Texteingabe ermöglicht. Hierfür müssen vor allem die Vorverarbeitungsschritte (Data Preparation) auch auf neue Inputs (Inferenzmodus) angewendet werden. 


Abgedeckte Setups (aus Opal Forum): 
Special Treatment of Data: 
Die natürlichsprachigen Daten müssen möglichst informationserhaltend codiert werden, um sie als Inputs für ML-Modelle nutzbar zu machen. 
Comparing different Methods: 
klassische Ansätze vs RNN-Varianten 
Learn something new: 
Nur ein Teammitglied hat Erfahrung mit log. Regression und Random Forests, aber nicht im Kontext von NLP. Abgesehen davon sind alle uns alle Methoden nur in der Theorie bekannt, haben damit jedoch noch nie gearbeitet. Auch das Arbeiten mit natürlicher Sprache im Kontext von Machine Learning und die damit einhergehenden Anforderungen sind neu für uns. 
You build your own App: 
Wir programmieren eine App, mit der wir Inferenz für unsere Modelle durchführen können. Für eine beliebige natürlichsprachige Eingabe werden die Emojis vorgeschlagen, die laut Modell die höchste Wahrscheinlichkeit besitzen
