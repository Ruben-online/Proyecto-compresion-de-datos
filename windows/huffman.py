def encode(text):
    if not text:
        return "", {}

    # Contar las frecuencias de los caracteres
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1

    # Crear los nodos iniciales (como tuplas)
    nodes = [(ch, f, None, None) for ch, f in freq.items()]

    #Caso especial: si hay un solo caracter, se asigna codigo "0"
    if len(nodes) == 1:
        only_char = nodes[0][0]
        codes = {only_char: "0"}
        return "".join(codes[c] for c in text), codes

    # Construir el arbol de Huffman
    def key_fn(n):
        label = n[0] if n[0] is not None else "{"
        return (n[1], 0 if n[0] is not None else 1, label)

    while len(nodes) > 1:
        nodes.sort(key=key_fn)
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = (None, left[1] + right[1], left, right)
        nodes.append(parent)

    root = nodes[0]

    # Generar los codigos Huffman
    codes = {}

    def traverse(node, prefix):
        ch, _, L, R = node
        if ch is not None:
            codes[ch] = prefix or "0"
            return
        traverse(L, prefix + "0")
        traverse(R, prefix + "1")

    traverse(root, "")

    # Codificar el texto en bits
    bit_string = "".join(codes[c] for c in text)
    return bit_string, codes


def decode(bits, codes):
    # Invertir la tabla de codigos para decodificar
    reverse = {v: k for k, v in codes.items()}
    output, buffer = [], ""
    for b in bits:
        buffer += b
        if buffer in reverse:
            output.append(reverse[buffer])
            buffer = ""
    # Unir los caracteres decodificados
    return "".join(output)
