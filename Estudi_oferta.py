import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import base64
from streamlit_option_menu import option_menu
import io
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import plotly.graph_objects as go
import matplotlib.colors as colors
import json

############################################################  TITULO DE PESTAÑA DE PÁGINA WEB ################################################
path = ""
st.set_page_config(
    page_title="Estudi d'oferta de nova construcció",
    page_icon="""data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAA1VBMVEVHcEylpKR6eHaBgH9GREGenJxRT06op6evra2Qj49kYWCbmpqdnJyWlJS+vb1CPzyurKyHhYWMiYl7eXgOCgiPjY10cnJZV1WEgoKCgYB9fXt
    /fHyzsrGUk5OTkZGlo6ONioqko6OLioq7urqysbGdnJuurazCwcHLysp+fHx9fHuDgYGJh4Y4NTJcWVl9e3uqqalcWlgpJyacm5q7urrJyMizsrLS0tKIhoaMioqZmJiTkpKgn5+Bf36WlZWdnJuFg4O4t7e2tbXFxMR3dXTg39/T0dLqKxxpAAAAOHRSTlMA/WCvR6hq/
    v7+OD3U9/1Fpw+SlxynxXWZ8yLp+IDo2ufp9s3oUPII+jyiwdZ1vczEli7waWKEmIInp28AAADMSURBVBiVNczXcsIwEAVQyQZLMrYhQOjV1DRKAomKJRkZ+P9PYpCcfbgze+buAgDA5nf1zL8TcLNamssiPG/
    vt2XbwmA8Rykqton/XVZAbYKTSxzVyvVlPMc4no2KYhFaePvU8fDHmGT93i47Xh8ijPrB/0lTcA3lcGQO7otPmZJfgwhhoytPeKX5LqxOPA9i7oDlwYwJ3p0iYaEqWDdlRB2nkDjgJPA7nX0QaVq3kPGPZq/V6qUqt9BAmVaCUcqEdACzTBFCpcyvFfAAxgMYYVy1sTwAAAAASUVORK5CYII=""",
    layout="wide"
)

############################################################  FUNCIONES: CSS, DESCARGAR EXCELS, SUBIR IMAGEN APCE ################################################
def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css_file(path + "main.css")

with open(path + "APCE_mod.png", "rb") as f:
    data_uri = base64.b64encode(f.read()).decode("utf-8")
markdown = f"""
<div class="image-apce-container">
<img src="data:image/png;base64, {data_uri}" alt="image" class="image-apce">
</div>
"""
st.markdown(markdown, unsafe_allow_html=True)


############################################################  CONFIGURAR MENU DE OPCIONES ################################################
# Creating a dropdown menu with options and icons, and customizing the appearance of the menu using CSS styles.
st.write("")
st.write("")
left_col, right_col, margin_right = st.columns((0.25, 1, 0.25))
with right_col:
    # with stylable_container(
    #     key="menu_option",
    #     css_styles=[
    #     """
    #     {
    #         position: fixed;
    #         z-index:100;
    #     }
    #     """]):
    selected = option_menu(
        menu_title=None,  # required
        options=["Catalunya","Províncies i àmbits","Municipis", "Districtes de Barcelona"],
        icons=[None,"map","house-fill","house-fill"],
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
        styles={
            "container": {"padding": "0px!important", "background-color": "#cce8e2", "align":"justify", "overflow":"hidden"},
            "icon": {"color": "#005c48", "font-size": "1.1em"},
            "nav-link": {
                "font-size": "1.1em",
                "text-align": "center",
                "font-weight": "bold",
                "color":"#005442",
                "padding": "5px",
                "--hover-color": "#DAE4E0",
                "background-color": "#cce8e2",
                "overflow":"hidden",
                },
            "nav-link-selected": {"background-color": "#66b9a7"},
            })


# st.markdown("<div class='header'><div>", unsafe_allow_html=True)
############################################################ IMPORTAMOS JSON ##############################################
@st.cache_resource
def carregant_dades():
    with open(path + 'DT_oferta.json', 'r') as outfile:
        list_of_df = [pd.DataFrame.from_dict(item) for item in json.loads(outfile.read())]
    shapefile_prov = gpd.read_file(path + "Provincias.geojson")
    shapefile_prov = shapefile_prov[shapefile_prov["NAME_1"]=="Cataluña"]
    bbdd_estudi_prom = list_of_df[0].copy()
    bbdd_estudi_hab = list_of_df[1].copy()
    bbdd_estudi_prom_2023 = list_of_df[2].copy()
    bbdd_estudi_hab_2023 = list_of_df[3].copy()
    bbdd_estudi_prom_2024 = list_of_df[4].copy()
    bbdd_estudi_hab_2024 = list_of_df[5].copy()
    bbdd_estudi_prom_2025 = list_of_df[6].copy()
    bbdd_estudi_hab_2025 = list_of_df[7].copy()
    mun_2018_2019 = list_of_df[8].copy()
    mun_2020_2021 = list_of_df[9].copy()
    mun_2022 = list_of_df[10].copy()
    mun_2023 = list_of_df[11].copy()
    mun_2024 = list_of_df[12].copy()
    mun_2025 = list_of_df[13].copy()

    maestro_estudi = list_of_df[14].copy()
    dis_2018_2019 = list_of_df[15].copy()
    dis_2020_2021 = list_of_df[16].copy()
    dis_2022 = list_of_df[17].copy()
    dis_2023 = list_of_df[18].copy()
    dis_2024 = list_of_df[19].copy()
    dis_2025 = list_of_df[20].copy()

    table117_22 = list_of_df[21].copy()
    table121_22 = list_of_df[22].copy()
    table125_22 = list_of_df[23].copy()

    table117_23 = list_of_df[24].copy()
    table121_23 = list_of_df[25].copy()
    table125_23 = list_of_df[26].copy()

    table117_24 = list_of_df[27].copy()
    table121_24 = list_of_df[28].copy()
    table125_24 = list_of_df[29].copy()

    table117_25 = list_of_df[30].copy()
    table121_25 = list_of_df[31].copy()
    table125_25 = list_of_df[32].copy()


    return([bbdd_estudi_prom, bbdd_estudi_hab, bbdd_estudi_prom_2023, bbdd_estudi_hab_2023, bbdd_estudi_prom_2024, bbdd_estudi_hab_2024, bbdd_estudi_prom_2025, bbdd_estudi_hab_2025, mun_2018_2019, mun_2020_2021,mun_2022, mun_2023, mun_2024, mun_2025, maestro_estudi, dis_2018_2019, dis_2020_2021, dis_2022, dis_2023, dis_2024, dis_2025, table117_22,
            table121_22, table125_22, table117_23, table121_23, table125_23, table117_24, table121_24, table125_24, table117_25, table121_25, table125_25, shapefile_prov])



bbdd_estudi_prom, bbdd_estudi_hab, bbdd_estudi_prom_2023, bbdd_estudi_hab_2023, bbdd_estudi_prom_2024, bbdd_estudi_hab_2024, bbdd_estudi_prom_2025, bbdd_estudi_hab_2025, \
mun_2018_2019, mun_2020_2021, mun_2022, mun_2023, mun_2024, mun_2025, maestro_estudi, dis_2018_2019, \
dis_2020_2021, dis_2022, dis_2023, dis_2024, dis_2025, table117_22, table121_22, table125_22, table117_23, \
table121_23, table125_23, table117_24, table121_24, table125_24, table117_25, table121_25, table125_25, shapefile_prov = carregant_dades()


############################################################  IMPORTAMOS BBDD 2022 ################################################
@st.cache_resource
def tidy_bbdd(df_prom, df_hab, any):
    # Importar BBDD promocions d'habitatge
    # bbdd_estudi_prom = pd.read_excel(path + 'BBDD 2022_2021 03.02.23.xlsx', sheet_name='Promocions 2022_2021')
    bbdd_estudi_prom= df_prom.copy()
    bbdd_estudi_prom.columns = bbdd_estudi_prom.iloc[0,:]
    bbdd_estudi_prom = bbdd_estudi_prom[bbdd_estudi_prom["ESTUDI"]==any]
    bbdd_estudi_prom['TIPO_aux'] = np.where(bbdd_estudi_prom['TIPO'].isin([1,2]), 'Habitatges unifamiliars', 'Habitatges plurifamiliars')

    mapping = {1: 'Unifamiliars aïllats', 
            2: 'Unifamiliars adossats', 
            3: 'Plurifamiliars en bloc obert', 
            4: 'Plurifamiliars en bloc tancat'}

    mapping1 = {1: "De nova Construcció",
                2: "Rehabilitació integral"}

    mapping2 = {1: "Pendent d'enderroc", 
            2: "Solar", 
            3: "Buidat", 
            4: "Cimentació",
            5: "Estructura",
            6: "Tancaments exteriors",
            7: "Tancaments interiors",
            8: "Claus en mà",
            9: "NS/NC"}

    mapping3 = {
                    1: 'A',
                    1.2:"A",
                    2: 'B',
                    2.3: "B",
                    3: 'C',
                    4: 'D',
                    4.5: "D",
                    5: 'E',
                    5.3 : "C",
                    6: "F",
                    7: "G",
                    8: "En tràmits",
                    9: "Sense informació"
    }

    mapping4 = {
                    0: "Altres",
                    1: "Plaça d'aparcament opcional",
                    2: "Plaça d'aparcament inclosa",
                    3: "Sense plaça d'aparcament",
    }


    # bbdd_estudi_hab['QENERGC'] = bbdd_estudi_hab['QENERGC'].map(number_to_letter_map)

    bbdd_estudi_prom['TIPO'] = bbdd_estudi_prom['TIPO'].map(mapping)

    bbdd_estudi_prom['TIPH'] = bbdd_estudi_prom['TIPH'].map(mapping1)


    bbdd_estudi_prom['ESTO'] = bbdd_estudi_prom['ESTO'].map(mapping2)

    bbdd_estudi_prom['QENERGC'] = bbdd_estudi_prom['QENERGC'].map(mapping3)

    bbdd_estudi_prom['APAR'] = bbdd_estudi_prom['APAR'].map(mapping4)


    # Importar BBDD habitatges
    # bbdd_estudi_hab = pd.read_excel(path + 'BBDD 2022_2021 03.02.23.xlsx', sheet_name='Habitatges 2022_2021')
    bbdd_estudi_hab = df_hab.copy()
    bbdd_estudi_hab.columns = bbdd_estudi_hab.iloc[0,:]
    bbdd_estudi_hab = bbdd_estudi_hab[bbdd_estudi_hab["ESTUDI"]==any]





    # ["Total dormitoris","Banys i lavabos","Cuines estàndard","Cuines americanes","Terrasses, balcons i patis","Estudi/golfes","Safareig","Altres interiors","Altres exteriors"]

    # ["DORM", "LAV", "cuina_normal", "cuina_amer", "TER", "Golfes", "Safareig","Altres interiors","Altres exteriors" ]

    bbdd_estudi_hab['TIPOG'] = np.where(bbdd_estudi_hab['TIPO'].isin([1,2]), 'Habitatges unifamiliars', 'Habitatges plurifamiliars')
    bbdd_estudi_hab['TIPO'] = bbdd_estudi_hab['TIPO'].map(mapping)
    bbdd_estudi_hab['QENERGC'] = bbdd_estudi_hab['QENERGC'].map(mapping3)
    bbdd_estudi_hab['APAR'] = bbdd_estudi_hab['APAR'].map(mapping4)

    bbdd_estudi_hab = bbdd_estudi_hab.dropna(axis=1 , how ='all')



    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'V0006':'Total dormitoris_aux', 
                                                            "DORM": "Total dormitoris",
                                                            "LAV": "Banys i lavabos",
                                                            "TER": "Terrasses, balcons i patis",
                                                            'NOMD01C':'Superfície útil',
                                                            "Preu_m2_util": "Preu m2 útil",
                                                            "NOMD01F_2022": "Preu mitjà",
                                                            'NOMD01P':'Estudi/golfes', 
                                                            'NOMD01Q':'Safareig', 
                                                            'NOMD01K': 'Cuines estàndard', 
                                                            'NOMD01L': 'Cuines americanes', 
                                                            "NOMD01R": "Altres interiors", 
                                                            "NOMD01S":"Altres exteriors"})

    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'V0006':'Total dormitoris_aux', 
                                                            "DORM": "Total dormitoris",
                                                            "LAV": "Banys i lavabos",
                                                            "TER": "Terrasses, balcons i patis",
                                                            'NOMD01C':'Superfície útil',
                                                            "Preu_m2_util": "Preu m2 útil",
                                                            'NOMD01P':'Estudi/golfes', 
                                                            'NOMD01Q':'Safareig', 
                                                            'NOMD01K': 'Cuines estàndard', 
                                                            'NOMD01L': 'Cuines americanes', 
                                                            "NOMD01R": "Altres interiors", 
                                                            "NOMD01S":"Altres exteriors"})


    # Canviar de nom tots els equipaments
    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'EQUIC_1': 'Zona enjardinada', 
                                                        'EQUIC_2': 'Parc infantil',
                                                        'EQUIC_3': 'Piscina comunitària', 
                                                        'EQUIC_4': 'Traster', 
                                                        'EQUIC_5': 'Ascensor', 
                                                        'EQUIC_6': 'Equipament Esportiu',  
                                                        'EQUIC_7': 'Sala de jocs', 
                                                        'EQUIC_8': 'Sauna', 
                                                        "EQUIC_9_50": "Altres",
                                                        'EQUIC_99': 'Cap dels anteriors'})
    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'EQUIC_1': 'Zona enjardinada', 
                                                        'EQUIC_2': 'Parc infantil',
                                                        'EQUIC_3': 'Piscina comunitària', 
                                                        'EQUIC_4': 'Traster', 
                                                        'EQUIC_5': 'Ascensor', 
                                                        'EQUIC_6': 'Equipament Esportiu',  
                                                        'EQUIC_7': 'Sala de jocs', 
                                                        'EQUIC_8': 'Sauna', 
                                                        "QUAL_ALTRES": "Altres",
                                                        'EQUIC_99': 'Cap dels anteriors'})
    bbdd_estudi_prom["Ascensor"] = np.where(bbdd_estudi_prom["Ascensor"]>=1, 1, bbdd_estudi_prom["Ascensor"])
    bbdd_estudi_hab["Ascensor"] = np.where(bbdd_estudi_hab["Ascensor"]>=1, 1, bbdd_estudi_hab["Ascensor"])
    # Canviar de nom totes les qualitats
    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {"QUALIC_5": "Aire condicionat", 
                                                        "QUALIC_6": "Bomba de calor", 
                                                        "QUALI_A": "Aerotèrmia", 
                                                        'QUALIC_7':"Calefacció", 
                                                        'QUALIC_8':"Preinstal·lació d'A.C./B. Calor/Calefacció", 
                                                        'QUALIC_9': 'Parquet', 
                                                        'QUALIC_10':'Armaris encastats',
                                                        'QUALIC_12':'Placa de cocció amb gas',
                                                        'QUALIC_13':'Placa de cocció vitroceràmica',
                                                        "QUALIC_14":"Placa d'inducció",
                                                        'QUALIC_22':'Plaques solars'})


    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {"QUALIC_5": "Aire condicionat", 
                                                        "QUALIC_6": "Bomba de calor", 
                                                        "QUALI_A": "Aerotèrmia", 
                                                        'QUALIC_7':"Calefacció", 
                                                        'QUALIC_8':"Preinstal·lació d'A.C./B. Calor/Calefacció", 
                                                        'QUALIC_9': 'Parquet', 
                                                        'QUALIC_10':'Armaris encastats',
                                                        'QUALIC_12':'Placa de cocció amb gas',
                                                        'QUALIC_13':'Placa de cocció vitroceràmica',
                                                        "QUALIC_14":"Placa d'inducció",
                                                        'QUALIC_22':'Plaques solars'})
    #  Canviar nom a tipus de calefacció
    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'CALEFC_3': 'De gasoil', 
                                                        'CALEFC_4': 'De gas natural', 
                                                        'CALEFC_5': 'De propà', 
                                                        'CALEFC_6': "D'electricitat", 
                                                        'CALEFC_9': "No s'indica tipus"})




    bbdd_estudi_prom['TIPV'] = np.where(bbdd_estudi_prom['TIPV_1'] >= 1, "Venda a través d'immobiliària independent",
                                        np.where(bbdd_estudi_prom['TIPV_2'] >= 1, "Venda a través d'immobiliaria del mateix promotor",
                                                np.where(bbdd_estudi_prom['TIPV_3'] >= 1, "Venda directa del promotor", "Sense informació")))


    bbdd_estudi_prom['TIPOL_VENDA'] = np.where(bbdd_estudi_prom['TIPOL_VENDA_1'] == 1, "0D",
                                        np.where(bbdd_estudi_prom['TIPOL_VENDA_2'] == 1, "1D",
                                                np.where(bbdd_estudi_prom['TIPOL_VENDA_3'] == 1, "2D",
                                                        np.where(bbdd_estudi_prom['TIPOL_VENDA_4'] == 1, "3D",
                                                            np.where(bbdd_estudi_prom['TIPOL_VENDA_5'] == 1, "4D", 
                                                                np.where(bbdd_estudi_prom['TIPOL_VENDA_6'] == 1, "5+D", "NA"))))))

                        
                                                    
    #  "Venda a través d'immobiliària independent", "Venda a través d'immobiliaria del mateix promotor", "Venda directa del promotor"

    bbdd_estudi_hab['TIPH'] = bbdd_estudi_hab['TIPH'].map(mapping1)

    bbdd_estudi_hab['ESTO'] = bbdd_estudi_hab['ESTO'].map(mapping2)


    vars = ['Zona enjardinada', 'Parc infantil', 'Piscina comunitària', 
            'Traster', 'Ascensor', 'Equipament Esportiu', 'Sala de jocs', 
            'Sauna', 'Altres', "Aire condicionat", "Bomba de calor", 
            "Aerotèrmia", "Calefacció", "Preinstal·lació d'A.C./B. Calor/Calefacció", 
            "Parquet", "Armaris encastats", 'Placa de cocció amb gas', 
            'Placa de cocció vitroceràmica', "Placa d'inducció", 'Plaques solars', "APAR"]
    vars_aux = ['Zona enjardinada', 'Parc infantil', 'Piscina comunitària', 
            'Traster', 'Ascensor', 'Equipament Esportiu', 'Sala de jocs', 
            'Sauna', 'Altres', "Aire condicionat", "Bomba de calor", 
            "Aerotèrmia", "Calefacció", "Preinstal·lació d'A.C./B. Calor/Calefacció", 
            "Parquet", "Armaris encastats", 'Placa de cocció amb gas', 
            'Placa de cocció vitroceràmica', "Placa d'inducció", 'Plaques solars', "Safareig","Terrasses, balcons i patis"]
    for i in vars:
        bbdd_estudi_prom[i] = bbdd_estudi_prom[i].replace({np.nan: 0})
    for i in vars_aux:
        bbdd_estudi_hab[i] = bbdd_estudi_hab[i].replace({np.nan: 0})
    bbdd_estudi_hab["Calefacció"] = bbdd_estudi_hab["Calefacció"].replace({' ': 0}) 
    bbdd_estudi_prom["Calefacció"] = bbdd_estudi_prom["Calefacció"].replace({' ': 0}) 


    bbdd_estudi_hab["Tram_Sup_util"] = bbdd_estudi_hab["Tram_Sup_util"].str.replace(" ", "")
    bbdd_estudi_hab["Tram_Sup_util"] = bbdd_estudi_hab["Tram_Sup_util"].str[3:]



    # Afegir categories a algunes columnes de la base de dades d'habitatge

    room_dict =  {i: f"{i}D" if i <= 4 else "5+D" for i in range(0, 20)}
    toilet_dict = {i: f"{i} Bany" if i <= 1 else "2 i més Banys" for i in range(1, 20)}
    bbdd_estudi_hab_mod = bbdd_estudi_hab.copy()

    bbdd_estudi_hab_mod['Total dormitoris'] = bbdd_estudi_hab_mod['Total dormitoris'].map(room_dict)
    bbdd_estudi_hab_mod['Banys i lavabos'] = bbdd_estudi_hab_mod['Banys i lavabos'].map(toilet_dict)
    bbdd_estudi_hab_mod["Terrasses, balcons i patis"] = np.where(bbdd_estudi_hab_mod["Terrasses, balcons i patis"]>=1, 1, 0)

    bbdd_estudi_hab["Nom DIST"] = bbdd_estudi_hab["Nom DIST"].str.replace(r'^\d{2}\s', '', regex=True)
    bbdd_estudi_hab_mod["Nom DIST"] = bbdd_estudi_hab_mod["Nom DIST"].str.replace(r'^\d{2}\s', '', regex=True)

    return([bbdd_estudi_prom, bbdd_estudi_hab, bbdd_estudi_hab_mod])


bbdd_estudi_prom, bbdd_estudi_hab, bbdd_estudi_hab_mod = tidy_bbdd(bbdd_estudi_prom, bbdd_estudi_hab, 2022)
############################################################  IMPORTAMOS BBDD FINAL 2023 ################################################
@st.cache_resource
def tidy_bbdd_2023(df_prom, df_hab, any):
    # bbdd_estudi_prom = pd.read_excel(path + 'P3007 BBDD desembre APCE.xlsx', sheet_name='Promocions 2023')
    bbdd_estudi_prom = df_prom.copy()
    bbdd_estudi_prom.columns = bbdd_estudi_prom.iloc[0,:]
    bbdd_estudi_prom = bbdd_estudi_prom[bbdd_estudi_prom["ESTUDI"]==any]
    bbdd_estudi_prom['TIPO_aux'] = np.where(bbdd_estudi_prom['TIPO'].isin([1,2]), 'Habitatges unifamiliars', 'Habitatges plurifamiliars')

    mapping = {1: 'Unifamiliars aïllats', 
            2: 'Unifamiliars adossats', 
            3: 'Plurifamiliars en bloc obert', 
            4: 'Plurifamiliars en bloc tancat'}

    mapping1 = {1: "De nova Construcció",
                2: "Rehabilitació integral"}

    mapping2 = {1: "Pendent d'enderroc", 
            2: "Solar", 
            3: "Buidat", 
            4: "Cimentació",
            5: "Estructura",
            6: "Tancaments exteriors",
            7: "Tancaments interiors",
            8: "Claus en mà",
            9: "NS/NC"}

    mapping3 = {
                    1: 'A',
                    1.2:"A",
                    2: 'B',
                    2.3: "B",
                    3: 'C',
                    4: 'D',
                    4.5: "D",
                    5: 'E',
                    5.3 : "C",
                    6: "F",
                    7: "G",
                    8: "En tràmits",
                    9: "Sense informació"
    }

    mapping4 = {
                    0: "Altres",
                    1: "Plaça d'aparcament opcional",
                    2: "Plaça d'aparcament inclosa",
                    3: "Sense plaça d'aparcament",
    }



    bbdd_estudi_prom['TIPO'] = bbdd_estudi_prom['TIPO'].map(mapping)

    bbdd_estudi_prom['TIPH'] = bbdd_estudi_prom['TIPH'].map(mapping1)


    bbdd_estudi_prom['ESTO'] = bbdd_estudi_prom['ESTO'].map(mapping2)

    bbdd_estudi_prom['QENERGC'] = bbdd_estudi_prom['QENERGC'].map(mapping3)

    bbdd_estudi_prom['APAR'] = bbdd_estudi_prom['APAR'].map(mapping4)


    # Importar BBDD habitatges
    # bbdd_estudi_hab = pd.read_excel(path + 'P3007 BBDD desembre APCE.xlsx', sheet_name='Habitatges 2023')
    bbdd_estudi_hab = df_hab.copy()
    bbdd_estudi_hab.columns = bbdd_estudi_hab.iloc[0,:]
    bbdd_estudi_hab = bbdd_estudi_hab[bbdd_estudi_hab["ESTUDI"]==any]





    # ["Total dormitoris","Banys i lavabos","Cuines estàndard","Cuines americanes","Terrasses, balcons i patis","Estudi/golfes","Safareig","Altres interiors","Altres exteriors"]

    # ["DORM", "LAV", "cuina_normal", "cuina_amer", "TER", "Golfes", "Safareig","Altres interiors","Altres exteriors" ]

    bbdd_estudi_hab['TIPOG'] = np.where(bbdd_estudi_hab['TIPO'].isin([1,2]), 'Habitatges unifamiliars', 'Habitatges plurifamiliars')
    bbdd_estudi_hab['TIPO'] = bbdd_estudi_hab['TIPO'].map(mapping)
    bbdd_estudi_hab['QENERGC'] = bbdd_estudi_hab['QENERGC'].map(mapping3)
    bbdd_estudi_hab['APAR'] = bbdd_estudi_hab['APAR'].map(mapping4)

    bbdd_estudi_hab = bbdd_estudi_hab.dropna(axis=1 , how ='all')



    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'V0006':'Total dormitoris_aux', 
                                                            "DORM": "Total dormitoris",
                                                            "LAV": "Banys i lavabos",
                                                            "TER": "Terrasses, balcons i patis",
                                                            'NOMD01C':'Superfície útil',
                                                            "Preu_m2_util": "Preu m2 útil",
                                                            "NOMD01F_2022": "Preu mitjà",
                                                            'NOMD01P':'Estudi/golfes', 
                                                            'NOMD01Q':'Safareig', 
                                                            'NOMD01K': 'Cuines estàndard', 
                                                            'NOMD01L': 'Cuines americanes', 
                                                            "NOMD01R": "Altres interiors", 
                                                            "NOMD01S":"Altres exteriors"})

    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'V0006':'Total dormitoris_aux', 
                                                            "DORM": "Total dormitoris",
                                                            "LAV": "Banys i lavabos",
                                                            "TER": "Terrasses, balcons i patis",
                                                            'NOMD01C':'Superfície útil',
                                                            "Preu_m2_util": "Preu m2 útil",
                                                            'NOMD01P':'Estudi/golfes', 
                                                            'NOMD01Q':'Safareig', 
                                                            'NOMD01K': 'Cuines estàndard', 
                                                            'NOMD01L': 'Cuines americanes', 
                                                            "NOMD01R": "Altres interiors", 
                                                            "NOMD01S":"Altres exteriors"})


    # Canviar de nom tots els equipaments
    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'EQUIC_1': 'Zona enjardinada', 
                                                        'EQUIC_2': 'Parc infantil',
                                                        'EQUIC_3': 'Piscina comunitària', 
                                                        'EQUIC_4': 'Traster', 
                                                        'EQUIC_5': 'Ascensor', 
                                                        'EQUIC_6': 'Equipament Esportiu',  
                                                        'EQUIC_7': 'Sala de jocs', 
                                                        'EQUIC_8': 'Sauna', 
                                                        "EQUIC_9_50": "Altres",
                                                        'EQUIC_99': 'Cap dels anteriors'})
    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'EQUIC_1': 'Zona enjardinada', 
                                                        'EQUIC_2': 'Parc infantil',
                                                        'EQUIC_3': 'Piscina comunitària', 
                                                        'EQUIC_4': 'Traster', 
                                                        'EQUIC_5': 'Ascensor', 
                                                        'EQUIC_6': 'Equipament Esportiu',  
                                                        'EQUIC_7': 'Sala de jocs', 
                                                        'EQUIC_8': 'Sauna', 
                                                        "QUAL_ALTRES": "Altres",
                                                        'EQUIC_99': 'Cap dels anteriors'})
    bbdd_estudi_prom["Ascensor"] = np.where(bbdd_estudi_prom["Ascensor"]>=1, 1, bbdd_estudi_prom["Ascensor"])
    bbdd_estudi_hab["Ascensor"] = np.where(bbdd_estudi_hab["Ascensor"]>=1, 1, bbdd_estudi_hab["Ascensor"])


    # Canviar de nom totes les qualitats
    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {"QUALIC_5": "Aire condicionat", 
                                                        "QUALIC_6": "Bomba de calor", 
                                                        "QUALI_A": "Aerotèrmia", 
                                                        'QUALIC_7':"Calefacció", 
                                                        'QUALIC_8':"Preinstal·lació d'A.C./B. Calor/Calefacció", 
                                                        'QUALIC_9': 'Parquet', 
                                                        'QUALIC_10':'Armaris encastats',
                                                        'QUALIC_12':'Placa de cocció amb gas',
                                                        'QUALIC_13':'Placa de cocció vitroceràmica',
                                                        "QUALIC_14":"Placa d'inducció",
                                                        'QUALIC_22':'Plaques solars'})


    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {"QUALIC_5": "Aire condicionat", 
                                                        "QUALIC_6": "Bomba de calor", 
                                                        "QUALI_A": "Aerotèrmia", 
                                                        'QUALIC_7':"Calefacció", 
                                                        'QUALIC_8':"Preinstal·lació d'A.C./B. Calor/Calefacció", 
                                                        'QUALIC_9': 'Parquet', 
                                                        'QUALIC_10':'Armaris encastats',
                                                        'QUALIC_12':'Placa de cocció amb gas',
                                                        'QUALIC_13':'Placa de cocció vitroceràmica',
                                                        "QUALIC_14":"Placa d'inducció",
                                                        'QUALIC_22':'Plaques solars'})
    #  Canviar nom a tipus de calefacció
    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'CALEFC_3': 'De gasoil', 
                                                        'CALEFC_4': 'De gas natural', 
                                                        'CALEFC_5': 'De propà', 
                                                        'CALEFC_6': "D'electricitat", 
                                                        'CALEFC_9': "No s'indica tipus"})




    bbdd_estudi_prom['TIPV'] = np.where(bbdd_estudi_prom['TIPV_1'] >= 1, "Venda a través d'immobiliària independent",
                                        np.where(bbdd_estudi_prom['TIPV_2'] >= 1, "Venda a través d'immobiliaria del mateix promotor",
                                                np.where(bbdd_estudi_prom['TIPV_3'] >= 1, "Venda directa del promotor", "Sense informació")))


    bbdd_estudi_prom['TIPOL_VENDA'] = np.where(bbdd_estudi_prom['TIPOL_VENDA_1'] == 1, "0D",
                                        np.where(bbdd_estudi_prom['TIPOL_VENDA_2'] == 1, "1D",
                                                np.where(bbdd_estudi_prom['TIPOL_VENDA_3'] == 1, "2D",
                                                        np.where(bbdd_estudi_prom['TIPOL_VENDA_4'] == 1, "3D",
                                                            np.where(bbdd_estudi_prom['TIPOL_VENDA_5'] == 1, "4D", 
                                                                np.where(bbdd_estudi_prom['TIPOL_VENDA_6'] == 1, "5+D", "NA"))))))

                        
                                                    
    #  "Venda a través d'immobiliària independent", "Venda a través d'immobiliaria del mateix promotor", "Venda directa del promotor"

    bbdd_estudi_hab['TIPH'] = bbdd_estudi_hab['TIPH'].map(mapping1)

    bbdd_estudi_hab['ESTO'] = bbdd_estudi_hab['ESTO'].map(mapping2)


    vars = ['Zona enjardinada', 'Parc infantil', 'Piscina comunitària', 
            'Traster', 'Ascensor', 'Equipament Esportiu', 'Sala de jocs', 
            'Sauna', 'Altres', "Aire condicionat", "Bomba de calor", 
            "Aerotèrmia", "Calefacció", "Preinstal·lació d'A.C./B. Calor/Calefacció", 
            "Parquet", "Armaris encastats", 'Placa de cocció amb gas', 
            'Placa de cocció vitroceràmica', "Placa d'inducció", 'Plaques solars', "APAR"]
    vars_aux = ['Zona enjardinada', 'Parc infantil', 'Piscina comunitària', 
            'Traster', 'Ascensor', 'Equipament Esportiu', 'Sala de jocs', 
            'Sauna', 'Altres', "Aire condicionat", "Bomba de calor", 
            "Aerotèrmia", "Calefacció", "Preinstal·lació d'A.C./B. Calor/Calefacció", 
            "Parquet", "Armaris encastats", 'Placa de cocció amb gas', 
            'Placa de cocció vitroceràmica', "Placa d'inducció", 'Plaques solars', "Safareig","Terrasses, balcons i patis"]
    for i in vars:
        bbdd_estudi_prom[i] = bbdd_estudi_prom[i].replace({np.nan : 0})
    for i in vars_aux:
        bbdd_estudi_hab[i] = bbdd_estudi_hab[i].replace({np.nan : 0})
    bbdd_estudi_hab["Calefacció"] = bbdd_estudi_hab["Calefacció"].replace({' ': 0}) 
    bbdd_estudi_prom["Calefacció"] = bbdd_estudi_prom["Calefacció"].replace({' ': 0}) 


    bbdd_estudi_hab["Tram_Sup_util"] = bbdd_estudi_hab["Tram_Sup_util"].str.replace(" ", "")
    bbdd_estudi_hab["Tram_Sup_util"] = bbdd_estudi_hab["Tram_Sup_util"].str[3:]



    # Afegir categories a algunes columnes de la base de dades d'habitatge

    room_dict =  {i: f"{i}D" if i <= 4 else "5+D" for i in range(0, 20)}
    toilet_dict = {i: f"{i} Bany" if i <= 1 else "2 i més Banys" for i in range(1, 20)}
    bbdd_estudi_hab_mod = bbdd_estudi_hab.copy()

    bbdd_estudi_hab_mod['Total dormitoris'] = bbdd_estudi_hab_mod['Total dormitoris'].map(room_dict)
    bbdd_estudi_hab_mod['Banys i lavabos'] = bbdd_estudi_hab_mod['Banys i lavabos'].map(toilet_dict)
    bbdd_estudi_hab_mod["Terrasses, balcons i patis"] = np.where(bbdd_estudi_hab_mod["Terrasses, balcons i patis"]>=1, 1, 0)

    bbdd_estudi_hab["Nom DIST"] = bbdd_estudi_hab["Nom DIST"].str.replace(r'^\d{2}\s', '', regex=True)
    bbdd_estudi_hab_mod["Nom DIST"] = bbdd_estudi_hab_mod["Nom DIST"].str.replace(r'^\d{2}\s', '', regex=True)

    return([bbdd_estudi_prom, bbdd_estudi_hab, bbdd_estudi_hab_mod])

