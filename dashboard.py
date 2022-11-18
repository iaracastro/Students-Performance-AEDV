import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns
import plotly.express as px
import streamlit as st

st.set_page_config(page_title = "Performance de Estudantes", page_icon=":bar_chart:", layout = "wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df = pd.read_csv('exams.csv')
df.drop_duplicates(inplace=True)
###############################################################################################
df=df.rename(columns={"gender":"sexo",
                      "race/ethnicity":"grupo_etnico",
                      "parental level of education":"educ_parental",
                      "lunch":"lanche",
                      "test preparation course":"curso_preparatorio",
                      "math score":"notas_matematica",
                      "reading score":"notas_leitura",
                      "writing score":"notas_redacao"})

df['sexo']=df['sexo'].replace({'male': 'Homem',
                               'female': 'Mulher'})

df['grupo_etnico']=df['grupo_etnico'].replace({'group A': 'Grupo A',
                                               'group B': 'Grupo B',
                                               'group C': 'Grupo C',
                                               'group D': 'Grupo D',
                                               'group E': 'Grupo E'})

df['educ_parental']=df['educ_parental'].replace({'high school': "Ensino Médio",
                                                 'some high school':'Ensino Médio Incompleto',
                                                 'some college':'Faculdade Incompleta',
                                                 "associate's degree":"Grau de Associado",
                                                 "bachelor's degree":"Bacharel",
                                                 "master's degree":"Mestrado"})

df['lanche']=df['lanche'].replace({'standard':'Sem Desconto',
                                   'free/reduced':'Com Desconto'})

df['curso_preparatorio']=df['curso_preparatorio'].replace({'completed':'Completo',
                                                           'none':'Nenhum'})


materias = {'notas_matematica':'Matemática', 'notas_leitura':'Leitura', 'notas_redacao':'Redação', 'media':'Todas'}

fatores = {'educ_parental':'Educação Parental', 'lanche':'Lanche', 'curso_preparatorio': "Curso Preparatório"}

df['media'] = df[['notas_matematica', 'notas_leitura', 'notas_redacao']].mean(axis=1)
################################################################################################
order_grupo_etnico = ["Grupo A", "Grupo B","Grupo C","Grupo D","Grupo E"]
order_educ_parental = ["Ensino Médio Incompleto", "Ensino Médio", "Faculdade Incompleta","Grau de Associado", "Bacharel","Mestrado"]
order_lanche = ["Sem Desconto", "Com Desconto"]
order_curso_preparatorio = ["Nenhum", "Completo"]
st.sidebar.header("Selecione os filtros")
################################################################################################
sexo_type = st.sidebar.selectbox(
    "Selecione o sexo:",
    options = ("Tudo", "Homem","Mulher")
)

etnic_group_type = st.sidebar.selectbox(
    "Selecione o grupo étnico:",
    options = ("Tudo", "Grupo A", "Grupo B","Grupo C","Grupo D","Grupo E")
)
################################################################################################
#df_selection_type2 when is both genders
if sexo_type == "Tudo":
    if etnic_group_type == "Tudo":
        df_selection_type = df
        df_selection_type2 = df
    else:
        df_selection_type = df.query(
        "grupo_etnico == @etnic_group_type")
        df_selection_type2 = df.query(
        "grupo_etnico == @etnic_group_type")
else:
    df_selection_type2 = df.query(
    "grupo_etnico == @etnic_group_type"
    )
    if etnic_group_type == "Tudo":
        df_selection_type = df.query(
        "sexo == @sexo_type"
        )
    else:
        df_selection_type = df.query(
        "grupo_etnico == @etnic_group_type & sexo == @sexo_type"   
        )
    
    

##########################################################


######## MATÉRIAS #########################################
materias_type = st.sidebar.selectbox(
    "Selecione a matéria:",
    options = ("Todas", "Matemática", "Leitura", "Redação")
)

materia = list(materias.keys())[list(materias.values()).index(materias_type)]
if materias_type == "Todas":
    df_corr = df_selection_type[["notas_matematica", "notas_leitura", "notas_redacao"]]
    materias_type = "média de todas as matérias"
else:
    df_corr = df_selection_type[[materia]]

######## TÍTULO ##########################################
st.title(":bar_chart: Performance de Estudantes em Exames")

########## PIES ###########################################

sex_pie = px.pie(df, values = df_selection_type['sexo'].value_counts().values, names = df_selection_type['sexo'].value_counts().index, width = 200, height = 200,
                     color_discrete_sequence=['#6e9bf4', '#f8748c'])

sex_pie.update_layout(margin = dict(l=1, r=1, t=1, b=1,pad=0), legend=dict(x=1))
#, title=dict(text="Sexo",x=0,y=0.95)

etnic_group_pie = px.pie(df, values = df_selection_type['grupo_etnico'].value_counts().values, names = df_selection_type['grupo_etnico'].value_counts().index, width = 200, height = 200,
color_discrete_sequence=['#bb83f4', '#fc8d62', '#66c2a5', '#e78ac3','#ffd92f'])

etnic_group_pie.update_layout(margin = dict(l=5, r=5, t=5, b=5,pad=0), legend=dict(x=1))
#, title=dict(text="Grupo",x=0,y=0.95)

########## COUNTERS #######################

total_students = int(df_selection_type.value_counts().sum())
media_mat = round(df_selection_type['notas_matematica'].mean(),2)
media_leitura = round(df_selection_type['notas_leitura'].mean(),2)
media_redacao = round(df_selection_type['notas_redacao'].mean(),2)

########## ROWS AND COLUMNS #######################

a1, a2, a3, a4 = st.columns((1/3, 2/9,2/9,2/9))

with a1:
    st.metric("Total de Estudantes", total_students)
    st.markdown("""---""")
with a2:
    st.metric("Média em Matemática", media_mat)
    st.markdown("""---""")
with a3:
    st.metric("Média em Leitura", media_leitura)
    st.markdown("""---""")
with a4:
    st.metric("Média em Redação", media_redacao)
    st.markdown("""---""")

#####################################################
b1, b2 = st.columns((1/3,2/3))

with b1:
    st.write("Sexo")
    st.plotly_chart(sex_pie, use_container_width=True) 
    st.write("Grupo Étnico")
    st.plotly_chart(etnic_group_pie, use_container_width=True)

####################################################
with b2:
    fator_type = st.selectbox('Selecione o fator', options=("Educação Parental", "Lanche", "Curso Preparatório"))

fator = list(fatores.keys())[list(fatores.values()).index(fator_type)]
df_corr["Fator"] = df_selection_type[[fator]]
st.markdown("""---""")
if fator_type == "Educação Parental":
    ordem = order_educ_parental
    palette = "husl"
    c1, c3, c2 = st.columns((3/8, 1/8, 4/8))
else:
    if fator_type == "Lanche":
        palette=['#ffd92f', '#a6d854']
    else:
        palette=['#e0dcdc', '#a6d854']
    c1, c3, c2 = st.columns((3.375/9, 1/9, 3.725/9))
    if fator_type == "Lanche":
        ordem = order_lanche
    else:
        ordem = order_curso_preparatorio

sns.barplot(data=df_selection_type, x=materia, y=fator,palette=palette,order= ordem)
plt.xlabel(f"Notas em {materias_type}")
plt.ylabel(fator_type)
plt.xlim(0,100)
figsize= ((2, 1.1))

with b2:
    st.pyplot(plt.gcf(), use_container_width=True)

########################################

if fator_type == "Educação Parental":
    options = order_educ_parental
elif fator_type == "Lanche":
    options = order_lanche
else:
    options = order_curso_preparatorio

options.insert(0,"Todos")
with c1:
    fator_especifico = st.selectbox('Selecione uma opção', options=options)
    plt.figure(figsize=(7,5))
    if fator_especifico != "Todos":
        query = str(f"{fator} == '{fator_especifico}'")
        df_selection_hist = df_selection_type.query(query)
        df_selection_hist2 = df_selection_type2.query(query)
    else:
        df_selection_hist = df_selection_type
        df_selection_hist2 = df_selection_type2
    #Precisar de um query pro histograma?
    if sexo_type == "Tudo":
        histogram = sns.histplot(x=df_selection_hist2[materia], hue=df_selection_hist2["sexo"], stat="probability",bins=[0,10,20,30,40,50,60,70,80,90,100],color = '#589cd4')
    else:
        histogram = sns.histplot(x=df_selection_hist[materia], stat="probability",bins=[0,10,20,30,40,50,60,70,80,90,100],color = '#589cd4')

    plt.ylabel("",rotation=0)
    plt.xlabel(materias_type.capitalize())
    st.write(f"Histograma de {materias_type}")
    st.pyplot(plt.gcf(), use_container_width=True)
    
########################################

exams_dummy = pd.get_dummies(df_corr)

if materias_type == "média de todas as matérias":
    exams_dummy['media'] = exams_dummy[['notas_matematica', 'notas_leitura', 'notas_redacao']].mean(axis=1)

for i in list(materias.keys()):
    exams_dummy[i] = df_selection_type[[i]].mean(axis=1)

corr = exams_dummy.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))

if fator_type == "Educação Parental":
    plt.figure(figsize=(1.5,2))
if fator_type == "Lanche":
    plt.figure(figsize=(1,1.6))
if fator_type == "Curso Preparatório":
    plt.figure(figsize=(1.1,1.2))

heatmap = sns.heatmap(corr[[materia]].sort_values(by=materia, ascending=False)[4:], 
                      vmin=-1, vmax=1, annot=True, annot_kws={"size": 10}, cmap="coolwarm")
with c2:
    st.write(f'Correlação de {fator_type.lower()} com {materias_type}')
    st.pyplot(plt.gcf())
########## SAMPLE ######################


########################################
