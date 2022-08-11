import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import plotly.express as px

df = pd.read_csv('./dataset/data_covid.csv')
#df.head()
# Convertimos fechas en datetime
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Seleccionamos columnas que vemos mas relevantes para el informe
selecc_col_dic = {   'state' : 'Estado', # Estado 
                 'date' : 'Fecha',  # Fecha
                 'critical_staffing_shortage_today_yes': 'Reporta_escasez_de_personal', # Hospitales que informan escasez de personal
                 'critical_staffing_shortage_today_no': 'Reportan_sin_escasez_de_personal', # Hospitales
                 'critical_staffing_shortage_today_not_reported': 'No_reportan_sobre_escasez_de_personal', #Hospitales
                 'inpatient_beds': 'Camas_hospital', #hospital_camas  
                 'inpatient_beds_used_covid': 'Camas_usadas_sosp_conf', # hospital_camas_usadas_sospech_confir_covid
                 'previous_day_admission_adult_covid_confirmed': 'Admision_adulto_conf_dia_previo', # día_anterior_admisión_adulto_covid_confirmado
                 'previous_day_admission_pediatric_covid_confirmed': 'Admision_pediatrico_conf_dia_previo', # día_anterior_ingreso_pediátrico_covid_confirmado
                  'staffed_adult_icu_bed_occupancy': 'Camas_UCI_ocupadas_general', # numero_total_camas_UCI_ocupadas_general
                  'staffed_icu_adult_patients_confirmed_covid': 'Camas_UCI_adultos_ocupadas_conf', # numero_camas_UCI_ocupadas_Covid_confirmado_adultos
                  'total_adult_patients_hospitalized_confirmed_covid': 'Camas_comunes_adulto_ocupadas_conf', # numero_camas_comunes_ocupadas_Covid_confirmado
                  'total_pediatric_patients_hospitalized_confirmed_covid': 'Camas_comunes_pediatrico_ocupadas_conf', # numero_camas_comunes_ocupadas_Covid_confirmado_pediatrico
                  'total_staffed_adult_icu_beds': 'Camas_UCI_adultos', # numero_camas_UCI_adultos
                  'inpatient_beds_utilization': 'Porcentaje_utilizacion_camas', # porcentaje de camas utilizadas en el estado
                  #'geocoded_state', # estado_geocodificado 
                  'previous_day_admission_adult_covid_confirmed_18_19': 'Rango_18_19_confirmados_hospitalizados', # rango etario
                  'previous_day_admission_adult_covid_confirmed_20_29': 'Rango_20_29_confirmados_hospitalizados', # rango etario
                  'previous_day_admission_adult_covid_confirmed_30_39': 'Rango_30_39_confirmados_hospitalizados', # rango etario
                  'previous_day_admission_adult_covid_confirmed_40_49': 'Rango_40_49_confirmados_hospitalizados', # rango etario
                  'previous_day_admission_adult_covid_confirmed_50_59': 'Rango_50_59_confirmados_hospitalizados', # rango etario
                  'previous_day_admission_adult_covid_confirmed_60_69': 'Rango_60_69_confirmados_hospitalizados',  # rango etario
                  'previous_day_admission_adult_covid_confirmed_70_79': 'Rango_70_79_confirmados_hospitalizados', # rango etario
                  'previous_day_admission_adult_covid_confirmed_80': 'Rango_80_mas_confirmados_hospitalizados',     # rango etario
                  'previous_day_admission_adult_covid_confirmed_unknown': 'Rango_desconocido_confirmados_hospitalizados', # rango etario
                  'deaths_covid': 'Muertes_covid', # muertes covid conf y sospechosos
                   'all_pediatric_inpatient_beds': 'Camas_pediatricas', # Total camas pediatricas
                   'previous_day_admission_pediatric_covid_confirmed_0_4': 'Rango_0_4_confirmados_hospitalizados',
                   'previous_day_admission_pediatric_covid_confirmed_5_11': 'Rango_5_11_confirmados_hospitalizados',
                   'previous_day_admission_pediatric_covid_confirmed_12_17': 'Rango_12_17_confirmados_hospitalizados'
                }
df = df[list(selecc_col_dic.keys())]
df.rename(selecc_col_dic, axis= 1, inplace= True)
fecha_max = str(df.Fecha.values.max())[:10]
fecha_min = str(df.Fecha.values.min())[:10]

