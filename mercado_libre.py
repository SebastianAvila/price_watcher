import requests  # Línea 1: Importa la biblioteca 'requests' para hacer solicitudes HTTP a páginas web.
from bs4 import (
    BeautifulSoup,
)  # Línea 2: Importa 'BeautifulSoup' de la biblioteca 'bs4' para analizar y extraer datos del HTML.

BASE_URL = "https://listado.mercadolibre.com.mx/"  # Línea 4: Define la URL base de Mercado Libre México para construir la URL de búsqueda.

HEADERS = {  # Línea 6-12: Define un diccionario con encabezados HTTP para simular una solicitud de un navegador web real, evitando bloqueos.
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "es-MX,es;q=0.9",
}


def buscar_precios(
    query: str,
) -> list[
    float
]:  # Línea 14: Define la función 'buscar_precios' que toma una consulta (query) como cadena y devuelve una lista de precios flotantes.
    url = BASE_URL + query.replace(
        " ", "-"
    )  # Línea 15: Construye la URL completa reemplazando espacios en la consulta por guiones.
    print(
        "URL generada:", url
    )  # Línea 16: Imprime la URL generada para depuración, permitiendo verificar si la consulta se formó correctamente.
    response = requests.get(
        url, headers=HEADERS, timeout=15
    )  # Línea 17: Hace una solicitud GET a la URL con los encabezados definidos y un tiempo de espera de 15 segundos.

    if (
        response.status_code != 200
    ):  # Línea 19: Verifica si la respuesta HTTP no es exitosa (código 200 significa OK).
        print(
            "⚠️ Error Mercado Libre:", response.status_code
        )  # Línea 20: Imprime un mensaje de error con el código de estado.
        print(
            "Contenido HTML:", response.text
        )  # Línea 21: Imprime el contenido HTML de la respuesta para depuración en caso de error.
        return []  # Línea 22: Retorna una lista vacía si hay un error.

    soup = BeautifulSoup(
        response.text, "lxml"
    )  # Línea 24: Crea un objeto BeautifulSoup para analizar el HTML de la respuesta usando el parser 'lxml'.

    precios = (
        []
    )  # Línea 26: Inicializa una lista vacía para almacenar los precios extraídos.

    for price in soup.select(
        "span.andes-money-amount"
    ):  # Línea 28: Itera sobre todos los elementos HTML que coinciden con el selector CSS 'span.andes-money-amount' (donde se muestran los precios en Mercado Libre).
        fraction = price.select_one(
            "span.andes-money-amount__fraction"
        )  # Línea 29: Selecciona el elemento hijo que contiene la parte principal del precio (sin centavos).
        cents = price.select_one(
            "span.andes-money-amount__cents"
        )  # Línea 30: Selecciona el elemento hijo que contiene los centavos (si existen).

        if (
            not fraction
        ):  # Línea 32: Si no se encuentra el elemento 'fraction', salta a la siguiente iteración (evita errores).
            continue  # Línea 33: Continúa con el siguiente precio.

        # Imprimir precios capturados antes del filtrado  # Línea 35: Comentario explicativo.
        try:  # Línea 36: Intenta convertir el texto del precio a un número flotante.
            valor = fraction.text.replace(
                ",", ""
            ).replace(
                ".", ""
            )  # Línea 37: Obtiene el texto de 'fraction' y elimina comas y puntos (separadores de miles).
            if cents:  # Línea 38: Si hay centavos, los agrega al valor.
                valor += (
                    "." + cents.text
                )  # Línea 39: Concatena los centavos con un punto decimal.
            print(
                "Precio capturado:", valor
            )  # Línea 40: Imprime el precio capturado antes de filtros para depuración.
            valor_float = float(valor)  # Línea 41: Convierte el valor a flotante.
            precios.append(valor_float)  # Línea 42: Agrega el precio a la lista.
        except (
            ValueError
        ):  # Línea 43: Si hay un error al convertir (ej. texto no numérico), salta a la siguiente iteración.
            continue  # Línea 44: Continúa con el siguiente precio.

    # Filtrar precios menores a 3000  # Línea 46: Comentario explicativo.
    precios = [
        p for p in precios if int(p) > 3000
    ]  # Línea 47: Filtra la lista para incluir solo precios mayores a 3000.

    for p in precios:
        print("Precio mayor a 3000:", p)

    # Excluir precios con palabras clave  # Línea 49: Comentario explicativo.
    precios = [
        p
        for p in precios
        if not any(
            keyword in str(p)
            for keyword in ["meses sin intereses", "fundas", "accesorios"]
        )
    ]  # Línea 50: Filtra la lista para excluir precios que contengan palabras clave no deseadas (convierte el precio a cadena para buscar).

    for p in precios:  # Línea 51: Itera sobre los precios filtrados.
        print(
            "Precio válido:", p
        )  # Línea 52: Imprime cada precio válido después del filtrado.

    return precios  # Línea 52: Retorna la lista de precios filtrados.
