from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QLabel
from qgis.PyQt.QtGui import QFont
from PyQt5.QtCore import Qt
from qgis.PyQt.QtGui import QPixmap
from qgis.core import QgsExpression 
from qgis.core import QgsFeatureRequest
import sys
import processing
from qgis.core import QgsProcessingFeatureSourceDefinition

class NumberInputDialog(QDialog):
    def __init__(self):
        super(NumberInputDialog, self).__init__()
        self.setWindowTitle('Coastal Dynamics Analyzer - UNIPA')
        self.layout = QVBoxLayout()
        
        # Aggiungi l'immagine di QGIS come sfondo
        #qgis_image = QLabel()
        #qgis_image.setPixmap(QPixmap('‪C:\\Users\\Niloufar\\Downloads\\wave.jpg'))  # Sostituisci 'path_to_qgis_icon.png' con il percorso del file dell'icona di QGIS
        #qgis_image.setAlignment(Qt.AlignCenter)
        #self.layout.addWidget(qgis_image)
        
        note3 = QLabel ("Welcome to Coastal Dynamics Analyzer \nCDA")
        note3.setAlignment(Qt.AlignCenter)
        note3.setStyleSheet("font-size: 18pt; font-weight: bold; font-style: italic; font-family: Arial;")
        
        note33 = QLabel ("Developed for QGIS, plug-in version 1.0")
        note33.setAlignment(Qt.AlignCenter)
        note33.setStyleSheet("font-size: 10pt; font-weight: bold; font-style: italic; font-family: Arial;")
        
        note3.show()
        
        note24 = QLabel("\n \n CREATE BASELINE:")
        font = QFont()
        font.setBold(True)
        note24.setFont(font)
        
        note224 = QLabel("\n        Enter 0 to generate a PCHIP baseline from shoreline  ^ ")
        font = QFont()
        note224.setStyleSheet("font-size: 10pt")
        
        note_ll = QLabel("^       Run 0 only the first time to create the reference baseline. \n         The plug-in will automatically save the geometry in a folder specified by the user.   \n ")
        note_ll.setStyleSheet("font-style: italic")

        note2 = QLabel("\n \n STEP RULES:")
        font = QFont()
        font.setBold(True)
        note2.setFont(font)
        
        note22 = QLabel("For more info see CDA User Manual ")
        note222 = QLabel(" ")
        
        note_label = QLabel("""        Enter 1 if you want to create transect from baseline
        Enter 2 if you want to repair transect geometries
        Enter 3 if you want to save shape files and csv format *
        Enter 4 if you want to calculate SCE and LRR **
        Enter 5 if you want to clip transect between two shorelines (NSM - EPR) ***
        """)
        note_label.setStyleSheet("font-size: 10pt")
        
        note_l = QLabel("*       Run 3 after each execution of step 2 \n**     Run 4 when all transects of the diachronic analysis to be performed have been calculated \n***   You need at least two shoreline transect \n ")
        note_l.setStyleSheet("font-style: italic")
        
        linenote = QLabel ("______________________________________________________________________________")
        note4 = QLabel ("\n \n Powered by Department of Engineering, University of Palermo \nMarine and Coastal Engineering Lab")
        note4.setAlignment(Qt.AlignCenter)
        note4.setStyleSheet("font-size: 8pt; font-weight: bold; font-style: italic; font-family: Arial;")
        note4.show()

        self.layout.addWidget(note3)
        self.layout.addWidget(note33)
        self.layout.addWidget(note24)
        self.layout.addWidget(note224)
        self.layout.addWidget(note_ll)
        self.layout.addWidget(note2)
        self.layout.addWidget(note_label)
        self.layout.addWidget(note_l)
        self.layout.addWidget(linenote)
        self.layout.addWidget(note22)
        self.layout.addWidget(note222)
        
        

        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)
        self.input_field.setPlaceholderText ("Insert a step ID [ from 0 to 5 ]")


        ok_button = QPushButton('Run CDA')
        ok_button.clicked.connect(self.on_ok_clicked)
        
        
        # Imposta il testo in grassetto per il pulsante
        font = QFont()
        font.setBold(True)
        ok_button.setFont(font)
        self.layout.addWidget(ok_button)

        self.setLayout(self.layout)
        
        self.layout.addWidget(note4)
        
        note_lll = QLabel(" \n Cite as Qwerty et al., 2024 ")
        note_lll.setStyleSheet("font-style: italic")
        note_lll.setAlignment(Qt.AlignRight)  # Imposta l'allineamento a sinistra
        self.layout.addWidget(note_lll)

        # Crea una QLabel per il testo del link
        link_label = QLabel('<a href="https://www.unipa.it/dipartimenti/ingegneria/cds/ingegneriaambientaleperlosvilupposostenibile2303">Click here</a>')
        link_label.setOpenExternalLinks(True)  # Apre il link nel browser esterno quando viene cliccato
        link_label.setAlignment(Qt.AlignRight)  # Imposta l'allineamento a destra

        # Aggiungi la QLabel al layout
        self.layout.addWidget(link_label)
        
        # Pulsante rosso per chiudere la finestra
        # Pulsante rosso per chiudere la finestra
        quit_button = QPushButton('Quit CDA')
        quit_button.setStyleSheet("background-color: grey;")
        quit_button.clicked.connect(self.reject)  # Chiude la finestra di dialogo

        # Imposta il testo in grassetto per il pulsante
        font = QFont()
        font.setBold(True)
        quit_button.setFont(font)

        # Aggiungi il pulsante al layout
        self.layout.addWidget(quit_button)

    def on_ok_clicked(self):
        try:
            global AA
            input_value = int(self.input_field.text())
            if -1 < input_value < 6:
                AA = input_value
                self.accept()  # Chiude la finestra di dialogo
            else:
                QMessageBox.warning(self, 'CDA Error', 'Insert a valid number step between 1 and 5')
        except ValueError:
            QMessageBox.warning(self, 'CDA Error', 'Insert a valid number step')
