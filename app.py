from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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
    comparar = request.args.get('comparar')  # País opcional para comparación
    criterio = request.args.get('criterio')

    if not pais or criterio not in INDICADORES:
        return jsonify({"error": "Faltan parámetros"}), 400

    pais_codigo = PAISES_CODIGOS.get(pais)
    if not pais_codigo:
        return jsonify({"error": "País no válido"}), 400

    # URL para la API del Banco Mundial
    indicador_codigo = INDICADORES[criterio]
    url = f"https://api.worldbank.org/v2/country/{pais_codigo}/indicator/{indicador_codigo}?format=json"

    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": "No se pudieron obtener datos"}), 500

    data = response.json()
    
    # Extraer el valor más reciente disponible
    if len(data) > 1 and "value" in data[1][0]:
        resultado = data[1][0]["value"]
    else:
        resultado = "Datos no disponibles"

    resultado_comparar = None
    if comparar:
        pais_codigo_comparar = PAISES_CODIGOS.get(comparar)
        if not pais_codigo_comparar or pais_codigo_comparar == pais_codigo:
            return jsonify({"error": "País inválido para comparar"}), 400
        
        url_comparar = f"https://api.worldbank.org/v2/country/{pais_codigo_comparar}/indicator/{indicador_codigo}?format=json"
        response_comparar = requests.get(url_comparar)
        data_comparar = response_comparar.json()
        
        if len(data_comparar) > 1 and "value" in data_comparar[1][0]:
            resultado_comparar = data_comparar[1][0]["value"]
        else:
            resultado_comparar = "Datos no disponibles"

    return jsonify({
        "pais": pais,
        "criterio": criterio,
        "valor": resultado,
        "comparar": comparar if comparar else None,
        "valor_comparar": resultado_comparar if comparar else None
    })

if __name__ == '__main__':
    app.run(debug=True)
