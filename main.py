from mercado_libre import buscar_precios


if __name__ == "__main__":
    producto = "motorola edge 60 pro 256gb"
    precios = buscar_precios(producto)

    # print("Producto buscado:", producto)
    # print("Total precios válidos:", len(precios))
    # if precios:
    #     print("Precios encontrados:", precios)
    #     print("Precio más bajo:", min(precios))
    #     print("Precio más alto:", max(precios))
    # else:
    #     print("No se encontraron precios válidos.")