# Funcion principal
def main():
    #titulo
    st.title('Proyecto I2')
    
    #titulo de sidebar
    st.sidebar.header('Parametros')

    #Ponemos los parametros customizables en el sidebar
    st.sidebar.subheader('Intervalo Fechas Muestras - Mapa Geografico')
    fecha_inicio = st.sidebar.date_input('Fecha Inicio: ', value= dt.date.fromisoformat(fecha_min), min_value= dt.date.fromisoformat(fecha_min), max_value= dt.date.fromisoformat(fecha_max))
    fecha_final = st.sidebar.date_input('Fecha Final: ', value= dt.date.fromisoformat('2022-06-30'), min_value= dt.date.fromisoformat(fecha_min), max_value= dt.date.fromisoformat(fecha_max))
    
    
    # Filtramos dataset
    df_fechas = df[(df['Fecha'] >= str(fecha_inicio)) & (df['Fecha'] <= str(fecha_final))]
    df_agrup_state = df_fechas[['Estado', 'Camas_comunes_adulto_ocupadas_conf', 'Camas_comunes_pediatrico_ocupadas_conf']]
    df_agrup_state['Hospitalizados'] = df_agrup_state['Camas_comunes_adulto_ocupadas_conf'] + df_agrup_state['Camas_comunes_pediatrico_ocupadas_conf']
    df_agrup_state = df_agrup_state.groupby('Estado', as_index= False).sum()
    df_agrup_state = df_agrup_state.sort_values(by = 'Camas_comunes_adulto_ocupadas_conf' ,ascending= False)
   
    # Mapa Hospitalizados
    def grafico_mapa(df):
        figura_mapa= px.choropleth(df,
                           locations= df['Estado'],
                           locationmode= 'USA-states',
                           scope= 'usa',
                           color= df['Hospitalizados'],
                           color_continuous_scale= 'hot_r',
                           labels= {'locations': 'Estado', 'color_continuous_scale': 'Hospita'},
                           )
        figura_mapa.update_layout(
                            title_text= 'Hospitalizados por COVID-19 por Estado (USA)',
                            #geo_scope= 'usa',
                    
                           )
        return figura_mapa


    figura_mapa = grafico_mapa(df_agrup_state)
    st.plotly_chart(figura_mapa)


    # Mostramos informacion en cuerpo de pagina
    st.subheader('Top 5 Estados con Mayor Ocupacion Hosp. COVID')
    st.write('Fecha inicio:', fecha_inicio, 'Fecha Final:', fecha_final)
    
    #Grafico
    def grafico_figura1(df):
        figura1 = px.bar(df, 
                        x= df.Estado,
                        y= df.Hospitalizados,
                    title= 'Top 5 Estados con mayor camas (comunes utilizadas)',
                    )
        return figura1
    
    figura1 = grafico_figura1(df_agrup_state[['Estado', 'Hospitalizados']].head(5))
    st.plotly_chart(figura1)
    

    ## Punto 2
    #Ponemos los parametros customizables en el sidebar
    st.sidebar.subheader('Intervalo Fechas - Ocupacion Camas')
    fecha_inicio_2 = st.sidebar.date_input('Fecha Inicio Ocupación: ', value= dt.date.fromisoformat(fecha_min), min_value= dt.date.fromisoformat(fecha_min), max_value= dt.date.fromisoformat(fecha_max))
    fecha_final_2 = st.sidebar.date_input('Fecha Final Ocupación: ', value= dt.date.fromisoformat('2021-06-15'), min_value= dt.date.fromisoformat(fecha_min), max_value= dt.date.fromisoformat(fecha_max))

    df_fechas2 = df[(df['Fecha'] >= str(fecha_inicio_2)) & (df['Fecha'] <= str(fecha_final_2))] 
    df_fechas2 = df_fechas2[['Fecha', 'Camas_comunes_adulto_ocupadas_conf', 'Camas_comunes_pediatrico_ocupadas_conf', 'Camas_UCI_adultos_ocupadas_conf']]
    df_fechas2['Hospitalizados'] = df_fechas2['Camas_comunes_adulto_ocupadas_conf'] + df_fechas2['Camas_comunes_pediatrico_ocupadas_conf']

    df_fechas2 = df_fechas2.groupby('Fecha', as_index= False).sum()
    df_fechas2.drop(['Camas_comunes_pediatrico_ocupadas_conf','Camas_comunes_adulto_ocupadas_conf'], axis=1, inplace= True)
    df_fechas2.rename({'Camas_UCI_adultos_ocupadas_conf':'Hospitalizados_UCI'}, axis= 1, inplace= True)
    
    st.subheader('Ocupación de camas por COVID')
    st.write('Fecha inicio:', fecha_inicio_2, 'Fecha Final:', fecha_final_2)

    # Graficamos
    max_2020 = df_fechas2.Hospitalizados.max()
    fecha_punto_max = str(df_fechas2[(df_fechas2['Hospitalizados'] == max_2020)].Fecha.values)[2:12]
    
    def grafico_figura2(df):
        figura8 = px.line(df,
                    x= df.Fecha,
                    y= [df.Hospitalizados, df.Hospitalizados_UCI]
                    )
                    
        return figura8
    
    figura2 = grafico_figura2(df_fechas2)
    st.plotly_chart(figura2)

    st.write('Punto Max:', max_2020, 'Fecha:', fecha_punto_max)
    
    ## Punto 3
    # cinco Estados que más camas UCI -Unidades de Cuidados Intensivos- utilizaron durante el año 2020
    st.sidebar.subheader('')
    
    
    st.subheader('Estados que más camas UCI -Unidades de Cuidados Intensivos- utilizaron durante el año 2020')
    
    # Filtramos dataset
    df_2020 = df[(df['Fecha'] <= '2020-12-31')]
    df_agrup_state_UCI = df_2020[['Estado', 'Camas_UCI_adultos_ocupadas_conf']].groupby('Estado').sum()

   
    opciones = st.slider('Select a modulus', 1, len(df_agrup_state_UCI), 5)
    df_agrup_state_UCI = df_agrup_state_UCI.sort_values(by = 'Camas_UCI_adultos_ocupadas_conf' ,ascending= False).head(opciones)

    #Graficamos
    def grafico_figura3(df):
        figura3 = px.bar(df_agrup_state_UCI)
        return figura3
    
    figura3 = grafico_figura3(df_agrup_state_UCI)
    st.plotly_chart(figura3)
    

    #st.bar_chart(fig_UCI)
    



# Indicamos este archivo como principal
if __name__ == '__main__':
    main()