bbdd_estudi_prom_2023, bbdd_estudi_hab_2023, bbdd_estudi_hab_mod_2023 = tidy_bbdd_2023(bbdd_estudi_prom_2023, bbdd_estudi_hab_2023, 2023)


############################################################  IMPORTAMOS BBDD FINAL 2024 ################################################
@st.cache_resource
def tidy_bbdd_2024(df_prom, df_hab, any):
    # bbdd_estudi_prom = pd.read_excel(path + 'P3007 BBDD desembre APCE.xlsx', sheet_name='Promocions 2024')
    bbdd_estudi_prom = df_prom.copy()
    bbdd_estudi_prom.columns = bbdd_estudi_prom.iloc[0,:]
    bbdd_estudi_prom = bbdd_estudi_prom[bbdd_estudi_prom["ESTUDI"]==any]
    bbdd_estudi_prom['TIPO_aux'] = np.where(bbdd_estudi_prom['TIPO'].isin([1,2]), 'Habitatges unifamiliars', 'Habitatges plurifamiliars')

    mapping = {1: 'Unifamiliars aïllats', 
            2: 'Unifamiliars adossats', 
            3: 'Plurifamiliars en bloc obert', 
            4: 'Plurifamiliars en bloc tancat'}

    mapping1 = {1: "De nova Construcció",
                2: "Rehabilitació integral"}

    mapping2 = {1: "Pendent d'enderroc", 
            2: "Solar", 
            3: "Buidat", 
            4: "Cimentació",
            5: "Estructura",
            6: "Tancaments exteriors",
            7: "Tancaments interiors",
            8: "Claus en mà",
            9: "NS/NC"}

    mapping3 = {
                    1: 'A',
                    1.2:"A",
                    2: 'B',
                    2.3: "B",
                    3: 'C',
                    4: 'D',
                    4.5: "D",
                    5: 'E',
                    5.3 : "C",
                    6: "F",
                    7: "G",
                    8: "En tràmits",
                    9: "Sense informació"
    }

    mapping4 = {
                    0: "Altres",
                    1: "Plaça d'aparcament opcional",
                    2: "Plaça d'aparcament inclosa",
                    3: "Sense plaça d'aparcament",
    }



    bbdd_estudi_prom['TIPO'] = bbdd_estudi_prom['TIPO'].map(mapping)

    bbdd_estudi_prom['TIPH'] = bbdd_estudi_prom['TIPH'].map(mapping1)


    bbdd_estudi_prom['ESTO'] = bbdd_estudi_prom['ESTO'].map(mapping2)

    bbdd_estudi_prom['QENERGC'] = bbdd_estudi_prom['QENERGC'].map(mapping3)

    bbdd_estudi_prom['APAR'] = bbdd_estudi_prom['APAR'].map(mapping4)


    # Importar BBDD habitatges
    # bbdd_estudi_hab = pd.read_excel(path + 'P3007 BBDD desembre APCE.xlsx', sheet_name='Habitatges 2023')
    bbdd_estudi_hab = df_hab.copy()
    bbdd_estudi_hab.columns = bbdd_estudi_hab.iloc[0,:]
    bbdd_estudi_hab = bbdd_estudi_hab[bbdd_estudi_hab["ESTUDI"]==any]





    # ["Total dormitoris","Banys i lavabos","Cuines estàndard","Cuines americanes","Terrasses, balcons i patis","Estudi/golfes","Safareig","Altres interiors","Altres exteriors"]

    # ["DORM", "LAV", "cuina_normal", "cuina_amer", "TER", "Golfes", "Safareig","Altres interiors","Altres exteriors" ]

    bbdd_estudi_hab['TIPOG'] = np.where(bbdd_estudi_hab['TIPO'].isin([1,2]), 'Habitatges unifamiliars', 'Habitatges plurifamiliars')
    bbdd_estudi_hab['TIPO'] = bbdd_estudi_hab['TIPO'].map(mapping)
    bbdd_estudi_hab['QENERGC'] = bbdd_estudi_hab['QENERGC'].map(mapping3)
    bbdd_estudi_hab['APAR'] = bbdd_estudi_hab['APAR'].map(mapping4)

    bbdd_estudi_hab = bbdd_estudi_hab.dropna(axis=1 , how ='all')



    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'V0006':'Total dormitoris_aux', 
                                                            "DORM": "Total dormitoris",
                                                            "LAV": "Banys i lavabos",
                                                            "TER": "Terrasses, balcons i patis",
                                                            'NOMD01C':'Superfície útil',
                                                            "Preu_m2_util": "Preu m2 útil",
                                                            "NOMD01F_2022": "Preu mitjà",
                                                            'NOMD01P':'Estudi/golfes', 
                                                            'NOMD01Q':'Safareig', 
                                                            'NOMD01K': 'Cuines estàndard', 
                                                            'NOMD01L': 'Cuines americanes', 
                                                            "NOMD01R": "Altres interiors", 
                                                            "NOMD01S":"Altres exteriors"})

    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'V0006':'Total dormitoris_aux', 
                                                            "DORM": "Total dormitoris",
                                                            "LAV": "Banys i lavabos",
                                                            "TER": "Terrasses, balcons i patis",
                                                            'NOMD01C':'Superfície útil',
                                                            "Preu_m2_util": "Preu m2 útil",
                                                            'NOMD01P':'Estudi/golfes', 
                                                            'NOMD01Q':'Safareig', 
                                                            'NOMD01K': 'Cuines estàndard', 
                                                            'NOMD01L': 'Cuines americanes', 
                                                            "NOMD01R": "Altres interiors", 
                                                            "NOMD01S":"Altres exteriors"})


    # Canviar de nom tots els equipaments
    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'EQUIC_1': 'Zona enjardinada', 
                                                        'EQUIC_2': 'Parc infantil',
                                                        'EQUIC_3': 'Piscina comunitària', 
                                                        'EQUIC_4': 'Traster', 
                                                        'EQUIC_5': 'Ascensor', 
                                                        'EQUIC_6': 'Equipament Esportiu',  
                                                        'EQUIC_7': 'Sala de jocs', 
                                                        'EQUIC_8': 'Sauna', 
                                                        "EQUIC_9_50": "Altres",
                                                        'EQUIC_99': 'Cap dels anteriors'})
    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'EQUIC_1': 'Zona enjardinada', 
                                                        'EQUIC_2': 'Parc infantil',
                                                        'EQUIC_3': 'Piscina comunitària', 
                                                        'EQUIC_4': 'Traster', 
                                                        'EQUIC_5': 'Ascensor', 
                                                        'EQUIC_6': 'Equipament Esportiu',  
                                                        'EQUIC_7': 'Sala de jocs', 
                                                        'EQUIC_8': 'Sauna', 
                                                        "QUAL_ALTRES": "Altres",
                                                        'EQUIC_99': 'Cap dels anteriors'})
    bbdd_estudi_prom["Ascensor"] = np.where(bbdd_estudi_prom["Ascensor"]>=1, 1, bbdd_estudi_prom["Ascensor"])
    bbdd_estudi_hab["Ascensor"] = np.where(bbdd_estudi_hab["Ascensor"]>=1, 1, bbdd_estudi_hab["Ascensor"])


    # Canviar de nom totes les qualitats
    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {"QUALIC_5": "Aire condicionat", 
                                                        "QUALIC_6": "Bomba de calor", 
                                                        "QUALI_A": "Aerotèrmia", 
                                                        'QUALIC_7':"Calefacció", 
                                                        'QUALIC_8':"Preinstal·lació d'A.C./B. Calor/Calefacció", 
                                                        'QUALIC_9': 'Parquet', 
                                                        'QUALIC_10':'Armaris encastats',
                                                        'QUALIC_12':'Placa de cocció amb gas',
                                                        'QUALIC_13':'Placa de cocció vitroceràmica',
                                                        "QUALIC_14":"Placa d'inducció",
                                                        'QUALIC_22':'Plaques solars'})


    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {"QUALIC_5": "Aire condicionat", 
                                                        "QUALIC_6": "Bomba de calor", 
                                                        "QUALI_A": "Aerotèrmia", 
                                                        'QUALIC_7':"Calefacció", 
                                                        'QUALIC_8':"Preinstal·lació d'A.C./B. Calor/Calefacció", 
                                                        'QUALIC_9': 'Parquet', 
                                                        'QUALIC_10':'Armaris encastats',
                                                        'QUALIC_12':'Placa de cocció amb gas',
                                                        'QUALIC_13':'Placa de cocció vitroceràmica',
                                                        "QUALIC_14":"Placa d'inducció",
                                                        'QUALIC_22':'Plaques solars'})
    #  Canviar nom a tipus de calefacció
    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'CALEFC_3': 'De gasoil', 
                                                        'CALEFC_4': 'De gas natural', 
                                                        'CALEFC_5': 'De propà', 
                                                        'CALEFC_6': "D'electricitat", 
                                                        'CALEFC_9': "No s'indica tipus"})




    bbdd_estudi_prom['TIPV'] = np.where(bbdd_estudi_prom['TIPV_1'] >= 1, "Venda a través d'immobiliària independent",
                                        np.where(bbdd_estudi_prom['TIPV_2'] >= 1, "Venda a través d'immobiliaria del mateix promotor",
                                                np.where(bbdd_estudi_prom['TIPV_3'] >= 1, "Venda directa del promotor", "Sense informació")))


    bbdd_estudi_prom['TIPOL_VENDA'] = np.where(bbdd_estudi_prom['TIPOL_VENDA_1'] == 1, "0D",
                                        np.where(bbdd_estudi_prom['TIPOL_VENDA_2'] == 1, "1D",
                                                np.where(bbdd_estudi_prom['TIPOL_VENDA_3'] == 1, "2D",
                                                        np.where(bbdd_estudi_prom['TIPOL_VENDA_4'] == 1, "3D",
                                                            np.where(bbdd_estudi_prom['TIPOL_VENDA_5'] == 1, "4D", 
                                                                np.where(bbdd_estudi_prom['TIPOL_VENDA_6'] == 1, "5+D", "NA"))))))

                        
                                                    
    #  "Venda a través d'immobiliària independent", "Venda a través d'immobiliaria del mateix promotor", "Venda directa del promotor"

    bbdd_estudi_hab['TIPH'] = bbdd_estudi_hab['TIPH'].map(mapping1)

    bbdd_estudi_hab['ESTO'] = bbdd_estudi_hab['ESTO'].map(mapping2)


    vars = ['Zona enjardinada', 'Parc infantil', 'Piscina comunitària', 
            'Traster', 'Ascensor', 'Equipament Esportiu', 'Sala de jocs', 
            'Sauna', 'Altres', "Aire condicionat", "Bomba de calor", 
            "Aerotèrmia", "Calefacció", "Preinstal·lació d'A.C./B. Calor/Calefacció", 
            "Parquet", "Armaris encastats", 'Placa de cocció amb gas', 
            'Placa de cocció vitroceràmica', "Placa d'inducció", 'Plaques solars', "APAR"]
    vars_aux = ['Zona enjardinada', 'Parc infantil', 'Piscina comunitària', 
            'Traster', 'Ascensor', 'Equipament Esportiu', 'Sala de jocs', 
            'Sauna', 'Altres', "Aire condicionat", "Bomba de calor", 
            "Aerotèrmia", "Calefacció", "Preinstal·lació d'A.C./B. Calor/Calefacció", 
            "Parquet", "Armaris encastats", 'Placa de cocció amb gas', 
            'Placa de cocció vitroceràmica', "Placa d'inducció", 'Plaques solars', "Safareig","Terrasses, balcons i patis"]
    for i in vars:
        bbdd_estudi_prom[i] = bbdd_estudi_prom[i].replace({np.nan : 0})
    for i in vars_aux:
        bbdd_estudi_hab[i] = bbdd_estudi_hab[i].replace({np.nan : 0})
    bbdd_estudi_hab["Calefacció"] = bbdd_estudi_hab["Calefacció"].replace({' ': 0}) 
    bbdd_estudi_prom["Calefacció"] = bbdd_estudi_prom["Calefacció"].replace({' ': 0}) 


    bbdd_estudi_hab["Tram_Sup_util"] = bbdd_estudi_hab["Tram_Sup_util"].str.replace(" ", "")
    bbdd_estudi_hab["Tram_Sup_util"] = bbdd_estudi_hab["Tram_Sup_util"].str[3:]



    # Afegir categories a algunes columnes de la base de dades d'habitatge

    room_dict =  {i: f"{i}D" if i <= 4 else "5+D" for i in range(0, 20)}
    toilet_dict = {i: f"{i} Bany" if i <= 1 else "2 i més Banys" for i in range(1, 20)}
    bbdd_estudi_hab_mod = bbdd_estudi_hab.copy()

    bbdd_estudi_hab_mod['Total dormitoris'] = bbdd_estudi_hab_mod['Total dormitoris'].map(room_dict)
    bbdd_estudi_hab_mod['Banys i lavabos'] = bbdd_estudi_hab_mod['Banys i lavabos'].map(toilet_dict)
    bbdd_estudi_hab_mod["Terrasses, balcons i patis"] = np.where(bbdd_estudi_hab_mod["Terrasses, balcons i patis"]>=1, 1, 0)

    bbdd_estudi_hab["Nom DIST"] = bbdd_estudi_hab["Nom DIST"].str.replace(r'^\d{2}\s', '', regex=True)
    bbdd_estudi_hab_mod["Nom DIST"] = bbdd_estudi_hab_mod["Nom DIST"].str.replace(r'^\d{2}\s', '', regex=True)

    return([bbdd_estudi_prom, bbdd_estudi_hab, bbdd_estudi_hab_mod])

bbdd_estudi_prom_2024, bbdd_estudi_hab_2024, bbdd_estudi_hab_mod_2024 = tidy_bbdd_2024(bbdd_estudi_prom_2024, bbdd_estudi_hab_2024, 2024)


############################################################  IMPORTAMOS BBDD FINAL 1S2025 ################################################
@st.cache_resource
def tidy_bbdd_semestral(df_prom, df_hab, any):
    bbdd_estudi_prom = df_prom.copy()
    bbdd_estudi_prom.columns = bbdd_estudi_prom.iloc[0,:]
    bbdd_estudi_prom = bbdd_estudi_prom[bbdd_estudi_prom["ESTUDI"]==any]
    bbdd_estudi_prom['TIPO_aux'] = np.where(bbdd_estudi_prom['TIPO'].isin([1,2]), 'Habitatges unifamiliars', 'Habitatges plurifamiliars')

    mapping = {1: 'Unifamiliars aïllats', 
            2: 'Unifamiliars adossats', 
            3: 'Plurifamiliars en bloc obert', 
            4: 'Plurifamiliars en bloc tancat'}

    mapping1 = {1: "De nova Construcció",
                2: "Rehabilitació integral"}

    mapping2 = {1: "Pendent d'enderroc", 
            2: "Solar", 
            3: "Buidat", 
            4: "Cimentació",
            5: "Estructura",
            6: "Tancaments exteriors",
            7: "Tancaments interiors",
            8: "Claus en mà",
            9: "NS/NC"}

    mapping3 = {
                    1: 'A',
                    1.2:"A",
                    2: 'B',
                    2.3: "B",
                    3: 'C',
                    4: 'D',
                    4.5: "D",
                    5: 'E',
                    5.3 : "C",
                    6: "F",
                    7: "G",
                    8: "En tràmits",
                    9: "Sense informació"
    }

    mapping4 = {
                    0: "Altres",
                    1: "Plaça d'aparcament opcional",
                    2: "Plaça d'aparcament inclosa",
                    3: "Sense plaça d'aparcament",
    }



    bbdd_estudi_prom['TIPO'] = bbdd_estudi_prom['TIPO'].map(mapping)

    bbdd_estudi_prom['TIPH'] = bbdd_estudi_prom['TIPH'].map(mapping1)


    bbdd_estudi_prom['ESTO'] = bbdd_estudi_prom['ESTO'].map(mapping2)

    bbdd_estudi_prom['QENERGC'] = bbdd_estudi_prom['QENERGC'].map(mapping3)

    bbdd_estudi_prom['APAR'] = bbdd_estudi_prom['APAR'].map(mapping4)


    # Importar BBDD habitatges
    # bbdd_estudi_hab = pd.read_excel(path + 'BBDD juny 2024 APCE.xlsx', sheet_name='Habitatges 2024')
    bbdd_estudi_hab = df_hab.copy()
    bbdd_estudi_hab.columns = bbdd_estudi_hab.iloc[0,:]
    bbdd_estudi_hab = bbdd_estudi_hab[bbdd_estudi_hab["ESTUDI"]==any]





    # ["Total dormitoris","Banys i lavabos","Cuines estàndard","Cuines americanes","Terrasses, balcons i patis","Estudi/golfes","Safareig","Altres interiors","Altres exteriors"]

    # ["DORM", "LAV", "cuina_normal", "cuina_amer", "TER", "Golfes", "Safareig","Altres interiors","Altres exteriors" ]

    bbdd_estudi_hab['TIPOG'] = np.where(bbdd_estudi_hab['TIPO'].isin([1,2]), 'Habitatges unifamiliars', 'Habitatges plurifamiliars')
    bbdd_estudi_hab['TIPO'] = bbdd_estudi_hab['TIPO'].map(mapping)
    bbdd_estudi_hab['QENERGC'] = bbdd_estudi_hab['QENERGC'].map(mapping3)
    bbdd_estudi_hab['APAR'] = bbdd_estudi_hab['APAR'].map(mapping4)

    bbdd_estudi_hab = bbdd_estudi_hab.dropna(axis=1 , how ='all')



    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'V0006':'Total dormitoris_aux', 
                                                            "DORM": "Total dormitoris",
                                                            "LAV": "Banys i lavabos",
                                                            "TER": "Terrasses, balcons i patis",
                                                            'NOMD01C':'Superfície útil',
                                                            "Preu_m2_util": "Preu m2 útil",
                                                            "NOMD01F_2022": "Preu mitjà",
                                                            'NOMD01P':'Estudi/golfes', 
                                                            'NOMD01Q':'Safareig', 
                                                            'NOMD01K': 'Cuines estàndard', 
                                                            'NOMD01L': 'Cuines americanes', 
                                                            "NOMD01R": "Altres interiors", 
                                                            "NOMD01S":"Altres exteriors"})

    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'V0006':'Total dormitoris_aux', 
                                                            "DORM": "Total dormitoris",
                                                            "LAV": "Banys i lavabos",
                                                            "TER": "Terrasses, balcons i patis",
                                                            'NOMD01C':'Superfície útil',
                                                            "Preu_m2_util": "Preu m2 útil",
                                                            'NOMD01P':'Estudi/golfes', 
                                                            'NOMD01Q':'Safareig', 
                                                            'NOMD01K': 'Cuines estàndard', 
                                                            'NOMD01L': 'Cuines americanes', 
                                                            "NOMD01R": "Altres interiors", 
                                                            "NOMD01S":"Altres exteriors"})


    # Canviar de nom tots els equipaments
    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'EQUIC_1': 'Zona enjardinada', 
                                                        'EQUIC_2': 'Parc infantil',
                                                        'EQUIC_3': 'Piscina comunitària', 
                                                        'EQUIC_4': 'Traster', 
                                                        'EQUIC_5': 'Ascensor', 
                                                        'EQUIC_6': 'Equipament Esportiu',  
                                                        'EQUIC_7': 'Sala de jocs', 
                                                        'EQUIC_8': 'Sauna', 
                                                        "EQUIC_9_50": "Altres",
                                                        'EQUIC_99': 'Cap dels anteriors'})
    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'EQUIC_1': 'Zona enjardinada', 
                                                        'EQUIC_2': 'Parc infantil',
                                                        'EQUIC_3': 'Piscina comunitària', 
                                                        'EQUIC_4': 'Traster', 
                                                        'EQUIC_5': 'Ascensor', 
                                                        'EQUIC_6': 'Equipament Esportiu',  
                                                        'EQUIC_7': 'Sala de jocs', 
                                                        'EQUIC_8': 'Sauna', 
                                                        "QUAL_ALTRES": "Altres",
                                                        'EQUIC_99': 'Cap dels anteriors'})
    bbdd_estudi_prom["Ascensor"] = np.where(bbdd_estudi_prom["Ascensor"]>=1, 1, bbdd_estudi_prom["Ascensor"])
    bbdd_estudi_hab["Ascensor"] = np.where(bbdd_estudi_hab["Ascensor"]>=1, 1, bbdd_estudi_hab["Ascensor"])


    # Canviar de nom totes les qualitats
    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {"QUALIC_5": "Aire condicionat", 
                                                        "QUALIC_6": "Bomba de calor", 
                                                        "QUALI_A": "Aerotèrmia", 
                                                        'QUALIC_7':"Calefacció", 
                                                        'QUALIC_8':"Preinstal·lació d'A.C./B. Calor/Calefacció", 
                                                        'QUALIC_9': 'Parquet', 
                                                        'QUALIC_10':'Armaris encastats',
                                                        'QUALIC_12':'Placa de cocció amb gas',
                                                        'QUALIC_13':'Placa de cocció vitroceràmica',
                                                        "QUALIC_14":"Placa d'inducció",
                                                        'QUALIC_22':'Plaques solars'})


    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {"QUALIC_5": "Aire condicionat", 
                                                        "QUALIC_6": "Bomba de calor", 
                                                        "QUALI_A": "Aerotèrmia", 
                                                        'QUALIC_7':"Calefacció", 
                                                        'QUALIC_8':"Preinstal·lació d'A.C./B. Calor/Calefacció", 
                                                        'QUALIC_9': 'Parquet', 
                                                        'QUALIC_10':'Armaris encastats',
                                                        'QUALIC_12':'Placa de cocció amb gas',
                                                        'QUALIC_13':'Placa de cocció vitroceràmica',
                                                        "QUALIC_14":"Placa d'inducció",
                                                        'QUALIC_22':'Plaques solars'})
    #  Canviar nom a tipus de calefacció
    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'CALEFC_3': 'De gasoil', 
                                                        'CALEFC_4': 'De gas natural', 
                                                        'CALEFC_5': 'De propà', 
                                                        'CALEFC_6': "D'electricitat", 
                                                        'CALEFC_9': "No s'indica tipus"})




    bbdd_estudi_prom['TIPV'] = np.where(bbdd_estudi_prom['TIPV_1'] >= 1, "Venda a través d'immobiliària independent",
                                        np.where(bbdd_estudi_prom['TIPV_2'] >= 1, "Venda a través d'immobiliaria del mateix promotor",
                                                np.where(bbdd_estudi_prom['TIPV_3'] >= 1, "Venda directa del promotor", "Sense informació")))


    # bbdd_estudi_prom['TIPOL_VENDA'] = np.where(bbdd_estudi_prom['TIPOL_VENDA_1'] == 1, "0D",
    #                                     np.where(bbdd_estudi_prom['TIPOL_VENDA_2'] == 1, "1D",
    #                                             np.where(bbdd_estudi_prom['TIPOL_VENDA_3'] == 1, "2D",
    #                                                     np.where(bbdd_estudi_prom['TIPOL_VENDA_4'] == 1, "3D",
    #                                                         np.where(bbdd_estudi_prom['TIPOL_VENDA_5'] == 1, "4D", 
    #                                                             np.where(bbdd_estudi_prom['TIPOL_VENDA_6'] == 1, "5+D", "NA"))))))

                        
                                                    
    #  "Venda a través d'immobiliària independent", "Venda a través d'immobiliaria del mateix promotor", "Venda directa del promotor"

    bbdd_estudi_hab['TIPH'] = bbdd_estudi_hab['TIPH'].map(mapping1)

    bbdd_estudi_hab['ESTO'] = bbdd_estudi_hab['ESTO'].map(mapping2)


    vars = ['Zona enjardinada', 'Parc infantil', 'Piscina comunitària', 
            'Traster', 'Ascensor', 'Equipament Esportiu', 
            'Sauna', 'Altres', "Aire condicionat", "Bomba de calor", 
            "Aerotèrmia", "Calefacció", "Preinstal·lació d'A.C./B. Calor/Calefacció", 
            "Parquet", "Armaris encastats", 'Placa de cocció amb gas', 
            'Placa de cocció vitroceràmica', "Placa d'inducció", 'Plaques solars', "APAR"]
    vars_aux = ['Zona enjardinada', 'Parc infantil', 'Piscina comunitària', 
            'Traster', 'Ascensor', 'Equipament Esportiu', 
            'Sauna', 'Altres', "Aire condicionat", "Bomba de calor", 
            "Aerotèrmia", "Calefacció", "Preinstal·lació d'A.C./B. Calor/Calefacció", 
            "Parquet", "Armaris encastats", 'Placa de cocció amb gas', 
            'Placa de cocció vitroceràmica', "Placa d'inducció", 'Plaques solars', "Safareig","Terrasses, balcons i patis"]
    for i in vars:
        bbdd_estudi_prom[i] = bbdd_estudi_prom[i].replace({np.nan : 0})
    for i in vars_aux:
        bbdd_estudi_hab[i] = bbdd_estudi_hab[i].replace({np.nan : 0})
    bbdd_estudi_hab["Calefacció"] = bbdd_estudi_hab["Calefacció"].replace({' ': 0}) 
    bbdd_estudi_prom["Calefacció"] = bbdd_estudi_prom["Calefacció"].replace({' ': 0}) 


    bbdd_estudi_hab["Tram_Sup_util"] = bbdd_estudi_hab["Tram_Sup_util"].str.replace(" ", "")
    bbdd_estudi_hab["Tram_Sup_util"] = bbdd_estudi_hab["Tram_Sup_util"].str[3:]



    # Afegir categories a algunes columnes de la base de dades d'habitatge

    room_dict =  {i: f"{i}D" if i <= 4 else "5+D" for i in range(0, 20)}
    toilet_dict = {i: f"{i} Bany" if i <= 1 else "2 i més Banys" for i in range(1, 20)}
    bbdd_estudi_hab_mod = bbdd_estudi_hab.copy()

    bbdd_estudi_hab_mod['Total dormitoris'] = bbdd_estudi_hab_mod['Total dormitoris'].map(room_dict)
    bbdd_estudi_hab_mod['Banys i lavabos'] = bbdd_estudi_hab_mod['Banys i lavabos'].map(toilet_dict)
    bbdd_estudi_hab_mod["Terrasses, balcons i patis"] = np.where(bbdd_estudi_hab_mod["Terrasses, balcons i patis"]>=1, 1, 0)

    bbdd_estudi_hab["Nom DIST"] = bbdd_estudi_hab["Nom DIST"].str.replace(r'^\d{2}\s', '', regex=True)
    bbdd_estudi_hab_mod["Nom DIST"] = bbdd_estudi_hab_mod["Nom DIST"].str.replace(r'^\d{2}\s', '', regex=True)

    return([bbdd_estudi_prom, bbdd_estudi_hab, bbdd_estudi_hab_mod])

bbdd_estudi_prom_2025, bbdd_estudi_hab_2025, bbdd_estudi_hab_mod_2025 = tidy_bbdd_semestral(bbdd_estudi_prom_2025, bbdd_estudi_hab_2025, 2025)


############################################################  IMPORTAR HISTÓRICO DE MUNICIPIOS 2016 - 2024 ################################################
@st.cache_resource
def import_hist_mun(df_1819, df_2021, df_22, df_23, df_24, df_25, maestro_df):
    # mun_2018_2019 = pd.read_excel(path + "Resum 2018 - 2019.xlsx", sheet_name="Municipis 2018-2019")
    mun_2018_2019 = df_1819.copy()
    mun_2019 = mun_2018_2019.iloc[:,14:27]

    # mun_2020_2021 = pd.read_excel(path + "Resum 2020 - 2021.xlsx", sheet_name="Municipis")
    mun_2020_2021 = df_2021.copy()
    mun_2020 = mun_2020_2021.iloc[:,:13]
    mun_2020 = mun_2020.dropna(how ='all',axis=0)
    mun_2021 = mun_2020_2021.iloc[:,14:27]
    mun_2021 = mun_2021.dropna(how ='all',axis=0)

    # mun_2022 = pd.read_excel(path + "Resum 2022.xlsx", sheet_name="Municipis")
    mun_2022 = df_22.copy()
    mun_2022 = mun_2022.iloc[:,14:27]
    mun_2022 = mun_2022.dropna(how ='all',axis=0)

    # mun_2023 = pd.read_excel(path + "Resum 2023.xlsx", sheet_name="Municipis")
    mun_2023 = df_23.copy()
    mun_2023 = mun_2023.iloc[:,14:27]
    mun_2023 = mun_2023.dropna(how ='all',axis=0)

    mun_2024 = df_24.copy()
    mun_2024 = mun_2024.iloc[:,14:27]
    mun_2024 = mun_2024.dropna(how ='all',axis=0)

    mun_2025 = df_25.copy()
    mun_2025 = mun_2025.iloc[:,14:27]
    mun_2025 = mun_2025.dropna(how ='all',axis=0)

    # maestro_estudi = pd.read_excel(path + "Maestro estudi_oferta.xlsx", sheet_name="Maestro")
    maestro_estudi = maestro_df.copy()

    return([mun_2019, mun_2020, mun_2021, mun_2022, mun_2023, mun_2024, mun_2025, maestro_estudi])
mun_2019, mun_2020, mun_2021, mun_2022, mun_2023, mun_2024, mun_2025, maestro_estudi = import_hist_mun(mun_2018_2019, mun_2020_2021, mun_2022, mun_2023, mun_2024, mun_2025, maestro_estudi)

############################################################  IMPORTAR HISTÓRICO DE DISTRITOS DE BCN 2016 - 2024 ################################################
@st.cache_resource
def import_hist_dis(df_1819, df_2021, df_22, df_23, df_24, df_25):
    # dis_2018_2019 = pd.read_excel(path + "Resum 2018 - 2019.xlsx", sheet_name="BCN+districtes+barris")
    dis_2018_2019 = df_1819.copy()   
    dis_2019 = dis_2018_2019.iloc[:,14:27]

    # dis_2020_2021 = pd.read_excel(path + "Resum 2020 - 2021.xlsx", sheet_name="BCN+districtes+barris")
    dis_2020_2021 = df_2021.copy() 
    dis_2020 = dis_2020_2021.iloc[:,:13]
    dis_2020 = dis_2020.dropna(how ='all',axis=0)
    dis_2021 = dis_2020_2021.iloc[:,14:27]
    dis_2021 = dis_2021.dropna(how ='all',axis=0)

    # dis_2022 = pd.read_excel(path + "Resum 2022.xlsx", sheet_name="BCN+districtes+barris")
    dis_2022 = df_22.copy()
    dis_2022 = dis_2022.iloc[:,14:27]
    dis_2022 = dis_2022.dropna(how ='all',axis=0)

    # dis_2023 = pd.read_excel(path + "Resum 2023.xlsx", sheet_name="BCN districte+barris")
    dis_2023 = df_23.copy()
    dis_2023 = dis_2023.iloc[:,14:27]
    dis_2023 = dis_2023.dropna(how ='all',axis=0)

    dis_2024 = df_24.copy()
    dis_2024 = dis_2024.iloc[:,14:27]
    dis_2024 = dis_2024.dropna(how ='all',axis=0)

    dis_2025 = df_25.copy()
    dis_2025 = dis_2025.iloc[:,14:27]
    dis_2025 = dis_2025.dropna(how ='all',axis=0)

    return([dis_2019, dis_2020, dis_2021, dis_2022, dis_2023, dis_2024, dis_2025])
dis_2019, dis_2020, dis_2021, dis_2022, dis_2023, dis_2024, dis_2025 = import_hist_dis(dis_2018_2019, dis_2020_2021, dis_2022, dis_2023, dis_2024, dis_2025)
############################################################  IMPORTAR HISTÓRICO DE DISTRITOS DE BCN 2016 - 2024 ################################################
@st.cache_resource
def tidy_data(mun_year, year):
    df =mun_year.T
    df.columns = df.iloc[0,:]
    df = df.iloc[1:,:].reset_index()
    df.columns.values[:3] = ['Any', 'Tipologia', "Variable"]
    df['Tipologia'] = df['Tipologia'].ffill()
    df['Any'] = year
    geo = df.columns[3:].values
    df_melted = pd.melt(df, id_vars=['Any', 'Tipologia', 'Variable'], value_vars=geo, value_name='Valor')
    df_melted.columns.values[3] = 'GEO'
    return(df_melted)
############################################################  CALCULOS PROVINCIAS, AMBITOS TERRITORIALES Y COMARCAS ################################################
def weighted_mean(data):
    weighted_sum = (data['Valor'] * data['Unitats']).sum()
    sum_peso = data['Unitats'].sum()
    # data["Valor"] = weighted_sum / sum_peso
    return weighted_sum / sum_peso
