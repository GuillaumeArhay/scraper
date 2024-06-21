import dash
from dash import html, dcc, Input, Output, State
import trafilatura

app = dash.Dash(__name__)
server = app.server  # Nécessaire pour Gunicorn

app.layout = html.Div([
    html.H1("Scraper d'URL avec Trafilatura"),
    dcc.Input(
        id='url-input',
        type='text',
        placeholder='Entrez une URL à scraper',
        style={'width': '100%', 'margin-bottom': '10px'}
    ),
    html.Button('Scraper', id='scrape-button', n_clicks=0),
    html.Div(id='output-content', style={'whiteSpace': 'pre-wrap', 'marginTop': '20px'})
])

@app.callback(
    Output('output-content', 'children'),
    Input('scrape-button', 'n_clicks'),
    State('url-input', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, url):
    if url:
        try:
            downloaded = trafilatura.fetch_url(url)
            content = trafilatura.extract(downloaded)
            return content if content else "Aucun contenu extrait."
        except Exception as e:
            return f"Erreur lors du scraping : {str(e)}"
    return "Veuillez entrer une URL valide."

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000)