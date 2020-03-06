import pandas as pd 
import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.express as px
import plotly.graph_objects as go

# Bases de données
avantageSample = pd.read_csv('avantageSample.csv', sep=',')
remunerationSample = pd.read_csv('remunerationSample.csv', sep=',')
entreprise = pd.read_csv('entrepriseClean.csv', sep=',', na_filter=False)
conventionSample = pd.read_csv('conventionSample.csv', sep=',')

avantageSample['avant_nature'] = avantageSample['avant_nature'].str.upper()
dic = {'É':'E', 'Ê':'E', '[':'', 
       ']':'', ': ':'', 'HÃ‰BERGEMENT':'HEBERGEMENT', 
       'DEJEUNER (REPAS)':'REPAS', 'DEJEUNER':'REPAS', 'DÎNER':'REPAS',
       '(':'', 'AUTRE:REPAS':'REPAS', 'AUTRE REPAS':'REPAS',
        ')':'', 'REPAS REPAS':'REPAS'}
for key, value in dic.items():
    avantageSample['avant_nature'] = avantageSample['avant_nature'].str.replace(key, value)

# Nouvelles bases de données
df2=pd.DataFrame(avantageSample.groupby("avant_nature").size())
df2.columns=['presentage de avantage nature']
df2=df2.sort_values('presentage de avantage nature',ascending=False).head(50)
df2['nature des avantages']= df2['presentage de avantage nature']/df2['presentage de avantage nature'].sum()



df3=pd.DataFrame(entreprise.groupby("secteur")["denomination_sociale"].count())
df4=pd.DataFrame(remunerationSample.groupby("categorie")["benef_identifiant_valeur"].count())
avantage_recu_benef=pd.DataFrame(avantageSample.groupby("categorie")["avant_montant_ttc"].sum())
remuneration_recu_benef=pd.DataFrame(remunerationSample.groupby("categorie")["remu_montant_ttc"].sum())
remuneration_recu_benef['avant_montant_ttc']=avantage_recu_benef['avant_montant_ttc']

group_data5=pd.DataFrame(conventionSample.groupby(['denomination_sociale'])['conv_objet'].count())
group_data5=group_data5.sort_values(['conv_objet'],ascending=False).head(25)
avantage_recu_benef=pd.DataFrame(avantageSample.groupby("categorie")["avant_montant_ttc"].sum())
avantage_recu_benef = avantage_recu_benef.sort_values(['avant_montant_ttc'],ascending=False)

# Figures :

# Figure 2:
fig1= px.bar(df2, x=df2.index, y='nature des avantages',height=600)
#fig1.update_layout(title_text='Répartition de la nature des avantages', yaxis=dict( tickformat= ',.0%',range=[0,1]),margin=dict(l=20, r=20, t=20, b=20),layout = go.Layout(title='XYZ',
#xaxis={'tickfont': {'family': 'PT Sans Narrpw','size': 12}}))
fig1.update_layout( yaxis=dict( tickformat= ',.0%',range=[0,1]),)

# Figure 3:
fig2 = go.Figure(data=[
    go.Bar(name='remu_montant_ttc', x=remuneration_recu_benef.index, y=remuneration_recu_benef['remu_montant_ttc']),
    go.Bar(name='avant_montant_ttc', x=remuneration_recu_benef.index, y=remuneration_recu_benef['avant_montant_ttc'])
])
fig2.update_layout(barmode='group')

# Figure 5:
fig3 = px.pie(df3, values='denomination_sociale', names=df3.index)

# Figure 6:
fig4 = px.pie(df4, values='benef_identifiant_valeur', names=df4.index)

# Figure 4:
fig5 = px.bar(group_data5, x=group_data5.index, y='conv_objet')

#fig5.update_layout(title_text='Les 25 entreprises qui concluent le plus de conventions',)

# Figure 1:
fig6 = px.bar(avantage_recu_benef, x=avantage_recu_benef.index, y='avant_montant_ttc')
#fig6.update_layout(title_text='Rémunération reçue par catégorie de bénéficiaire',)

# Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div(children=[
    html.H1(children='Rémunération reçue par catégorie de bénéficiaire'),
        dcc.Graph(
            id='fig6',
            figure=fig6)
    ],style={'marginBottom': '5em'}),
	
    html.Div(children=[
        html.H1(children='Répartition de la nature des avantages'),
        dcc.Graph(
            id='fig1',
            figure=fig1
        )
    ],style={'marginBottom': '5em'}),
    html.Div(children=[
        html.H1(children='Rémunération perçue en fonction de la catégorie du bénéficiaire'),
        dcc.Graph(
            id='fig2',
            figure=fig2
        )
    ],style={'marginBottom': '5em'}),
    html.Div(children=[
        html.H1(children='Les 25 entreprises qui concluent le plus de conventions'),
        dcc.Graph(
            id='fig5',
            figure=fig5
        )
    ],style={'marginBottom': '5em'}),
    html.Div(children=[
        html.H1(children='Répartition des entreprises par secteur'),
        dcc.Graph(
            id='fig3',
            figure=fig3
        )
    ],style={'marginBottom': '5em'}),
    html.Div(children=[
        html.H1(children='Répartition des bénéficiaires par catégorie'),
        dcc.Graph(
            id='fig4',
            figure=fig4
        )
    ],style={'marginBottom': '5em'})
])


if __name__ == '__main__':
    app.run_server(debug=True)