@st.cache_resource
def geo_mun():
    df_vf_aux = pd.DataFrame()

    for df_frame, year in zip(["mun_2019", "mun_2020", "mun_2021", "mun_2022", "mun_2023", "mun_2024", "mun_2025"], [2019, 2020, 2021, 2022, 2023, 2024, 2025]):
        df_vf_aux = pd.concat([df_vf_aux, tidy_data(eval(df_frame), year)], axis=0)


    df_vf_aux['Variable']= np.where(df_vf_aux['Variable']=="Preu de     venda per      m² útil (€)", "Preu de venda per m² útil (€)", df_vf_aux['Variable'])
    df_vf_aux['Valor'] = pd.to_numeric(df_vf_aux['Valor'], errors='coerce')
    df_vf_aux['GEO'] = np.where(df_vf_aux['GEO']=="Municipis de Catalunya", "Catalunya", df_vf_aux['GEO'])
    df_vf_aux = df_vf_aux[~df_vf_aux['GEO'].str.contains("província|Província|Municipis")]

    df_vf_merged = pd.merge(df_vf_aux, maestro_estudi, how="left", on="GEO")
    df_vf_merged = df_vf_merged[~df_vf_merged["Província"].isna()].dropna(axis=1, how="all")
    df_vf = df_vf_merged[df_vf_merged["Variable"]!="Unitats"]
    df_unitats = df_vf_merged[df_vf_merged["Variable"]=="Unitats"].drop("Variable", axis=1)
    df_unitats = df_unitats.rename(columns={"Valor": "Unitats"})
    df_final_cat = pd.merge(df_vf, df_unitats, how="left")
    df_final = df_final_cat[df_final_cat["GEO"]!="Catalunya"]
    df_final_cat_aux1 = df_final_cat[df_final_cat["GEO"]=="Catalunya"][["Any", "Tipologia", "Variable","Valor"]]
    cat_df_aux2_melted = pd.melt(df_final_cat[df_final_cat["GEO"]=="Catalunya"][["Any", "Tipologia", "Unitats"]], id_vars=["Any", "Tipologia"], var_name="Variable", value_name="Valor")
    df_final_cat = pd.concat([df_final_cat_aux1, cat_df_aux2_melted], axis=0)


    ambits_df_aux1 = df_final.set_index(["Any", "Tipologia", "Variable", "Àmbits territorials"]).groupby(["Any", "Tipologia", "Variable", "Àmbits territorials"]).apply(weighted_mean).reset_index().rename(columns= {0:"Valor"})
    ambits_df_aux2 = df_final[["Any","Àmbits territorials","Tipologia", "GEO", "Unitats"]].drop_duplicates(["Any","Àmbits territorials","Tipologia", "GEO", "Unitats"]).drop("GEO", axis=1).groupby(["Any", "Àmbits territorials", "Tipologia"]).sum().reset_index()
    ambits_df_aux2_melted = pd.melt(ambits_df_aux2, id_vars=["Any", "Tipologia", "Àmbits territorials"], var_name="Variable", value_name="Valor")
    ambits_df = pd.concat([ambits_df_aux1, ambits_df_aux2_melted], axis=0)
    ambits_df = ambits_df.rename(columns={"Àmbits territorials":"GEO"})

    comarques_df_aux1 = df_final.set_index(["Any", "Tipologia", "Variable", "Comarques"]).groupby(["Any", "Tipologia", "Variable", "Comarques"]).apply(weighted_mean).reset_index().rename(columns= {0:"Valor"}).dropna(axis=0)
    comarques_df_aux2 = df_final[["Any","Comarques","Tipologia", "GEO", "Unitats"]].drop_duplicates(["Any","Comarques","Tipologia", "GEO", "Unitats"]).drop("GEO", axis=1).groupby(["Any", "Comarques", "Tipologia"]).sum().reset_index()
    comarques_df_aux2_melted = pd.melt(comarques_df_aux2, id_vars=["Any", "Tipologia", "Comarques"], var_name="Variable", value_name="Valor")
    comarques_df = pd.concat([comarques_df_aux1, comarques_df_aux2_melted], axis=0)
    comarques_df = comarques_df.rename(columns={"Comarques":"GEO"})

    provincia_df_aux1 = df_final.set_index(["Any", "Tipologia", "Variable", "Província"]).groupby(["Any", "Tipologia", "Variable", "Província"]).apply(weighted_mean).reset_index().rename(columns= {0:"Valor"})
    provincia_df_aux2 = df_final[["Any","Província","Tipologia", "GEO", "Unitats"]].drop_duplicates(["Any","Província","Tipologia", "GEO", "Unitats"]).drop("GEO", axis=1).groupby(["Any", "Província", "Tipologia"]).sum().reset_index()
    provincia_df_aux2_melted = pd.melt(provincia_df_aux2, id_vars=["Any", "Tipologia", "Província"], var_name="Variable", value_name="Valor")
    provincia_df = pd.concat([provincia_df_aux1, provincia_df_aux2_melted], axis=0)
    provincia_df = provincia_df.rename(columns={"Província":"GEO"})
    return([df_vf_aux, df_vf, df_final_cat, df_final, ambits_df, comarques_df, provincia_df])
df_vf_aux, df_vf, df_final_cat, df_final, ambits_df, comarques_df, provincia_df = geo_mun()

@st.cache_resource
def geo_dis_long():
    df_vf_aux = pd.DataFrame()
    for df_frame, year in zip(["dis_2019", "dis_2020", "dis_2021", "dis_2022", "dis_2023", "dis_2024", "dis_2025"], [2019, 2020, 2021, 2022, 2023, 2024, 2025]):
        df_vf_aux = pd.concat([df_vf_aux, tidy_data(eval(df_frame), year)], axis=0)
    df_vf_aux['Variable']= np.where(df_vf_aux['Variable']=="Preu de     venda per      m² útil (€)", "Preu de venda per m² útil (€)", df_vf_aux['Variable'])
    df_vf_aux['Valor'] = pd.to_numeric(df_vf_aux['Valor'], errors='coerce')
    df_vf_aux = df_vf_aux[df_vf_aux['GEO']!="Municipi de Barcelona"]

    df_vf_aux = df_vf_aux[df_vf_aux["GEO"].isin(["Ciutat Vella", "01 Ciutat Vella",  "Eixample", "02 Eixample", "Sants-Montjuïc", "03 Sants-Montjuïc", 
                                        "Les Corts", "04 Les Corts", "Sarrià-Sant Gervasi", "Sarrià - Sant Gervasi", "05 Sarrià - Sant Gervasi", "Gràcia", "06 Gràcia",
                                        "Horta-Guinardó", "07 Horta-Guinardó", "Nou Barris", "08 Nou Barris", "Sant Andreu", "09 Sant Andreu",
                                        "Sant Martí", "10 Sant Martí"])]
    df_vf_aux["GEO"] = df_vf_aux["GEO"].str.replace("Sarrià-Sant Gervasi", "Sarrià - Sant Gervasi")
    for i in ["01 ", "02 ", "03 ", "04 ", "05 ", "06 ", "07 ", "08 ", "09 ", "10 "]:
        df_vf_aux["GEO"] = df_vf_aux["GEO"].str.replace(i, "")
    df_vf_aux = df_vf_aux.drop_duplicates(subset=["Any", "Tipologia", "Variable", "GEO"], keep='first')
    return(df_vf_aux)
df_dis_long = geo_dis_long()

def filedownload(df, filename):
    towrite = io.BytesIO()
    df.to_excel(towrite, index=True, header=True)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode("latin-1")
    href = f"""
    <div class="download-button-container">
        <a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">
            <button class="download-button">Descarregar</button>
        </a>
    </div>
    """
    return href

############################################################ CATALUNYA FUNCIONS #########################################################
# @st.cache_resource
def map_prov_prom(df_prom, shapefile_prov):
    provprom_map = df_prom[["PROVINCIA"]].value_counts().reset_index()
    provprom_map.columns = ["NAME_2", "PROMOCIONS"]
    fig, ax = plt.subplots(1,1, figsize=(10,10))
    divider = make_axes_locatable(ax)
    tmp = shapefile_prov.copy()
    tmp = pd.merge(tmp, provprom_map, how="left", on="NAME_2")
    # cax = divider.append_axes("right", size="3%", pad=-1) #resize the colorbar
    cmap = colors.LinearSegmentedColormap.from_list("mi_paleta", ["#DAE4E0","#008B6C"]) 
    tmp.plot(column='PROMOCIONS', ax=ax, cmap=cmap, legend=False)
    tmp.geometry.boundary.plot(color='black', ax=ax, linewidth=0.3) #Add some borders to the geometries
    for i, row in tmp.iterrows():
        x, y = row['geometry'].centroid.coords[0]
        ax.annotate(f"""{row['NAME_2']}\n{row["PROMOCIONS"]}""", xy=(x, y), xytext=(3,3), textcoords="offset points", fontsize=10, color="black")
                        # bbox=dict(facecolor='white', alpha=0.5)
                        # arrowprops=dict(facecolor='black', arrowstyle="->")
                        
    ax.axis('off')
    fig.patch.set_alpha(0)
    return(fig)
@st.cache_resource
def plot_caracteristiques(df_hab):
    table61_tipo = df_hab.groupby(['Total dormitoris', 'Banys i lavabos']).size().div(len(df_hab)).reset_index(name='Proporcions').sort_values(by="Proporcions", ascending=False)
    table61_tipo["Proporcions"] = table61_tipo["Proporcions"]*100
    table61_tipo["Tipologia"] = np.where(table61_tipo["Banys i lavabos"]==1, table61_tipo["Total dormitoris"].astype(str) + " dormitoris i " + table61_tipo["Banys i lavabos"].astype(str) + " bany", table61_tipo["Total dormitoris"].astype(str) + " dormitoris i " + table61_tipo["Banys i lavabos"].astype(str) + " banys")
    fig = px.bar(table61_tipo.head(4), x="Proporcions", y="Tipologia", orientation='h', title="", 
    labels={'x':"Proporcions sobre el total d'habitatges", 'y':"Tipologia"})
    fig.layout.xaxis.title.text = "Proporcions sobre el total d'habitatges"
    fig.layout.yaxis.title.text = "Tipologia"
    fig.layout.title.text = "Principals tipologies dels habitatges en oferta (%)"
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    fig.update_traces(marker=dict(color="#66b9a7"))
    return(fig)

@st.cache_resource
def plot_rehabilitacio_cat(df_hab):
    table38hab_cat = df_hab[["TIPH"]].value_counts().reset_index().sort_values(["TIPH"])
    table38hab_cat.columns = ["TIPOLOGIA", "Habitatges"]
    table38hab_cat = table38hab_cat.pivot_table(columns="TIPOLOGIA", values="Habitatges").reset_index()
    table38hab_cat = table38hab_cat.T.reset_index()
    table38hab_cat.columns = ["Tipus", "Habitatges en oferta"]
    table38hab_cat = table38hab_cat[table38hab_cat["Tipus"]!="index"]
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=table38hab_cat["Tipus"],
        values=table38hab_cat["Habitatges en oferta"],
        hole=0.5, 
        showlegend=True, 
        marker=dict(
            colors=["#66b9a7", "#00D0A3"], 
            line=dict(color='#FFFFFF', width=1) 
        ),
        textposition='outside',
        textinfo='percent+label' 
    ))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    fig.update_layout(
        title=f"Habitatges en oferta de rehabilitació integral i d'obra nova a Catalunya (%)",
        font=dict(size=12),
        legend=dict(
            x=0.7,  # Set legend position
            y=0.85
        )
    )
    return(fig)
@st.cache_resource
def plot_qualitats(df_hab):
    table62_hab = df_hab[["Aire condicionat","Bomba de calor","Aerotèrmia","Calefacció","Preinstal·lació d'A.C./B. Calor/Calefacció",'Parquet','Armaris encastats','Placa de cocció amb gas','Placa de cocció vitroceràmica',"Placa d'inducció",'Plaques solars']].rename(columns={"Aerotèrmia":"Aerotèrmia"}).sum(axis=0)
    table62_hab = pd.DataFrame({"Qualitats":table62_hab.index, "Total":table62_hab.values})
    table62_hab = table62_hab.set_index("Qualitats").apply(lambda row: (row / df_hab.shape[0])*100).reset_index().sort_values("Total", ascending=True)
    fig = px.bar(table62_hab, x="Total", y="Qualitats", orientation='h', title="", labels={'x':"Proporcions sobre el total d'habitatges", 'y':"Qualitats"})
    fig.layout.xaxis.title.text = "Proporcions sobre el total d'habitatges (%)"
    fig.layout.yaxis.title.text = "Qualitats"
    fig.update_traces(marker=dict(color="#66b9a7"))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def plot_equipaments(df_hab):
    table67_hab = df_hab[["Zona enjardinada", "Parc infantil", "Piscina comunitària", "Traster", "Ascensor", "Equipament Esportiu", "Sala de jocs", "Sauna", "Altres", "Cap dels anteriors"]].sum(axis=0, numeric_only=True)
    table67_hab = pd.DataFrame({"Equipaments":table67_hab.index, "Total":table67_hab.values})
    table67_hab = table67_hab.set_index("Equipaments").apply(lambda row: row.mul(100) / df_hab.shape[0]).reset_index().sort_values("Total", ascending=True)
    fig = px.bar(table67_hab, x="Total", y="Equipaments", orientation='h', title="", labels={'x':"Proporcions sobre el total d'habitatges", 'y':"Equipaments"})
    fig.layout.xaxis.title.text = "Proporcions sobre el total d'habitatges (%)"
    fig.layout.yaxis.title.text = "Equipaments"
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    fig.update_traces(marker=dict(color="#66b9a7"))
    return(fig)
@st.cache_resource
def indicadors_preu_mitjanes(df_hab):
    table76_tipo = df_hab[["Total dormitoris", "TIPOG","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris", "TIPOG"]).groupby(["TIPOG", "Total dormitoris"]).mean().reset_index()
    table76_total = df_hab[["Total dormitoris","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris"]).groupby(["Total dormitoris"]).mean().reset_index()
    table76_total["TIPOG"] = "Total habitatges"
    table76 = pd.concat([table76_tipo, table76_total], axis=0)
    table76 = pd.merge(table76, df_hab[["TIPOG","Total dormitoris"]].groupby(["TIPOG","Total dormitoris"]).size().reset_index().rename(columns={0:"Total"}), how="left", on=["TIPOG","Total dormitoris"])
    table76 = table76.rename(columns={"TIPOG":"Tipologia"})
    fig = px.bar(table76, x="Preu mitjà", y="Total dormitoris", color="Tipologia", orientation='h', color_discrete_sequence=["#00D0A3","#AAC4BA","#008B6C"], barmode="group", title="", labels={'x':"Preu m\u00b2 útil (mitjana)", 'y':"Tipologia d'habitatge"})
    fig.layout.xaxis = dict(title="Preu mitjà", tickformat=",d")
    fig.layout.yaxis = dict(title="Tipologia d'habitatge")
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    fig.update_layout(font=dict(size=13), legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.75))
    return(fig)
@st.cache_resource
def indicadors_preum2_mitjanes(df_hab):
    table76_tipo = df_hab[["Total dormitoris", "TIPOG","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris", "TIPOG"]).groupby(["TIPOG", "Total dormitoris"]).mean().reset_index()
    table76_total = df_hab[["Total dormitoris","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris"]).groupby(["Total dormitoris"]).mean().reset_index()
    table76_total["TIPOG"] = "Total habitatges"
    table76 = pd.concat([table76_tipo, table76_total], axis=0)
    table76 = pd.merge(table76, df_hab[["TIPOG","Total dormitoris"]].groupby(["TIPOG","Total dormitoris"]).size().reset_index().rename(columns={0:"Total"}), how="left", on=["TIPOG","Total dormitoris"])
    table76 = table76.rename(columns={"TIPOG":"Tipologia"})
    fig = px.bar(table76, x="Preu m2 útil", y="Total dormitoris", color="Tipologia", orientation='h', color_discrete_sequence=["#00D0A3","#AAC4BA","#008B6C"], barmode="group", title="", labels={'x':"Preu m\u00b2 útil (mitjana)", 'y':"Tipologia d'habitatge"})
    fig.layout.xaxis = dict(title="Preu per m\u00b2 útil", tickformat=",d")
    fig.layout.yaxis.title.text = "Tipologia d'habitatge"
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    fig.update_layout(font=dict(size=13), legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.75))
    return(fig)
@st.cache_resource
def indicadors_super_mitjanes(df_hab):
    table76_tipo = df_hab[["Total dormitoris", "TIPOG","Superfície útil", "Preu mitjà", "Preu m2 útil"]].groupby(["TIPOG", "Total dormitoris"]).mean().reset_index()
    table76_total = df_hab[["Total dormitoris","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris"]).groupby(["Total dormitoris"]).mean().reset_index()
    table76_total["TIPOG"] = "Total habitatges"
    table76 = pd.concat([table76_tipo, table76_total], axis=0)
    table76 = pd.merge(table76, df_hab[["TIPOG","Total dormitoris"]].groupby(["TIPOG","Total dormitoris"]).size().reset_index().rename(columns={0:"Total"}), how="left", on=["TIPOG","Total dormitoris"])
    table76 = table76.rename(columns={"TIPOG":"Tipologia"})
    fig = px.bar(table76, x="Superfície útil", y="Total dormitoris", color="Tipologia", orientation='h', color_discrete_sequence=["#00D0A3","#AAC4BA","#008B6C"], barmode="group", title="", labels={'x':"Preu m\u00b2 útil (mitjana)", 'y':"Tipologia d'habitatge"})
    fig.layout.xaxis.title.text = "Superfície útil"
    fig.layout.yaxis.title.text = "Tipologia d'habitatge"
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    fig.update_layout(font=dict(size=13), legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.75))
    return(fig)
@st.cache_resource
def plot_var_CAT(df117, df121, df125):
    # table117 = pd.read_excel(path + "Estudi_oferta_taules 2022.xlsx", sheet_name="table117", header=1).iloc[1:,]
    table117 = df117.copy()
    # table121 = pd.read_excel(path + "Estudi_oferta_taules 2022.xlsx", sheet_name="table121", header=1).iloc[1:,]
    table121 = df121.copy()
    # table125 = pd.read_excel(path + "Estudi_oferta_taules 2022.xlsx", sheet_name="table125", header=1).iloc[1:,]
    table125 = df125.copy()
    table117 = table117[(table117["Província"].isna()) & (table117["Municipi"].isna())][["Variació % Preu m2 útil","Variació % Preu mitjà", "Variació % Superfície útil"]]
    table121 = table121[(table121["Província"].isna()) & (table121["Municipi"].isna())][["Variació % Preu m2 útil","Variació % Preu mitjà", "Variació % Superfície útil"]]
    table125 = table125[(table125["Província"].isna()) & (table125["Municipi"].isna())][["Variació % Preu m2 útil","Variació % Preu mitjà", "Variació % Superfície útil"]]
    table_var = pd.concat([table117, table121, table125], axis=0)
    table_var["Tipologia"] = ["Total habitatges", "Habitatges unifamiliars", "Habitatges plurifamiliars"]
    table_var_melted = pd.melt(table_var, id_vars="Tipologia", var_name = "Variable")

    fig = px.bar(table_var_melted, x="Tipologia", y="value", color="Variable", color_discrete_sequence=["#008B6C","#00D0A3","#AAC4BA"], barmode="group", title="", labels={'x':"Preu m\u00b2 útil (mitjana)", 'y':"Tipologia d'habitatge"})
    fig.layout.xaxis.title.text = "Tipologia"
    fig.layout.yaxis.title.text = "Variació anual (%)"
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    fig.update_layout(font=dict(size=13), legend=dict(orientation='h', yanchor='bottom', y=1, x=0))
    return(fig)
@st.cache_resource
def table_geo_cat(any_ini, any_fin):
        df_cat = df_final_cat[(df_final_cat["Any"]>=any_ini) & (df_final_cat["Any"]<=any_fin)].drop_duplicates(["Any", "Tipologia", "Variable", "Valor"]).pivot(index=["Any"], columns=["Tipologia", "Variable"], values="Valor")
        df_cat_n = df_cat.sort_index(axis=1, level=[0,1])
        num_cols = df_cat_n.select_dtypes(include=['float64', 'int64']).columns
        df_cat_n[num_cols] = df_cat_n[num_cols].round(0)
        df_cat_n[num_cols] = df_cat_n[num_cols].astype(int)
        num_cols = df_cat_n.select_dtypes(include=['float64', 'int']).columns
        df_cat_n[num_cols] = df_cat_n[num_cols].map(lambda x: '{:,.0f}'.format(x).replace(',', '#').replace('.', ',').replace('#', '.'))
        return(df_cat_n)
####################################### PROVÍNCIES I AMBITS FUNCIONS #################################################
@st.cache_resource
def table_geo(geo, any_ini, any_fin, selected):
    if selected=="Àmbits territorials":
        df_prov_filtered = ambits_df[(ambits_df["GEO"]==geo) & (ambits_df["Any"]>=any_ini) & (ambits_df["Any"]<=any_fin)].pivot(index=["Any"], columns=["Tipologia", "Variable"], values="Valor")
        df_prov_n = df_prov_filtered.sort_index(axis=1, level=[0,1])
        num_cols = df_prov_n.select_dtypes(include=['float64', 'int64']).columns
        df_prov_n[num_cols] = df_prov_n[num_cols].round(0)
        df_prov_n[num_cols] = df_prov_n[num_cols].astype("float64")
        num_cols = df_prov_n.select_dtypes(include=['float64', 'int']).columns
        df_prov_n[num_cols] = df_prov_n[num_cols].map(lambda x: '{:,.0f}'.format(x).replace(',', '#').replace('.', ',').replace('#', '.'))
        return(df_prov_n)
    if selected=="Províncies" or selected=="Catalunya":
        df_prov_filtered = provincia_df[(provincia_df["GEO"]==geo) & (provincia_df["Any"]>=any_ini) & (provincia_df["Any"]<=any_fin)].pivot(index=["Any"], columns=["Tipologia", "Variable"], values="Valor")
        df_prov_n = df_prov_filtered.sort_index(axis=1, level=[0,1])
        num_cols = df_prov_n.select_dtypes(include=['float64', 'int64']).columns
        df_prov_n[num_cols] = df_prov_n[num_cols].round(0)
        df_prov_n[num_cols] = df_prov_n[num_cols].astype(int)
        num_cols = df_prov_n.select_dtypes(include=['float64', 'int']).columns
        df_prov_n[num_cols] = df_prov_n[num_cols].map(lambda x: '{:,.0f}'.format(x).replace(',', '#').replace('.', ',').replace('#', '.'))
        return(df_prov_n)
@st.cache_resource
def tipog_donut(df_hab, prov):
    donut_tipog = df_hab[df_hab["PROVINCIA"]==prov][["PROVINCIA", "TIPO"]].value_counts(normalize=True).reset_index()
    donut_tipog.columns = ["PROVINCIA", "TIPO", "Habitatges en oferta"]
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=donut_tipog["TIPO"],
        values=donut_tipog["Habitatges en oferta"],
        hole=0.5, 
        showlegend=True, 
        marker=dict(
            colors=["#008B6C", "#00D0A3",  "#66b9a7", "#DAE4E0"], 
            line=dict(color='#FFFFFF', width=1) 
        ),
        textposition='outside',
        textinfo='percent+label' 
    ))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    fig.update_layout(
        title=f'Habitatges en oferta per tipologia',
        font=dict(size=12),
        legend=dict(
            x=0.85,  # Set legend position
            y=0.85
        )
    )
    return(fig)
@st.cache_resource
def num_dorms_prov(df_hab, prov):
    table33_prov =  pd.crosstab(df_hab["PROVINCIA"], df_hab["Total dormitoris"]).reset_index().rename(columns={"PROVINCIA":"Província"})
    table33_prov = table33_prov[table33_prov["Província"]==prov].drop("Província", axis=1).T.reset_index()
    table33_prov.columns = ["Total dormitoris", "Habitatges en oferta"]

    fig = go.Figure(go.Bar(x=table33_prov["Total dormitoris"], y=table33_prov["Habitatges en oferta"], marker_color='#66b9a7'))
    fig.layout.yaxis = dict(title="Habitages en oferta", tickformat=",d")
    fig.update_layout(
        title=f"Habitatges en oferta segons nombre d'habitacions",
        xaxis_title="Nombre d'habitacions",
    )
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def qualitats_prov(df_hab, prov):
    table62_hab = df_hab[df_hab["PROVINCIA"]==prov][["Aire condicionat","Bomba de calor","Aerotèrmia","Calefacció","Preinstal·lació d'A.C./B. Calor/Calefacció",'Parquet','Armaris encastats','Placa de cocció amb gas','Placa de cocció vitroceràmica',"Placa d'inducció",'Plaques solars']].sum(axis=0)
    table62_hab = pd.DataFrame({"Equipaments":table62_hab.index, "Total":table62_hab.values})
    table62_hab = table62_hab.set_index("Equipaments").apply(lambda row: (row / df_hab[df_hab["PROVINCIA"]==prov].shape[0])*100)
    table62_hab = table62_hab.sort_values("Total", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=table62_hab["Total"],  # Use values as x-axis data
        y=table62_hab.index,  # Use categories as y-axis data
        orientation="h",  # Set orientation to horizontal
        marker=dict(color="#66b9a7"),  # Set bar color
    ))
    fig.update_layout(
        title="Qualitats d'habitatges en oferta",
        xaxis_title="% d'habitatges en oferta",
        yaxis_title="Qualitats",
    )
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def equipaments_prov(df_hab, prov):
    table67_hab = df_hab[df_hab["PROVINCIA"]==prov][["Zona enjardinada", "Parc infantil", "Piscina comunitària", "Traster", "Ascensor", "Equipament Esportiu", "Sala de jocs", "Sauna", "Altres", "Cap dels anteriors"]].sum(axis=0, numeric_only=True)
    table67_hab = pd.DataFrame({"Equipaments":table67_hab.index, "Total":table67_hab.values})
    table67_hab = table67_hab.set_index("Equipaments").apply(lambda row: row.mul(100) / df_hab[df_hab["PROVINCIA"]==prov].shape[0])
    table67_hab = table67_hab.sort_values("Total", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=table67_hab["Total"],  # Use values as x-axis data
        y=table67_hab.index,  # Use categories as y-axis data
        orientation="h",  # Set orientation to horizontal
        marker=dict(color="#66b9a7"),  # Set bar color
    ))
    fig.update_layout(
        title="Equipaments d'habitatges en oferta",
        xaxis_title="% d'habitatges en oferta",
        yaxis_title="Equipaments",
    )
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def tipo_obra_prov(df_hab, prov):
    table38hab_prov = df_hab[["PROVINCIA", "TIPH"]].value_counts().reset_index().sort_values(["PROVINCIA", "TIPH"])
    table38hab_prov.columns = ["PROVINCIA", "TIPOLOGIA", "Habitatges"]
    table38hab_prov = table38hab_prov.pivot_table(index="PROVINCIA", columns="TIPOLOGIA", values="Habitatges").reset_index().rename(columns={"PROVINCIA":"Província"})
    table38hab_prov = table38hab_prov[table38hab_prov["Província"]==prov].drop("Província", axis=1).T.reset_index()
    table38hab_prov.columns = ["Tipus", "Habitatges en oferta"]
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=table38hab_prov["Tipus"],
        values=table38hab_prov["Habitatges en oferta"],
        hole=0.5, 
        showlegend=True, 
        marker=dict(
            colors=["#008B6C",  "#00D0A3"], 
            line=dict(color='#FFFFFF', width=1) 
        ),
        textposition='outside',
        textinfo='percent+label' 
    ))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    fig.update_layout(
        title=f'Habitatges en oferta per tipus (obra nova o rehabilitació)',
        font=dict(size=12),
        legend=dict(
            x=0.7,  # Set legend position
            y=0.85
        )
    )
    return(fig)
@st.cache_resource
def cons_acabats(df_prom, df_hab, prov):
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=["Habitatges en construcció", "Habitatges acabats"],
        values=[metric_estat(df_prom, df_hab, prov)[0] - metric_estat(df_prom, df_hab, prov)[1], metric_estat(df_prom, df_hab, prov)[1]],
        hole=0.5, 
        showlegend=True, 
        marker=dict(
            colors=["#008B6C",  "#00D0A3"], 
            line=dict(color='#FFFFFF', width=1) 
        ),
        textposition='outside',
        textinfo='percent+label' 
    ))
    fig.update_layout(
        title=f'Habitatges en construcció i acabats',
        font=dict(size=12),
        legend=dict(
            x=0.7,  # Set legend position
            y=1.1
        )
    )
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def metric_estat(df_prom, df_hab, prov):
    table11_prov = df_prom[["PROVINCIA", "HABIP"]].groupby("PROVINCIA").sum().reset_index()
    hab_oferta = table11_prov[table11_prov["PROVINCIA"]==prov].iloc[0,1]
    table17_hab_prov = df_hab[["PROVINCIA", "ESTO"]].value_counts().reset_index().sort_values(["PROVINCIA", "ESTO"])
    table17_hab_prov.columns = ["PROVINCIA","ESTAT", "PROMOCIONS"]
    table17_hab_prov = table17_hab_prov.pivot_table(index="PROVINCIA", columns="ESTAT", values="PROMOCIONS").reset_index()
    table17_hab_prov = table17_hab_prov[["PROVINCIA","Claus en mà"]].rename(columns={"PROVINCIA": "Província","Claus en mà":"Acabats sobre habitatges en oferta"})
    acabats_oferta = table17_hab_prov[table17_hab_prov["Província"]==prov].iloc[0,1]
    return([hab_oferta, acabats_oferta])
@st.cache_resource
def metric_rehab(df_hab, prov):
    table38hab_prov = df_hab[["PROVINCIA", "TIPH"]].value_counts().reset_index().sort_values(["PROVINCIA", "TIPH"])
    table38hab_prov.columns = ["PROVINCIA", "TIPOLOGIA", "Habitatges"]
    table38hab_prov = table38hab_prov.pivot_table(index="PROVINCIA", columns="TIPOLOGIA", values="Habitatges").reset_index().rename(columns={"PROVINCIA":"Província"})
    table38hab_prov = table38hab_prov[table38hab_prov["Província"]==prov].drop("Província", axis=1).T.reset_index()
    table38hab_prov.columns = ["Tipus", "Habitatges en oferta"]
    return([table38hab_prov.iloc[0,1], table38hab_prov.iloc[1,1]])
############################################################# MUNICIPIS FUNCIONS #############################################
@st.cache_resource
def data_text_mun(df_hab, df_hab_mod, selected_mun):
    table80_mun = df_hab_mod[df_hab_mod["Municipi"]==selected_mun][["Municipi", "TIPOG", "Superfície útil", "Preu mitjà", "Preu m2 útil"]].groupby(["Municipi"]).agg({"Municipi":['count'], "Superfície útil": [np.mean], "Preu mitjà": [np.mean], "Preu m2 útil": [np.mean]}).reset_index()
    table25_mun = df_hab[df_hab["Municipi"]==selected_mun][["Municipi", "TIPOG"]].value_counts(normalize=True).reset_index().rename(columns={"proportion":"Proporció"})
    table61_hab = df_hab[df_hab["Municipi"]==selected_mun].groupby(['Total dormitoris']).size().reset_index(name='Proporcions').sort_values(by="Proporcions", ascending=False)
    table61_lav = df_hab[df_hab["Municipi"]==selected_mun].groupby(['Banys i lavabos']).size().reset_index(name='Proporcions').sort_values(by="Proporcions", ascending=False)

    try:
        proporcio_tipo = round(table25_mun[table25_mun["TIPOG"]=="Habitatges plurifamiliars"]["Proporció"].values[0]*100,2)
    except IndexError:
        proporcio_tipo = 0
    return([round(table80_mun["Preu mitjà"].values[0][0],2), round(table80_mun["Superfície útil"].values[0][0],2), 
            round(table80_mun["Preu m2 útil"].values[0][0],2), proporcio_tipo, 
            table61_hab["Total dormitoris"].values[0], table61_lav["Banys i lavabos"].values[0]])
@st.cache_resource
def plotmun_streamlit(data, selected_mun, kpi):
    df = data[(data['Municipi']==selected_mun)]
    fig = px.histogram(df, x=kpi, title= "", labels={'x':kpi, 'y':'Freqüència'})
    fig.data[0].marker.color = "#66b9a7"
    fig.layout.xaxis.title.text = kpi
    fig.layout.yaxis.title.text = 'Freqüència'
    mean_val = df[kpi].mean()
    fig.layout.shapes = [dict(type='line', x0=mean_val, y0=0, x1=mean_val, y1=1, yref='paper', xref='x', 
                            line=dict(color="black", width=2, dash='dot'))]
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    fig.layout.xaxis = dict(title=kpi, tickformat=",d")
    return(fig)
@st.cache_resource
def count_plot_mun(data, selected_mun):
    df = data[data['Municipi'] == selected_mun]
    df = df["TIPOG"].value_counts().sort_values(ascending=True).reset_index()
    df.columns = ['TIPOG', 'count']
    custom_colors = ["#00D0A3","#AAC4BA"]
    fig = px.pie(df, values='count', names='TIPOG', title="", hole=0.4,
                 color_discrete_sequence=custom_colors)
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig

@st.cache_resource
def dormscount_plot_mun(data, selected_mun):
    df = data[data['Municipi']==selected_mun]
    custom_order = ["0D", "1D", "2D", "3D", "4D", "5+D"]
    df = df["Total dormitoris"].value_counts().reindex(custom_order)
    fig = px.bar(df,  y=df.values, x=df.index,title="", labels={'x':"Número d'habitacions", 'y':"Número d'habitatges"}, text= df.values)
    fig.layout.yaxis = dict(title="Nombre d'habitatges", tickformat=",d")
    fig.layout.xaxis.title.text = "Nombre d'habitacions"
    fig.update_traces(marker=dict(color="#66b9a7"))
    max_width = 0.1
    fig.update_layout(bargap=(1 - max_width) / 2, bargroupgap=0)
    for trace in fig.data:
        trace.text = [f"{val:,.0f}" if not np.isnan(val) else '' for val in trace.y]
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def lavcount_plot_mun(data, selected_mun):
    df = data[data['Municipi']==selected_mun]

    df = df["Banys i lavabos"].value_counts().sort_values(ascending=True)
    fig = px.bar(df,  y=df.values, x=df.index,title="", labels={'x':"Número de lavabos", 'y':"Número d'habitatges"}, text= df.values)
    fig.layout.yaxis = dict(title="Nombre d'habitatges", tickformat=",d")
    fig.layout.xaxis.title.text = "Nombre de lavabos"
    fig.update_traces(marker=dict(color="#66b9a7"))
    max_width = 0.00001
    fig.update_layout(bargap=(1 - max_width) / 2, bargroupgap=0)
    for trace in fig.data:
        trace.text = [f"{val:,.0f}" if not np.isnan(val) else '' for val in trace.y]
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def table_mun(Municipi, any_ini, any_fin):
    df_mun_filtered = df_final[(df_final["GEO"]==Municipi) & (df_final["Any"]>=any_ini) & (df_final["Any"]<=any_fin)].drop(["Àmbits territorials","Corones","Comarques","Província", "codiine"], axis=1).pivot(index=["Any"], columns=["Tipologia", "Variable"], values="Valor")
    df_mun_unitats = df_final[(df_final["GEO"]==Municipi) & (df_final["Any"]>=any_ini) & (df_final["Any"]<=any_fin)].drop(["Àmbits territorials","Corones","Comarques","Província", "codiine"], axis=1).drop_duplicates(["Any","Tipologia","Unitats"]).pivot(index=["Any"], columns=["Tipologia"], values="Unitats")
    df_mun_unitats.columns= [("HABITATGES PLURIFAMILIARS", "Unitats"), ("HABITATGES UNIFAMILIARS", "Unitats"), ("TOTAL HABITATGES", "Unitats")]
    df_mun_n = pd.concat([df_mun_filtered, df_mun_unitats], axis=1)
    # df_mun_n[("HABITATGES PLURIFAMILIARS", "Unitats %")] = (df_mun_n[("HABITATGES PLURIFAMILIARS", "Unitats")]/df_mun_n[("TOTAL HABITATGES", "Unitats")])*100
    # df_mun_n[("HABITATGES UNIFAMILIARS", "Unitats %")] = (df_mun_n[("HABITATGES UNIFAMILIARS", "Unitats")] /df_mun_n[("TOTAL HABITATGES", "Unitats")])*100
    df_mun_n = df_mun_n.sort_index(axis=1, level=[0,1])
    num_cols = df_mun_n.select_dtypes(include=['float64', 'Int64']).columns
    df_mun_n[num_cols] = df_mun_n[num_cols].round(0)
    df_mun_n[num_cols] = df_mun_n[num_cols].astype("Int64")
    num_cols = df_mun_n.select_dtypes(include=['float64', 'Int64']).columns
    df_mun_n[num_cols] = df_mun_n[num_cols].map(lambda x: '{:,.0f}'.format(x).replace(',', '#').replace('.', ',').replace('#', '.'))
    return(df_mun_n)
