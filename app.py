from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Habilitar CORS para evitar bloqueos de GitHub Pages

# Diccionario con códigos de los países según la API del Banco Mundial
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

# Diccionario con indicadores de salud (Código de la API del Banco Mundial)
INDICADORES = {
    "Accesibilidad y Cobertura del Sistema de Salud": "SH.UHC.SRVS.CV.XD",
    "Financiamiento y Gasto en Salud": "SH.XPD.CHEX.GD.ZS",
    "Calidad de la Atención Médica": "SH.STA.BRTC.ZS",
    "Resultados en Salud": "SP.DYN.LE00.IN",
    "Sostenibilidad y Eficiencia del Sistema": "SH.MED.BEDS.ZS",
    "Innovación y Desarrollo Tecnológico": "IT.NET.USER.ZS",
    "Regulación y Gobernanza del Sistema": "SH.ANM.ALL.ZS"
}

@app.route('/get_data', methods=['GET'])
def get_data():
    pais = request.args.get('pais')
    criterio = request.args.get('criterio')

    if not pais or not criterio:
        return jsonify({"error": "Faltan parámetros"}), 400

    pais_codigo = PAISES_CODIGOS.get(pais)
    indicador_codigo = INDICADORES.get(criterio)

    if not pais_codigo or not indicador_codigo:
        return jsonify({"error": "País o criterio no válido"}), 400

    url = f"https://api.worldbank.org/v2/country/{pais_codigo}/indicator/{indicador_codigo}?format=json"

    response = requests.get(url)
    data = response.json()

    # Verificar si hay datos disponibles y filtrar valores no nulos
    if len(data) > 1 and isinstance(data[1], list) and len(data[1]) > 0:
        ultimo_dato = next((x for x in data[1] if x.get("value") is not None), None)
        resultado = ultimo_dato["value"] if ultimo_dato else "Datos no disponibles"
    else:
        resultado = "Datos no disponibles"

    return jsonify({
        "pais": pais,
        "criterio": criterio,
        "valor": resultado
    })

if __name__ == '__main__':
    app.run(debug=True)