# Creazione e visualizzazione della finestra di dialogo
dialog = NumberInputDialog()
if dialog.exec_() == QDialog.Accepted:
    print("Insert Number:", AA)
else:
    print("Quit")
    dialog.close()

if AA ==1:
    from qgis.core import QgsProcessing
    from qgis.core import QgsProcessingAlgorithm
    from qgis.core import QgsProcessingMultiStepFeedback
    from qgis.core import QgsProcessingParameterVectorLayer
    from qgis.core import QgsProcessingParameterString
    from qgis.core import QgsProcessingParameterNumber
    from qgis.core import QgsProcessingParameterFeatureSink
    import processing


    class Calc_transect(QgsProcessingAlgorithm):

        def initAlgorithm(self, config=None):
            self.addParameter(QgsProcessingParameterVectorLayer('baseline_layer', 'Baseline layer ', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
            self.addParameter(QgsProcessingParameterString('coastline_date', 'Coastline date', multiLine=False, defaultValue='DD/MM/YYYY'))
            self.addParameter(QgsProcessingParameterVectorLayer('coastline_layer', 'Coastline layer', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
            self.addParameter(QgsProcessingParameterNumber('transect_length', 'Transect length', type=QgsProcessingParameterNumber.Double, minValue=0.01, defaultValue=10))
            self.addParameter(QgsProcessingParameterNumber('transect_resolution', 'Transect resolution', type=QgsProcessingParameterNumber.Double, minValue=0.1, defaultValue=150))
            self.addParameter(QgsProcessingParameterNumber('transect_side_insert_0__left_1__right_2__both', 'Transect side (Insert 0 -> left; 1 -> right; 2 -> both)', type=QgsProcessingParameterNumber.Integer, minValue=0, maxValue=2, defaultValue=0))
            self.addParameter(QgsProcessingParameterFeatureSink('Transect', 'Transect', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

        def processAlgorithm(self, parameters, context, model_feedback):
            # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
            # overall progress through the model
            feedback = QgsProcessingMultiStepFeedback(8, model_feedback)
            results = {}
            outputs = {}

            # Punti lungo la geometria
            alg_params = {
                'DISTANCE': parameters['transect_resolution'],
                'END_OFFSET': 0,
                'INPUT': parameters['baseline_layer'],
                'START_OFFSET': 0,
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['PuntiLungoLaGeometria'] = processing.run('native:pointsalonglines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(1)
            if feedback.isCanceled():
                return {}

            # Da punti a percorso
            alg_params = {
                'CLOSE_PATH': False,
                'GROUP_EXPRESSION': '',
                'INPUT': outputs['PuntiLungoLaGeometria']['OUTPUT'],
                'NATURAL_SORT': False,
                'ORDER_EXPRESSION': '',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['DaPuntiAPercorso'] = processing.run('native:pointstopath', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(2)
            if feedback.isCanceled():
                return {}

            # Transetto
            alg_params = {
                'ANGLE': 90,
                'INPUT': outputs['DaPuntiAPercorso']['OUTPUT'],
                'LENGTH': parameters['transect_length'],
                'SIDE': parameters['transect_side_insert_0__left_1__right_2__both'],
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['Transetto'] = processing.run('native:transect', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(3)
            if feedback.isCanceled():
                return {}

            # Intersezione di linee
            alg_params = {
                'INPUT': outputs['Transetto']['OUTPUT'],
                'INPUT_FIELDS': [''],
                'INTERSECT': parameters['coastline_layer'],
                'INTERSECT_FIELDS': [''],
                'INTERSECT_FIELDS_PREFIX': '',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['IntersezioneDiLinee'] = processing.run('native:lineintersections', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(4)
            if feedback.isCanceled():
                return {}

            # Intersezione di linee percorso
            alg_params = {
                'INPUT': outputs['Transetto']['OUTPUT'],
                'INPUT_FIELDS': [''],
                'INTERSECT': outputs['DaPuntiAPercorso']['OUTPUT'],
                'INTERSECT_FIELDS': [''],
                'INTERSECT_FIELDS_PREFIX': '',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['IntersezioneDiLineePercorso'] = processing.run('native:lineintersections', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(5)
            if feedback.isCanceled():
                return {}

            # Collega tramite linee (hub lines)
            alg_params = {
                'ANTIMERIDIAN_SPLIT': False,
                'GEODESIC': False,
                'GEODESIC_DISTANCE': 1000,
                'HUBS': outputs['IntersezioneDiLinee']['OUTPUT'],
                'HUB_FIELD': 'TR_ID',
                'HUB_FIELDS': [''],
                'SPOKES': outputs['IntersezioneDiLineePercorso']['OUTPUT'],
                'SPOKE_FIELD': 'TR_ID',
                'SPOKE_FIELDS': [''],
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['CollegaTramiteLineeHubLines'] = processing.run('native:hublines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(6)
            if feedback.isCanceled():
                return {}

            # Calcolatore di campi
            alg_params = {
                'FIELD_LENGTH': 12,
                'FIELD_NAME': 'length',
                'FIELD_PRECISION': 6,
                'FIELD_TYPE': 0,  # Decimale (doppia precisione)
                'FORMULA': '$length',
                'INPUT': outputs['CollegaTramiteLineeHubLines']['OUTPUT'],
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['CalcolatoreDiCampi'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(7)
            if feedback.isCanceled():
                return {}

            coastline_date_value = parameters['coastline_date']
            
            # Calcolatore di campi_anni
            alg_params = {
                'FIELD_LENGTH': 10,
                'FIELD_NAME': 'date',
                'FIELD_PRECISION': 0,
                'FIELD_TYPE': 2,  # Testo (stringa)
                'FORMULA': f"'{coastline_date_value}'",
                'INPUT': outputs['CalcolatoreDiCampi']['OUTPUT'],
                'OUTPUT': parameters['Transect']
            }
            outputs['CalcolatoreDiCampi_anni'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['Transect'] = outputs['CalcolatoreDiCampi_anni']['OUTPUT']
            return results

        def name(self):
            return 'CDA - Calc_Transect'

        def displayName(self):
            return 'CDA - Calc_Transect'

        def group(self):
            return ''

        def groupId(self):
            return ''

        def createInstance(self):
            return Calc_transect()

elif AA == 2:
    from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton
    from qgis.core import QgsProject, QgsFeatureRequest, QgsExpression

    class LayerSelectionDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("CDA - Select transect layers to be fixed")
            self.layout = QVBoxLayout()

            self.layer_check_boxes = []
            self.populate_layer_check_boxes()  # Popola il layout con le caselle di controllo dei layer
            for checkbox in self.layer_check_boxes:
                self.layout.addWidget(checkbox)

            self.select_button = QPushButton("Select")
            self.select_button.clicked.connect(self.on_select_button_clicked)
            self.layout.addWidget(self.select_button)

            self.selected_layer_names = []  # Lista per memorizzare i nomi dei layer selezionati

            self.setLayout(self.layout)
            self.resize(280, 300)

        def populate_layer_check_boxes(self):
            # Ottieni i nomi di tutti i layer presenti nella TOC
            layers = QgsProject.instance().mapLayers().values()
            for layer in layers:
                checkbox = QCheckBox(layer.name())
                self.layer_check_boxes.append(checkbox)

        def on_select_button_clicked(self):
            # Ottieni i nomi dei layer selezionati
            self.selected_layer_names = [checkbox.text() for checkbox in self.layer_check_boxes if checkbox.isChecked()]
            print(f"Layers selezionati: {self.selected_layer_names}")

            # Chiudi la finestra di dialogo
            self.close()

    # Creare e visualizzare la finestra di dialogo di selezione del layer
    dialog = LayerSelectionDialog()
    dialog.exec_()

    # Ottieni i nomi dei layer selezionati
    selected_layer_names = dialog.selected_layer_names

    # Loop attraverso i nomi dei layer selezionati
    for layer_name in selected_layer_names:
        # Ottieni il riferimento al layer selezionato dalla TOC
        selected_layer = QgsProject.instance().mapLayersByName(layer_name)[0]

        field_tr_id = 'TR_ID'  # Nome del campo per cui selezionare gli elementi unici
        field_length = 'length'  # Nome del campo della lunghezza

        # Creazione di un dizionario per memorizzare la lunghezza più piccola per ogni TR_ID
        min_length_dict = {}

        # Loop attraverso le feature del layer per trovare la lunghezza più piccola per ogni TR_ID
        for feature in selected_layer.getFeatures():
            tr_id = feature[field_tr_id]
            length = feature[field_length]
            if tr_id not in min_length_dict or length < min_length_dict[tr_id]:
                min_length_dict[tr_id] = length

        # Seleziona le feature con la lunghezza più piccola per ogni TR_ID
        selection = []
        for tr_id, min_length in min_length_dict.items():
            exp = QgsExpression('"{}" = {} AND "{}" = {}'.format(field_tr_id, tr_id, field_length, min_length))
            it = selected_layer.getFeatures(QgsFeatureRequest(exp))
            ids = [i.id() for i in it]
            selection.extend(ids)

        selected_layer.selectByIds(selection)


elif AA == 3:
    from qgis.core import QgsProcessing
    from qgis.core import QgsProcessingAlgorithm
    from qgis.core import QgsProcessingMultiStepFeedback
    from qgis.core import QgsProcessingParameterVectorLayer
    from qgis.core import QgsProcessingParameterFileDestination
    from qgis.core import QgsProcessingParameterFeatureSink
    import processing


    class Save_selected(QgsProcessingAlgorithm):

        def initAlgorithm(self, config=None):
            self.addParameter(QgsProcessingParameterVectorLayer('insert_transect_layer_to_repair', 'Insert transect layer to repair', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
            self.addParameter(QgsProcessingParameterFileDestination('Csv_', 'CSV_', fileFilter='GeoPackage (*.gpkg *.GPKG);;ESRI shapefile (*.shp *.SHP);;(Geo)Arrow (*.arrow *.feather *.arrows *.ipc *.ARROW *.FEATHER *.ARROWS *.IPC);;(Geo)Parquet (*.parquet *.PARQUET);;AutoCAD DXF (*.dxf *.DXF);;File ESRI Geodatabase (*.gdb *.GDB);;FlatGeobuf (*.fgb *.FGB);;Foglio di calcolo MS Office Open XML [XLSX] (*.xlsx *.XLSX);;Foglio di calcolo Open Document [ODS] (*.ods *.ODS);;Formato GPS eXchange [GPX] (*.gpx *.GPX);;Formato Testo Delimitato [CSV] (*.csv *.CSV);;Geoconcept (*.gxt *.txt *.GXT *.TXT);;Geography Markup Language [GML] (*.gml *.GML);;GeoJSON - Delimitato da Newline (*.geojsonl *.geojsons *.json *.GEOJSONL *.GEOJSONS *.JSON);;GeoJSON (*.geojson *.GEOJSON);;GeoRSS (*.xml *.XML);;INTERLIS 1 (*.itf *.xml *.ili *.ITF *.XML *.ILI);;INTERLIS 2 (*.xtf *.xml *.ili *.XTF *.XML *.ILI);;Keyhole Markup Language [KML] (*.kml *.KML);;Microstation DGN (*.dgn *.DGN);;PostgreSQL SQL dump (*.sql *.SQL);;S-57 Base file (*.000 *.000);;SQLite (*.sqlite *.SQLITE);;TAB Mapinfo (*.tab *.TAB)', createByDefault=True, defaultValue=None))
            self.addParameter(QgsProcessingParameterFeatureSink('Rep_tr', 'Rep_TR', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))

        def processAlgorithm(self, parameters, context, model_feedback):
            # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
            # overall progress through the model
            feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
            results = {}
            outputs = {}

            # Estrarre elementi selezionati
            alg_params = {
                'INPUT': parameters['insert_transect_layer_to_repair'],
                'OUTPUT': parameters['Rep_tr']
            }
            outputs['EstrarreElementiSelezionati'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['Rep_tr'] = outputs['EstrarreElementiSelezionati']['OUTPUT']

            feedback.setCurrentStep(1)
            if feedback.isCanceled():
                return {}

            # Salva elementi vettoriali su file
            alg_params = {
                'ACTION_ON_EXISTING_FILE': 0,  # Crea o sovrascrive un file
                'DATASOURCE_OPTIONS': '',
                'INPUT': outputs['EstrarreElementiSelezionati']['OUTPUT'],
                'LAYER_NAME': '',
                'LAYER_OPTIONS': '',
                'OUTPUT': parameters['Csv_']
            }
            outputs['SalvaElementiVettorialiSuFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['Csv_'] = outputs['SalvaElementiVettorialiSuFile']['OUTPUT']
            return results

        def name(self):
            return 'CDA - Save_Selected'

        def displayName(self):
            return 'CDA - Save_Selected'

        def group(self):
            return ''

        def groupId(self):
            return ''

        def createInstance(self):
            return Save_selected()
elif AA == 4:
    import os
    import csv
    from PyQt5.QtWidgets import QFileDialog
    from collections import defaultdict
    import datetime
    import numpy as np

    # Seleziona la cartella
    folder_path = QFileDialog.getExistingDirectory(None, "CDA - Select CSV saved folder")

    # Verifica che la cartella sia stata selezionata
    if not folder_path:
        print("No select folder.")
        exit()

    # Dizionario per memorizzare le informazioni di tutti i file CSV
    all_info = defaultdict(dict)
    all_tr_ids = set()

    # Importa tutti i file CSV nella cartella
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            with open(os.path.join(folder_path, filename), 'r', encoding='latin-1') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    tr_id = row.get("TR_ID")
                    date_str = row.get("date")
                    # Converti la data in formato datetime
                    date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
                    # Converti la data in un numero rappresentativo
                    date_num = date_obj.toordinal()
                    length = float(row.get("length"))  # Converte la lunghezza in float per poterla confrontare
                    all_info[filename][tr_id] = {"Date": date_num, "Length": length}
                    all_tr_ids.add(tr_id)

    # Dizionario per memorizzare i coefficienti angolari della regressione lineare per ogni TR_ID
    lrr_values = {}

    # Calcola la regressione lineare per ogni TR_ID
    for tr_id in all_tr_ids:
        x = []
        y = []
        for filename, info in all_info.items():
            if tr_id in info:
                x.append(info[tr_id]["Date"])
                y.append(info[tr_id]["Length"])
        x = np.array(x)
        y = np.array(y)
        
        # Calcola i coefficienti della regressione lineare
        mean_x = np.mean(x)
        mean_y = np.mean(y)
        num = np.sum((x - mean_x) * (y - mean_y))
        den = np.sum((x - mean_x) ** 2)
        lrr_values[tr_id] = num / den

    # Calcola il valore massimo della colonna "length" per ogni riga
    max_length_per_row = {}
    max_length_date_per_row = {}
    for tr_id in all_tr_ids:
        max_length_info = max((info[tr_id]["Length"], info[tr_id]["Date"]) for info in all_info.values() if tr_id in info)
        max_length_per_row[tr_id] = max_length_info[0]
        max_length_date_per_row[tr_id] = max_length_info[1]

    # Ordina gli ID
    sorted_tr_ids = sorted(all_tr_ids, key=lambda x: int(x))

    # Scrivi le informazioni in un unico file
    output_file = os.path.join(folder_path, "info_all.csv")
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["ID"] + [f"{filename}_Date" for filename in sorted(all_info.keys())] + [f"{filename}_Length" for filename in sorted(all_info.keys())] + ["SCE", "date_SCE", "LRR"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Scrivi le informazioni per ogni ID
        for tr_id in sorted_tr_ids:
            row_data = {"ID": tr_id}
            for filename, info in all_info.items():
                if tr_id in info:
                    date_obj = datetime.datetime.fromordinal(info[tr_id]["Date"])
                    row_data[f"{filename}_Date"] = date_obj.strftime('%d/%m/%Y')
                    row_data[f"{filename}_Length"] = info[tr_id]["Length"]
                else:
                    row_data[f"{filename}_Date"] = "null"
                    row_data[f"{filename}_Length"] = "null"
            
            # Aggiungi le colonne SCE, date_SCE e LRR
            if tr_id in lrr_values:
                row_data["LRR"] = lrr_values[tr_id]
            else:
                row_data["LRR"] = "null"
            
            # Converti il numero rappresentativo della data_SCE in un oggetto data
            date_SCE_obj = datetime.datetime.fromordinal(max_length_date_per_row[tr_id])
            # Modifica qui per salvare la data_SCE nel formato DD/MM/YYYY
            row_data["date_SCE"] = date_SCE_obj.strftime('%d/%m/%Y')
        
            # Aggiungi le colonne SCE
            row_data["SCE"] = max_length_per_row[tr_id]
            
            writer.writerow(row_data)

    print("Operazione completata. Il file 'info_all.csv' è stato creato nella cartella selezionata.")

elif AA == 5:
    from qgis.core import QgsProcessing
    from qgis.core import QgsProcessingAlgorithm
    from qgis.core import QgsProcessingMultiStepFeedback
    from qgis.core import QgsProcessingParameterVectorLayer
    from qgis.core import QgsProcessingParameterNumber
    from qgis.core import QgsProcessingParameterFeatureSink
    import processing


    class TransectClip(QgsProcessingAlgorithm):

        def initAlgorithm(self, config=None):
            self.addParameter(QgsProcessingParameterVectorLayer('transect_year_1', 'Transect (Year 1)', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
            self.addParameter(QgsProcessingParameterVectorLayer('transect_year_2', 'Transect (Year 2)', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
            self.addParameter(QgsProcessingParameterNumber('years_between_coastlines', 'Years between coastlines', type=QgsProcessingParameterNumber.Integer, minValue=1, defaultValue=1))
            self.addParameter(QgsProcessingParameterFeatureSink('Nsm_epr_transect', 'NSM_EPR_Transect', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

        def processAlgorithm(self, parameters, context, model_feedback):
            # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
            # overall progress through the model
            feedback = QgsProcessingMultiStepFeedback(8, model_feedback)
            results = {}
            outputs = {}

            # Estrai vertici A1
            alg_params = {
                'INPUT': parameters['transect_year_1'],
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['EstraiVerticiA1'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(1)
            if feedback.isCanceled():
                return {}

            # Estrai vertici A2
            alg_params = {
                'INPUT': parameters['transect_year_2'],
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['EstraiVerticiA2'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(2)
            if feedback.isCanceled():
                return {}

            # Differenza simmetrica
            alg_params = {
                'GRID_SIZE': None,
                'INPUT': outputs['EstraiVerticiA1']['OUTPUT'],
                'OVERLAY': outputs['EstraiVerticiA2']['OUTPUT'],
                'OVERLAY_FIELDS_PREFIX': '',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['DifferenzaSimmetrica'] = processing.run('native:symmetricaldifference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(3)
            if feedback.isCanceled():
                return {}

            # Intersezione Y1
            alg_params = {
                'GRID_SIZE': None,
                'INPUT': outputs['DifferenzaSimmetrica']['OUTPUT'],
                'INPUT_FIELDS': [''],
                'OVERLAY': parameters['transect_year_1'],
                'OVERLAY_FIELDS': [''],
                'OVERLAY_FIELDS_PREFIX': '',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['IntersezioneY1'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(4)
            if feedback.isCanceled():
                return {}

            # Intersezione Y2
            alg_params = {
                'GRID_SIZE': None,
                'INPUT': outputs['DifferenzaSimmetrica']['OUTPUT'],
                'INPUT_FIELDS': [''],
                'OVERLAY': parameters['transect_year_2'],
                'OVERLAY_FIELDS': [''],
                'OVERLAY_FIELDS_PREFIX': '',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['IntersezioneY2'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(5)
            if feedback.isCanceled():
                return {}

            # Collega tramite linee (hub lines)
            alg_params = {
                'ANTIMERIDIAN_SPLIT': False,
                'GEODESIC': False,
                'GEODESIC_DISTANCE': 1000,
                'HUBS': outputs['IntersezioneY1']['OUTPUT'],
                'HUB_FIELD': 'TR_ID_4',
                'HUB_FIELDS': [''],
                'SPOKES': outputs['IntersezioneY2']['OUTPUT'],
                'SPOKE_FIELD': 'TR_ID_4',
                'SPOKE_FIELDS': [''],
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['CollegaTramiteLineeHubLines'] = processing.run('native:hublines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(6)
            if feedback.isCanceled():
                return {}

            # Calcolatore di campi
            alg_params = {
                'FIELD_LENGTH': 12,
                'FIELD_NAME': 'NSM',
                'FIELD_PRECISION': 6,
                'FIELD_TYPE': 0,  # Decimale (doppia precisione)
                'FORMULA': '"length_3_2" - "length_3"',
                'INPUT': outputs['CollegaTramiteLineeHubLines']['OUTPUT'],
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['CalcolatoreDiCampi'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(7)
            if feedback.isCanceled():
                return {}

            coastline_date_value = parameters['years_between_coastlines']
            
            # Calcolatore di campi
            alg_params = {
                'FIELD_LENGTH': 12,
                'FIELD_NAME': 'EPR',
                'FIELD_PRECISION': 6,
                'FIELD_TYPE': 0,  # Decimale (doppia precisione)
                'FORMULA': '"NSM" / {}'.format(coastline_date_value),
                'INPUT': outputs['CalcolatoreDiCampi']['OUTPUT'],
                'OUTPUT': parameters['Nsm_epr_transect']
            }
            outputs['CalcolatoreDiCampi'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['Nsm_epr_transect'] = outputs['CalcolatoreDiCampi']['OUTPUT']
            return results

        def name(self):
            return 'CDA - TRANSECT_Clip'

        def displayName(self):
            return 'CDA - TRANSECT_Clip'

        def group(self):
            return ''

        def groupId(self):
            return ''

        def createInstance(self):
            return TransectClip()
elif AA == 0:
    from qgis.PyQt.QtWidgets import QFileDialog, QLineEdit, QDialog, QVBoxLayout, QPushButton, QApplication
    from qgis.PyQt.QtCore import QDir
    from qgis.core import (
        QgsVectorLayer,
        QgsFields,
        QgsField,
        QgsFeature,
        QgsGeometry,
        QgsVectorFileWriter,
        QgsPointXY,
        QgsWkbTypes,
    )
    from PyQt5.QtCore import QVariant
    from PyQt5.QtCore import QFile
    from scipy.interpolate import CubicSpline
    from qgis.core import QgsProject


    # Apri una finestra di dialogo per selezionare la cartella di input per la baseline
    infolder_baseline = QFileDialog.getExistingDirectory(None, 'CDA - Select the baseline input folder', QDir.homePath())

    # Apri una finestra di dialogo per selezionare la cartella di input per le linee di riva
    infolder_shoreline = QFileDialog.getExistingDirectory(None, 'CDA - Select the shoreline input folder', QDir.homePath())

    # Apri una finestra di dialogo per selezionare la cartella di output per la baseline
    outfolder_baseline = QFileDialog.getExistingDirectory(None, 'CDA - Select the baseline output folder', QDir.homePath())

    outfolder_transects = QFileDialog.getExistingDirectory(None, 'CDA - Select the TEMP materials output folder', QDir.homePath())

    infolder_baseline += QDir.separator()
    infolder_shoreline += QDir.separator()
    outfolder_baseline += QDir.separator()
    outfolder_transects += QDir.separator()

    # Verifica se l'utente ha annullato la selezione di una cartella
    if infolder_baseline == '' or infolder_shoreline == '' or outfolder_baseline == '':
        print('Selection of the cancelled folder. The programme will be terminated.')
        exit()

    # --------------------------------------- PARAMETRI --------------------------------------------------------------
    dialog = QDialog()
    layout = QVBoxLayout()
    dialog.setLayout(layout)

    line_edits = []
    prompt = ['Enter distance between transect:', 'Enter length of transect:']
    for text in prompt:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(text)
        layout.addWidget(line_edit)
        line_edits.append(line_edit)

    button = QPushButton('INPUT DONE')
    layout.addWidget(button)

    button.clicked.connect(dialog.accept)
    dialog.exec_()

    a = float(line_edits[0].text())
    b = float(line_edits[1].text())

    dist_trans = a  # Definizione di dist_trans
    length_trans = b  # Definizione di length_trans

    # --------------------------------------- PART 1 --------------------------------------------------------------
    # lettura base line
    for file_path in QDir(infolder_baseline).entryList(['*.shp']):
        base_in = QgsVectorLayer(infolder_baseline + file_path, '', 'ogr')

    base_in_features = base_in.getFeatures()
    for feature in base_in_features:
        base_geometry = feature.geometry()

    # ricampionare base line in vertici equidistanti
    dx = 1
    sampling = round(base_geometry.length() / dist_trans) + 1
    n_transects = round((base_geometry.length()) / dist_trans)
    with open(outfolder_transects + 'n_transects.txt', 'w') as f:
        f.write(str(n_transects))

    # Ottenere i vertici della geometria della linea di base
    unique_points = base_geometry.vertices()
    coordinates = [(pt.x(), pt.y()) for pt in unique_points]

    # Rimuovere i punti duplicati lungo l'asse x
    unique_coordinates = []
    seen_x = set()  # Usiamo un set per memorizzare le coordinate X già viste

    for coord in coordinates:
        x, y = coord  # Assegna la coordinata X e Y dalla tupla coord
        if x not in seen_x:
            unique_coordinates.append(coord)
            seen_x.add(x)

    # Ordinare le coordinate in base all'asse X
    sorted_coordinates = sorted(unique_coordinates, key=lambda coord: coord[0])

    # Dividere le coordinate ordinate in tuple separate di X e Y
    unique_X, unique_Y = zip(*sorted_coordinates)


    # Definisci il numero di punti su cui eseguire la spline
    num_points = sampling  # Modifica questo valore a tuo piacimento

    # Calcola il passo tra i punti x
    step = (max(unique_X) - min(unique_X)) / (num_points - 1)

    # Genera un array di punti x equidistanti nell'intervallo da x_min a x_max
    x_values = [min(unique_X) + i * step for i in range(num_points)]

    spline = CubicSpline(unique_X, unique_Y)

    # Calcola i corrispondenti valori di y utilizzando la spline
    y_values = spline(x_values)

    # Crea i punti interpolati lungo la base utilizzando le coordinate x e y
    interpolated_points = [QgsPointXY(x, y) for x, y in zip(x_values, y_values)]


    # --------------------------------------- NEW base line struct -------------------------------------
    baseline = QgsVectorLayer('LineString', 'baseline', 'memory')
    baseline_fields = QgsFields()
    baseline_fields.append(QgsField('ID', QVariant.Int))
    baseline_fields.append(QgsField('X', QVariant.Double))
    baseline_fields.append(QgsField('Y', QVariant.Double))
    baseline_provider = baseline.dataProvider()
    baseline_provider.addAttributes(baseline_fields)
    baseline.updateFields()

    # Creazione delle feature
    features = []
    for i, pt in enumerate(interpolated_points):
        # Crea una nuova feature
        feature = QgsFeature(baseline_fields)
        # Imposta gli attributi per questa feature
        feature.setAttribute('ID', i)
        feature.setAttribute('X', pt.x())
        feature.setAttribute('Y', pt.y())
        # Imposta la geometria per questa feature
        feature.setGeometry(QgsGeometry.fromPolylineXY(interpolated_points))
        # Aggiungi la feature alla lista delle feature
        features.append(feature)

        #print(f"Feature {i}: ID={i}, X={pt.x()}, Y={pt.y()}")  # Aggiunto per il debug

    # Lunghezza del provider dei dati prima dell'aggiunta delle feature
    length_before_adding_features = baseline_provider.featureCount()

    # Aggiunta delle feature al data provider del layer baseline
    baseline_provider.addFeatures(features)
    # Aggiornamento dei limiti del layer
    baseline.updateExtents() 

    # Lunghezza del provider dei dati dopo l'aggiunta delle feature
    length_after_adding_features = baseline_provider.featureCount()

    ######################################
    ###############
    ###########
    # Calcola la lunghezza della linea
    baseline_length = base_geometry.length()

    # Calcola Irregularity come rapporto tra lunghezza della linea e il numero di transetti
    irregularity = baseline_length / n_transects/100

    # Calcola la media delle differenze tra tutte le posizioni Y dei punti interpolati
    y_differences = [abs(y_values[i+1] - y_values[i]) for i in range(len(y_values) - 1)]
    mean_y_difference = sum(y_differences) / len(y_differences)

    # Calcola Roughness come prodotto tra Irregularity e la media delle differenze Y
    roughness = irregularity * mean_y_difference/2

    # Scrivi i risultati nel file di output
    with open(outfolder_transects + 'n_transects.txt', 'w') as f:
        f.write(f"Number of transects: {n_transects}\n")
        f.write(f"Irregularity: {irregularity}\n")
        f.write(f"Roughness: {roughness}\n")

        # Aggiungi un campo "JOIN" al layer baseline
        baseline_provider.addAttributes([QgsField("JOIN", QVariant.Int)])
        baseline.updateFields()
        baseline.updateExtents()
######################################
    ###############
    ###########
    
    # Imposta tutti i valori del campo "JOIN" su 1 per ogni feature
    for feature in baseline.getFeatures():
        baseline.dataProvider().changeAttributeValues({feature.id(): {baseline.fields().indexFromName("JOIN"): 1}})

    # Esegui il dissolvi basato sul campo "JOIN"
    dissolved_baseline = processing.run("native:dissolve", {
        'INPUT': baseline,
        'FIELD': ['JOIN'],  # Campo su cui eseguire il dissolvi
        'OUTPUT': 'memory:'
    })['OUTPUT']

    
    # Rimuovi eventuali caratteri di escape dalla fine del percorso della directory
    outfolder_baseline = outfolder_baseline.rstrip("\\")
    
    # Salva la geometria del layer dissolto
    dissolved_output_shapefile = outfolder_baseline + '/dissolved_baseline.shp'
    QgsVectorFileWriter.writeAsVectorFormat(dissolved_baseline, dissolved_output_shapefile, 'UTF-8', baseline.crs(), 'ESRI Shapefile')
    

    # Specifica il percorso completo del file shapefile
    output_shapefile = outfolder_baseline + '/baseline.shp'

    # Scrivi il layer baseline su disco come shapefile
    QgsVectorFileWriter.writeAsVectorFormat(baseline, output_shapefile, 'UTF-8', baseline.crs(), 'ESRI Shapefile')

    # Copia il file di proiezione
    QFile.copy(infolder_baseline + 'baseline.prj', outfolder_baseline + 'baseline.prj')
    # Copia il file di proiezione
    QFile.copy(infolder_baseline + 'baseline.prj', outfolder_baseline + 'dissolved_baseline.prj')

    # Caricare il risultato baseline nella TOC
    project_instance = QgsProject.instance()
    baseline_layer = QgsVectorLayer(output_shapefile, 'Baseline', 'ogr')

else:
    pass
    
###from PyQt5.QtWidgets import QMessageBox

# Dopo che il tuo script è stato eseguito con successo
###QMessageBox.information(None, " CDA ", "Processing done! \nClose this window and the next one \nAll the processes ended correctly!")
