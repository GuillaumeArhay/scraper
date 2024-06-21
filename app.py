import dash
from dash import html, dcc, Input, Output, State
import trafilatura
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Nécessaire pour Gunicorn

app.layout = dbc.Container([
    html.H1("Scraper d'URL avec Trafilatura", className="my-4 text-center"),
    dbc.Card([
        dbc.CardBody([
            dbc.Input(
                id='url-input',
                type='text',
                placeholder='Entrez une URL à scraper',
                className="mb-3"
            ),
            dbc.Button('Scraper', id='scrape-button', color="primary", className="mb-3 w-100"),
            dbc.Spinner(
                dbc.Card(
                    dbc.CardBody(
                        html.Div(id='output-content', style={'whiteSpace': 'pre-wrap'})
                    ),
                    className="mt-3"
                ),
                            ),
        ])
    ])
], fluid=True, className="p-5")

@app.callback(
    Output('output-content', 'children'),
    Input('scrape-button', 'n_clicks'),
    State('url-input', 'value'),
    prevent_initial_call=True)
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
