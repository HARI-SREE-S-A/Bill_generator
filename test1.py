import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64


# Define external CSS stylesheet
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define inline CSS styles
label_style = {'margin-top': '10px'}
button_style = {'margin-top': '20px'}

app.layout = html.Div([
    html.H1("Donation Receipt Generator", className="display-4 text-center mt-5"),
    html.Div([
        html.Label("Name:", style=label_style),
        dcc.Input(id='name', type='text', className="form-control"),
        html.Label("Mobile Number:", style=label_style),
        dcc.Input(id='mobile_number', type='text', className="form-control"),
        html.Label("Email:", style=label_style),
        dcc.Input(id='email', type='text', className="form-control"),
        html.Label("PAN Card:", style=label_style),
        dcc.Input(id='pan_card', type='text', className="form-control"),
        html.Label("Address:", style=label_style),
        dcc.Input(id='address', type='text', className="form-control"),
        html.Label("Amount:", style=label_style),
        dcc.Input(id='amount', type='number', className="form-control"),
        html.Label("Method of Payment:", style=label_style),
        dcc.Dropdown(
            id='payment_method',
            options=[
                {'label': 'Cash', 'value': 'Cash'},
                {'label': 'Credit Card', 'value': 'Credit Card'},
                {'label': 'Debit Card', 'value': 'Debit Card'},
                {'label': 'Net Banking', 'value': 'Net Banking'}
            ],
            className="form-control"
        ),
        html.Button('Submit', id='submit-val', n_clicks=0, className="btn btn-primary", style=button_style),
        html.Div(id='container-button-basic', className="mt-3"),
        html.A(html.Button('Download Receipt', id='download-receipt', className="btn btn-success"), id="download-link", href="", target="_blank", download="receipt.pdf")
    ], className="container")
])


@app.callback(
    Output('container-button-basic', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('name', 'value'),
     State('mobile_number', 'value'),
     State('email', 'value'),
     State('pan_card', 'value'),
     State('address', 'value'),
     State('amount', 'value'),
     State('payment_method', 'value')]
)
def update_output(n_clicks, name, mobile_number, email, pan_card, address, amount, payment_method):
    if n_clicks > 0:
        data = {
            'Name': name,
            'Mobile Number': mobile_number,
            'Email': email,
            'PAN Card': pan_card,
            'Address': address,
            'Amount': amount,
            'Method of Payment': payment_method,
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.DataFrame([data])
        df.to_excel('donations.xlsx', index=False)

        return html.Div([
            html.H4('Data Submitted Successfully!', className="text-success")
        ])


@app.callback(
    Output('download-link', 'href'),
    [Input('submit-val', 'n_clicks')],
    [State('name', 'value'),
     State('mobile_number', 'value'),
     State('email', 'value'),
     State('pan_card', 'value'),
     State('address', 'value'),
     State('amount', 'value'),
     State('payment_method', 'value')]
)
def generate_and_return_pdf(n_clicks, name, mobile_number, email, pan_card, address, amount, payment_method):
    if n_clicks > 0:
        pdf_content = generate_pdf(name, mobile_number, email, pan_card, address, amount, payment_method)
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
        return f'data:application/pdf;base64,{pdf_base64}'
    else:
        return ''


def generate_pdf(name, mobile_number, email, pan_card, address, amount, payment_method):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Donation Receipt", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Mobile Number: {mobile_number}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.cell(200, 10, txt=f"PAN Card: {pan_card}", ln=True)
    pdf.cell(200, 10, txt=f"Address: {address}", ln=True)
    pdf.cell(200, 10, txt=f"Amount: {amount}", ln=True)
    pdf.cell(200, 10, txt=f"Method of Payment: {payment_method}", ln=True)

    pdf_path = "receipt.pdf"
    pdf.output(pdf_path)
    with open(pdf_path, 'rb') as f:
        return f.read()


if __name__ == '__main__':
    app.run_server(debug=True)

