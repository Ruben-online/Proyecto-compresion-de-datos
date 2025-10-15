from PIL import Image

# Comprimir una cadena de pixeles
def compress_rle(data: str) -> str:
    if not data:
        return ""
    result = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i-1]:
            count += 1
        else:
            result.append(data[i-1] + str(count))
            count = 1
    result.append(data[-1] + str(count))
    return " ".join(result)

# Descomprimir cadena RLE
def decompress_rle(data: str) -> str:
    if not data:
        return ""
    result = []
    for token in data.split():
        ch, num = token[0], int(token[1:])
        result.append(ch * num)
    return "".join(result)

# Funciones auxiliares para imagenes

# Convertir imagen a cadena de caracteres (0/1) segun pixeles
def image_to_string(img_path, threshold=128):
    img = Image.open(img_path).convert("L")  # convertir a escala de grises
    width, height = img.size
    pixels = list(img.getdata())
    bits = ''.join('1' if px > threshold else '0' for px in pixels)
    return bits, width, height

# Reconstruir imagen desde cadena binaria
def string_to_image(bit_string, width, height, output_path):
    img = Image.new('L', (width, height))
    pixels = [255 if b == '1' else 0 for b in bit_string]
    img.putdata(pixels)
    img.save(output_path)
