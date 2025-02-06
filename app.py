from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Habilita CORS para evitar bloqueos de GitHub Pages

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

# Diccionario con indicadores de salud y sus explicaciones
INDICADORES = {
    "Accesibilidad y Cobertura del Sistema de Salud": {
        "codigo": "SH.UHC.SRVS.CV.XD",
        "explicacion": "Porcentaje de la población con acceso a servicios esenciales de salud."
    },
    "Financiamiento y Gasto en Salud": {
        "codigo": "SH.XPD.CHEX.GD.ZS",
        "explicacion": "Porcentaje del PIB destinado al gasto en salud."
    },
    "Calidad de la Atención Médica": {
        "codigo": "SH.STA.BRTC.ZS",
        "explicacion": "Tasa de mortalidad materna por cada 100,000 nacimientos."
    },
    "Resultados en Salud": {
        "codigo": "SP.DYN.LE00.IN",
        "explicacion": "Esperanza de vida al nacer en años."
    },
    "Sostenibilidad y Eficiencia del Sistema": {
        "codigo": "SH.MED.BEDS.ZS",
        "explicacion": "Número de camas hospitalarias por cada 1,000 habitantes."
    },
    "Innovación y Desarrollo Tecnológico": {
        "codigo": "IT.NET.USER.ZS",
        "explicacion": "Porcentaje de la población con acceso a Internet."
    },
    "Regulación y Gobernanza del Sistema": {
        "codigo": "SH.ANM.ALL.ZS",
        "explicacion": "Cobertura de vacunación en niños menores de un año."
    }
}

@app.route('/get_data', methods=['GET'])
def get_data():
    pais = request.args.get('pais')
    comparar = request.args.get('comparar')  # País opcional para comparación
    criterio = request.args.get('criterio')

    if not pais or not criterio:
        return jsonify({"error": "Faltan parámetros"}), 400

    pais_codigo = PAISES_CODIGOS.get(pais)
    indicador = INDICADORES.get(criterio)

    if not pais_codigo or not indicador:
        return jsonify({"error": "País o criterio no válido"}), 400

    url = f"https://api.worldbank.org/v2/country/{pais_codigo}/indicator/{indicador['codigo']}?format=json"

    response = requests.get(url)
    data = response.json()

    resultado = "Datos no disponibles"
    fecha = "N/A"

    if len(data) > 1 and isinstance(data[1], list) and len(data[1]) > 0:
        ultimo_dato = next((x for x in data[1] if x.get("value") is not None), None)
        if ultimo_dato:
            resultado = ultimo_dato["value"]
            fecha = ultimo_dato["date"]

    resultado_comparar = None
    fecha_comparar = "N/A"

    if comparar:
        pais_codigo_comparar = PAISES_CODIGOS.get(comparar)
        if not pais_codigo_comparar or pais_codigo_comparar == pais_codigo:
            return jsonify({"error": "País inválido para comparar"}), 400

        url_comparar = f"https://api.worldbank.org/v2/country/{pais_codigo_comparar}/indicator/{indicador['codigo']}?format=json"
        response_comparar = requests.get(url_comparar)
        data_comparar = response_comparar.json()

        if len(data_comparar) > 1 and isinstance(data_comparar[1], list) and len(data_comparar[1]) > 0:
            ultimo_dato_comparar = next((x for x in data_comparar[1] if x.get("value") is not None), None)
            if ultimo_dato_comparar:
                resultado_comparar = ultimo_dato_comparar["value"]
                fecha_comparar = ultimo_dato_comparar["date"]

    return jsonify({
        "pais": pais,
        "criterio": criterio,
        "valor": resultado,
        "fecha": fecha,
        "explicacion": indicador["explicacion"],
        "fuente": "Banco Mundial",
        "comparar": comparar if comparar else None,
        "valor_comparar": resultado_comparar if comparar else None,
        "fecha_comparar": fecha_comparar if comparar else None
    })

if __name__ == '__main__':
    app.run(debug=True)





