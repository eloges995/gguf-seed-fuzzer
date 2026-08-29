import struct

def build_gguf_bytes():
    """Construit les octets du mini fichier GGUF, sans toucher au disque."""
    data = b''
    data += b'GGUF'                      # magic
    data += struct.pack('<I', 3)         # version
    data += struct.pack('<Q', 0)         # n_tensors = 0
    data += struct.pack('<Q', 1)         # n_kv = 1
    key = b'general.architecture'
    data += struct.pack('<Q', len(key))
    data += key
    data += struct.pack('<I', 8)         # type STRING
    val = b'llama'
    data += struct.pack('<Q', len(val))
    data += val
    return data

def write_seed(path='mini_seed.gguf'):
    """Écrit le seed sur disque."""
    with open(path, 'wb') as f:
        f.write(build_gguf_bytes())
    print(f'Mini seed créé : {path}')

def parse_gguf_header(data):
    """Parse l'en-tête d'un fichier GGUF. Lève ValueError si invalide."""
    if len(data) < 4:
        raise ValueError("Fichier trop court pour contenir un magic number")

    magic = data[:4]
    if magic != b'GGUF':
        raise ValueError(f"Magic number invalide : {magic!r}, attendu b'GGUF'")

    if len(data) < 24:
        raise ValueError("Fichier trop court pour contenir l'en-tête complet")

    version = struct.unpack('<I', data[4:8])[0]
    n_tensors = struct.unpack('<Q', data[8:16])[0]
    n_kv = struct.unpack('<Q', data[16:24])[0]

    return {'version': version, 'n_tensors': n_tensors, 'n_kv': n_kv}

if __name__ == '__main__':
    write_seed()
