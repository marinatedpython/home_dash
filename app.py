import pandas as pd 
import pathlib
import datetime as dt 
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.express as px


# Get data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('data').resolve()


# Declare app
app = dash.Dash(__name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}])


# Load data with Pandas
df = pd.read_csv(DATA_PATH.joinpath('home.csv'))
df['inception_date'] = df['inception_date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
df['inception_year'] = df['inception_date'].dt.year
df['inception_month'] = df['inception_date'].dt.month
unique_years = sorted(list(df['inception_date'].dt.year.unique()))
months = list(df['inception_date'].dt.month.unique())
months_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
			   5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
			   9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}

year_options = [
	{'label': str(year), 'value': year} 
	for year in unique_years
]


# Create app layout
app.layout = html.Div(
	[
		html.Div(
			[
				html.Div(
					[
						html.Img(
							src=app.get_asset_url('house.jpg'),
							id='suburb-image',
						)
					],
					className='one-third column'
				),
				html.Div(
					[
						html.Div(
							[
								html.H3(
									'Consumer Home Insurance ',
									style={
										'margin-bottom': '0px'
									}
								),
								html.H5(
									'Portfolio Dashboard',
									style={
										'margin-top': '0px'
									}
								)
							]
						)
					],
					className='one-half column',
					id='title'
				),
				html.Div(
					[
						html.A(
							html.Button(
								'Latest Weather',
								id='weather-button'
							),
							href='http://www.bom.gov.au/'
						)
					],
					className='one-third column',
					id='button'
				)
			],
			id='header',
			className='row flex-display',
			style={
				'margin-bottom': '25px'
			}
		),
		html.Div(
			[
				html.Div(
					[
						html.P(
							'Select Aggregate Summary Year(s):',
							className='control_label'
						),
						dcc.Checklist(
							id='summary_years',
							options=year_options,
							className='dcc_control',
							value=[]
						),
						html.Br(),
						html.P(
							'Select Calendar Year(s) for Loss Ratio Comparison Graph:',
							className='control_label'
						),
						dcc.Dropdown(
							id='loss_ratio_years',
							options=year_options,
							multi=True,
							value=unique_years
						),
						html.P(
							'Select Month Range for Loss Ratio Comparison Graph:',
							className='control_label'
						),
						dcc.RangeSlider(
							id='loss_ratio_months',
							min=min(months),
							max=max(months),
							value=[min(months), min(months) + 11],
							marks=months_dict,
							className='dcc_control'
						),
						html.Br(),
						html.P(
							'Select Year(s) for Claims Severity Distribution Graph:',
							className='control_label'
						),
						dcc.Dropdown(
							id='severity_dist_years',
							options=year_options,
							multi=True,
							value=[unique_years[-1]]
						),
						html.Br(),
						html.P(
							'Select Years(s) for Sum Insured Distribution Graph:',
							className='control_label'
						),
						dcc.Dropdown(
							id='sum_insured_years',
							options=year_options,
							multi=True,
							value=[unique_years[-1]]
						)
					],
					className='pretty_container four columns',
					id='filter-options'
				),
				html.Div(
					[
						html.Div(
							[
								html.Div(
									[
										html.H6(
											id='premium_text'
										),
										html.P(
											'Aggregate Premium'
										)
									],
									id='premium',
									className='mini_container',
									style={
										'width': '194px',
										'text-align': 'center'
									}
								),
								html.Div(
									[
										html.H6(
											id='claim_text'
										),
										html.P(
											'Aggregate Claims'
										),
									],
									id='claims',
									className='mini_container',
									style={
										'width': '194px',
										'text-align': 'center'
									}
								),
								html.Div(
									[
										html.H6(
											id='sum_insured_text'
										),
										html.P(
											'Aggregate Sum Insured'
										)
									],
									id='sum_insured',
									className='mini_container',
									style={
										'width': '194px',
										'text-align': 'center'
									}
								)
							],
							id='info-container',
							className='row container-display'
						),
						html.Div(
							[
								dcc.Graph(
									id='loss_ratio_graph'
								)
							],
							id='loss_ratio_container',
							className='pretty_container'
						)
					],
					id='right-column',
					className='eight columns'
				)
			],
			className='row flex-display'
		),
		html.Div(
			[
				html.Div(
					[
						dcc.Graph(
							id='severity_graph'
						)
					],
					className='pretty_container twelve columns'
				),
				html.Div(
					[
						dcc.Graph(
							id='sum_insured_graph'
						)
					],
					className='pretty_container twelve columns'
				)
			],
			#className='row flex-display'
		)
	],
	id='mainContainer',
	style={
		'display': 'flex',
		'flex-direction': 'column'
	}
)


# Create callbacks

@app.callback(
	Output('premium_text', 'children'),
	[
		Input('summary_years', 'value')
	]
)
def update_premium_text(summary_years):
	result = round(df[df['inception_year'].isin(summary_years)]['written_premium'].sum(), 2)
	return f'{result:,}'

@app.callback(
	Output('claim_text', 'children'),
	[
		Input('summary_years', 'value')
	]
)
def update_claims_text(summary_years):
	result = round(df[df['inception_year'].isin(summary_years)]['claim_incurred'].sum(), 2)
	return f'{result:,}'


@app.callback(
	Output('sum_insured_text', 'children'),
	[
		Input('summary_years', 'value')
	]
)
def update_sum_insured_text(summary_years):
	result = int(df[df['inception_year'].isin(summary_years)]['sum_insured'].sum())
	return f'{result:,}'


@app.callback(
	Output('loss_ratio_graph', 'figure'),
	[
		Input('loss_ratio_years', 'value'),
		Input('loss_ratio_months', 'value')
	]
)
def make_loss_ratio_graph(loss_ratio_years, loss_ratio_months):
	loss_ratio_months = [i for i in range(loss_ratio_months[0], loss_ratio_months[-1])] 
	dff = df[df['inception_year'].isin(loss_ratio_years) &
			 df['inception_month'].isin(loss_ratio_months)
	]
	loss_ratios = [(dff[dff['inception_year'] == i]['claim_incurred'].sum() / dff[dff['inception_year'] == i]['written_premium'].sum()) for i in loss_ratio_years]
	fig = px.bar(x=loss_ratio_years, y=loss_ratios)
	fig.update_layout(
		xaxis=dict(
			tickmode='array',
			tickvals=unique_years,
		),
		title_text='Loss Ratio Graph',
		xaxis_title_text='Year',
		yaxis_title_text='Loss Ratio'
	)
	return fig


@app.callback(
	Output('severity_graph', 'figure'),
	[
		Input('severity_dist_years', 'value')
	]
)
def make_severity_dist(severity_dist_years):
	dff = df[df['inception_year'].isin(severity_dist_years)]
	dff = dff[dff['claim_incurred'] > 0]
	fig = px.histogram(dff, x='claim_incurred', marginal='violin', nbins=10000)
	fig.update_layout(
		title_text='Incurred Claims Distribution',
		xaxis_title_text='Claim Amount',
		yaxis_title_text='Count'
	)
	return fig 


@app.callback(
	Output('sum_insured_graph', 'figure'),
	[
		Input('sum_insured_years', 'value')
	]
)
def make_sum_insured_graph(sum_insured_years):
	dff = df[df['inception_year'].isin(sum_insured_years)]
	fig = px.histogram(dff, x='sum_insured', marginal='violin', nbins=10000)
	fig.update_layout(
		title_text='Sum Insured Distribution',
		xaxis_title_text='Sum Insured',
		yaxis_title_text='Count'
	)
	return fig





if __name__ == '__main__':
	app.run_server(debug=True)