@st.cache_resource
def plot_mun_hist_units(selected_mun, variable_int, any_ini, any_fin):
    df_preus = df_vf_aux[(df_vf_aux['Variable']==variable_int) & (df_vf_aux['GEO']==selected_mun) & (df_vf_aux["Any"]>=any_ini) & (df_vf_aux["Any"]<=any_fin)].drop(['Variable'], axis=1).reset_index().drop('index', axis=1)
    df_preus['Valor'] = np.where(df_preus['Valor']==0, np.nan, round(df_preus['Valor'], 1))
    df_preus['Any'] = df_preus['Any'].astype(int)
    df_preus = df_preus[df_preus["Tipologia"]!="TOTAL HABITATGES"]
    fig = px.bar(df_preus, x='Any', y='Valor', color='Tipologia', color_discrete_sequence=["#AAC4BA","#00D0A3"], range_y=[0, None], labels={'Valor': variable_int, 'Any': 'Any'}, text= "Valor")
    fig.layout.yaxis = dict(title= variable_int,tickformat=",d")
    valid_years = sorted(df_preus['Any'].unique())
    fig.update_xaxes(tickvals=valid_years)
    for trace in fig.data:
        trace.text = [f"{val:,.0f}" if not np.isnan(val) else '' for val in trace.y]
    max_width = 0.2
    fig.update_layout(bargap=(1 - max_width) / 2, bargroupgap=0)
    fig.update_layout(font=dict(size=13), legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='right', x=0.75))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def plot_mun_hist(selected_mun, variable_int, any_ini, any_fin):
    df_preus = df_vf[(df_vf['Variable']==variable_int) & (df_vf['GEO']==selected_mun) & (df_vf["Any"]>=any_ini) & (df_vf["Any"]<=any_fin)].drop(['Variable'], axis=1).reset_index().drop('index', axis=1)
    df_preus['Valor'] = np.where(df_preus['Valor']==0, np.nan, round(df_preus['Valor'], 1))
    df_preus['Any'] = df_preus['Any'].astype(int)
    fig = px.bar(df_preus, x='Any', y='Valor', color='Tipologia', color_discrete_sequence=["#008B6C","#AAC4BA","#00D0A3"], range_y=[0, None], labels={'Valor': variable_int, 'Any': 'Any'}, text='Valor', barmode='group')
    fig.layout.yaxis = dict(title= variable_int,tickformat=",d")
    for trace in fig.data:
        trace.text = [f"{val:,.0f}" if not np.isnan(val) else '' for val in trace.y]
    max_width = 0.5
    fig.update_layout(bargap=(1 - max_width) / 2, bargroupgap=0)
    fig.update_layout(font=dict(size=13), legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.75))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def matrix_hab_lav(df_hab, mun, pivot_name):
    resum_mun_hab_lav = df_hab[(df_hab["Municipi"]==mun)].groupby(["Total dormitoris", "Banys i lavabos"])[["Preu mitjà", "Preu m2 útil", "Superfície útil"]].mean().reset_index()
    resum_mun_hab_lav = resum_mun_hab_lav[(resum_mun_hab_lav["Total dormitoris"]>0) & (resum_mun_hab_lav["Banys i lavabos"]>0)]
    resum_mun_hab_lav["Total dormitoris"] = resum_mun_hab_lav["Total dormitoris"].astype(str) + " habitacions"
    resum_mun_hab_lav["Banys i lavabos"] = resum_mun_hab_lav["Banys i lavabos"].astype(str) + " lavabos"
    resum_mun_hab_lav = resum_mun_hab_lav.round(1)
    resum_mun_hab_lav[["Preu mitjà", "Preu m2 útil", "Superfície útil"]] = resum_mun_hab_lav[["Preu mitjà", "Preu m2 útil", "Superfície útil"]].map(lambda x: '{:,.0f}'.format(x).replace(',', '#').replace('.', ',').replace('#', '.'))
    if pivot_name=="Preu m2 útil":
        resum_mun_hab_lav_pivoted_preu = resum_mun_hab_lav.pivot(index="Total dormitoris", columns="Banys i lavabos", values=pivot_name)
        return(resum_mun_hab_lav_pivoted_preu)
    if pivot_name=="Superfície útil":
        resum_mun_hab_lav_pivoted_super = resum_mun_hab_lav.pivot(index="Total dormitoris", columns="Banys i lavabos", values=pivot_name)
        return(resum_mun_hab_lav_pivoted_super)
