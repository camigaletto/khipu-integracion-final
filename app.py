from flask import Flask, redirect, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("KHIPU_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pagar")
def pagar():
    url = "https://payment-api.khipu.com/v3/payments"

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "amount": 5000,
        "currency": "CLP",
        "subject": "Cobro de Prueba",
        "transaction_id": "pedido001",
        "return_url": "http://localhost:5000/success",
        "cancel_url": "http://localhost:5000/cancel"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        return f"<h3>Error al crear el pago:</h3><pre>{response.status_code}<br>{response.text}</pre>"

    payment_url = response.json()["payment_url"]
    return redirect(payment_url)

@app.route("/success")
def success():
    return "<h1>¡Pago exitoso!</h1>"

@app.route("/cancel")
def cancel():
    return "<h1>Pago cancelado</h1>"

if __name__ == "__main__":
    app.run(debug=True)
