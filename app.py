from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilita CORS para evitar bloqueos

# Códigos de países
PAISES_CODIGOS = {
    "Colombia": "COL",
    "Estados Unidos": "USA",
    "Venezuela": "VEN",
    "México": "MEX",
    "Perú": "PER",
    "Brasil": "BRA",
    "España": "ESP",
    "Puerto Rico": "PRI",
    "República Dominicana": "DOM",
    "Filipinas": "PHL",
    "Arabia Saudita": "SAU"
}

# Indicadores con descripción
INDICADORES = {
    "Accesibilidad y Cobertura del Sistema de Salud": {
        "codigo": "SH.UHC.SRVS.CV.XD",
        "descripcion": "Mide el acceso a servicios esenciales de salud y cobertura universal."
    },
    "Financiamiento y Gasto en Salud": {
        "codigo": "SH.XPD.CHEX.GD.ZS",
        "descripcion": "Porcentaje del PIB que se gasta en salud en cada país."
    }
}

@app.route('/get_data', methods=['GET'])
def get_data():
    pais = request.args.get('pais')
    comparar = request.args.get('comparar')
    criterio = request.args.get('criterio')

    if not pais or not criterio:
        return jsonify({"error": "Faltan parámetros"}), 400

    pais_codigo = PAISES_CODIGOS.get(pais)
    indicador_info = INDICADORES.get(criterio)

    if not pais_codigo or not indicador_info:
        return jsonify({"error": "País o criterio no válido"}), 400

    indicador_codigo = indicador_info["codigo"]
    descripcion = indicador_info["descripcion"]
    fuente = "Banco Mundial"
    fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    url = f"https://api.worldbank.org/v2/country/{pais_codigo}/indicator/{indicador_codigo}?format=json"

    response = requests.get(url)
    data = response.json()

    resultado = "Datos no disponibles"
    if len(data) > 1 and isinstance(data[1], list):
        for item in data[1]:
            if item.get("value") is not None:
                resultado = item["value"]
                break

    resultado_comparar = "Datos no disponibles"
    if comparar:
        pais_codigo_comparar = PAISES_CODIGOS.get(comparar)
        if pais_codigo_comparar and pais_codigo_comparar != pais_codigo:
            url_comparar = f"https://api.worldbank.org/v2/country/{pais_codigo_comparar}/indicator/{indicador_codigo}?format=json"
            response_comparar = requests.get(url_comparar)
            data_comparar = response_comparar.json()

            if len(data_comparar) > 1 and isinstance(data_comparar[1], list):
                for item in data_comparar[1]:
                    if item.get("value") is not None:
                        resultado_comparar = item["value"]
                        break

    return jsonify({
        "pais": pais,
        "criterio": criterio,
        "descripcion": descripcion,
        "valor": resultado,
        "fuente": fuente,
        "fecha": fecha_consulta,
        "comparar": comparar if comparar else None,
        "valor_comparar": resultado_comparar if comparar else None
    })

if __name__ == '__main__':
    app.run(debug=True)