@st.cache_resource
def caracteristiques_mun(df_hab, mun):
    table_tipus = df_hab.groupby(["PROVINCIA",'Municipi'])[["Total dormitoris","Banys i lavabos","Cuines estàndard","Cuines americanes","Terrasses, balcons i patis","Estudi/golfes","Safareig", "Altres interiors", "Altres exteriors"]].mean().reset_index().drop(["PROVINCIA"], axis=1)
    table_tipus = table_tipus[table_tipus["Municipi"]==mun].drop("Municipi", axis=1).T
    table_tipus.columns = ["Total"]
    table_tipus["Total"] = round(table_tipus["Total"],2)
    table62_hab = table_tipus.sort_values("Total", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=table62_hab["Total"],  # Use values as x-axis data
        y=table62_hab.index,  # Use categories as y-axis data
        orientation="h",  # Set orientation to horizontal
        marker=dict(color="#66b9a7"),  # Set bar color
    ))
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Tipus d'habitatge",
    )
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def qualitats_mun(df_hab, mun):
    table62_hab = df_hab[df_hab["Municipi"]==mun][["Aire condicionat","Bomba de calor","Aerotèrmia","Calefacció","Preinstal·lació d'A.C./B. Calor/Calefacció",'Parquet','Armaris encastats','Placa de cocció amb gas','Placa de cocció vitroceràmica',"Placa d'inducció",'Plaques solars']].sum(axis=0)
    table62_hab = pd.DataFrame({"Equipaments":table62_hab.index, "Total":table62_hab.values})
    table62_hab = table62_hab.set_index("Equipaments").apply(lambda row: row.mul(100) / df_hab[df_hab["Municipi"]==mun].shape[0])
    table62_hab = table62_hab.sort_values("Total", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=table62_hab["Total"],  # Use values as x-axis data
        y=table62_hab.index,  # Use categories as y-axis data
        orientation="h",  # Set orientation to horizontal
        marker=dict(color="#66b9a7"),  # Set bar color
    ))
    fig.update_layout(
        xaxis_title="% d'habitatges en oferta",
        yaxis_title="Qualitats",
    )
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def equipaments_mun(df_hab, mun):
    table67_hab = df_hab[df_hab["Municipi"]==mun][["Zona enjardinada", "Parc infantil", "Piscina comunitària", "Traster", "Ascensor", "Equipament Esportiu", "Sala de jocs", "Sauna", "Altres", "Cap dels anteriors"]].sum(axis=0, numeric_only=True)
    table67_hab = pd.DataFrame({"Equipaments":table67_hab.index, "Total":table67_hab.values})
    table67_hab = table67_hab.set_index("Equipaments").apply(lambda row: row.mul(100) / df_hab[df_hab["Municipi"]==mun].shape[0])
    table67_hab = table67_hab.sort_values("Total", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=table67_hab["Total"],  # Use values as x-axis data
        y=table67_hab.index,  # Use categories as y-axis data
        orientation="h",  # Set orientation to horizontal
        marker=dict(color="#66b9a7"),  # Set bar color
    ))
    fig.update_layout(
        xaxis_title="% d'habitatges en oferta",
        yaxis_title="Equipaments",
    )
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def plot_table_energ_mun(df_hab, mun):
    table67hab_aux = df_hab[df_hab["Municipi"]==mun][["QENERGC"]].value_counts().reset_index()
    table67hab_aux.columns = ["Qualificació energètica", "Habitatges"]
    table67hab_ener = table67hab_aux.assign(index=table67hab_aux["Qualificació energètica"].map({"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "En tràmits": 8, "Sense informació": 9}))
    table67hab_ener['Grup'] = table67hab_ener["Qualificació energètica"].map(
        {"A": "A", 
        "B": "B", 
        "C": "C-G", 
        "D": "C-G", 
        "E": "C-G", 
        "F": "C-G", 
        "G": "C-G", 
        "En tràmits": "En tràmits", 
        "Sense informació": "Sense informació"}
    )
    table67hab_ener = table67hab_ener.drop("index", axis=1)
    table67hab_grouped = table67hab_ener.groupby("Grup").sum().reset_index()
    table67hab_grouped["Habitatges"] = round(table67hab_grouped["Habitatges"] * 100 / df_hab[df_hab["Municipi"] == mun].shape[0], 1)
    fig = px.pie(table67hab_grouped, values='Habitatges', names="Grup", title="", hole=0.4,
                color="Grup",color_discrete_sequence=["#AAC4BA", "#008B6C", "#00D0A3", "#D8BEB3", "white"])
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(legend=dict(x=0, y=1.25, orientation="h"))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def n_promocions_habs_mun(df_prom, selected_mun):
    grandaria_promo = df_prom[df_prom["Municipi"] == selected_mun][["HABIT"]].rename(columns={"HABIT":"count"}).reset_index().drop("index", axis=1)
    grandaria_promo = grandaria_promo.sort_values("count", ascending=False).reset_index().drop("index", axis=1)
    mean_promo = grandaria_promo["count"].mean()
    fig = px.histogram(grandaria_promo, 
                x=grandaria_promo["count"], nbins=11, 
                )
    fig.update_layout(
        xaxis_title="Nombre d'habitatges per promoció",
        yaxis_title="Nombre de promocions al municipi",
        bargap=0.1
    )
    fig.add_annotation(
        x=1, y=1,  
        text=f"<b>Mitjana d'habitatges totals per promoció: {mean_promo:.0f}</b>",
        showarrow=False,
        xref="paper", yref="paper",
        font=dict(size=15, color="black"),
        bgcolor="#66b9a7", 
        borderwidth=1,
        borderpad=4
    )
    fig.update_traces(marker=dict(color="#66b9a7"))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def cale_tipus_mun(df_prom, mun):
    cale_tipus_mun = df_prom[['Municipi','De gasoil', 'De gas natural','De propà', "D'electricitat", "No s'indica tipus"]].fillna(0).groupby("Municipi")[['De gasoil', 'De gas natural','De propà', "D'electricitat", "No s'indica tipus"]].sum().reset_index()
    cale_tipus_mun = cale_tipus_mun[cale_tipus_mun["Municipi"]==mun].T.reset_index()
    cale_tipus_mun.columns = ["Tipus", "Total"]
    cale_tipus_mun = cale_tipus_mun[cale_tipus_mun["Tipus"]!="Municipi"]
    fig = px.pie(cale_tipus_mun, values='Total', names="Tipus", title="", hole=0.4,
    color="Tipus",color_discrete_sequence=["#00D0A3", "#D8BEB3","#AAC4BA", "#008B6C", "white"])
    fig.update_traces(textposition='outside', textinfo='percent+label', sort=False)
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def aparcament_mun(df_hab, mun):
    table_aparcament_mun = df_hab[df_hab["APAR"]!="Altres"][["Municipi","APAR"]].groupby(["Municipi","APAR"]).size().reset_index().rename(columns={0:"Proporcions"}).set_index(["Municipi"])
    table_aparcament_mun = table_aparcament_mun.pivot_table(index=["Municipi"], columns="APAR", values="Proporcions").reset_index().set_index(["Municipi"])
    table_aparcament_mun = table_aparcament_mun.apply(lambda row: row.mul(100)/row.sum(), axis=1).reset_index()
    table_aparcament_mun = table_aparcament_mun[table_aparcament_mun["Municipi"]==mun].T.reset_index()
    table_aparcament_mun.columns = ["Tipus", "Total"]
    table_aparcament_mun = table_aparcament_mun[table_aparcament_mun["Tipus"]!="Municipi"]
    fig = px.pie(table_aparcament_mun, values='Total', names="Tipus", title="", hole=0.4,
    color="Tipus",color_discrete_sequence=["#AAC4BA","#00D0A3","white"])
    fig.update_traces(textposition='outside', textinfo='percent+label', sort=False)
    fig.update_layout(legend=dict(x=0, y=1.3, orientation="h"))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
############################################################ DISTRICTES FUNCIONS #############################################
@st.cache_resource
def data_text_dis(df_hab, selected_dis):
    table80_dis = df_hab[(df_hab["Municipi"]=="Barcelona") & (df_hab["Nom DIST"]==selected_dis)][["Nom DIST", "TIPOG", "Superfície útil", "Preu mitjà", "Preu m2 útil"]].groupby(["Nom DIST"]).agg({"Nom DIST":['count'], "Superfície útil": [np.mean], "Preu mitjà": [np.mean], "Preu m2 útil": [np.mean]}).reset_index()
    table25_dis = df_hab[(df_hab["Municipi"]=="Barcelona") & (df_hab["Nom DIST"]==selected_dis)][["Nom DIST", "TIPOG"]].value_counts(normalize=True).reset_index().rename(columns={"proportion":"Proporció"})
    table61_hab = df_hab[(df_hab["Municipi"]=="Barcelona") & (df_hab["Nom DIST"]==selected_dis)].groupby(['Total dormitoris']).size().reset_index(name='Proporcions').sort_values(by="Proporcions", ascending=False)
    table61_lav = df_hab[(df_hab["Municipi"]=="Barcelona") & (df_hab["Nom DIST"]==selected_dis)].groupby(['Banys i lavabos']).size().reset_index(name='Proporcions').sort_values(by="Proporcions", ascending=False)

    return([round(table80_dis["Preu mitjà"].values[0][0],2), round(table80_dis["Superfície útil"].values[0][0],2), 
            round(table80_dis["Preu m2 útil"].values[0][0],2), round(table25_dis[table25_dis["TIPOG"]=="Habitatges plurifamiliars"]["Proporció"].values[0]*100,2), 
            table61_hab["Total dormitoris"].values[0], table61_lav["Banys i lavabos"].values[0]])
@st.cache_resource
def plotdis_streamlit(data, selected_dis, kpi):
    df = data[(data['Nom DIST']==selected_dis)]
    fig = px.histogram(df, x=kpi, title= "", labels={'x':kpi, 'y':'Freqüència'})
    fig.data[0].marker.color = "#66b9a7"
    fig.layout.xaxis.title.text = kpi
    fig.layout.yaxis.title.text = 'Freqüència'
    mean_val = df[kpi].mean()
    fig.layout.shapes = [dict(type='line', x0=mean_val, y0=0, x1=mean_val, y1=1, yref='paper', xref='x', 
                            line=dict(color="black", width=2, dash='dot'))]
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def count_plot_dis(data, dis):
    df = data[(data['Municipi'] == "Barcelona") & (data['Nom DIST'] == dis)]
    df = df["TIPOG"].value_counts().sort_values(ascending=True).reset_index()
    df.columns = ['TIPOG', 'count']
    custom_colors = ["#00D0A3","#AAC4BA"]
    fig = px.pie(df, values='count', names='TIPOG', title="", hole=0.4,
                 color_discrete_sequence=custom_colors)
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def dormscount_plot_dis(data, selected_dis):
    df = data[data['Nom DIST']==selected_dis]
    custom_order = ["0D", "1D", "2D", "3D", "4D", "5+D"]
    df = df["Total dormitoris"].value_counts().reindex(custom_order)
    fig = px.bar(df,  y=df.values, x=df.index,title="", labels={'x':"Número d'habitacions", 'y':"Número d'habitatges"}, text= df.values)
    fig.layout.yaxis.title.text = "Número d'habitatges"
    fig.layout.xaxis.title.text = "Número d'habitacions"
    fig.update_traces(marker=dict(color="#66b9a7"))
    max_width = 0.1
    fig.update_layout(bargap=(1 - max_width) / 2, bargroupgap=0)
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def lavcount_plot_dis(data, selected_dis):
    df = data[data['Nom DIST']==selected_dis]

    df = df["Banys i lavabos"].value_counts().sort_values(ascending=True)
    fig = px.bar(df,  y=df.values, x=df.index,title="", labels={'x':"Número de lavabos", 'y':"Número d'habitatges"}, text= df.values)
    fig.layout.yaxis.title.text = "Número d'habitatges"
    fig.layout.xaxis.title.text = "Número de lavabos"
    fig.update_traces(marker=dict(color="#66b9a7"))
    max_width = 0.1
    fig.update_layout(bargap=(1 - max_width) / 2, bargroupgap=0)
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def geo_dis(districte, any_ini, any_fin):
    df_vf_aux = pd.DataFrame()
    for df_frame, year in zip(["dis_2019", "dis_2020", "dis_2021", "dis_2022", "dis_2023", "dis_2024"], [2019, 2020, 2021, 2022, 2023, 2024]):
        df_vf_aux = pd.concat([df_vf_aux, tidy_data(eval(df_frame), year)], axis=0)
    df_vf_aux['Variable']= np.where(df_vf_aux['Variable']=="Preu de     venda per      m² útil (€)", "Preu de venda per m² útil (€)", df_vf_aux['Variable'])
    df_vf_aux['Valor'] = pd.to_numeric(df_vf_aux['Valor'], errors='coerce')

    df_vf_aux = df_vf_aux[df_vf_aux['GEO']!="Municipi de Barcelona"]
    df_vf_aux["GEO"] = df_vf_aux["GEO"].str.replace(r"\d+\s", "", regex=True)
    df_vf_aux = df_vf_aux[df_vf_aux["GEO"].isin(["Ciutat Vella", "Eixample", "Sants-Montjuïc", 
                                                "Les Corts", "Sarrià-Sant Gervasi", "Sarrià - Sant Gervasi", "Gràcia", 
                                                "Horta-Guinardó", "Nou Barris", "Sant Andreu",
                                                "Sant Martí"])]
    df_vf_aux["GEO"] = df_vf_aux["GEO"].str.replace("Sarrià-Sant Gervasi", "Sarrià - Sant Gervasi")
    df_vf_aux = df_vf_aux[df_vf_aux["GEO"]==districte].drop_duplicates(subset=["Any", "Tipologia", "Variable", "GEO"], keep="first")
    df_wide = pd.pivot(data=df_vf_aux, index="Any", columns=["Tipologia", "Variable"], values="Valor")
    num_cols = df_wide.select_dtypes(include=['float64', 'int64']).columns
    df_wide[num_cols] = df_wide[num_cols].round(0)
    df_wide[num_cols] = df_wide[num_cols].astype("Int64")
    num_cols = df_wide.select_dtypes(include=['float64', 'Int64']).columns
    df_wide[num_cols] = df_wide[num_cols].map(lambda x: '{:,.0f}'.format(x).replace(',', '#').replace('.', ',').replace('#', '.'))
    df_wide = df_wide[(df_wide.index>=any_ini) & (df_wide.index<=any_fin)]
    return(df_wide)
@st.cache_resource
def plot_dis_hist_units(selected_dis, variable_int, any_ini, any_fin):
    df_preus = df_dis_long[(df_dis_long['Variable']==variable_int) & (df_dis_long['GEO']==selected_dis) & (df_dis_long["Any"]>=any_ini) & (df_dis_long["Any"]<=any_fin)].drop(['Variable'], axis=1).reset_index().drop('index', axis=1)
    df_preus['Valor'] = np.where(df_preus['Valor']==0, np.nan, round(df_preus['Valor'], 1))
    df_preus['Any'] = df_preus['Any'].astype(int)
    df_preus = df_preus[df_preus["Tipologia"]!="TOTAL HABITATGES"]
    fig = px.bar(df_preus[df_preus["Valor"]>0], x='Any', y='Valor', color='Tipologia', color_discrete_sequence=["#AAC4BA","#00D0A3"], range_y=[0, None], labels={'Valor': variable_int, 'Any': 'Any'}, text= "Valor")
    fig.layout.yaxis = dict(title= variable_int,tickformat=",d")
    valid_years = sorted(df_preus['Any'].unique())
    fig.update_xaxes(tickvals=valid_years)
    max_width = 0.2
    fig.update_layout(bargap=(1 - max_width) / 2, bargroupgap=0)
    fig.update_layout(font=dict(size=13), legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='right', x=0.75))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def plot_dis_hist(selected_dis, variable_int, any_ini, any_fin):
    df_preus = df_dis_long[(df_dis_long['Variable']==variable_int) & (df_dis_long['GEO']==selected_dis) & (df_dis_long["Any"]>=any_ini) & (df_dis_long["Any"]<=any_fin)].drop(['Variable'], axis=1).reset_index().drop('index', axis=1)
    df_preus['Valor'] = np.where(df_preus['Valor']==0, np.nan, round(df_preus['Valor'], 1))
    df_preus['Any'] = df_preus['Any'].astype(int)
    fig = px.bar(df_preus[df_preus["Valor"]>0], x='Any', y='Valor', color='Tipologia', color_discrete_sequence=["#008B6C","#AAC4BA","#00D0A3"], range_y=[0, None], labels={'Valor': variable_int, 'Any': 'Any'}, text='Valor', barmode='group')
    fig.layout.yaxis = dict(title= variable_int,tickformat=",d")
    for trace in fig.data:
        trace.text = [f"{val:,.0f}" for val in trace.y]
    max_width = 0.2
    fig.update_layout(bargap=(1 - max_width) / 2, bargroupgap=0)
    fig.update_layout(font=dict(size=13), legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.75))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def matrix_hab_lav_dis(df_hab, dis, pivot_name):
    resum_dis_hab_lav = df_hab[(df_hab['Municipi']=="Barcelona") & (df_hab['Nom DIST']==dis) & (df_hab["TIPOG"]=="Habitatges plurifamiliars")].groupby(["Total dormitoris", "Banys i lavabos"])[["Preu mitjà", "Preu m2 útil", "Superfície útil"]].mean().reset_index()
    resum_dis_hab_lav = resum_dis_hab_lav[(resum_dis_hab_lav["Total dormitoris"]>0) & (resum_dis_hab_lav["Banys i lavabos"]>0)]
    resum_dis_hab_lav["Total dormitoris"] = resum_dis_hab_lav["Total dormitoris"].astype(str) + " habitacions"
    resum_dis_hab_lav["Banys i lavabos"] = resum_dis_hab_lav["Banys i lavabos"].astype(str) + " lavabos"
    resum_dis_hab_lav = resum_dis_hab_lav.round(1)
    resum_dis_hab_lav[["Preu mitjà", "Preu m2 útil", "Superfície útil"]] = resum_dis_hab_lav[["Preu mitjà", "Preu m2 útil", "Superfície útil"]].map(lambda x: '{:,.0f}'.format(x).replace(',', '#').replace('.', ',').replace('#', '.'))
    if pivot_name=="Preu m2 útil":
        resum_dis_hab_lav_pivoted_preu = resum_dis_hab_lav.pivot(index="Total dormitoris", columns="Banys i lavabos", values=pivot_name)
        return(resum_dis_hab_lav_pivoted_preu)
    if pivot_name=="Superfície útil":
        resum_dis_hab_lav_pivoted_super = resum_dis_hab_lav.pivot(index="Total dormitoris", columns="Banys i lavabos", values=pivot_name)
        return(resum_dis_hab_lav_pivoted_super)
@st.cache_resource
def caracteristiques_dis(df_hab, dis):
    table_tipus = df_hab[df_hab["Municipi"]=="Barcelona"].groupby(['Nom DIST'])[["Total dormitoris","Banys i lavabos","Cuines estàndard","Cuines americanes","Terrasses, balcons i patis","Estudi/golfes","Safareig", "Altres interiors", "Altres exteriors"]].mean().reset_index()
    table_tipus = table_tipus[table_tipus['Nom DIST']==dis].T
    table_tipus.columns = ["Total"]
    table_tipus = table_tipus[table_tipus.index!="Nom DIST"]
    table_tipus["Total"] = round(table_tipus["Total"].astype(float),2)
    table62_hab = table_tipus.sort_values("Total", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=table62_hab["Total"],
        y=table62_hab.index,
        orientation="h",
        marker=dict(color="#66b9a7"),
    ))
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Tipus d'habitatge",
    )
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def qualitats_dis(df_hab, dis):
    table62_hab = df_hab[(df_hab["Municipi"]=="Barcelona") & (df_hab["Nom DIST"]==dis)][["Aire condicionat","Bomba de calor","Aerotèrmia","Calefacció","Preinstal·lació d'A.C./B. Calor/Calefacció",'Parquet','Armaris encastats','Placa de cocció amb gas','Placa de cocció vitroceràmica',"Placa d'inducció",'Plaques solars']].sum(axis=0)
    table62_hab = pd.DataFrame({"Equipaments":table62_hab.index, "Total":table62_hab.values})
    table62_hab = table62_hab.set_index("Equipaments").apply(lambda row: row.mul(100) / df_hab[(df_hab["Municipi"]=="Barcelona") & (df_hab["Nom DIST"]==dis)].shape[0])
    table62_hab = table62_hab.sort_values("Total", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=table62_hab["Total"],
        y=table62_hab.index,
        orientation="h",
        marker=dict(color="#66b9a7"),
    ))
    fig.update_layout(
        xaxis_title="% d'habitatges en oferta",
        yaxis_title="Qualitats",
    )
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def equipaments_dis(df_hab, dis):
    table67_hab = df_hab[(df_hab["Municipi"]=="Barcelona") & (df_hab["Nom DIST"]==dis)][["Zona enjardinada", "Parc infantil", "Piscina comunitària", "Traster", "Ascensor", "Equipament Esportiu", "Sala de jocs", "Sauna", "Altres", "Cap dels anteriors"]].sum(axis=0, numeric_only=True)
    table67_hab = pd.DataFrame({"Equipaments":table67_hab.index, "Total":table67_hab.values})
    table67_hab = table67_hab.set_index("Equipaments").apply(lambda row: row.mul(100) / df_hab[(df_hab["Municipi"]=="Barcelona") & (df_hab["Nom DIST"]==dis)].shape[0])
    table67_hab = table67_hab.sort_values("Total", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=table67_hab["Total"],
        y=table67_hab.index,
        orientation="h",
        marker=dict(color="#66b9a7"),
    ))
    fig.update_layout(
        xaxis_title="% d'habitatges en oferta",
        yaxis_title="Equipaments",
    )
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def plot_table_energ_dis(df_hab, dis):
    table67hab_aux = df_hab[(df_hab["Municipi"]=="Barcelona") & (df_hab["Nom DIST"]==dis)][["QENERGC"]].value_counts().reset_index()
    table67hab_aux.columns = ["Qualificació energètica", "Habitatges"]
    table67hab_ener = table67hab_aux.assign(index=table67hab_aux["Qualificació energètica"].map({"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "En tràmits": 8, "Sense informació": 9}))
    table67hab_ener['Grup'] = table67hab_ener["Qualificació energètica"].map(
        {"A": "A", 
        "B": "B", 
        "C": "C-G", 
        "D": "C-G", 
        "E": "C-G", 
        "F": "C-G", 
        "G": "C-G", 
        "En tràmits": "En tràmits", 
        "Sense informació": "Sense informació"}
    )
    table67hab_ener = table67hab_ener.drop("index", axis=1)
    table67hab_grouped = table67hab_ener.groupby("Grup").sum().reset_index()
    table67hab_grouped["Habitatges"] = round(table67hab_grouped["Habitatges"] * 100 / df_hab[(df_hab["Municipi"]=="Barcelona") & (df_hab["Nom DIST"]==dis)].shape[0], 1)
    fig = px.pie(table67hab_grouped, values='Habitatges', names="Grup", title="", hole=0.4,
                color="Grup",color_discrete_sequence=["#AAC4BA", "#008B6C", "#00D0A3", "#D8BEB3", "white"])
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(legend=dict(x=0, y=1.25, orientation="h"))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def n_promocions_habs_dis(df_prom, dis):
    grandaria_promo = df_prom[(df_prom["Municipi"]=="Barcelona") & (df_prom["Nom DIST"].str[3:] == dis)][["HABIT"]].rename(columns={"HABIT":"count"}).reset_index().drop("index", axis=1)
    grandaria_promo = grandaria_promo.sort_values("count", ascending=False).reset_index().drop("index", axis=1)
    mean_promo = grandaria_promo["count"].mean()
    fig = px.histogram(grandaria_promo, 
                x=grandaria_promo["count"], nbins=11, 
                )
    fig.update_layout(
        xaxis_title="Nombre d'habitatges per promoció",
        yaxis_title="Nombre de promocions al municipi",
        bargap=0.1
    )
    fig.add_annotation(
        x=1, y=1, 
        text=f"<b>Mitjana d'habitatges totals per promoció: {mean_promo:.0f}</b>",
        showarrow=False,
        xref="paper", yref="paper",
        font=dict(size=15, color="black"),
        bgcolor="#66b9a7", 
        borderwidth=1,
        borderpad=4
    )

    fig.update_traces(marker=dict(color="#66b9a7"))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return fig
@st.cache_resource
def cale_tipus_dis(df_prom, dis):
    cale_tipus_dis = df_prom[df_prom["Municipi"]=="Barcelona"][['Nom DIST','De gasoil', 'De gas natural','De propà', "D'electricitat", "No s'indica tipus"]].fillna(0).groupby("Nom DIST")[['De gasoil', 'De gas natural','De propà', "D'electricitat", "No s'indica tipus"]].sum().reset_index()
    cale_tipus_dis["Nom DIST"] = cale_tipus_dis["Nom DIST"].str[3:]
    cale_tipus_dis = cale_tipus_dis[cale_tipus_dis["Nom DIST"]==dis].transpose(copy=True).reset_index()
    cale_tipus_dis.columns = ["Tipus", "Total"]
    cale_tipus_dis = cale_tipus_dis[cale_tipus_dis["Tipus"]!="Nom DIST"]
    fig = px.pie(cale_tipus_dis, values='Total', names="Tipus", title="", hole=0.4,
    color="Tipus",color_discrete_sequence=["#00D0A3", "#D8BEB3","#AAC4BA", "#008B6C", "white"])
    fig.update_traces(textposition='outside', textinfo='percent+label', sort=False)
    # fig.update_layout(legend=dict(x=0, y=1.15, orientation="h"))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
@st.cache_resource
def aparcament_dis(df_hab, dis):
    table_aparcament_dis_aux = df_hab[df_hab["APAR"]!="Altres"][["Nom DIST", "APAR"]].groupby(["Nom DIST", "APAR"]).size().reset_index().rename(columns={0:"Unitats"})
    table_aparcament_dis = table_aparcament_dis_aux.pivot_table(index="Nom DIST", columns="APAR", values="Unitats").reset_index()
    table_aparcament_dis = table_aparcament_dis[table_aparcament_dis["Nom DIST"]==dis].transpose(copy=True).reset_index()
    table_aparcament_dis.columns = ["Tipus", "Total"]
    table_aparcament_dis = table_aparcament_dis[table_aparcament_dis["Tipus"]!="Nom DIST"]
    fig = px.pie(table_aparcament_dis, values='Total', names="Tipus", title="", hole=0.4,
    color="Tipus",color_discrete_sequence=["#AAC4BA","#00D0A3","white"])
    fig.update_traces(textposition='outside', textinfo='percent+label', sort=False)
    fig.update_layout(legend=dict(x=0, y=1.3, orientation="h"))
    fig.layout.paper_bgcolor = "#cce8e2"
    fig.layout.plot_bgcolor = "#cce8e2"
    return(fig)
############################################################  CATALUNYA: 2022 ################################################
if selected == "Catalunya":
    # with stylable_container(
    # key="menu_cat",
    # css_styles=[
    # """
    # {
    #     position: fixed;
    #     z-index:100;
    #     margin-top:50px;
    # }
    # """]):
    left, right = st.columns((1,1))
    with left:
        edicio_any = ["2022","2023","2024", "1S2025"]
        selected_edition = st.radio("**Any**", edicio_any, edicio_any.index("2024"), horizontal=True)
    with right:
        if selected_edition!="1S2025":
            index_names = ["Introducció","Característiques", "Qualitats i equipaments", "Superfície i preus", "Comparativa any anterior"]
            selected_index = st.radio("**Contingut**", index_names, horizontal=True)
        if selected_edition=="1S2025":
            index_names = ["Introducció","Característiques", "Superfície i preus", "Comparativa any anterior"]
            selected_index = st.radio("**Contingut**", index_names, horizontal=True)
    if selected_edition=="2022":
        if selected_index=="Introducció":
            st.subheader("**ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ: INTRODUCCIÓ**")
            st.write("""<p style="margin-top: 10px"> L’Estudi de l’Oferta d’Habitatge de Nova Construcció de 2022 ha inclòs un total de 84
                municipis de Catalunya, en els quals s’han censat 928
                promocions d’obra nova (87 menys que l’any passat) i un
                total de 21.796 habitatges, dels quals un 37,5% estan a
                la venda (8.181, un 30% més que l’any passat).
                Aquesta oferta activa -en funció de
                les promocions- és força similar a
                les províncies de Barcelona i Tarragona (36,2% i 33,2% respectivament), i s’incrementa significativament a Girona (52,1%) i Lleida (44,8%).
                De tots els municipis analitzats, el que compta amb més
                presència d’oferta és el de Barcelona, amb un total de
                199 promocions i 1.390 habitatges en venda. Addicionalment, els municipis amb més promocions de Catalunya són
                Sabadell, L’Hospitalet de Llobregat, Badalona, Terrassa i Vilanova i la Geltrú.
                Dels habitatges en oferta de venda a les promocions analitzades en aquest estudi un 25,5% estan finalitzats i un
                47,2% es troben en diferents fases constructives. 
                Per tipologies edificatòries, destaquen els habitatges plurifamiliars de bloc tancat, concretament, el 57,9% dels
                habitatges, mentre que els plurifamiliars de bloc obert registren un 38%. A més distància, es situen els habitatges
                unifamiliars adossats (3,8%) i els unifamiliars aïllats (0,4%).
                Finalment, la major part dels habitatges inclosos en l’estudi 2022 són d’obra nova (93,6%), reduint-se la rehabilitació integral
                a un 6,4% (4 dècimes menys que a 2021), majoritàriament concentrada als municipis de la província de Barcelona
                (88,9%) i de forma destacada al municipi de Barcelona (31,5% del total d’habitatges en venda).</p></body>""",
            unsafe_allow_html=True)
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.markdown("""**Nombre de promocions per província a Catalunya**""")
                st.pyplot(map_prov_prom(bbdd_estudi_prom, shapefile_prov))
            with right_col:
                st.markdown("**Nombre d'habitatges en oferta per municipis a Catalunya**")
                @st.cache_resource
                def map_mun_hab_oferta():
                    prommun_map = bbdd_estudi_prom[["CODIMUN", "Municipi","HABIP"]].groupby(["CODIMUN", "Municipi"]).sum().reset_index()
                    prommun_map.columns = ["municipi", "Municipi_n", "Habitatges en oferta"]
                    prommun_map["municipi"] = prommun_map["municipi"].astype(float)

                    shapefile_mun = gpd.read_file(path + "shapefile_mun.geojson")
                    shapefile_mun["municipi"] = shapefile_mun["municipi"].astype(float)
                    tmp = pd.merge(shapefile_mun, prommun_map, how="left", on="municipi")
                    fig, ax = plt.subplots(1,1, figsize=(20,20))
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes("right", size="3%", pad=-1) #resize the colorbar
                    cmap = colors.LinearSegmentedColormap.from_list("mi_paleta", ["#AAC4BA","#008B6C"]) 
                    tmp['Habitatges en oferta']= tmp['Habitatges en oferta'].astype(float)
                    tmp.plot(column='Habitatges en oferta', ax=ax,cax=cax, cmap=cmap, legend=True)
                    tmp.geometry.boundary.plot(color='black', ax=ax, linewidth=0.3) #Add some borders to the geometries
                    ax.axis('off')
                    fig.patch.set_alpha(0)
                    return(fig)
                st.pyplot(map_mun_hab_oferta())
        if selected_index=="Característiques":
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.subheader("**CARACTERÍSTIQUES**")
                st.write("""
                <p>
                    Les principals tipologies en oferta als municipis catalans estudiats són els habitatges de 3 dormitoris i 2
                    banys (45,3%). Amb percentatges menors, però significatius es contemplen els habitatges de 2 dormitoris i 2
                    banys (16,8%), els de 2 dormitoris i 1 bany (12,0%), i els de 4 dormitoris i 2 banys (8,8%).
                    Els habitatges a la venda a Catalunya per nombre de dormitoris són els següents: els tipus loft (39); els
                    d’un dormitori (431) els de 2 dormitoris (2.432); els de tres dormitoris (4.138); els de quatre dormitoris (1.088), i
                    els de cinc o més dormitoris (53).
                </p>""",
                unsafe_allow_html=True
                )
            with right_col:
                st.plotly_chart(plot_caracteristiques(bbdd_estudi_hab), use_container_width=True, responsive=True)

        if selected_index=="Qualitats i equipaments":
            st.subheader("**QUALITATS I EQUIPAMENTS**")
            st.write("""
            <p>
                Les qualitats més recurrents en els habitatges són: la bomba de calor -fred
                i calor- (83,6%), la placa d’inducció (69,8%), el parquet (62,5%), els armaris
                encastats (59,4%), l’aerotèrmia (47,3%), la calefacció instal·lada només
                calor (42,94%), la placa de cocció vitroceràmica (21,7%) i les plaques solars
                (12,5%).
                Quant a equipaments, el més comú és l’ascensor (91,6%), seguit a certa
                distància per la piscina comunitària (50,3%), el traster (48,4%) i la zona enjardinada
                (37,7%).
            </p>""",
            unsafe_allow_html=True
            )
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.write("""<p><b>Principals qualitats dels habitatges</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(plot_qualitats(bbdd_estudi_hab), use_container_width=True, responsive=True)


            with right_col:
                st.write("""<p><b>Principals equipaments dels habitatges</b></p>""", unsafe_allow_html=True)
                # st.plotly_chart(plot_equipaments(bbdd_estudi_hab), use_container_width=True, responsive=True)
                st.write(plot_equipaments(bbdd_estudi_hab))

        if selected_index=="Superfície i preus":
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.subheader("SUPERFÍCIE I PREUS")
                st.write("""
                <p>
                    En general, conforme augmenta la superfície també ho
                    fa el nombre de dormitoris, situant-se la màxima recur-
                    rència en els habitatges de 3 dormitoris entre els 60m\u00b2 i els
                    90m\u00b2, i en els de 2 dormitoris amb superfícies inferiors
                    als 70m\u00b2.
                    La mitjana de la superfície útil dels habitatges en venda
                    en els municipis estudiats és de 80,7m\u00b2, amb un preu
                    mitjà de 368.809€ (4.532,6€/m\u00b2 útil). Per sota de la mitjana de preu, a nivell general, es situen els habitatges d’un,
                    de dos i de tres dormitoris. Si l’anàlisi es fa a partir de la
                    mitjana del preu m\u00b2 útil, per sota de la mitjana resten els
                    habitatges de 3 i 4 dormitoris.
                    El 16,8% del conjunt d’habitatges en oferta de venda
                    no supera els 210.000€. Entre aquests habitatges se situen el 46,6% de les d’un dormitori i el 29,2% dels de
                    dos dormitoris. A la banda més alta es troben el 9,9% d’habitatges amb preus superiors als 600.000€, entre els
                    quals es localitza el 66,0% dels de cinc o més dormitoris.
                    Els habitatges unifamiliars obtenen mitjanes de superfície força més altes (155,5m\u00b2), així com de preu
                    (515.392€), però el m\u00b2 útil (3.302€/m\u00b2) se situa per sota
                    la mitjana general, evidenciant que el desplaçament a
                    l’alça del preu no compensa el de la superfície.
                    Els habitatges plurifamiliars estan més propers a les
                    mitjanes generals, doncs aporten força més influència sobre aquestes, amb una mitjana de superfície de
                    77,5m\u00b2, un preu de venda de 362.492€, i un preu de venda per m\u00b2 útil de 4.586€.
                </p>""",
                unsafe_allow_html=True
                )

            with right_col:
                st.write("""<p><b>Preu mitjà per tipologia d'habitatge (€)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_preu_mitjanes(bbdd_estudi_hab_mod), use_container_width=True, responsive=True)
            left, right = st.columns((1,1))
            with left:
                st.write("""<p><b>Preu per m\u00b2 útil per tipologia d'habitatge (€/m\u00b2 útil)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_preum2_mitjanes(bbdd_estudi_hab_mod), use_container_width=True, responsive=True)
            with right:
                st.write("""<p><b>Superfície útil per tipologia d'habitatge (m\u00b2 útil)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_super_mitjanes(bbdd_estudi_hab_mod), use_container_width=True, responsive=True)
        if selected_index=="Comparativa any anterior":
            left_col, right_col = st.columns((1, 1))
            with left_col: 
                st.subheader("**COMPARATIVA 2022-2021**") 
                st.write("""
                <p>
                    El 2022, els municipis estudiats registren un nombre de promocions inferior en 87 unitats respecte de
                    2021, aconseguint les 928. En relació amb el nombre
                    d’habitatges, el total de 2022 (8.181 habitatges) suposa un increment del 30% respecte dels 6.294 habitatges
                    registrats el 2021. Cal fer esment que de les 1.015 promocions de 2021, 601 ja han estat totalment venudes
                    al 2022 i, en relació als habitatges de 2021, el 52,6%
                    han estat venuts. En definitiva, el cens dut a terme el
                    2022 -com va passar l’any anterior- suposa una important renovació de les unitats mostrals: el 55,4% de les
                    promocions són de nova incorporació, i pel que fa als
                    habitatges es van incorporar un 63,5% de nous respecte
                    a l’any 2021.
                    Respecte de les tipologies de promoció, les variacions
                    respecte 2021 són molt atenuades, mantenint-se la seva
                    distribució proporcional. Si aquesta mateixa anàlisi es
                    fa per habitatges, pràcticament no varien els números
                    de 2022 en relació amb 2021 i, lògicament per la seva
                    morfologia, els habitatges plurifamiliars són la majoria
                    (95,9% el 2022 vers 94,7% el 2021).
                </p>
                <p>
                    La superfície mitjana dels habitatges a la venda el
                    2022 és de 80,7m\u00b2, amb un descens del 4,9% respecte de 2021. Aquest descens es registra en els diferents
                    tipus d’habitatge, a excepció dels de 5 i més dormitoris, que registren un increment de superfície del 7,4%.
                    El preu mitjà de l’habitatge a la venda en els municipis
                    estudiats a Catalunya el 2022 és de 368.809€, un 2%
                    menys que el registrat el 2021. Aquest descens de preu
                    es dona només a la tipologia d’habitatges de 3 dormitoris (la més nombrosa), mentre que a la resta de les
                    tipologies el preu s’incrementa de forma molt lleu, entre
                    un 0,8% i un 2%, excepte els habitatges de 5 i més dormitoris, amb un augment del 5,7%, si bé només hi ha 53
                    unitats censades. Pel que fa al preu per m\u00b2 útil, en el conjunt dels municipis estudiats, és de 4.533€, valor que suposa un preu
                    superior en un 2,5% respecte del 2021.
                </p>
                <p>
                    Per tipologia, els habitatges unifamiliars registren un descens del
                    -9,0% pel que fa a superfície mitjana, i un lleuger -0,9%
                    pel que fa al preu mitjà de venda, mentre que el preu per
                    m\u00b2 útil s’incrementa de mitjana un 8,3%.
                    Per altra banda, els habitatges plurifamiliars veuen disminuïda la seva
                    superfície (-3,2%), i presenten variació quant a preu,
                    amb un descens del preu mitjà de venda del -1,6%, i un
                    augment d’un 2,0% pel que fa a preu m\u00b2 útil.
                </p>
                <p>
                    En aquest sentit, cal recordar que l’evolució de l’IPC a
                    l’exercici 2022 ha estat del 8%.
                </p>""",
                unsafe_allow_html=True
                )
            with right_col:
                st.markdown("")
                st.write("""<p><b>Variació anual dels principals indicadors per tipologia d'habitatge (%)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(plot_var_CAT(table117_22, table121_22, table125_22), use_container_width=True, responsive=True)
            st.markdown(table_geo_cat(2019, int(selected_edition)).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo_cat(2019, int(selected_edition)), f"Estudi_oferta_Catalunya_22.xlsx"), unsafe_allow_html=True)


############################################################  CATALUNYA: 2023 ################################################
    if selected_edition=="2023":
        if selected_index=="Introducció":
            st.subheader("**ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ: INTRODUCCIÓ**")
            st.write("""<p style="margin-top: 10px"> 
            <p>
            Les dades exposades presenten els resultats de l'Estudi d'Oferta de Nova Construcció a Catalunya de l'any 2023 per tal de disposar d’informació actualitzada del sector i de la seva evolució, en diferents nivells de 
            desagregació territorial (província, municipi, …). Aquest treball té una base censal resultat d’una recerca exhaustiva de les ofertes de les promocions d’habitatge d’obra nova mitjançant un treball de camp amb recerques on-line, telefòniques i algunes visites presencials. 
            El cens parteix de la darrera actualització realitzada l’any precedent (2022). En aquesta edició incorporem 33 municipis addicionals incrementant l'abast de l'estudi fins a 135 municipis, seleccionats per criteris demográfics.
            En l’execució del treball de camp no han estat incloses les promocions amb limitació d’informació disponible, és a dir, sense informació contrastada de preus i superfícies. 
            </p>
            <p>
            Com a punt de partida, l’estudi d'oferta de 2023 inclou 116 municipis rellevants en l’àmbit de l’habitatge, distribuïts per tot el territori, en els quals s’han inventariat 1.123 promocions d’obra nova, amb un total de 10.296 habitatges a la venda. 
            Respecte el 2022, el nombre de promocions registrades ha incrementat en 195 promocions i el nombre total d’habitatges a la venda ha passat de 8.181 a 10.296, és a dir, un 26% més.
            En relació a les bases mostrals de promocions i habitatges, les dades de 2023 inclouen 665 promocions de l’edició de 2022, és a dir, el 71,7% de les promocions de 2022 continuen tenint algun habitatge en venda un any després. 
            Pel que fa als habitatges, dels 8.181 censats l’any 2022, el 24,0% han estat venuts i, per tant, es mantenen en oferta 6.221 habitatges. Per completar la mostra de 2023, 
            s’han incorporat 458 promocions noves que en el seu conjunt acumulen una oferta de 4.075 habitatges.
            </p>
            <p>
            El municipi amb més presència d’oferta és el de Barcelona, amb un total de 224 promocions i 1.560 habitatges en venda. A continuació, els municipis amb més promocions són Sabadell amb 55 promocions i 663 habitatges, 
            Terrassa amb 51 promocions i 730 habitatges, Badalona amb 48 promocions i 315 habitatges i L’Hospitalet de Llobregat amb 46 promocions i 383 habitatges. 
            Per altra banda, s’han localitzat un total de 30 municipis amb una oferta inferior a 10 habitatges, corresponents a 1 o 2 promocions: en concret, 16 municipis a la província de Barcelona, 
            5 a la província de Girona, 3 a la província de Lleida i 6 a la província de Tarragona.        
            </p>
            """,
            unsafe_allow_html=True
        )
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.markdown("**Nombre de promocions per província a Catalunya**")
                st.pyplot(map_prov_prom(bbdd_estudi_prom_2023, shapefile_prov))
            with right_col:
                st.markdown("**Nombre d'habitatges en oferta per municipis a Catalunya**")
                @st.cache_resource
                def map_mun_hab_oferta23():
                    prommun_map = bbdd_estudi_prom_2023[["CODIMUN", "Municipi","HABIP"]].groupby(["CODIMUN", "Municipi"]).sum().reset_index()
                    prommun_map.columns = ["municipi", "Municipi_n", "Habitatges en oferta"]
                    prommun_map["municipi"] = prommun_map["municipi"].astype(int)

                    shapefile_mun = gpd.read_file(path + "shapefile_mun.geojson")
                    shapefile_mun["municipi"] = shapefile_mun["codiine"].astype(int)

                    tmp = pd.merge(shapefile_mun, prommun_map, how="left", on="municipi")
                    fig, ax = plt.subplots(1,1, figsize=(20,20))
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes("right", size="3%", pad=-1) #resize the colorbar
                    cmap = colors.LinearSegmentedColormap.from_list("mi_paleta", ["#AAC4BA","#008B6C"]) 
                    tmp['Habitatges en oferta']= tmp['Habitatges en oferta'].astype(float)
                    tmp.plot(column='Habitatges en oferta', ax=ax,cax=cax, cmap=cmap, legend=True)
                    tmp.geometry.boundary.plot(color='black', ax=ax, linewidth=0.3) #Add some borders to the geometries
                    ax.axis('off')
                    fig.patch.set_alpha(0)
                    return(fig)
                st.pyplot(map_mun_hab_oferta23())
        if selected_index=="Característiques":
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.subheader("**CARACTERÍSTIQUES**")
                st.write("""
                <p>
                El prototip d’habitatge mitjà a Catalunya tindria les següents característiques: 2,7 dormitoris, 1,9 banys i/o lavabos, 74,7% cuina americana, 25,3% cuina estàndard i amb 1 terrassa, balcó o pati.
                Segons el nombre d'habitacions: els tipus loft (40 habitatges) es caracteritzen per tenir un sol espai i cuina americana; els d’un sol dormitori (535 habitatges) majoritàriament tenen un sol bany (83,6%) 
                i cuina americana (93,3%); en els de dos dormitoris (3.100 habitatges) el 55,4% tenen més d’un bany, la cuina americana també és majoritària (86,3%), així com la disposició de terrasses, balcons i/o patis (75,0%); 
                en els de tres dormitoris (5.222 habitatges) la pràctica totalitat (97,7%) tenen més d’un bany, la cuina americana també és majoritària (70,7%) i el 83,0% disposen de terrasses, balcons i/o patis; 
                en els de quatre dormitoris (1.334 habitatges) pràcticament tots tenen més d’un bany (99,9%), el 55,5% compten amb cuina americana, el 86,7% disposa de terrasses, balcons i/o patis i un 49,6% té safareig; 
                en els de cinc i més dormitoris (65 habitatges) tots tenen dos banys o més, la cuina americana també és majoritària (69,2%), el 96,9% disposen de terrasses, balcons i/o patis i un 52,3% disposen de safareig.
                Així, la principal tipologia en oferta seria la dels habitatges de 3 dormitoris i 2 banys (45,4%). Amb percentatges menors però significatius es contemplen els habitatges de 2 dormitoris i 2 banys (15,6%), 
                els de 2 dormitoris i 1 bany (13,4%) i els de 4 dormitoris i 2 banys (8,1%).
                </p>""",
                unsafe_allow_html=True
                )
            with right_col:
                st.plotly_chart(plot_caracteristiques(bbdd_estudi_hab_2023), use_container_width=True, responsive=True)
        if selected_index=="Qualitats i equipaments":
            st.subheader("**QUALITATS I EQUIPAMENTS**")
            st.write("""
            <p>
                Les qualitats més recurrents als habitatges són: la bomba de calor -fred i calor- (87,6%), 
                la placa d’inducció (71,4%), el parquet (66,5%), la calefacció instal·lada només calor (64,5%), 
                la aerotèrmia (58,8%) i els armaris encastats (53,4%).
                Quant a equipaments, el més comú és l’ascensor (91,0%), 
                seguit a certa distància per el traster (49,7%), la piscina comunitària (48,5%) 
                i la zona enjardinada (38,1%).
            </p>""",
            unsafe_allow_html=True
            )
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.write("""<p><b>Principals qualitats dels habitatges (%)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(plot_qualitats(bbdd_estudi_hab_2023), use_container_width=True, responsive=True)

            with right_col:
                st.write("""<p><b>Principals equipaments dels habitatges (%)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(plot_equipaments(bbdd_estudi_hab_2023), use_container_width=True, responsive=True)

        if selected_index=="Superfície i preus":
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.subheader("SUPERFÍCIES I PREUS")
                st.write("""
                <p>
                En general, conforme augmenta la superfície, incrementa el nombre de dormitoris, situant-se la màxima recurrència en els habitatges de 3 dormitoris entre els 60 i els 90 m² (3.950 habitatges, 38,4% de l’oferta d’habitatges) 
                i en els de 2 dormitoris amb superfícies inferiors als 70 m² (2.379 habitatges, 23,1% de l’oferta d’habitatges). En els extrems es trobarien els 721 habitatges de menys de 50 m² bàsicament amb 1 o 2 dormitoris i els 
                231 habitatges de més de 160 m² a l’entorn de 4 dormitoris. A la vista de les dades, s’expressa també una certa correlació entre les variables preu habitatge i nombre de dormitoris, 
                de tal manera que quants més dormitoris té en disposició l’habitatge, major és el seu preu de venda en general. 
                El 16,2% del conjunt d’habitatges en oferta no supera els 210.000€ (l’any 2020 aquest percentatge era del 22,9%, l’any 2021 del 18,8% i l’any 2022 del 16,8%) i entre aquests habitatges es situen el 42,6% dels d’un dormitori.
                Addicionalment i seguint la lògica expressada, un major nombre de dormitoris, implica generalment una major superfície, per tant, a la relació entre la variable preu i nombre de dormitoris cal afegir-li la variable superfície. 
                No obstant això, cal considerar obviament la incidència d’altres variables (localització, qualitats, ...) que fan que aquesta relació no tingui un comportament lineal. Els dos extrems de la relació entre superfície útil i preu, 
                serien el 53,5% dels habitatges de menys de 50 m² que es situen en preus inferiors a 210.000€ i el 64,5% d’habitatges de més de 160 m² que es situen en preus per sobre els 600.000€.
                </p>
                <p>      
                La mitjana de la superfície útil dels habitatges censats és de 80,6 m² i la del preu, de 365.798€ (4.492,7€/m² útil). Generalment, per sota de la mitjana de preu es situen els habitatges d’un i de dos dormitoris. 
                Si l’anàlisi es fa a partir de la mitjana del preu/m\u00b2 útil, per sota la mitjana resten els habitatges de 3 i 4 dormitoris. En els habitatges unifamiliars s’obtenen mitjanes de superfície força més altes (145,4 m²), 
                així com de preu (540.465€), però el m² útil (3.741,5€) es situa per sota la mitjana general, evidenciant que el desplaçament a l’alça del preu no compensa el de la superfície. Contràriament, els habitatges plurifamiliars es troben més 
                propers a les mitjanes generals doncs aporten força més influència degut a la seva elevada proporció sobre el total, sent aquesta aportació de 77,2 m² de superfície i de 356.751€ de preu (4.531,6€/m² útil).   
                </p>         
                """,
                unsafe_allow_html=True
                )

            with right_col:
                st.write("""<p><b>Preu mitjà per tipologia d'habitatge (€)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_preu_mitjanes(bbdd_estudi_hab_mod_2023), use_container_width=True, responsive=True)
            left, right = st.columns((1,1))
            with left:
                st.write("""<p><b>Preu per m\u00b2 útil per tipologia d'habitatge (€/m\u00b2 útil)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_preum2_mitjanes(bbdd_estudi_hab_mod_2023), use_container_width=True, responsive=True)
            with right:
                st.write("""<p><b>Superfície útil per tipologia d'habitatge (m\u00b2 útil)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_super_mitjanes(bbdd_estudi_hab_mod_2023), use_container_width=True, responsive=True)

        if selected_index=="Comparativa any anterior":
            left_col, right_col = st.columns((1, 1))
            with left_col: 
                st.subheader("**COMPARATIVA 2023-2022**") 
                st.write("""
                <p>
                    L’any 2023 s’han registrat un total de 1.123 promocions i suposa un increment de 195 promocions respecte 2022. El nombre d'habitatges va augmentar de 8.181 al 2022 a 10.296 habitatges al 2023, que suposa un increment del 25,9%.
                    Cal esmentar que de les 928 promocions de 2022, 263 ja han estat totalment venudes al 2023 i, en el cas dels habitatges, el 24,0% han estat venuts.
                    Respecte de les quatre tipologies de promoció (unifamiliars aïllades o adossats i plurifamiliars en bloc obert o tancat), les variacions són molt atenuades respecte 2022, 
                    mantenint-se la seva distribució. Si aquest mateix anàlisi es fa per habitatges, les variacions són reduides i els habitatges plurifamiliars continuen sent majoritaris (95,1% en 2023, 95,9% en 2022). 
                </p>
                <p>
                    La superfície mitjana dels habitatges a la venda és de 80,6 m² (80,7 m² l’any 2022), amb una lleugera variació del -0,2%. Aquesta variació és irregular en els diferents tipus d’habitatges, 
                    assolint un descens màxim del -4,1% als habitatges tipus loft i un increment de l’1,9% als de 4 dormitoris. 
                </p>
                <p>
                    El preu mitjà de l’habitatge a la venda a Catalunya és de 365.798€, un 0,8% inferior al registrat en el cens de 2022. Aquest descens de preu es dona de manera més acusada als habitatges tipus loft (-5,0%) i de 2 dormitoris (-4,6%).
                    Contràriament, els habitatges de 5 i més dormitoris incrementen el seu preu en un 7,0% i el d’1 dormitori en un 5,1%. 
                </p>
                <p>
                    Pel que fa al preu per m² útil, en el conjunt dels municipis és de 4.492,7€, valor que suposa un preu inferior en gairebé un punt (0,9%) en referència a 2022. 
                    El comportament per tipologies es positiu en els habitatges de 5 i més dormitoris i d’1 dormitori, nul en els de 3 dormitoris i negatiu en els casos dels loft i de 2 i 4 dormitoris.
                </p>""",
                unsafe_allow_html=True
                )
            with right_col:
                st.markdown("")
                st.write("""<p><b>Variació anual dels principals indicadors per tipologia d'habitatge (%)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(plot_var_CAT(table117_23, table121_23, table125_23), use_container_width=True, responsive=True)
            st.markdown(table_geo_cat(2019, int(selected_edition)).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo_cat(2019, int(selected_edition)), f"Estudi_oferta_Catalunya_2023.xlsx"), unsafe_allow_html=True)

############################################################  CATALUNYA: 2024 ################################################
    if selected_edition=="2024":
        if selected_index=="Introducció":
            st.subheader("**ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ: INTRODUCCIÓ**")
            st.write("""<p style="margin-top: 10px"> 
            <p>
            Les dades exposades presenten els resultats de l'Estudi d'Oferta de Nova Construcció a Catalunya de l'any 2024 per tal de disposar d’informació actualitzada del sector i de la seva evolució, en diferents nivells de desagregació territorial (província, municipi…). Aquest treball té una base censal resultat d’una recerca exhaustiva de les ofertes de les promocions d’habitatge d’obra nova mitjançant un treball de camp amb recerques online, telefòniques i algunes visites presencials. El cens parteix de la darrera actualització realitzada l’any precedent (2023). En aquesta edició incorporem 141 municipis en total, 6 municipis més que en l’edició de 2023 municipis, tots seleccionats per criteris demográfics. En l’execució del treball de camp no han estat incloses les promocions amb limitació d’informació disponible, és a dir, sense informació contrastada de preus i superfícies.
            </p>
            <p>    
            Com a punt de partida, l’estudi de 2024 inclou 120 municipis rellevants en l’àmbit de l’habitatge, distribuïts per tot el territori, en els quals s’han inventariat 1.138 promocions d’obra nova, amb un total de 6.610 habitatges a la venda. Respecte a l’any 2023 quan es van inventariar 1.123 promocions, el nombre de promocions registrades s'ha incrementat en 15 promocions més i el nombre total d’habitatges a la venda ha passat de 10.296 a 6.610, es a dir, ha baixat en 3.686 unitats, un 35,8% menys. En relació a les bases mostrals de promocions i habitatges, les dades de 2024 inclouen 651 promocions de l’edició de 2023, és a dir, el 58,0% de les promocions de 2023, un any després continuen tenint algun habitatge en venda. Pel que fa als habitatges, dels 10.296 censats l’any 2023, el 66,4% han estat venuts i, per tant, es mantenen en oferta 3.455 habitatges dels estudiats l’any passat.
            </p>
            <p>          
            El municipi amb més presència d’oferta és el de Barcelona, amb un total de 175 promocions i 800 habitatges en venda. A continuació, els municipis amb més promocions són Terrassa amb 54 promocions i 308 habitatges, Sabadell amb 50 promocions i 354 habitatges (és el segon municipi en ordre d’importància per nombre d’habitatges en oferta), Badalona amb 41 promocions i 193 habitatges, Vilanova i la Geltrú amb 38 promocions i 266 habitatges i L’Hospitalet de Llobregat amb 35 promocions i 251 habitatges. Per altra banda, s’han localitzat un total de 27 municipis amb una oferta inferior a 10 habitatges, corresponents a 1, 2, 3 o 4 promocions: en concret, 19 municipis a la província de Barcelona, 3 a la província de Girona, 2 a la província de Lleida i 3 a la província de Tarragona.
            </p>      
            """,
            unsafe_allow_html=True
        )
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.markdown("**Nombre de promocions per província a Catalunya**")
                st.pyplot(map_prov_prom(bbdd_estudi_prom_2024, shapefile_prov))
            with right_col:
                st.markdown("**Nombre d'habitatges en oferta per municipis a Catalunya**")
                @st.cache_resource
                def map_mun_hab_oferta24():
                    prommun_map = bbdd_estudi_prom_2024[["CODIMUN", "Municipi","HABIP"]].groupby(["CODIMUN", "Municipi"]).sum().reset_index()
                    prommun_map.columns = ["municipi", "Municipi_n", "Habitatges en oferta"]
                    prommun_map["municipi"] = prommun_map["municipi"].astype(int)

                    shapefile_mun = gpd.read_file(path + "shapefile_mun.geojson")
                    shapefile_mun["municipi"] = shapefile_mun["codiine"].astype(int)

                    tmp = pd.merge(shapefile_mun, prommun_map, how="left", on="municipi")
                    fig, ax = plt.subplots(1,1, figsize=(20,20))
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes("right", size="3%", pad=-1) #resize the colorbar
                    cmap = colors.LinearSegmentedColormap.from_list("mi_paleta", ["#AAC4BA","#008B6C"]) 
                    tmp['Habitatges en oferta']= tmp['Habitatges en oferta'].astype(float)
                    tmp.plot(column='Habitatges en oferta', ax=ax,cax=cax, cmap=cmap, legend=True)
                    tmp.geometry.boundary.plot(color='black', ax=ax, linewidth=0.3) #Add some borders to the geometries
                    ax.axis('off')
                    fig.patch.set_alpha(0)
                    return(fig)
                st.pyplot(map_mun_hab_oferta24())
        if selected_index=="Característiques":
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.subheader("**CARACTERÍSTIQUES**")
                st.write("""
                <p>
                El prototip d’habitatge mitjà a Catalunya tindria les següents característiques: 2,8 dormitoris, 2 banys i/o lavabos, 80% cuina americana, 20% cuina estàndard i amb 1,2 terrassa, balcó o pati. Segons el nombre d'habitacions: els d’un sol dormitori (301 habitatges) majoritàriament tenen un sol bany (81,7%) i cuina americana (98,7%); en els de dos dormitoris (1.840 habitatges) el 56,7% tenen més d’un bany, la cuina americana també és majoritària (90,4%), així com la disposició de terrasses, balcons i/o patis (85,9%); en els de tres dormitoris (3.388 habitatges) la pràctica totalitat (98,3%) tenen més d’un bany, la cuina americana també és majoritària (75,7%) i el 90,5% disposen de terrasses, balcons i/o patis; en els de quatre dormitoris (1.025 habitatges) pràcticament tots (el 99,9%) tenen més d’un bany, el 71,5% compten amb cuina americana, el 88,3% disposen de terrasses, balcons i/o patis i un 46,1% té safareig; en els de cinc i més dormitoris (54 habitatges) tots tenen dos banys o més, la cuina americana també és majoritària (81,5%), el 88,9% disposen de terrasses, balcons i/o patis i un 64,8% disposen de safareig. Així, la principal tipologia en oferta seria la dels habitatges de 3 dormitoris i 2 banys (45,0%). Amb percentatges menors però significatius es contemplen els habitatges de 2 dormitoris i 2 banys (15,1%), els de 2 dormitoris i 1 bany (12,0%) i els de 4 dormitoris i 2 banys (8,9%).
                </p>""",
                unsafe_allow_html=True
                )
            with right_col:
                st.plotly_chart(plot_caracteristiques(bbdd_estudi_hab_2024), use_container_width=True, responsive=True)
        if selected_index=="Qualitats i equipaments":
            st.subheader("**QUALITATS I EQUIPAMENTS**")
            st.write("""
            <p>
            Les qualitats més recurrents en els habitatges són: la bomba de calor -fred i calor- (90,7%), l’aerotèrmia (72,5%), la placa d’inducció (69,9%), el parquet (59,5%), la calefacció instal·lada només calor (55,4%), i els armaris encastats (43,1%). Quant a equipaments, el més comú és l’ascensor (88,0%), seguit a certa distància per la piscina comunitària (53,6%), el traster (47,2%), i la zona enjardinada (42,2%).
            </p>""",
            unsafe_allow_html=True
            )
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.write("""<p><b>Principals qualitats dels habitatges (%)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(plot_qualitats(bbdd_estudi_hab_2024), use_container_width=True, responsive=True)

            with right_col:
                st.write("""<p><b>Principals equipaments dels habitatges (%)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(plot_equipaments(bbdd_estudi_hab_2024), use_container_width=True, responsive=True)

        if selected_index=="Superfície i preus":
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.subheader("SUPERFÍCIES I PREUS")
                st.write("""
                <p>
                En general, conforme augmenta la superfície, augmenta el nombre de dormitoris, situant-se la màxima recurrència en els habitatges de 3 dormitoris entre els 60 i els 90 m² (2.428 habitatges, 36,7% de l’oferta d’habitatges) i en els de 2 dormitoris amb superfícies inferiors als 70 m² (1.334 habitatges, 20,2% de l’oferta d’habitatges). En els extrems es trobarien els 320 habitatges de menys de 50 m² bàsicament amb 1 o 2 dormitoris i, 239 habitatges de més de 160 m² a l’entorn de 4 dormitoris. A la vista de les dades, s’expressa també una certa correlació entre les variables preu habitatge i nombre de dormitoris, de tal manera que quants més dormitoris té en disposició l’habitatge, major és el seu preu de venda en general. El 9,7% del conjunt d’habitatges en oferta de venda no supera els 210.000€ (l’any 2020 aquest percentatge era del 22,9% , l’any 2021 del 18,8%, l’any 2022 del 16,8% i l’any 2023 del 16,2%), entre aquests habitatges es situen el 34,6% dels d’un dormitori. Addicionalment i seguint la lògica expressada, un major nombre de dormitoris, implica –en general- una major superfície, per tant a la relació entre la variable preu i nombre de dormitoris cal afegir-li la variable superfície. Sempre tenint en compte la incidència d’altres variables (localització, qualitats, ...) que fan que aquesta relació no tingui un comportament lineal. Els dos pols de la relació superfície útil – preu, serien el 48,4% dels habitatges de menys de 50 m² que es situen en preus inferiors a 210.000€ i el 59,4% d’habitatges de més de 160 m² que es situen en preus per sobre els 600.000€.
                </p>
                <p>
                La mitjana de la superfície útil dels habitatges censats, és de 85,3 m² i la de preu de 400.323€ (4.678,5€/m² útil). Per sota de la mitjana de preu, a nivell general, es situen els habitatges d’un i de dos dormitoris. Si l’anàlisi es fa a partir de la mitjana del preu/ m² útil, per sota la mitjana resten els habitatges de 3 i 4 dormitoris. En els habitatges unifamiliars s’obtenen mitjanes de superfície força més altes (147,0 m²), així com de preu (557.432€), però el m² útil (3.833,1€) es situa per sota la mitjana general, evidenciant que el desplaçament a l’alça del preu no compensa el de la superfície. Els habitatges plurifamiliars estan més propers a les mitjanes generals doncs aporten força més influència sobre aquestes, essent aquesta aportació de 79,9 m² de superfície i de 386.515€ de preu (4.752,8€/m² útil).
                </p>      
                """,
                unsafe_allow_html=True
                )

            with right_col:
                st.write("""<p><b>Preu mitjà per tipologia d'habitatge (€)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_preu_mitjanes(bbdd_estudi_hab_mod_2024), use_container_width=True, responsive=True)
            left, right = st.columns((1,1))
            with left:
                st.write("""<p><b>Preu per m\u00b2 útil per tipologia d'habitatge (€/m\u00b2 útil)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_preum2_mitjanes(bbdd_estudi_hab_mod_2024), use_container_width=True, responsive=True)
            with right:
                st.write("""<p><b>Superfície útil per tipologia d'habitatge (m\u00b2 útil)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_super_mitjanes(bbdd_estudi_hab_mod_2024), use_container_width=True, responsive=True)

        if selected_index=="Comparativa any anterior":
            left_col, right_col = st.columns((1, 1))
            with left_col: 
                st.subheader("**COMPARATIVA 2024-2023**") 
                st.write("""
                <p>
                L’any 2024 s’han registrat un total de 1.138 promocions, 15 més que les de 2023 (1.123 promocions). En relació al nombre d’habitatges, el total de 2024, 6.610 habitatges, suposen un 35,8% menys que els 10.296 de 2023. Cal esmentar que de les 1.123 promocions de 2023, 472 ja han estat totalment venudes al 2024 i, en relació als habitatges de 2023 (10.296), el 66,4% han estat venuts. 
                </p>
                <p>
                Respecte de les quatre tipologies de promoció (unifamiliars aïllades o adossats i plurifamiliars en bloc obert o tancat), en relació a l’any 2023, les variacions són molt atenuades, mantenint-se la seva distribució proporcional amb un lleuger descens de les plurifamiliars en bloc tancat (-7,0%). Si aquesta mateixa anàlisi es fa per habitatges, varien molt poc els nombres de 2024 en relació a 2023 i, lògicament per la seva morfologia, els habitatges plurifamiliars són la majoria (91,9% en 2024, 95,1% en 2023). 
                </p>
                <p>
                La superfície mitjana dels habitatges a la venda és de 85,3 m² (80,6 m² l’any 2023), amb una variació del 5,9%. Aquesta variació és irregular en els diferents tipus d’habitatges, assolint un increment màxim del 7,4% als habitatges de 4 dormitoris. 
                </p>
                <p>
                El preu mitjà de l’habitatge a la venda a Catalunya és de 400.323€, un 9,4% superior al registrat en el cens de 2023. Aquest increment de preu es dona de manera més acusada als habitatges d’1D, 2D, 3D i 4D (15,5%, 6,3%, 7,9% i 8,1% respectivament). 
                </p>
                <p>
                Pel que fa al preu per m² útil, en el conjunt dels municipis és de 4.678,5€, valor que suposa un preu superior en poc més quatre punts (4,1%) en referència a 2023. El comportament per tipologies es positiu en els habitatges en les diferents composicions d’habitatges a excepció dels extrems (loft i 5 o més dormitoris, on el preu per m² útil baixa un 5,8% i un 3,1%).
                </p>""",
                unsafe_allow_html=True
                )
            with right_col:
                st.markdown("")
                st.write("""<p><b>Variació anual dels principals indicadors per tipologia d'habitatge (%)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(plot_var_CAT(table117_24, table121_24, table125_24), use_container_width=True, responsive=True)
            st.markdown(table_geo_cat(2019, int(selected_edition)).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo_cat(2019, int(selected_edition)), f"Estudi_oferta_Catalunya_2024.xlsx"), unsafe_allow_html=True)

############################################################  CATALUNYA: 1S2025 ################################################
    if selected_edition=="1S2025":
        if selected_index=="Introducció":
            st.subheader("**ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ: INTRODUCCIÓ**")
            st.write("""<p style="margin-top: 10px"> 
            <p>
            L’Estudi de l’Oferta d’Habitatges de Nova Construcció a Catalunya en la seva edició de l’any 2025 contempla els resultats de l’anàlisi del mercat residencial d’habitatges de nova construcció a Catalunya amb les dades processades fins al mes de juny. Es tracta doncs, d’unes dades provisionals i que es completaran amb la resta de la recerca de dades que es durà a terme fins a finals d’any. Com novetat en l’edició de 2025, el nombre de municipis a estudiar s’ha incrementat, passant dels 141 de l’edició de 2024, a una selecció més amplia amb un total de 159 municipis. En l’execució del treball de camp no han estat incloses les promocions amb limitació d’informació disponible, bàsicament no han estat considerades com unitats vàlides per la mostra les promocions sense informació contrastada de preus i superfícies.
            Els resultats que es presenten inclouen les informacions de les promocions localitzades a 123 municipis dels 159 objecte d’estudi. Novament, cal incidir en que es tracta de dades provisionals i que les feines de recerca continuen i la cobertura de municipis s’incrementarà a finals d’any.
            </p>
            <p>    
            De les 1.138 promocions d’obra nova inventariades al 2024, 426, el 37,4% ja han estat totalment venudes al juny de 2025. En conseqüència, actualment la mostra de l’estudi inclou 712 promocions de les 1.138 de 2024, i la mostra ha estat completada amb 166 noves promocions. Així doncs, els resultats del mes de juny de 2025 inclouen un total de 878 promocions.
            Les 878 promocions de 2025 censades fins el mes de juny, inclouen un total de 20.285 habitatges, dels quals, 6.184, el 30,5%, estan a la venda. Dels habitatges en venda, el 87,4% (5.403 habitatges) corresponen a promocions ja estudiades l’any 2024. En concret, l’any 2024 es van estudiar 6.610 habitatges i, d’aquests el 81,7% continuen a la venda.
            </p>
            <p>  
            El municipi amb més presència d’oferta és el de Barcelona, amb un total de 106 promocions i 625 habitatges en venda. A continuació, els municipis amb més promocions són Badalona amb 42 promocions i 238 habitatges, Terrassa amb 34 promocions i 275 habitatges, Vilanova i la Geltrú amb 34 promocions i 261 habitatges, Sabadell amb 24 promocions i 266 habitatges, Girona amb 20 promocions i 236 habitatges, l’Hospitalet de Llobregat amb 20 promocions i 180 habitatges i Calonge i Sant Antoni amb 19 promocions i 272 habitatges. A la resta de capitals de província el nombre de promocions és més baix: Lleida 14 promocions i 106 habitatges, i en el cas de Tarragona la mostra és de 8 promocions i 72 habitatges.
            </p>
            """,
            unsafe_allow_html=True
        )
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.markdown("**Nombre de promocions per província a Catalunya**")
                st.pyplot(map_prov_prom(bbdd_estudi_prom_2025, shapefile_prov))
            with right_col:
                st.markdown("**Nombre d'habitatges en oferta per municipis a Catalunya**")
                @st.cache_resource
                def map_mun_hab_oferta25():
                    prommun_map = bbdd_estudi_prom_2025[["CODIMUN", "Municipi","HABIP"]].groupby(["CODIMUN", "Municipi"]).sum().reset_index()
                    prommun_map.columns = ["municipi", "Municipi_n", "Habitatges en oferta"]
                    prommun_map["municipi"] = prommun_map["municipi"].astype(int)

                    shapefile_mun = gpd.read_file(path + "shapefile_mun.geojson")
                    shapefile_mun["municipi"] = shapefile_mun["codiine"].astype(int)

                    tmp = pd.merge(shapefile_mun, prommun_map, how="left", on="municipi")
                    fig, ax = plt.subplots(1,1, figsize=(20,20))
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes("right", size="3%", pad=-1) #resize the colorbar
                    cmap = colors.LinearSegmentedColormap.from_list("mi_paleta", ["#AAC4BA","#008B6C"]) 
                    tmp['Habitatges en oferta']= tmp['Habitatges en oferta'].astype(float)
                    tmp.plot(column='Habitatges en oferta', ax=ax,cax=cax, cmap=cmap, legend=True)
                    tmp.geometry.boundary.plot(color='black', ax=ax, linewidth=0.3) #Add some borders to the geometries
                    ax.axis('off')
                    fig.patch.set_alpha(0)
                    return(fig)
                st.pyplot(map_mun_hab_oferta25())
        if selected_index=="Característiques":
            st.subheader("**CARACTERÍSTIQUES**")
            st.write("""
            <p>
            El 52,5% dels habitatges en oferta són de 3 dormitoris i el 27,1% de dos dormitoris. S’observa doncs, una concentració del 79,6% de l’oferta d’habitatges en les tipologies de 2 i 3 dormitoris. En el cas de l’oferta d’habitatges de 4 dormitoris, es situa en un 15,0%. La resta, loft, un dormitori i 5 i més dormitoris, tenen penetracions molt baixes (5,4% en el seu conjunt). Cal comentar que a data juny 2025 no disposem de cap habitatge tipus loft en oferta.
            </p>      
            <p>
            El 92,7% de les promocions estudiades són d’obra nova i el 7,3% corresponen a rehabilitacions integrals. La presència de promocions de rehabilitació integral ascendeix fins a un 38,7% en el cas de la ciutat de Barcelona. En termes d’habitatges, l’oferta de rehabilitació integral és d’un 5,7% i puja fins a un 39,0% en el cas de la ciutat de Barcelona.
            </p>""",
            unsafe_allow_html=True
            )
            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.write("")
                st.write("")
                st.plotly_chart(plot_caracteristiques(bbdd_estudi_hab_2025), use_container_width=True, responsive=True)
            with right_col:
                st.plotly_chart(plot_rehabilitacio_cat(bbdd_estudi_hab_2025), use_container_width=True, responsive=True)

        if selected_index=="Superfície i preus":
            st.subheader("SUPERFÍCIES I PREUS")
            st.write("""
            <p>
            En general, conforme augmenta la superfície de l’habitatge, augmenta també el nombre de dormitoris, situant-se la màxima recurrència en els habitatges de 3 dormitoris (52,5% dels habitatges) amb una superfície mitjana de 86,0 m\u00b2 i en els de 2 dormitoris (27,1% dels habitatges) i una mitjana de superfície de 64,5 m\u00b2.
            La mitjana de superfície útil dels habitatges censats és de 84,5 m\u00b2 (141,6 m\u00b2 en el cas dels habitatges unifamiliars i 79,3 m\u00b2 en els plurifamiliars). Pel que fa al preu mitjà, pel conjunt d’habitatges és de 398.676 €, 549.540 € en el cas dels unifamiliars i 384.884 € en el cas dels plurifamiliars.

            </p> 
            <p>
            Els habitatges dels municipis de la província de Lleida, obtenen les mitjanes més altes de superfície, 96,7 m\u00b2. En el cas de la província de Tarragona, la mitjana de superfície és de 89,8 m\u00b2, en la província de Barcelona de 83,5 m\u00b2 i en la de Girona es localitza la mitjana de superfície més baixa, 82,6 m\u00b2.
            Pel que fa als preus, les províncies de Barcelona i Girona presenten les xifres més elevades: 416.470 € i 396.237 € respectivament en termes de valor absolut, i 4.954 €/m\u00b2 i 4.729 €/m\u00b2 pel que fa al preu per m\u00b2 útil. Les províncies de Lleida (320.215 €) i Tarragona (311.537 €) tenen unes mitjanes de preu significativament més baixes i que es veuen reflectides també en el preu per m\u00b2/útil: 3.236 € y 3.568 € respectivament.
            </p>      
            """,
            unsafe_allow_html=True
            )

            left_col, right_col = st.columns((1, 1))
            with left_col:
                st.write("""<p><b>Superfície útil per tipologia d'habitatge (m\u00b2 útil)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_super_mitjanes(bbdd_estudi_hab_mod_2025), use_container_width=True, responsive=True)
            with right_col:
                st.write("""<p><b>Preu mitjà per tipologia d'habitatge (€)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_preu_mitjanes(bbdd_estudi_hab_mod_2025), use_container_width=True, responsive=True)
            left, center, right = st.columns((0.5,1,0.5))
            with center:
                st.write("""<p><b>Preu per m\u00b2 útil per tipologia d'habitatge (€/m\u00b2 útil)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(indicadors_preum2_mitjanes(bbdd_estudi_hab_mod_2025), use_container_width=True, responsive=True)


        if selected_index=="Comparativa any anterior":
            left_col, right_col = st.columns((1, 1))
            with left_col: 
                st.subheader("**COMPARATIVA 1S2025-2024**")
                st.write("""
                <p>
                La superfície mitjana dels habitatges a la venda a baixat lleugerament, en concret un -0,9%, passant dels 85,3 m2 de 2024 als actuals 84,5 m2. Els habitatges amb més presència, els de 3 dormitoris, baixen mínimament en termes de superfície útil un -0,1%.
                </p>
                <p>
                El preu mitjà de l’habitatge a la venda en Catalunya és de 398.676 €, 1.647 € menys (-0,4%) que a finals de 2024 quan el preu es situava en 400.323 €. En el cas de la tipologia més habitual, 3 dormitoris, es produeix un increment de l’1,0%. Els habitatges de 4 dormitoris baixen un -0,6%, els d’1 dormitori baixen un -4,9%, els de 2 dormitoris un 0,2% i, en el cas de la tipologia de 5 i més dormitoris, el descens és d’un -12,3%.
                El preu mitjà de venda de l’habitatge baixa només a la província de Barcelona, en concret un -1,4%. A la resta de províncies el preu de venda puja en relació a 2024, en el cas de Lleida un 17,7%, un 1,9% en el cas de Tarragona i un 1,6% en el cas de la província de Girona.
                </p>
                <p>
                El preu de venda per m2 útil varia en el conjunt de Catalunya un 0,6% de 2024 a juny de 2025. Cal destacar el cas de les províncies de Tarragona i Lleida, on el preu de venda per m2 útil puja un 3,7% i un 6,4% respectivament.
                </p>""",
                unsafe_allow_html=True
                )
            with right_col:
                st.markdown("")
                st.write("""<p><b>Variació anual dels principals indicadors per tipologia d'habitatge (%)</b></p>""", unsafe_allow_html=True)
                st.plotly_chart(plot_var_CAT(table117_25, table121_25, table125_25), use_container_width=True, responsive=True)
            st.markdown(table_geo_cat(2019, 2026).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo_cat(2019, 2026), f"Estudi_oferta_Catalunya_2025.xlsx"), unsafe_allow_html=True)        


############################################################  PROVÍNCIES I ÀMBITS TERRITORIALS ################################################

if selected == "Províncies i àmbits":
    left, center, right = st.columns((1,1,1))
    with left:
        edicio_any = ["2022","2023","2024", "1S2025"]
        selected_edition = st.radio("**Any**", edicio_any, edicio_any.index("2024"), horizontal=True)
    with center:
        selected_option = st.radio("**Àrea geogràfica**", ["Províncies", "Àmbits territorials"], horizontal=True)
    with right:
        if selected_option=="Províncies":
            prov_names = ["Barcelona", "Girona", "Tarragona", "Lleida"]
            selected_geo = st.selectbox('**Selecciona una província**', prov_names, index= prov_names.index("Barcelona"))
        if selected_option=="Àmbits territorials":
            ambit_names = sorted([ambit_n for ambit_n in ambits_df["GEO"].unique().tolist() if ambit_n!="Catalunya"])
            selected_geo = st.selectbox('**Selecciona un àmbit territorial**', ambit_names, index= ambit_names.index("Metropolità"))

############################################################  PROVÍNCIES I ÀMBITS TERRITORIALS: 2022 ################################################
    if selected_edition=="2022":
        if selected_option=="Àmbits territorials":
            st.subheader(f"{selected_geo}")
            st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del 2023 per l'ambit territorial {selected_geo.split(',')[0].strip()} mostren que el preu mitjà dels habitatges en venda es troba 
            en {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2022)]["Valor"].values[0]:,.1f} € 
            amb una superfície mitjana útil de 
            {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Superfície mitjana (m² útils)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2022)]["Valor"].values[0]:,.1f} m\u00b2. 
            Per tant, el preu per m\u00b2 útil es situa en 
            {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Preu de venda per m² útil (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2022)]["Valor"].values[0]:,.1f} € de mitjana. 
            Per tipologies, els habitatges plurifamiliars obtenen una superfície mitjana de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Superfície mitjana (m² útils)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2022)]["Valor"].values[0]:,.1f} m\u00b2
            menor que els unifamiliars. Finalment, els habitatges plurifamiliars obtenen una mitjana de preu de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2022)]["Valor"].values[0]:,.1f} € 
            i un preu de m\u00b2 útil de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Preu de venda per m² útil (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2022)]["Valor"].values[0]:,.1f} m\u00b2
            """)
            st.markdown(table_geo(selected_geo, 2019, int(selected_edition), selected_option).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo(selected_geo, 2019, int(selected_edition), selected_option), f"Estudi_oferta_{selected_geo}.xlsx"), unsafe_allow_html=True)
        if selected_option=="Províncies":
            st.subheader(f"PROVÍNCIA DE {selected_geo.upper()}")
            if selected_geo=="Barcelona":
                st.write(f"""Els municipis analitzats a l’Estudi de l’Oferta d’Habitatge
                            de Nova Construcció de 2022 que pertanyen a
                            la província de Barcelona fan que aquesta se situï en primera
                            posició pel que fa a la mitjana de preu (389.716€)
                            i també quant al preu €/m\u00b2 de superfície útil (4.796€),
                            ambdós influenciats pel municipi de Barcelona en incidir
                            sobre les mitjanes de forma determinant, tant per la seva
                            aportació quantitativa com qualitativa. Addicionalment,
                            Barcelona se situa com la quarta província pel que fa a
                            la mitjana de superfície, de 79,6m\u00b2.
                            El nombre de promocions en oferta als municipis estudiats
                            a la província de Barcelona l’any 2022 era
                            de 730, amb 6.190 habitatges, xifra que representa el
                            78,7% del total de les promocions estudiades. El percentatge
                            d’habitatges que restaven per vendre és del
                            36,2% sobre un total de 17.121 habitatges existents
                            dins les promocions (en el moment d’elaborar aquest
                            estudi ja estaven venuts el 63,8% dels habitatges, majoritàriament
                            sobre plànol).
                            Pel que fa als habitatges unifamiliars, la mitjana de
                            superficie a la província se situa en 161,4m\u00b2, la mitjana
                            de preu de venda en 637.229€ i la de preu m\u00b2/ útil
                            en 3.813,6€. Pel que fa als habitatges plurifamiliars,
                            la superfície mitjana -en base als municipis estudiats
                            situats a la província- és de 77,3m\u00b2, amb una mitjana
                            de preu de venda de 382.726€, i un preu mitjà per m\u00b2
                            útil de 4.824€.""")
            if selected_geo=="Girona":
                st.write(f"""Els municipis analitzats a l’Estudi de l’Oferta d’Habitatge
                            de Nova Construcció de 2022 que pertanyen a
                            la província de Girona fan que aquesta se situï en tercera
                            posició en la mitjana de superfície (82,5m\u00b2), i en segona
                            posició respecte al preu mitjà (376.023€) i en el preu m\u00b2
                            de superfície útil (4.684€).
                            Pel que fa als habitatges plurifamiliars, la superfície
                            mitjana se situa en els 79,1m\u00b2, amb un preu mitjà
                            de 374.049€, i un preu per m\u00b2 de superfície útil
                            de 4.789€. Respecte dels habitatges unifamiliars,
                            aquestes mitjanes són de 131m\u00b2 de superfície, un
                            preu mitjà de 404.350€, i un preu per m\u00b2 de superfície
                            útil de 3.180€.
                            El nombre de promocions en oferta als municipis estudiats
                            a la província de Girona el 2022 era de 85 (un 9,2%
                            del total de les promocions estudiades a Catalunya, i 982
                            habitatges en venda.
                            El percentatge d’habitatges que restaven per vendre és
                            del 52,1% sobre un total de 1.884 habitatges existents
                            a les promocions de la província.""")
            if selected_geo=="Tarragona":
                st.write(f"""Els municipis analitzats a l’Estudi de l’Oferta d’Habitatge
                            de Nova Construcció de 2022 que pertanyen a la
                            província de Tarragona fan que aquesta se situï en segona
                            posició pel que fa a superfície mitjana (85,3m\u00b2), i
                            en tercera posició tant pel que fa a les mitjanes de preu
                            (244.164€) i de preu per m\u00b2 de superfície útil (2.958€).
                            Per tipologies d’habitatges, en els habitatges unifamiliars
                            les mitjanes registrades són: 167,2m\u00b2 de superfície,
                            amb un preu mitjà de 370.785€, i un preu per m\u00b2 de superfície
                            útil de 2.377€. Pel que fa als habitatges plurifamiliars,
                            la superfície mitjana se situa en els 73,6m\u00b2, amb
                            un preu mitjà de 226.195€, i un preu per m\u00b2 útil de 3.040€.
                            El nombre de promocions en oferta als municipis estudiats
                            a la província de Tarragona el 2022 era de 81, xifra
                            que representa un 8,7% del total de les promocions
                            estudiades a Catalunya (928 promocions). El nombre
                            d’habitatges que resten per vendre és de 692 unitats, un
                            33,2% sobre un total de 2.084 habitatges existents en les
                            promocions de la província.""")
            if selected_geo=="Lleida":
                st.write(f"""Els municipis analitzats a l’Estudi de l’Oferta d’Habitatge
                            de Nova Construcció de 2022 que pertanyen
                            a la província de Lleida obtenen la mitjana més alta de
                            superfície (86,5m\u00b2), i se situen en quarta posició pel que
                            fa a preu del m\u00b2 de superfície útil (2.351€).
                            Pel que fa habitatges plurifamiliars, la superfície mitja
                            provincial és de 83,8m\u00b2 i un preu mitjà per m\u00b2 útil de
                            2.292€. En el cas dels habitatges unifamiliars,
                            aquestes quantitats són de 131,7m\u00b2 de superfície mitjana
                            i de 3.327€ la mitjana del m\u00b2 de superfície útil.
                            El nombre de promocions en oferta als municipis estudiats
                            a la província de Lleida el 2022 era de 32 (amb 317
                            habitatges en venda), dada que representa un 3,4% del
                            total de les promocions estudiades (928 promocions). El
                            percentatge d’habitatges que restaven per vendre és del
                            44,8% sobre un total de 707 habitatges existents a les
                            promocions a la província.""")
            st.markdown(table_geo(selected_geo, 2019, int(selected_edition), selected_option).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo(selected_geo, 2019, int(selected_edition), selected_option), f"Estudi_oferta_{selected_geo}.xlsx"), unsafe_allow_html=True)
            left_col, right_col = st.columns((1,1))
            with left_col:
                st.plotly_chart(tipog_donut(bbdd_estudi_hab, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.plotly_chart(num_dorms_prov(bbdd_estudi_hab_mod, selected_geo), use_container_width=True, responsive=True)
            left_col, right_col = st.columns((1,1))
            with left_col:
                st.plotly_chart(qualitats_prov(bbdd_estudi_hab, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.plotly_chart(equipaments_prov(bbdd_estudi_hab, selected_geo), use_container_width=True, responsive=True)
            left_col, right_col = st.columns((2, 1))
            with left_col:
                st.plotly_chart(cons_acabats(bbdd_estudi_prom, bbdd_estudi_hab, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.markdown("")
                st.markdown("")
                st.metric("**Habitatges en oferta**", format(int(metric_estat(bbdd_estudi_prom, bbdd_estudi_hab,selected_geo)[0]), ",d"))
                st.metric("**Habitatges en construcció**", format(int(metric_estat(bbdd_estudi_prom, bbdd_estudi_hab, selected_geo)[0] - metric_estat(bbdd_estudi_prom, bbdd_estudi_hab, selected_geo)[1]), ",d"))
                st.metric("**Habitatges acabats**", format(int(metric_estat(bbdd_estudi_prom, bbdd_estudi_hab, selected_geo)[1]), ",d"))
            left_col, right_col = st.columns((2, 1))
            with left_col:
                st.plotly_chart(tipo_obra_prov(bbdd_estudi_hab, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.markdown("")
                st.markdown("")
                st.metric("**Habitatges de nova construcció**", format(int(metric_rehab(bbdd_estudi_hab, selected_geo)[0]), ",d"))
                st.metric("**Habitatges de rehabilitació integral**", format(int(metric_rehab(bbdd_estudi_hab, selected_geo)[1]), ",d"))

############################################################  PROVÍNCIES I ÀMBITS TERRITORIALS: 2023 ################################################
    if selected_edition=="2023":
        if selected_option=="Àmbits territorials":
            st.subheader(f"{selected_geo.upper()}")
            st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del 2023 per l'ambit territorial {selected_geo.split(',')[0].strip()} mostren que el preu mitjà dels habitatges en venda es troba 
            en {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2023)]["Valor"].values[0]:,.1f} € 
            amb una superfície mitjana útil de 
            {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Superfície mitjana (m² útils)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2023)]["Valor"].values[0]:,.1f} m\u00b2. 
            Per tant, el preu per m\u00b2 útil es situa en 
            {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Preu de venda per m² útil (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2023)]["Valor"].values[0]:,.1f} € de mitjana. 
            Per tipologies, els habitatges plurifamiliars obtenen una superfície mitjana de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Superfície mitjana (m² útils)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2023)]["Valor"].values[0]:,.1f} m\u00b2
            menor que els unifamiliars. Finalment, els habitatges plurifamiliars obtenen una mitjana de preu de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2023)]["Valor"].values[0]:,.1f} € 
            i un preu de m\u00b2 útil de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Preu de venda per m² útil (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2023)]["Valor"].values[0]:,.1f} m\u00b2
            """)
            st.markdown(table_geo(selected_geo, 2019, int(selected_edition), selected_option).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo(selected_geo, 2019, int(selected_edition), selected_option), f"Estudi_oferta_{selected_geo}.xlsx"), unsafe_allow_html=True)
        if selected_option=="Províncies":
            st.subheader(f"PROVÍNCIA DE {selected_geo.upper()}")
            if selected_geo=="Barcelona":
                st.write(f"""Els municipis analitzats a l’Estudi de l’Oferta d’Habitatge
                            de Nova Construcció a Catalunya 2023 que pertanyen a
                            la província de Barcelona es situen de mitjana en primera
                            posició pel que fa al preu (385.036€)
                            i també quant al preu €/m\u00b2 de superfície útil (4.757€),
                            ambdós influenciats pel municipi de Barcelona en incidir
                            sobre les mitjanes de forma determinant, tant per la seva
                            aportació quantitativa com qualitativa. Addicionalment,
                            Barcelona se situa com la quarta província pel que fa a
                            la mitjana de superfície, de 79,6m\u00b2.
                            El número de promocions en oferta als municipis estudiats
                            a la província de Barcelona l’any 2023 va ser
                            de 894, amb 8.012 habitatges, xifra que representa el
                            79,6% del total de les promocions estudiades. El percentatge
                            d’habitatges que restaven per vendre és del
                            38,7% sobre un total de 20.725 habitatges existents
                            dins les promocions (en el moment d’elaborar aquest
                            estudi ja estaven venuts el 61,3% dels habitatges, majoritàriament
                            sobre plànol).
                            Pel que fa als habitatges unifamiliars, la mitjana de
                            superficie a la província se situa en 149,0 m\u00b2, la mitjana
                            de preu de venda en 593.401€ i la de preu m\u00b2 útil
                            en 3.942,8€. Pel que fa als habitatges plurifamiliars,
                            la superfície mitjana és de 76,8 m\u00b2, amb una mitjana
                            de preu de venda de 376.425€, i un preu mitjà per m\u00b2
                            útil de 4.790,2€.""")
            if selected_geo=="Girona":
                st.write(f"""Els municipis analitzats a l’Estudi de l'Oferta d'Habitatge de 2023 que pertanyen a
                            la província de Girona es situen de mitjana en tercera
                            posició respecte a la superfície útil (82,9 m\u00b2) i en segona
                            posició respecte al preu mitjà (349.647€) i el preu m\u00b2
                            de superfície útil (4.244,9€).
                            Pel que fa als habitatges plurifamiliars, la superfície
                            mitjana es situa en els 79,6 m\u00b2, amb un preu mitjà
                            de 343.984€, i un preu per m\u00b2 de superfície útil
                            de 4.295€. Respecte dels habitatges unifamiliars,
                            aquestes mitjanes són de 140,1 m\u00b2 de superfície, un
                            preu mitjà de 446.945€ i un preu per m\u00b2 de superfície
                            útil de 3.392€.
                            El nombre de promocions en oferta als municipis estudiats
                            de la província de Girona al 2023 era de 109 (un 9,7%
                            del total de les promocions estudiades a Catalunya), que contenen 1.200
                            habitatges en venda.
                            El percentatge d’habitatges que restaven per vendre és
                            del 51,3% sobre un total de 2.338 habitatges existents
                            a les promocions de la província.""")
            if selected_geo=="Tarragona":
                st.write(f"""Els municipis analitzats a l’Estudi de l'Oferta d'Habitatge de 2023 que pertanyen a la
                            província de Tarragona es situen de mitjana en segona
                            posició pel que fa a superfície (83,5m\u00b2), i
                            en tercera posició tant pel que fa a les mitjanes de preu
                            (254.667€) i de preu per m\u00b2 de superfície útil (3.029€).
                            Per tipologies d’habitatges, en els habitatges unifamiliars
                            les mitjanes registrades són: 140,5m\u00b2 de superfície,
                            amb un preu mitjà de 441.762, i un preu per m\u00b2 de superfície
                            útil de 3.354€. Pel que fa als habitatges plurifamiliars,
                            la superfície mitjana se situa en els 74,7m\u00b2, amb
                            un preu mitjà de 225.741€, i un preu per m\u00b2 útil de 2.979€.
                            El nombre de promocions en oferta als municipis estudiats
                            a la província de Tarragona al 2023 va ser de 84, xifra
                            que representa un 7,4% del total de les promocions
                            estudiades a Catalunya. El percentatge d’habitatges que restaven per vendre és
                            del 32,3% sobre un total de 2.175 habitatges existents
                            a les promocions de la província.""")
            if selected_geo=="Lleida":
                st.write(f"""Els municipis analitzats a l’Estudi de l'Oferta d'Habitatge de 2023 que pertanyen
                            a la província de Lleida obtenen la mitjana més alta de
                            superfície (86,6 m\u00b2) i es situen en quarta posició pel que
                            fa el preu del m\u00b2 de superfície útil (2.428€).
                            Quant als habitatges plurifamiliars, la superfície mitjana
                            provincial és de 82,7 m\u00b2 constituint un preu mitjà per m\u00b2 útil de
                            2.332€. En el cas dels habitatges unifamiliars,
                            aquestes quantitats són de 134,5 m\u00b2 de superfície mitjana
                            i de 3.586 la mitjana del preu m\u00b2 de superfície útil.
                            El nombre de promocions en oferta als municipis estudiats
                            a la província de Lleida al 2023 va ser de 36 (amb 382
                            habitatges en venda), dada que representa un 3,2% del
                            total de les promocions estudiades. El
                            percentatge d’habitatges que restaven per vendre és del
                            41,9% sobre un total de 911 habitatges existents a les
                            promocions a la província.""")
            st.markdown(table_geo(selected_geo, 2019, int(selected_edition), selected_option).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo(selected_geo, 2019, int(selected_edition), selected_option), f"Estudi_oferta_{selected_geo}.xlsx"), unsafe_allow_html=True)
            left_col, right_col = st.columns((1,1))
            with left_col:
                st.plotly_chart(tipog_donut(bbdd_estudi_hab_2023, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.plotly_chart(num_dorms_prov(bbdd_estudi_hab_mod_2023, selected_geo), use_container_width=True, responsive=True)
            left_col, right_col = st.columns((1,1))
            with left_col:
                st.plotly_chart(qualitats_prov(bbdd_estudi_hab_2023, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.plotly_chart(equipaments_prov(bbdd_estudi_hab_2023, selected_geo), use_container_width=True, responsive=True)
            left_col, right_col = st.columns((2, 1))
            with left_col:
                st.plotly_chart(cons_acabats(bbdd_estudi_prom_2023, bbdd_estudi_hab_2023, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.markdown("")
                st.markdown("")
                st.metric("**Habitatges en oferta**", format(int(metric_estat(bbdd_estudi_prom_2023, bbdd_estudi_hab_2023, selected_geo)[0]), ",d"))
                st.metric("**Habitatges en construcció**", format(int(metric_estat(bbdd_estudi_prom_2023,  bbdd_estudi_hab_2023, selected_geo)[0] - metric_estat(bbdd_estudi_prom_2023, bbdd_estudi_hab_2023, selected_geo)[1]), ",d"))
                st.metric("**Habitatges acabats**", format(int(metric_estat(bbdd_estudi_prom_2023, bbdd_estudi_hab_2023, selected_geo)[1]), ",d"))
            left_col, right_col = st.columns((2, 1))
            with left_col:
                st.plotly_chart(tipo_obra_prov(bbdd_estudi_hab_2023, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.markdown("")
                st.markdown("")
                st.metric("**Habitatges de nova construcció**", format(int(metric_rehab(bbdd_estudi_hab_2023, selected_geo)[0]), ",d"))
                st.metric("**Habitatges de rehabilitació integral**", format(int(metric_rehab(bbdd_estudi_hab_2023, selected_geo)[1]), ",d"))

############################################################  PROVÍNCIES I ÀMBITS TERRITORIALS: 2024 ################################################
    if selected_edition=="2024":
        if selected_option=="Àmbits territorials":
            st.subheader(f"{selected_geo.upper()}")
            st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del 2024 per l'ambit territorial {selected_geo.split(',')[0].strip()} mostren que el preu mitjà dels habitatges en venda es troba 
            en {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2024)]["Valor"].values[0]:,.1f} € 
            amb una superfície mitjana útil de 
            {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Superfície mitjana (m² útils)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2024)]["Valor"].values[0]:,.1f} m\u00b2. 
            Per tant, el preu per m\u00b2 útil es situa en 
            {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Preu de venda per m² útil (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2024)]["Valor"].values[0]:,.1f} € de mitjana. 
            Per tipologies, els habitatges plurifamiliars obtenen una superfície mitjana de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Superfície mitjana (m² útils)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2024)]["Valor"].values[0]:,.1f} m\u00b2
            menor que els unifamiliars. Finalment, els habitatges plurifamiliars obtenen una mitjana de preu de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2024)]["Valor"].values[0]:,.1f} € 
            i un preu de m\u00b2 útil de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Preu de venda per m² útil (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2024)]["Valor"].values[0]:,.1f} m\u00b2
            """)
            st.markdown(table_geo(selected_geo, 2019, int(selected_edition), selected_option).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo(selected_geo, 2019, int(selected_edition), selected_option), f"Estudi_oferta_{selected_geo}.xlsx"), unsafe_allow_html=True)
        if selected_option=="Províncies":
            st.subheader(f"PROVÍNCIA DE {selected_geo.upper()}")
            if selected_geo=="Barcelona":
                st.write(f"""Els municipis analitzats a l’Estudi de l’Oferta d’Habitatge
                            de Nova Construcció a Catalunya 2024 que pertanyen a
                            la província de Barcelona es situen de mitjana en primera
                            posició pel que fa al preu (422.448€)
                            i també quant al preu €/m\u00b2 de superfície útil (4.929,2€),
                            ambdós influenciats pel municipi de Barcelona en incidir
                            sobre les mitjanes de forma determinant, tant per la seva
                            aportació quantitativa com qualitativa. Addicionalment,
                            Barcelona se situa com la tercera província pel que fa a
                            la mitjana de superfície, de 85 m\u00b2.
                            El número de promocions en oferta als municipis estudiats
                            a la província de Barcelona l’any 2024 va ser
                            de 885, amb 4.660 habitatges, xifra que representa el
                            77,7% del total de les promocions estudiades. El percentatge
                            d’habitatges que restaven per vendre és del
                            31,2% sobre un total de 19.797 habitatges existents
                            dins les promocions (en el moment d’elaborar aquest
                            estudi ja estaven venuts el 68,8% dels habitatges, majoritàriament
                            sobre plànol).
                            Pel que fa als habitatges unifamiliars, la mitjana de
                            superficie a la província se situa en 154,4 m\u00b2, la mitjana
                            de preu de venda en 608.145€ i la de preu m\u00b2 útil
                            en 3.976,7€. Quant als habitatges plurifamiliars,
                            la superfície mitjana és de 80,1 m\u00b2, amb una mitjana
                            de preu de venda de 409.168€, i un preu mitjà per m\u00b2
                            útil de 4.997,3€.""")
            if selected_geo=="Girona":
                st.write(f"""Els municipis analitzats a l’Estudi de l'Oferta d'Habitatge de 2024 que pertanyen a
                            la província de Girona es situen de mitjana en quarta
                            posició respecte a la superfície útil (82,1 m\u00b2) i en segona
                            posició respecte al preu mitjà (389.961€) i el preu m\u00b2
                            de superfície útil (4.696,8€).
                            Pel que fa als habitatges plurifamiliars, la superfície
                            mitjana es situa en els 78,5 m\u00b2, amb un preu mitjà
                            de 378.457€, i un preu per m\u00b2 de superfície útil
                            de 4.741€. Respecte dels habitatges unifamiliars,
                            aquestes mitjanes són de 131 m\u00b2 de superfície, un
                            preu mitjà de 543.145€ i un preu per m\u00b2 de superfície
                            útil de 4.107,3€.
                            El nombre de promocions en oferta als municipis estudiats
                            de la província de Girona al 2024 era de 126 (un 11%
                            del total de les promocions estudiades a Catalunya), que contenen 1.088
                            habitatges en venda.
                            El percentatge d’habitatges que restaven per vendre és
                            del 39,5% sobre un total de 2.752 habitatges existents
                            a les promocions de la província.""")
            if selected_geo=="Tarragona":
                st.write(f"""Els municipis analitzats a l’Estudi de l'Oferta d'Habitatge de 2024 que pertanyen a la
                            província de Tarragona es situen de mitjana en primera
                            posició pel que fa a superfície (91 m\u00b2), i
                            en tercera posició tant pel que fa a les mitjanes de preu
                            (305.655€) i de preu per m\u00b2 de superfície útil (3.440,1€).
                            Per tipologies d’habitatges, en els habitatges unifamiliars
                            les mitjanes registrades són: 140,7m\u00b2 de superfície,
                            amb un preu mitjà de 459.677, i un preu per m\u00b2 de superfície
                            útil de 3.394,9€. Pel que fa als habitatges plurifamiliars,
                            la superfície mitjana se situa en els 76,6m\u00b2, amb
                            un preu mitjà de 261.088€, i un preu per m\u00b2 útil de 3.453,2€.
                            El nombre de promocions en oferta als municipis estudiats
                            a la província de Tarragona al 2024 va ser de 84, xifra
                            que representa un 7,4% del total de les promocions
                            estudiades a Catalunya. El percentatge d’habitatges que restaven per vendre és
                            del 24,6% sobre un total de 2.265 habitatges existents
                            a les promocions de la província.""")
            if selected_geo=="Lleida":
                st.write(f"""Els municipis analitzats a l’Estudi de l'Oferta d'Habitatge de 2024 que pertanyen
                            a la província de Lleida obtenen la segona mitjana més alta de
                            superfície (90 m\u00b2) i es situen en quarta posició pel que
                            fa el preu del m\u00b2 de superfície útil (3.043€).
                            Quant als habitatges plurifamiliars, la superfície mitjana
                            provincial és de 86,5 m\u00b2 constituint un preu mitjà per m\u00b2 útil de
                            3.019,5€. En el cas dels habitatges unifamiliars,
                            aquestes quantitats són de 134,3 m\u00b2 de superfície mitjana
                            i de 3.345,5 la mitjana del preu m\u00b2 de superfície útil.
                            El nombre de promocions en oferta als municipis estudiats
                            a la província de Lleida al 2024 va ser de 43 (amb 305
                            habitatges en venda), dada que representa un 3,8% del
                            total de les promocions estudiades. El
                            percentatge d’habitatges que restaven per vendre és del
                            30,2% sobre un total de 1.011 habitatges existents a les
                            promocions a la província.""")
            st.markdown(table_geo(selected_geo, 2019, int(selected_edition), selected_option).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo(selected_geo, 2019, int(selected_edition), selected_option), f"Estudi_oferta_{selected_geo}.xlsx"), unsafe_allow_html=True)
            left_col, right_col = st.columns((1,1))
            with left_col:
                st.plotly_chart(tipog_donut(bbdd_estudi_hab_2024, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.plotly_chart(num_dorms_prov(bbdd_estudi_hab_mod_2024, selected_geo), use_container_width=True, responsive=True)
            left_col, right_col = st.columns((1,1))
            with left_col:
                st.plotly_chart(qualitats_prov(bbdd_estudi_hab_2024, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.plotly_chart(equipaments_prov(bbdd_estudi_hab_2024, selected_geo), use_container_width=True, responsive=True)
            left_col, right_col = st.columns((2, 1))
            with left_col:
                st.plotly_chart(cons_acabats(bbdd_estudi_prom_2024, bbdd_estudi_hab_2024, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.markdown("")
                st.markdown("")
                st.metric("**Habitatges en oferta**", format(int(metric_estat(bbdd_estudi_prom_2024, bbdd_estudi_hab_2024, selected_geo)[0]), ",d"))
                st.metric("**Habitatges en construcció**", format(int(metric_estat(bbdd_estudi_prom_2024,  bbdd_estudi_hab_2024, selected_geo)[0] - metric_estat(bbdd_estudi_prom_2024, bbdd_estudi_hab_2024, selected_geo)[1]), ",d"))
                st.metric("**Habitatges acabats**", format(int(metric_estat(bbdd_estudi_prom_2024, bbdd_estudi_hab_2024, selected_geo)[1]), ",d"))
            left_col, right_col = st.columns((2, 1))
            with left_col:
                st.plotly_chart(tipo_obra_prov(bbdd_estudi_hab_2024, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.markdown("")
                st.markdown("")
                st.metric("**Habitatges de nova construcció**", format(int(metric_rehab(bbdd_estudi_hab_2024, selected_geo)[0]), ",d"))
                st.metric("**Habitatges de rehabilitació integral**", format(int(metric_rehab(bbdd_estudi_hab_2024, selected_geo)[1]), ",d"))

############################################################  PROVÍNCIES I ÀMBITS TERRITORIALS: 1S2025 ################################################
    if selected_edition=="1S2025":
        if selected_option=="Àmbits territorials":
            st.subheader(f"{selected_geo.upper()}")
            st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del primer semestre de 2025 per l'ambit territorial {selected_geo.split(',')[0].strip()} mostren que el preu mitjà dels habitatges en venda es troba 
            en {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2025)]["Valor"].values[0]:,.1f} € 
            amb una superfície mitjana útil de 
            {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Superfície mitjana (m² útils)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2025)]["Valor"].values[0]:,.1f} m\u00b2. 
            Per tant, el preu per m\u00b2 útil es situa en 
            {ambits_df[(ambits_df["Tipologia"]=="TOTAL HABITATGES") & (ambits_df["Variable"]=="Preu de venda per m² útil (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2025)]["Valor"].values[0]:,.1f} €/m\u00b2 de mitjana. 
            Per tipologies, els habitatges plurifamiliars obtenen una superfície mitjana de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Superfície mitjana (m² útils)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2025)]["Valor"].values[0]:,.1f} m\u00b2, la seva mitjana de preu es troba en 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2025)]["Valor"].values[0]:,.1f} € 
            i un preu de m\u00b2 útil de 
            {ambits_df[(ambits_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (ambits_df["Variable"]=="Preu de venda per m² útil (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2025)]["Valor"].values[0]:,.1f} €/m\u00b2.
            D'altra banda, els habitatges unifamiliars registren una superfície mitjana de {ambits_df[(ambits_df["Tipologia"]=="HABITATGES UNIFAMILIARS") & (ambits_df["Variable"]=="Superfície mitjana (m² útils)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2025)]["Valor"].values[0]:,.1f} m\u00b2 amb una mitjana de preu de {ambits_df[(ambits_df["Tipologia"]=="HABITATGES UNIFAMILIARS") & (ambits_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2025)]["Valor"].values[0]:,.1f} €, per tant, el preu del m\u00b2 útil es situa en {ambits_df[(ambits_df["Tipologia"]=="HABITATGES UNIFAMILIARS") & (ambits_df["Variable"]=="Preu de venda per m² útil (€)") & (ambits_df["GEO"]==selected_geo) & (ambits_df["Any"]==2025)]["Valor"].values[0]:,.1f} €/m\u00b2.""")
            st.markdown(table_geo(selected_geo, 2019, 2026, selected_option).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo(selected_geo, 2019, 2026, selected_option), f"Estudi_oferta_{selected_geo}.xlsx"), unsafe_allow_html=True)
        if selected_option=="Províncies":
            st.subheader(f"PROVÍNCIA DE {selected_geo.upper()}")
            st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del primer semestre de 2025 per la província de {selected_geo} mostren que el preu mitjà dels habitatges en venda es troba en {provincia_df[(provincia_df["Tipologia"]=="TOTAL HABITATGES") & (provincia_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (provincia_df["GEO"]==selected_geo) & (provincia_df["Any"]==2025)]["Valor"].values[0]:,.1f} € amb una superfície mitjana útil de {provincia_df[(provincia_df["Tipologia"]=="TOTAL HABITATGES") & (provincia_df["Variable"]=="Superfície mitjana (m² útils)") & (provincia_df["GEO"]==selected_geo) & (provincia_df["Any"]==2025)]["Valor"].values[0]:,.1f} m\u00b2.Per tant, el preu per m\u00b2 útil es situa en {provincia_df[(provincia_df["Tipologia"]=="TOTAL HABITATGES") & (provincia_df["Variable"]=="Preu de venda per m² útil (€)") & (provincia_df["GEO"]==selected_geo) & (provincia_df["Any"]==2025)]["Valor"].values[0]:,.1f} €/m\u00b2 de mitjana. Per tipologies, els habitatges plurifamiliars obtenen una superfície mitjana de {provincia_df[(provincia_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (provincia_df["Variable"]=="Superfície mitjana (m² útils)") & (provincia_df["GEO"]==selected_geo) & (provincia_df["Any"]==2025)]["Valor"].values[0]:,.1f} m\u00b2, la seva mitjana de preu es troba en {provincia_df[(provincia_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (provincia_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (provincia_df["GEO"]==selected_geo) & (provincia_df["Any"]==2025)]["Valor"].values[0]:,.1f} € i un preu de m\u00b2 útil de {provincia_df[(provincia_df["Tipologia"]=="HABITATGES PLURIFAMILIARS") & (provincia_df["Variable"]=="Preu de venda per m² útil (€)") & (provincia_df["GEO"]==selected_geo) & (provincia_df["Any"]==2025)]["Valor"].values[0]:,.1f} €/m\u00b2. D'altra banda, els habitatges unifamiliars registren una superfície mitjana de {provincia_df[(provincia_df["Tipologia"]=="HABITATGES UNIFAMILIARS") & (provincia_df["Variable"]=="Superfície mitjana (m² útils)") & (provincia_df["GEO"]==selected_geo) & (provincia_df["Any"]==2025)]["Valor"].values[0]:,.1f} m\u00b2 amb una mitjana de preu de {provincia_df[(provincia_df["Tipologia"]=="HABITATGES UNIFAMILIARS") & (provincia_df["Variable"]=="Preu mitjà de venda de l'habitatge (€)") & (provincia_df["GEO"]==selected_geo) & (provincia_df["Any"]==2025)]["Valor"].values[0]:,.1f} €, per tant, el preu del m\u00b2 útil es situa en {provincia_df[(provincia_df["Tipologia"]=="HABITATGES UNIFAMILIARS") & (provincia_df["Variable"]=="Preu de venda per m² útil (€)") & (provincia_df["GEO"]==selected_geo) & (provincia_df["Any"]==2025)]["Valor"].values[0]:,.1f} €/m\u00b2.""")
            if selected_geo=="Barcelona":
                st.write(f""" """)
            if selected_geo=="Girona":
                st.write(f""" """)
            if selected_geo=="Tarragona":
                st.write(f""" """)
            if selected_geo=="Lleida":
                st.write(f""" """)
            st.markdown(table_geo(selected_geo, 2019, 2026, selected_option).to_html(), unsafe_allow_html=True)
            st.markdown(filedownload(table_geo(selected_geo, 2019, 2026, selected_option), f"Estudi_oferta_{selected_geo}.xlsx"), unsafe_allow_html=True)
            left_col, right_col = st.columns((1,1))
            with left_col:
                st.plotly_chart(tipog_donut(bbdd_estudi_hab_2025, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.plotly_chart(num_dorms_prov(bbdd_estudi_hab_mod_2025, selected_geo), use_container_width=True, responsive=True)
            # left_col, right_col = st.columns((1,1))
            # with left_col:
            #     st.plotly_chart(qualitats_prov(bbdd_estudi_hab_2025, selected_geo), use_container_width=True, responsive=True)
            # with right_col:
            #     st.plotly_chart(equipaments_prov(bbdd_estudi_hab_2025, selected_geo), use_container_width=True, responsive=True)
            left_col, right_col = st.columns((2, 1))
            with left_col:
                st.plotly_chart(cons_acabats(bbdd_estudi_prom_2025, bbdd_estudi_hab_2025, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.markdown("")
                st.markdown("")
                st.metric("**Habitatges en oferta**", format(int(metric_estat(bbdd_estudi_prom_2025, bbdd_estudi_hab_2025, selected_geo)[0]), ",d"))
                st.metric("**Habitatges en construcció**", format(int(metric_estat(bbdd_estudi_prom_2025,  bbdd_estudi_hab_2025, selected_geo)[0] - metric_estat(bbdd_estudi_prom_2025, bbdd_estudi_hab_2025, selected_geo)[1]), ",d"))
                st.metric("**Habitatges acabats**", format(int(metric_estat(bbdd_estudi_prom_2025, bbdd_estudi_hab_2025, selected_geo)[1]), ",d"))
            left_col, right_col = st.columns((2, 1))
            with left_col:
                st.plotly_chart(tipo_obra_prov(bbdd_estudi_hab_2025, selected_geo), use_container_width=True, responsive=True)
            with right_col:
                st.markdown("")
                st.markdown("")
                st.metric("**Habitatges de nova construcció**", format(int(metric_rehab(bbdd_estudi_hab_2025, selected_geo)[0]), ",d"))
                st.metric("**Habitatges de rehabilitació integral**", format(int(metric_rehab(bbdd_estudi_hab_2025, selected_geo)[1]), ",d"))

############################################################  MUNICIPIS DE CATALUNYA ################################################
if selected == "Municipis":
    left, right = st.columns((1,1))
    with left:
        edicio_any = ["2022","2023", "2024", "1S2025"]
        selected_edition = st.radio("**Any**", edicio_any, edicio_any.index("2024"), horizontal=True)
    with right:
        mun_names = sorted([name for name in df_vf[(df_vf["Any"]==int(selected_edition[-4:])) & (~df_vf["Valor"].isna())]["GEO"].unique() if name != "Catalunya"])
        selected_mun = st.selectbox('**Municipi seleccionat:**', mun_names, index= mun_names.index("Barcelona"))

############################################################  MUNICIPIS: 2022 ################################################
    if selected_edition=="2022":
        st.subheader(f"MUNICIPI DE {selected_mun.upper().split(',')[0].strip()}")
        st.markdown(f"""Els resultats de l'Estudi d'Oferta de Nova Construcció del 2022 pel municipi de {selected_mun.split(',')[0].strip()} mostren que el preu mitjà dels habitatges en venda es troba 
        en {data_text_mun(bbdd_estudi_hab, bbdd_estudi_hab_mod, selected_mun)[0]:,.1f} € amb una superfície mitjana útil de {data_text_mun(bbdd_estudi_hab, bbdd_estudi_hab_mod, selected_mun)[1]:,.1f} m\u00b2. Per tant, el preu per m\u00b2 útil es troba en {data_text_mun(bbdd_estudi_hab, bbdd_estudi_hab_mod, selected_mun)[2]:,.1f} € de mitjana. Per tipologies, els habitatges plurifamiliars
        representen el {data_text_mun(bbdd_estudi_hab, bbdd_estudi_hab_mod,selected_mun)[3]:,.1f}% sobre el total d'habitatges, la resta corresponen a habitatges unifamiliars. L'habitatge modal o més freqüent de nova construcció té {data_text_mun(bbdd_estudi_hab, bbdd_estudi_hab_mod, selected_mun)[4]} habitacions i {data_text_mun(bbdd_estudi_hab, bbdd_estudi_hab_mod, selected_mun)[5]} banys o lavabos.""")
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown(f"""**Distribució de Preus per m\u00b2 útil**""")
            st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod, selected_mun,"Preu m2 útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Preus per m\u00b2 útil segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav(bbdd_estudi_hab, selected_mun, "Preu m2 útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Característiques principals dels habitatges en oferta**""")
            st.plotly_chart(caracteristiques_mun(bbdd_estudi_hab, selected_mun), use_container_width=True, responsive=True)
            st.markdown(f"""**Qualitats dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(qualitats_mun(bbdd_estudi_hab_mod, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número d'habitacions**""")
            st.plotly_chart(dormscount_plot_mun(bbdd_estudi_hab_mod, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Qualificació energètica dels habitatges en oferta (% d'habitatges)**""")
            st.plotly_chart(plot_table_energ_mun(bbdd_estudi_hab, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Proporció d'habitatges segons el tipus d'instal·lació de calefacció (%)**""")
            st.plotly_chart(cale_tipus_mun(bbdd_estudi_prom, selected_mun), use_container_width=True, responsive=True)
        with right_col:
            st.markdown(f"""**Distribució de Superfície útil**""")
            st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod, selected_mun, "Superfície útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Superfície en m\u00b2 útils segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav(bbdd_estudi_hab, selected_mun,"Superfície útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Proporció d'habitatges en oferta a les promocions segons tipologia (%)**""")
            st.plotly_chart(count_plot_mun(bbdd_estudi_hab_mod, selected_mun), use_container_width=True, responsive=True)
            st.markdown(f"""**Equipaments dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(equipaments_mun(bbdd_estudi_hab_mod, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número de lavabos**""")
            st.plotly_chart(lavcount_plot_mun(bbdd_estudi_hab_mod, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Grandària de les promocions en nombre d'habitatges**""")
            st.plotly_chart(n_promocions_habs_mun(bbdd_estudi_prom, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Plaça d'aparacament inclosa o no en els habitatges en oferta (%)**""")
            st.plotly_chart(aparcament_mun(bbdd_estudi_hab, selected_mun), use_container_width=True, responsive=True)

        st.subheader("Comparativa amb anys anteriors: Municipi de " + selected_mun.split(',')[0].strip())
        st.markdown(table_mun(selected_mun, 2019, int(selected_edition)).to_html(), unsafe_allow_html=True)
        st.markdown(filedownload(table_mun(selected_mun, 2019, int(selected_edition)), f"Estudi_oferta_{selected_mun}.xlsx"), unsafe_allow_html=True)
        st.markdown("")
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució dels habitatges de nova construcció per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist_units(selected_mun, "Unitats", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució de la superfície útil mitjana per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, 'Superfície mitjana (m² útils)', 2019, int(selected_edition)), use_container_width=True, responsive=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució del preu de venda per m\u00b2 útil  per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, "Preu de venda per m² útil (€)", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució del preu venda mitjà per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, "Preu mitjà de venda de l'habitatge (€)", 2019, int(selected_edition)), use_container_width=True, responsive=True)

############################################################  MUNICIPIS: 2023 ################################################
    if selected_edition=="2023":
        st.subheader(f"MUNICIPI DE {selected_mun.upper().split(',')[0].strip()}")
        st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del 2023 pel municipi de {selected_mun.split(',')[0].strip()} mostren que el preu mitjà dels habitatges en venda es troba 
        en {data_text_mun(bbdd_estudi_hab_2023, bbdd_estudi_hab_mod_2023, selected_mun)[0]:,.1f} € amb una superfície mitjana útil de {data_text_mun(bbdd_estudi_hab_2023, bbdd_estudi_hab_mod_2023, selected_mun)[1]:,.1f} m\u00b2. Per tant, el preu per m\u00b2 útil es troba en {data_text_mun(bbdd_estudi_hab_2023, bbdd_estudi_hab_mod_2023, selected_mun)[2]:,.1f} € de mitjana. Per tipologies, els habitatges plurifamiliars
        representen el {data_text_mun(bbdd_estudi_hab_2023, bbdd_estudi_hab_mod_2023, selected_mun)[3]:,.1f}% sobre el total d'habitatges, la resta corresponen a habitatges unifamiliars. L'habitatge modal o més freqüent de nova construcció té {data_text_mun(bbdd_estudi_hab_2023, bbdd_estudi_hab_mod_2023, selected_mun)[4]} habitacions i {data_text_mun(bbdd_estudi_hab_2023, bbdd_estudi_hab_mod_2023, selected_mun)[5]} banys o lavabos.""")

        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown(f"""**Distribució de Preus per m\u00b2 útil**""")
            st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod_2023, selected_mun,"Preu m2 útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Preus per m\u00b2 útil segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav(bbdd_estudi_hab_2023, selected_mun, "Preu m2 útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Característiques principals dels habitatges en oferta**""")
            st.plotly_chart(caracteristiques_mun(bbdd_estudi_hab_2023, selected_mun), use_container_width=True, responsive=True)
            st.markdown(f"""**Qualitats dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(qualitats_mun(bbdd_estudi_hab_mod_2023, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número d'habitacions**""")
            st.plotly_chart(dormscount_plot_mun(bbdd_estudi_hab_mod_2023, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Qualificació energètica dels habitatges en oferta (% d'habitatges)**""")
            st.plotly_chart(plot_table_energ_mun(bbdd_estudi_hab_2023, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Proporció d'habitatges segons el tipus d'instal·lació de calefacció (%)**""")
            st.plotly_chart(cale_tipus_mun(bbdd_estudi_prom_2023, selected_mun), use_container_width=True, responsive=True)

        with right_col:
            st.markdown(f"""**Distribució de Superfície útil**""")
            st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod_2023, selected_mun, "Superfície útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Superfície en m\u00b2 útils segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav(bbdd_estudi_hab_2023, selected_mun,"Superfície útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Proporció d'habitatges en oferta a les promocions segons tipologia (%)**""")
            st.plotly_chart(count_plot_mun(bbdd_estudi_hab_mod_2023, selected_mun), use_container_width=True, responsive=True)
            st.markdown(f"""**Equipaments dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(equipaments_mun(bbdd_estudi_hab_mod_2023, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número de lavabos**""")
            st.plotly_chart(lavcount_plot_mun(bbdd_estudi_hab_mod_2023, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Grandària de les promocions en nombre d'habitatges**""")
            st.plotly_chart(n_promocions_habs_mun(bbdd_estudi_prom_2023, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Plaça d'aparacament inclosa o no en els habitatges en oferta (%)**""")
            st.plotly_chart(aparcament_mun(bbdd_estudi_hab_2023, selected_mun), use_container_width=True, responsive=True)

        st.subheader("Comparativa amb anys anteriors: Municipi de " + selected_mun.split(',')[0].strip())
        st.markdown(table_mun(selected_mun, 2019, int(selected_edition)).to_html(), unsafe_allow_html=True)
        st.markdown(filedownload(table_mun(selected_mun, 2019, int(selected_edition)), f"Estudi_oferta_{selected_mun}.xlsx"), unsafe_allow_html=True)
        st.markdown("")
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució dels habitatges de nova construcció per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist_units(selected_mun, "Unitats", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució de la superfície útil mitjana per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, 'Superfície mitjana (m² útils)', 2019, int(selected_edition)), use_container_width=True, responsive=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució del preu de venda per m\u00b2 útil  per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, "Preu de venda per m² útil (€)", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució del preu venda mitjà per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, "Preu mitjà de venda de l'habitatge (€)", 2019, int(selected_edition)), use_container_width=True, responsive=True)

############################################################  MUNICIPIS: 2024 ################################################
    if selected_edition=="2024":
        st.subheader(f"MUNICIPI DE {selected_mun.upper().split(',')[0].strip()}")
        st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del 2024 pel municipi de {selected_mun.split(',')[0].strip()} mostren que el preu mitjà dels habitatges en venda es troba 
        en {data_text_mun(bbdd_estudi_hab_2024, bbdd_estudi_hab_mod_2024, selected_mun)[0]:,.1f} € amb una superfície mitjana útil de {data_text_mun(bbdd_estudi_hab_2024, bbdd_estudi_hab_mod_2024, selected_mun)[1]:,.1f} m\u00b2. Per tant, el preu per m\u00b2 útil es troba en {data_text_mun(bbdd_estudi_hab_2024, bbdd_estudi_hab_mod_2024, selected_mun)[2]:,.1f} € de mitjana. Per tipologies, els habitatges plurifamiliars
        representen el {data_text_mun(bbdd_estudi_hab_2024, bbdd_estudi_hab_mod_2024, selected_mun)[3]:,.1f}% sobre el total d'habitatges, la resta corresponen a habitatges unifamiliars. L'habitatge modal o més freqüent de nova construcció té {data_text_mun(bbdd_estudi_hab_2024, bbdd_estudi_hab_mod_2024, selected_mun)[4]} habitacions i {data_text_mun(bbdd_estudi_hab_2024, bbdd_estudi_hab_mod_2024, selected_mun)[5]} banys o lavabos.""")

        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown(f"""**Distribució de Preus per m\u00b2 útil**""")
            st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod_2024, selected_mun,"Preu m2 útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Preus per m\u00b2 útil segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav(bbdd_estudi_hab_2024, selected_mun, "Preu m2 útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Característiques principals dels habitatges en oferta**""")
            st.plotly_chart(caracteristiques_mun(bbdd_estudi_hab_2024, selected_mun), use_container_width=True, responsive=True)
            st.markdown(f"""**Qualitats dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(qualitats_mun(bbdd_estudi_hab_mod_2024, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número d'habitacions**""")
            st.plotly_chart(dormscount_plot_mun(bbdd_estudi_hab_mod_2024, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Qualificació energètica dels habitatges en oferta (% d'habitatges)**""")
            st.plotly_chart(plot_table_energ_mun(bbdd_estudi_hab_2024, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Proporció d'habitatges segons el tipus d'instal·lació de calefacció (%)**""")
            st.plotly_chart(cale_tipus_mun(bbdd_estudi_prom_2024, selected_mun), use_container_width=True, responsive=True)

        with right_col:
            st.markdown(f"""**Distribució de Superfície útil**""")
            st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod_2024, selected_mun, "Superfície útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Superfície en m\u00b2 útils segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav(bbdd_estudi_hab_2024, selected_mun,"Superfície útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Proporció d'habitatges en oferta a les promocions segons tipologia (%)**""")
            st.plotly_chart(count_plot_mun(bbdd_estudi_hab_mod_2024, selected_mun), use_container_width=True, responsive=True)
            st.markdown(f"""**Equipaments dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(equipaments_mun(bbdd_estudi_hab_mod_2024, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número de lavabos**""")
            st.plotly_chart(lavcount_plot_mun(bbdd_estudi_hab_mod_2024, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Grandària de les promocions en nombre d'habitatges**""")
            st.plotly_chart(n_promocions_habs_mun(bbdd_estudi_prom_2024, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Plaça d'aparacament inclosa o no en els habitatges en oferta (%)**""")
            st.plotly_chart(aparcament_mun(bbdd_estudi_hab_2024, selected_mun), use_container_width=True, responsive=True)

        st.subheader("Comparativa amb anys anteriors: Municipi de " + selected_mun.split(',')[0].strip())
        st.markdown(table_mun(selected_mun, 2019, int(selected_edition)).to_html(), unsafe_allow_html=True)
        st.markdown(filedownload(table_mun(selected_mun, 2019, int(selected_edition)), f"Estudi_oferta_{selected_mun}.xlsx"), unsafe_allow_html=True)
        st.markdown("")
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució dels habitatges de nova construcció per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist_units(selected_mun, "Unitats", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució de la superfície útil mitjana per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, 'Superfície mitjana (m² útils)', 2019, int(selected_edition)), use_container_width=True, responsive=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució del preu de venda per m\u00b2 útil  per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, "Preu de venda per m² útil (€)", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució del preu venda mitjà per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, "Preu mitjà de venda de l'habitatge (€)", 2019, int(selected_edition)), use_container_width=True, responsive=True)

############################################################  MUNICIPIS: 1S2025 ################################################
    if selected_edition=="1S2025":
        st.subheader(f"MUNICIPI DE {selected_mun.upper().split(',')[0].strip()}")
        st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del primer semestre de 2025 pel municipi de {selected_mun.split(',')[0].strip()} mostren que el preu mitjà dels habitatges en venda es troba 
        en {data_text_mun(bbdd_estudi_hab_2025, bbdd_estudi_hab_mod_2025, selected_mun)[0]:,.1f} € amb una superfície mitjana útil de {data_text_mun(bbdd_estudi_hab_2025, bbdd_estudi_hab_mod_2025, selected_mun)[1]:,.1f} m\u00b2. Per tant, el preu per m\u00b2 útil es troba en {data_text_mun(bbdd_estudi_hab_2025, bbdd_estudi_hab_mod_2025, selected_mun)[2]:,.1f} € de mitjana. Per tipologies, els habitatges plurifamiliars
        representen el {data_text_mun(bbdd_estudi_hab_2025, bbdd_estudi_hab_mod_2025, selected_mun)[3]:,.1f}% sobre el total d'habitatges, la resta corresponen a habitatges unifamiliars. L'habitatge modal o més freqüent de nova construcció té {data_text_mun(bbdd_estudi_hab_2025, bbdd_estudi_hab_mod_2025, selected_mun)[4]} habitacions i {data_text_mun(bbdd_estudi_hab_2025, bbdd_estudi_hab_mod_2025, selected_mun)[5]} banys o lavabos.""")

        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown(f"""**Distribució de Preus per m\u00b2 útil**""")
            st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod_2025, selected_mun,"Preu m2 útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Preus per m\u00b2 útil segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav(bbdd_estudi_hab_2025, selected_mun, "Preu m2 útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Característiques principals dels habitatges en oferta**""")
            st.plotly_chart(caracteristiques_mun(bbdd_estudi_hab_2025, selected_mun), use_container_width=True, responsive=True)
            # st.markdown(f"""**Qualitats dels habitatges en oferta (% d'habitatges en oferta)**""")
            # st.plotly_chart(qualitats_mun(bbdd_estudi_hab_mod_2025, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número d'habitacions**""")
            st.plotly_chart(dormscount_plot_mun(bbdd_estudi_hab_mod_2025, selected_mun), use_container_width=True, responsive=True)
            # st.markdown("""**Qualificació energètica dels habitatges en oferta (% d'habitatges)**""")
            # st.plotly_chart(plot_table_energ_mun(bbdd_estudi_hab_2025, selected_mun), use_container_width=True, responsive=True)
            # st.markdown("""**Proporció d'habitatges segons el tipus d'instal·lació de calefacció (%)**""")
            # st.plotly_chart(cale_tipus_mun(bbdd_estudi_prom_2025, selected_mun), use_container_width=True, responsive=True)

        with right_col:
            st.markdown(f"""**Distribució de Superfície útil**""")
            st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod_2025, selected_mun, "Superfície útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Superfície en m\u00b2 útils segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav(bbdd_estudi_hab_2025, selected_mun,"Superfície útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Proporció d'habitatges en oferta a les promocions segons tipologia (%)**""")
            st.plotly_chart(count_plot_mun(bbdd_estudi_hab_mod_2025, selected_mun), use_container_width=True, responsive=True)
            # st.markdown(f"""**Equipaments dels habitatges en oferta (% d'habitatges en oferta)**""")
            # st.plotly_chart(equipaments_mun(bbdd_estudi_hab_mod_2025, selected_mun), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número de lavabos**""")
            st.plotly_chart(lavcount_plot_mun(bbdd_estudi_hab_mod_2025, selected_mun), use_container_width=True, responsive=True)
            # st.markdown("""**Grandària de les promocions en nombre d'habitatges**""")
            # st.plotly_chart(n_promocions_habs_mun(bbdd_estudi_hab_2025, selected_mun), use_container_width=True, responsive=True)
            # st.markdown("""**Plaça d'aparacament inclosa o no en els habitatges en oferta (%)**""")
            # st.plotly_chart(aparcament_mun(bbdd_estudi_hab_2025, selected_mun), use_container_width=True, responsive=True)

        st.subheader("Comparativa amb anys anteriors: Municipi de " + selected_mun.split(',')[0].strip())
        left_col, right_col = st.columns((1,1))
        st.markdown(table_mun(selected_mun, 2019, 2025).to_html(), unsafe_allow_html=True)
        st.markdown(filedownload(table_mun(selected_mun, 2019, 2025), f"Estudi_oferta_{selected_mun}.xlsx"), unsafe_allow_html=True)
        st.markdown("")
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució dels habitatges de nova construcció per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist_units(selected_mun, "Unitats", 2019, 2025), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució de la superfície útil mitjana per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, 'Superfície mitjana (m² útils)', 2019, 2025), use_container_width=True, responsive=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució del preu de venda per m\u00b2 útil  per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, "Preu de venda per m² útil (€)", 2019, 2025), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució del preu venda mitjà per tipologia d'habitatge**""")
            st.plotly_chart(plot_mun_hist(selected_mun, "Preu mitjà de venda de l'habitatge (€)", 2019, 2025), use_container_width=True, responsive=True)

############################################################  DISTRICTES DE BARCELONA ################################################
if selected=="Districtes de Barcelona":
    left, right = st.columns((1,1))
    with left:
        edicio_any = ["2022","2023", "2024","1S2025"]
        selected_edition = st.radio("**Any**", edicio_any, edicio_any.index("2024"), horizontal=True)
    with right:
        dis_names_aux_num = sorted(bbdd_estudi_prom["Nom DIST"].dropna().unique().tolist())
        dis_names_aux = [i[3:] for i in dis_names_aux_num]
        selected_dis = st.selectbox('**Districte seleccionat:**', dis_names_aux)
############################################################  DISTRICTES DE BARCELONA: 2022 ################################################
    if selected_edition=="2022":
        st.subheader("DISTRICTES DE BARCELONA")
        st.write(f"""Dels 3.278 habitatges pertanyents a les 199 promocions
                    registrades a la ciutat de Barcelona, resta per vendre el
                    42,4%. El comportament per districtes és força diferenciat
                    i oscil·la entre Ciutat Vella, on l’oferta és del 58,6%
                    dels habitatges, a Sant Martí i Les Corts, on aquesta
                    oferta disminueix fins a situar-se en un 25,4% i un 19,5%
                    respectivament. Per barris, aquest comportament evidencia
                    encara més les diferències: a Sant Antoni, Can
                    Baró, Porta, la Maternitat i Sant Ramon, Vallvidrera, el
                    Tibidabo i les Planes, el Turó de la Peira, Verdun, Prosperitat
                    i la Trinitat Vella resten per vendre la totalitat dels
                    habitatges, o la Font de la Guatlla, Sants, Sant Pere,
                    Santa Caterina i la Ribera, i Sants-Badal, on resten per
                    vendre més del 80% dels habitatges. En l’extrem contrari
                    se situen la Clota, el Poblenou, la Bordeta, el Poble Sec
                    i la Marina del Prat Vermell, on resten per vendre menys
                    del 10% dels habitatges.
                    Del 42,4% d’habitatges en oferta de venda al municipi de
                    Barcelona el 40,3% d’aquests estan acabats i el 44,1%
                    es troben en alguna fase constructiva.
                    L’oferta dels habitatges a la venda es concentra en la tipologia
                    de 2 dormitoris (41,7%) i de 3 dormitoris (35,5%),
                    reduint-se al 12,0% els d’1 dormitori i al 8,1% els de 4
                    dormitoris. Encara en percentatges menors es situen
                    l’1,8% d’habitatges tipus loft i el 0,9% d’habitatges de
                    cinc o més dormitoris.
                    A la ciutat de Barcelona és on la rehabilitació integral
                    té més presència, assolint el 30,7% de les promocions,que comporta el 31,5% dels habitatges en oferta. Per
                    districtes, la presència de la rehabilitació integral és desigual:
                    a Sarrià-Sant Gervasi, Nou Barris, Gràcia, Horta-
                    Guinardó i Sant Martí està per sota del 15%, mentre que
                    hi ha districtes on conforma la majoria de l’oferta com
                    Ciutat Vella (85,7%), l’Eixample (74,2%). Una situació
                    que es reflecteix més nítidament si l’anàlisi es trasllada
                    a escala de barris, registrant-se 27 barris (dels 52 barris
                    de la ciutat amb promocions actives) sense cap habitatge
                    en oferta provinent de la rehabilitació integral, mentre
                    hi ha barris on la totalitat de la seva oferta prové de la
                    rehabilitació integral: Sant Pere, Santa Caterina i la Ribera,
                    l’antiga Esquerra de l’Eixample, la Maternitat i Sant
                    Ramon i el Poble Sec. Destacar també l’alt percentatge
                    de promocions de rehabilitació integral al Barri Gòtic,
                    la Dreta de l’Eixample i el Raval.
                    El ventall entre els 1.390 habitatges en oferta respecte
                    a la superfície, el preu mitjà, i el preu per metre quadrat
                    útil és amplíssim si s’observa pels districtes de la ciutat.
                    A tall d’exemple, el preu mitjà màxim del metre quadrat
                    útil s’obté a l’Eixample (10.818€) i Sarrià-Sant Gervasi
                    (10.771€), i el preu mitjà mínim s’obté a Sant Andreu
                    (5.254€) i a Nou Barris (4.986€).
                    Així, la mitjana dels habitatges a la venda al municipi
                    de Barcelona és de 80,9m\u00b2 de superfície útil, amb un
                    preu de 630.559€ i un preu mitjà del metre quadrat útil
                    de 7.487€.""")
        st.subheader(f"{selected_dis.upper()}")
        st.markdown(f"""Els resultats de l'Estudi d'Oferta de Nova Construcció de 2022 pel districte de {selected_dis} de la ciutat de Barcelona mostren que el preu mitjà dels habitatges en venda es troba 
        en {data_text_dis(bbdd_estudi_hab, selected_dis)[0]:,.1f} € amb una superfície mitjana útil de {data_text_dis(bbdd_estudi_hab, selected_dis)[1]:,.1f} m\u00b2. Per tant, el preu per m\u00b2 útil es troba en {data_text_dis(bbdd_estudi_hab, selected_dis)[2]:,.1f} € de mitjana. Per tipologies, els habitatges plurifamiliars
        representen el {data_text_dis(bbdd_estudi_hab, selected_dis)[3]:,.1f}% sobre el total d'habitatges. L'habitatge modal o més freqüent de nova construcció té {data_text_dis(bbdd_estudi_hab, selected_dis)[4]} habitacions i {data_text_dis(bbdd_estudi_hab, selected_dis)[5]} banys o lavabos.""")
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown(f"""**Distribució de Preus per m\u00b2 útil**""")
            st.plotly_chart(plotdis_streamlit(bbdd_estudi_hab_mod, selected_dis,"Preu m2 útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Preus per m\u00b2 útil segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav_dis(bbdd_estudi_hab, selected_dis, "Preu m2 útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Característiques principals dels habitatges en oferta**""")
            st.plotly_chart(caracteristiques_dis(bbdd_estudi_hab, selected_dis), use_container_width=True, responsive=True)
            st.markdown(f"""**Qualitats dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(qualitats_dis(bbdd_estudi_hab_mod, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número d'habitacions**""")
            st.plotly_chart(dormscount_plot_dis(bbdd_estudi_hab_mod, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Qualificació energètica dels habitatges en oferta (% d'habitatges)**""")
            st.plotly_chart(plot_table_energ_dis(bbdd_estudi_hab, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Proporció d'habitatges segons el tipus d'instal·lació de calefacció (%)**""")
            st.plotly_chart(cale_tipus_dis(bbdd_estudi_prom, selected_dis), use_container_width=True, responsive=True)
        with right_col:
            st.markdown(f"""**Distribució de Superfície útil**""")
            st.plotly_chart(plotdis_streamlit(bbdd_estudi_hab_mod, selected_dis, "Superfície útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Superfície en m\u00b2 útils segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav_dis(bbdd_estudi_hab, selected_dis,"Superfície útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Proporció d'habitatges en oferta a les promocions segons tipologia (%)**""")
            st.plotly_chart(count_plot_dis(bbdd_estudi_hab_mod, selected_dis), use_container_width=True, responsive=True)
            st.markdown(f"""**Equipaments dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(equipaments_dis(bbdd_estudi_hab_mod, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número de lavabos**""")
            st.plotly_chart(lavcount_plot_dis(bbdd_estudi_hab_mod, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Grandària de les promocions en nombre d'habitatges**""")
            st.plotly_chart(n_promocions_habs_dis(bbdd_estudi_prom, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Plaça d'aparacament inclosa o no en els habitatges en oferta (%)**""")
            st.plotly_chart(aparcament_dis(bbdd_estudi_hab, selected_dis), use_container_width=True, responsive=True)


        st.subheader(f"Comparativa amb anys anteriors: Districte de {selected_dis}")
        st.markdown(geo_dis(selected_dis, 2019, int(selected_edition)).to_html(), unsafe_allow_html=True)
        st.markdown(filedownload(geo_dis(selected_dis, 2019, int(selected_edition)), f"Estudi_oferta_{selected_dis}.xlsx"), unsafe_allow_html=True)

        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("")
            st.markdown("")
            st.markdown("""**Evolució dels habitatges de nova construcció per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist_units(selected_dis, "Unitats", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("")
            st.markdown("")
            st.markdown("""**Evolució de la superfície útil mitjana per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, 'Superfície mitjana (m² útils)', 2019, int(selected_edition)), use_container_width=True, responsive=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució del preu de venda per m\u00b2 útil  per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, "Preu de venda per m² útil (€)", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució del preu venda mitjà per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, "Preu mitjà de venda de l'habitatge (€)", 2019, int(selected_edition)),use_container_width=True, responsive=True)

############################################################  DISTRICTES DE BARCELONA: 2023 ################################################
    if selected_edition=="2023":
        st.subheader("DISTRICTES DE BARCELONA")
        st.write(f"""<p>
                    L'Estudi d'Oferta de nova construcció de 2023 a la ciutat de Barcelona inclou un total de 224 promocions i 1.560 habitatges destinats a la venda, d’un total de 3.813 habitatges.
                    Els districtes amb major nombre de promocions són Horta-Guinardó (40), Eixample (35) i Sant Martí (29). Per altra banda, aquells que disposen de menor nombre de promocions són Nou Barris (9) i Les Corts (6). 
                    El ranking del nombre d'habitatges en oferta de venda per districte canvia lleugerament: Eixample (256), Horta-Guinardó (255), Sant Andreu (209) i Sant Martí (203). Aquells districtes amb menys habitatges a la venda són Nou Barris (66) i Les Corts (24). 
                    Addicionalment, l’oferta dels habitatges a la venda es concentra en la tipologia de 2 dormitoris (41,4%) i de 3 dormitoris (36,3%), reduint-se al 12,5% els d’1 dormitori i al 7,3% els de 4 dormitoris.
                    En percentatges menors, es situen els habitatges tipus loft (1,5%) i els habitatges de cinc o més dormitoris (1,0%). 
                    </p>   
                    <p>
                    En general, existeix una correspondència directa entre la superfície i el nombre de dormitoris de l’habitatge en oferta. 
                    Aquesta correspondència comporta que el 54,4% dels habitatges d’un dormitori tinguin superfícies iguals o inferiors als 50m², que el 56,2% dels habitatges de dos dormitoris tinguin superfícies entre els 50 i 70m², 
                    que el 46,7% dels habitatges de tres dormitoris tinguin entre 70 i 90m² i que el 50,9% dels habitatges de quatre dormitoris tinguin superfícies entre els 80 i els 100 m².
                    Els preus mitjans per superfícies oscil·len des dels 305.645 euros en els habitatges de menys de 50 m², fins els 1.888.514 euros pels habitatges de més de 160 m² (52 habitatges). 
                    Més concretament, els valors mitjans estimats, en general, configurarien un habitatge tipus de 80,7 m² amb un preu de 628.339€ i un preu del m² de superfície útil de 7.429€.
                    Els rangs de superfícies, preus mitjans i preus per metre quadrat útil és amplíssim pels diferents districtes de la ciutat. Com a tall de mostra la mitjana del preu màxim del metre quadrat útil 
                    que s’obté a Sarrià-Sant Gervasi (10.361€) i l’Eixample (9.949€) i la mitjana del preu mínim que s’obté a Sant Andreu (5.405€) i Nou Barris (5.368€).
                    El preu de venda per metre quadrat útil dels habitatges a la venda varia lleugerament en un -0,8% en relació a 2022 (que el situa en 7.429€/m2).
                    Aquest ajust és el resultat d’uns valors semblants en superfície mitjana i preu mitjà de venda dels últims 2 anys al municipi de Barcelona. 
                    Les variacions de preus presenten comportaments diferents en funció del districte, destaquem un increment del 13,9% en el preu per metre quadrat útil a Gràcia o del 10,7% a Sant Martí i un descens del 8,0% a l’Eixample.
                    </p>
                    """, unsafe_allow_html=True)
        st.subheader(f"{selected_dis.upper()}")
        st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del 2023 pel districte de {selected_dis} de la ciutat de Barcelona mostren que el preu mitjà dels habitatges en venda es troba 
        en {data_text_dis(bbdd_estudi_hab_2023, selected_dis)[0]:,.1f} € amb una superfície mitjana útil de {data_text_dis(bbdd_estudi_hab_2023, selected_dis)[1]:,.1f} m\u00b2. Per tant, el preu per m\u00b2 útil es troba en {data_text_dis(bbdd_estudi_hab_2023, selected_dis)[2]:,.1f} € de mitjana. Per tipologies, els habitatges plurifamiliars
        representen el {data_text_dis(bbdd_estudi_hab_2023, selected_dis)[3]:,.1f}% sobre el total d'habitatges. L'habitatge modal o més freqüent de nova construcció té {data_text_dis(bbdd_estudi_hab_2023, selected_dis)[4]} habitacions i {data_text_dis(bbdd_estudi_hab_2023, selected_dis)[5]} banys o lavabos.""")
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown(f"""**Distribució de Preus per m\u00b2 útil**""")
            st.plotly_chart(plotdis_streamlit(bbdd_estudi_hab_mod_2023, selected_dis,"Preu m2 útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Preus per m\u00b2 útil segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav_dis(bbdd_estudi_hab_2023, selected_dis, "Preu m2 útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Característiques principals dels habitatges en oferta**""")
            st.plotly_chart(caracteristiques_dis(bbdd_estudi_hab_2023, selected_dis), use_container_width=True, responsive=True)
            st.markdown(f"""**Qualitats dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(qualitats_dis(bbdd_estudi_hab_mod_2023, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número d'habitacions**""")
            st.plotly_chart(dormscount_plot_dis(bbdd_estudi_hab_mod_2023, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Qualificació energètica dels habitatges en oferta (% d'habitatges)**""")
            st.plotly_chart(plot_table_energ_dis(bbdd_estudi_hab_2023, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Proporció d'habitatges segons el tipus d'instal·lació de calefacció (%)**""")
            st.plotly_chart(cale_tipus_dis(bbdd_estudi_prom_2023, selected_dis), use_container_width=True, responsive=True)
        with right_col:
            st.markdown(f"""**Distribució de Superfície útil**""")
            st.plotly_chart(plotdis_streamlit(bbdd_estudi_hab_mod_2023, selected_dis, "Superfície útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Superfície en m\u00b2 útils segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav_dis(bbdd_estudi_hab_2023, selected_dis,"Superfície útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Proporció d'habitatges en oferta a les promocions segons tipologia (%)**""")
            st.plotly_chart(count_plot_dis(bbdd_estudi_hab_mod_2023, selected_dis), use_container_width=True, responsive=True)
            st.markdown(f"""**Equipaments dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(equipaments_dis(bbdd_estudi_hab_mod_2023, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número de lavabos**""")
            st.plotly_chart(lavcount_plot_dis(bbdd_estudi_hab_mod_2023, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Grandària de les promocions en nombre d'habitatges**""")
            st.plotly_chart(n_promocions_habs_dis(bbdd_estudi_prom_2023, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Plaça d'aparacament inclosa o no en els habitatges en oferta (%)**""")
            st.plotly_chart(aparcament_dis(bbdd_estudi_hab_2023, selected_dis), use_container_width=True, responsive=True)
        st.subheader(f"Comparativa amb anys anteriors: Districte de {selected_dis}")
        st.markdown(geo_dis(selected_dis, 2019, int(selected_edition)).to_html(), unsafe_allow_html=True)
        st.markdown(filedownload(geo_dis(selected_dis, 2019, int(selected_edition)), f"Estudi_oferta_{selected_dis}.xlsx"), unsafe_allow_html=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("")
            st.markdown("")
            st.markdown("""**Evolució dels habitatges de nova construcció per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist_units(selected_dis, "Unitats", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("")
            st.markdown("")
            st.markdown("""**Evolució de la superfície útil mitjana per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, 'Superfície mitjana (m² útils)', 2019, int(selected_edition)), use_container_width=True, responsive=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució del preu de venda per m\u00b2 útil  per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, "Preu de venda per m² útil (€)", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució del preu venda mitjà per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, "Preu mitjà de venda de l'habitatge (€)", 2019, int(selected_edition)),use_container_width=True, responsive=True)

############################################################  DISTRICTES DE BARCELONA: 2024 ################################################
    if selected_edition=="2024":
        st.subheader("DISTRICTES DE BARCELONA")
        st.write(f"""
                <p>
                L'Estudi d'Oferta de nova construcció de 2024 A la ciutat de Barcelona inclou un total de 175 promocions i 800 habitatges destinats a la venda, d’un total de 3.219 habitatges.
                Els districtes amb major nombre de promocions són Horta-Guinardó (35), Eixample (26) i Ciutat Vella (22). Els que disposen de menor nombre de promocions són Nou Barris (11) i Les Corts (2). El ranking del nombre d'habitatges en oferta de venda per districte roman inalterat respecte a les promocions: Horta-Guinardó (154), Eixample (136) i Ciutat Vella (103). Aquells districtes amb menys habitatges a la venda són Sarrià-Sant Gervasi (39) i Les Corts (6). Addicionalment, l’oferta dels habitatges a la venda es concentra en la tipologia de 2 dormitoris (41,4%) i de 3 dormitoris (35,8%), reduint-se al 13,9% els d’1 dormitori i al 8,5% els de 4 dormitoris. Encara en percentatges menors es situen els habitatges tipus loft (0,1%) i els de cinc o més dormitoris (0,4%). 
                </p>
                <p>
                En general, existeix una correspondència directa entre la superfície i el nombre de dormitoris de l’habitatge en oferta. Aquesta correspondència comporta que el 44,1% dels habitatges d’un dormitori tinguin superfícies iguals o inferiors als 50m², que el 55,9% dels habitatges de dos dormitoris tinguin superfícies entre els 50 i 70m², i que el 47,2% dels habitatges de tres dormitoris tinguin entre 70 i 90m². Els preus mitjans per superfícies oscil·len des dels 355.186€ en els habitatges de menys de 50 m², fins els 2.642.523€ pels habitatges de més de 160 m² (27 habitatges). Més concretament, els valors mitjans estimats, en general, configurarien un habitatge tipus de 83,5 m² amb un preu de 689.881€ i un preu del m² de superfície útil de 7.798€. El ventall entre els 800 habitatges en oferta, respecte a la superfície, el preu i el preu per metre quadrat útil és amplíssim si s’observa pels districtes de la ciutat, serveixi a tall de mostra la mitjana del preu màxim del metre quadrat útil que s’obté a l’Eixample (10.519€), Sarrià-Sant Gervasi (10.368€) i Les Corts (10.292€), i la mitjana del preu mínim que s’obté a  Horta-Guinardó (5.985€) i Nou Barris (5.399€). 
                </p>
                <p>
                L’any 2024 s’han registrat un total de 175 promocions, 49 menys que l’any 2023 quan es van registrar 224 promocions. En relació al nombre d’habitatges, el total de 2024, 800 habitatges, 760 menys que els 1.560 de 2023. Cal esmentar que de les 224 promocions de 2023, 104 (el 46,4%) ja han estat totalment venudes al 2024 i, en relació als habitatges de 2023 (1.560), el 67,1% han estat venuts. El preu de venda per metre quadrat útil dels habitatges a la venda s’incrementa en un 5,8% en relació a 2023 (que el situa en 7.798€/m2). Aquest increment és el resultat d’un increment del 3,5% en la superfície mitjana útil i d’un 9,8% en el preu mitjà de venda de l’habitatge.
                </p>
                    """, unsafe_allow_html=True)
        st.subheader(f"{selected_dis.upper()}")
        st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del 2024 pel districte de {selected_dis} de la ciutat de Barcelona mostren que el preu mitjà dels habitatges en venda es troba 
        en {data_text_dis(bbdd_estudi_hab_2024, selected_dis)[0]:,.1f} € amb una superfície mitjana útil de {data_text_dis(bbdd_estudi_hab_2024, selected_dis)[1]:,.1f} m\u00b2. Per tant, el preu per m\u00b2 útil es troba en {data_text_dis(bbdd_estudi_hab_2024, selected_dis)[2]:,.1f} € de mitjana. Per tipologies, els habitatges plurifamiliars
        representen el {data_text_dis(bbdd_estudi_hab_2024, selected_dis)[3]:,.1f}% sobre el total d'habitatges. L'habitatge modal o més freqüent de nova construcció té {data_text_dis(bbdd_estudi_hab_2024, selected_dis)[4]} habitacions i {data_text_dis(bbdd_estudi_hab_2024, selected_dis)[5]} banys o lavabos.""")
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown(f"""**Distribució de Preus per m\u00b2 útil**""")
            st.plotly_chart(plotdis_streamlit(bbdd_estudi_hab_mod_2024, selected_dis,"Preu m2 útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Preus per m\u00b2 útil segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav_dis(bbdd_estudi_hab_2024, selected_dis, "Preu m2 útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Característiques principals dels habitatges en oferta**""")
            st.plotly_chart(caracteristiques_dis(bbdd_estudi_hab_2024, selected_dis), use_container_width=True, responsive=True)
            st.markdown(f"""**Qualitats dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(qualitats_dis(bbdd_estudi_hab_mod_2024, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número d'habitacions**""")
            st.plotly_chart(dormscount_plot_dis(bbdd_estudi_hab_mod_2024, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Qualificació energètica dels habitatges en oferta (% d'habitatges)**""")
            st.plotly_chart(plot_table_energ_dis(bbdd_estudi_hab_2024, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Proporció d'habitatges segons el tipus d'instal·lació de calefacció (%)**""")
            st.plotly_chart(cale_tipus_dis(bbdd_estudi_prom_2024, selected_dis), use_container_width=True, responsive=True)
        with right_col:
            st.markdown(f"""**Distribució de Superfície útil**""")
            st.plotly_chart(plotdis_streamlit(bbdd_estudi_hab_mod_2024, selected_dis, "Superfície útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Superfície en m\u00b2 útils segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav_dis(bbdd_estudi_hab_2024, selected_dis,"Superfície útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Proporció d'habitatges en oferta a les promocions segons tipologia (%)**""")
            st.plotly_chart(count_plot_dis(bbdd_estudi_hab_mod_2024, selected_dis), use_container_width=True, responsive=True)
            st.markdown(f"""**Equipaments dels habitatges en oferta (% d'habitatges en oferta)**""")
            st.plotly_chart(equipaments_dis(bbdd_estudi_hab_mod_2024, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número de lavabos**""")
            st.plotly_chart(lavcount_plot_dis(bbdd_estudi_hab_mod_2024, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Grandària de les promocions en nombre d'habitatges**""")
            st.plotly_chart(n_promocions_habs_dis(bbdd_estudi_prom_2024, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Plaça d'aparacament inclosa o no en els habitatges en oferta (%)**""")
            st.plotly_chart(aparcament_dis(bbdd_estudi_hab_2024, selected_dis), use_container_width=True, responsive=True)
        st.subheader(f"Comparativa amb anys anteriors: Districte de {selected_dis}")
        st.markdown(geo_dis(selected_dis, 2019, int(selected_edition)).to_html(), unsafe_allow_html=True)
        st.markdown(filedownload(geo_dis(selected_dis, 2019, int(selected_edition)), f"Estudi_oferta_{selected_dis}.xlsx"), unsafe_allow_html=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("")
            st.markdown("")
            st.markdown("""**Evolució dels habitatges de nova construcció per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist_units(selected_dis, "Unitats", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("")
            st.markdown("")
            st.markdown("""**Evolució de la superfície útil mitjana per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, 'Superfície mitjana (m² útils)', 2019, int(selected_edition)), use_container_width=True, responsive=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució del preu de venda per m\u00b2 útil  per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, "Preu de venda per m² útil (€)", 2019, int(selected_edition)), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució del preu venda mitjà per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, "Preu mitjà de venda de l'habitatge (€)", 2019, int(selected_edition)),use_container_width=True, responsive=True)

############################################################  DISTRICTES DE BARCELONA: 1S2025 ################################################
    if selected_edition=="1S2025":
        st.subheader("DISTRICTES DE BARCELONA")
        st.write(f"""<p>
                        A la ciutat de Barcelona, els resultats del treball realitzat fins el mes de juny de 2025, inclouen un total de 106 promocions i 625 habitatges en venda, d’un total de 2.045 habitatges.
                        Els districtes amb major nombre de promocions són Eixample (21) i Horta-Guinardó (19). Els que disposen d’un menor nombre de promocions són Gràcia (6), Sarrià-Sant Gervasi (6) i Les Corts (1). La quantificació del nombre d’habitatges en oferta presenta alguna variació en comparació amb el de promocions. Horta-Guinardó és el districte amb més habitatges (122) i l’Eixample ocupa el segon lloc amb una habitatge menys (121). La oferta més baixa d’habitatges es localitza en els mateixos districtes amb menys promocions: Gràcia (37), Sarrià-Sant Gervasi (29) i Les Corts (4).
                        En el cas de la ciutat de Barcelona, les tipologies amb més oferta són les de 2 dormitoris amb un 41,1% i les de 3 dormitoris amb un 37,3% (al conjunt de Catalunya l’oferta de 3 dormitoris és superior a la de 2 dormitoris). Cal destacar que a la ciutat de Barcelona més de tres quartes parts de l’oferta correspon a habitatges de 2 o 3 dormitoris (78,4%).
                    </p>
                    <p>
                        La superfície mitjana dels habitatges a la venda és de 83,3 m\u00b2 útils, amb un descens mínim del -0,3% en relació a finals de 2024 (83,5 m\u00b2). Aquesta variació no és homogènia en tots els districtes i, en els extrems trobem diferències importants. D’aquesta manera la superfície dels habitatges a la venda en Sarrià-Sant Gervasi baixa un -11,5%, mentre que en els districtes de Sant Martí i Les Corts incrementa 9,5% i 5,9% respectivament.
                    </p>
                    <p>
                        El preu mitjà de l’habitatge a la venda a la ciutat de Barcelona és de 711.260 €, un 3,1% més en relació a finals de 2024 (689.881 €). En els districtes de Sant Martí i Gràcia, és on es produeix un increment més important, un 27,7% i 10,5% respectivament. 
                        Pel que fa al preu per m\u00b2 útil, és de 7.962 €, valor que suposa una variació d’un 2,1% en relació a 2024 (7.798 €).
                    </p>
                    """, unsafe_allow_html=True)
        st.subheader(f"{selected_dis.upper()}")
        st.markdown(f"""Els resultats de l'Estudi d'Oferta de nova construcció del primer semestre de 2025 pel districte de {selected_dis} de la ciutat de Barcelona mostren que el preu mitjà dels habitatges en venda es troba 
        en {data_text_dis(bbdd_estudi_hab_2025, selected_dis)[0]:,.1f} € amb una superfície mitjana útil de {data_text_dis(bbdd_estudi_hab_2025, selected_dis)[1]:,.1f} m\u00b2. Per tant, el preu per m\u00b2 útil es troba en {data_text_dis(bbdd_estudi_hab_2025, selected_dis)[2]:,.1f} € de mitjana. Per tipologies, els habitatges plurifamiliars
        representen el {data_text_dis(bbdd_estudi_hab_2025, selected_dis)[3]:,.1f}% sobre el total d'habitatges. L'habitatge modal o més freqüent de nova construcció té {data_text_dis(bbdd_estudi_hab_2025, selected_dis)[4]} habitacions i {data_text_dis(bbdd_estudi_hab_2025, selected_dis)[5]} banys o lavabos.""")
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown(f"""**Distribució de Preus per m\u00b2 útil**""")
            st.plotly_chart(plotdis_streamlit(bbdd_estudi_hab_mod_2025, selected_dis,"Preu m2 útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Preus per m\u00b2 útil segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav_dis(bbdd_estudi_hab_2025, selected_dis, "Preu m2 útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Característiques principals dels habitatges en oferta**""")
            st.plotly_chart(caracteristiques_dis(bbdd_estudi_hab_2025, selected_dis), use_container_width=True, responsive=True)
            # st.markdown(f"""**Qualitats dels habitatges en oferta (% d'habitatges en oferta)**""")
            # st.plotly_chart(qualitats_dis(bbdd_estudi_hab_mod_2025, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número d'habitacions**""")
            st.plotly_chart(dormscount_plot_dis(bbdd_estudi_hab_mod_2025, selected_dis), use_container_width=True, responsive=True)
            # st.markdown("""**Qualificació energètica dels habitatges en oferta (% d'habitatges)**""")
            # st.plotly_chart(plot_table_energ_dis(bbdd_estudi_hab_2025, selected_dis), use_container_width=True, responsive=True)
            # st.markdown("""**Proporció d'habitatges segons el tipus d'instal·lació de calefacció (%)**""")
            # st.plotly_chart(cale_tipus_dis(bbdd_estudi_prom_2025, selected_dis), use_container_width=True, responsive=True)
        with right_col:
            st.markdown(f"""**Distribució de Superfície útil**""")
            st.plotly_chart(plotdis_streamlit(bbdd_estudi_hab_mod_2025, selected_dis, "Superfície útil"), use_container_width=True, responsive=True)
            st.markdown(f"""**Superfície en m\u00b2 útils segons nombre d'habitacions i lavabos**""")
            st.markdown(matrix_hab_lav_dis(bbdd_estudi_hab_2025, selected_dis,"Superfície útil").to_html(), unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"""**Proporció d'habitatges en oferta a les promocions segons tipologia (%)**""")
            st.plotly_chart(count_plot_dis(bbdd_estudi_hab_mod_2025, selected_dis), use_container_width=True, responsive=True)
            # st.markdown(f"""**Equipaments dels habitatges en oferta (% d'habitatges en oferta)**""")
            # st.plotly_chart(equipaments_dis(bbdd_estudi_hab_mod_2025, selected_dis), use_container_width=True, responsive=True)
            st.markdown("""**Habitatges a la venda segons número de lavabos**""")
            st.plotly_chart(lavcount_plot_dis(bbdd_estudi_hab_mod_2025, selected_dis), use_container_width=True, responsive=True)
            # st.markdown("""**Grandària de les promocions en nombre d'habitatges**""")
            # st.plotly_chart(n_promocions_habs_dis(bbdd_estudi_hab_2025, selected_dis), use_container_width=True, responsive=True)
            # st.markdown("""**Plaça d'aparacament inclosa o no en els habitatges en oferta (%)**""")
            # st.plotly_chart(aparcament_dis(bbdd_estudi_hab_2025, selected_dis), use_container_width=True, responsive=True)
        st.subheader(f"Comparativa amb anys anteriors: Districte de {selected_dis}")
        st.markdown(geo_dis(selected_dis, 2019, 2026).to_html(), unsafe_allow_html=True)
        st.markdown(filedownload(geo_dis(selected_dis, 2019, 2026), f"Estudi_oferta_{selected_dis}.xlsx"), unsafe_allow_html=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("")
            st.markdown("")
            st.markdown("""**Evolució dels habitatges de nova construcció per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist_units(selected_dis, "Unitats", 2019, 2025), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("")
            st.markdown("")
            st.markdown("""**Evolució de la superfície útil mitjana per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, 'Superfície mitjana (m² útils)', 2019, 2025), use_container_width=True, responsive=True)
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.markdown("""**Evolució del preu de venda per m\u00b2 útil  per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, "Preu de venda per m² útil (€)", 2019, 2025), use_container_width=True, responsive=True)
        with right_col:
            st.markdown("""**Evolució del preu venda mitjà per tipologia d'habitatge**""")
            st.plotly_chart(plot_dis_hist(selected_dis, "Preu mitjà de venda de l'habitatge (€)", 2019, 2025),use_container_width=True, responsive=True)

# if selected=="Contacte":
#     CONTACT_EMAIL = "estudis@apcecat.cat"
#     st.write("")
#     st.subheader(":mailbox: Contacteu-nos!")
#     contact_form = f"""
#     <form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST">
#         <input type="hidden" name="_captcha" value="false">
#         <input type="text" name="name" placeholder="Nom" required>
#         <input type="email" name="email" placeholder="Correu electrònic" required>
#         <textarea name="message" placeholder="La teva consulta aquí"></textarea>
#         <button type="submit" class="button">Enviar ✉</button>
#     </form>
#     """
#     st.markdown(contact_form, unsafe_allow_html=True)


