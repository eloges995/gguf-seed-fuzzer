import struct
import pytest
from create_mini_seed import build_gguf_bytes, write_seed, parse_gguf_header

def test_magic_number():
    """Les 4 premiers octets doivent être le magic GGUF."""
    data = build_gguf_bytes()
    assert data[:4] == b'GGUF'

def test_version_is_3():
    """La version doit être 3, encodée en uint32 little-endian."""
    data = build_gguf_bytes()
    version = struct.unpack('<I', data[4:8])[0]
    assert version == 3

def test_n_tensors_is_zero():
    """n_tensors doit être 0 (uint64 little-endian)."""
    data = build_gguf_bytes()
    n_tensors = struct.unpack('<Q', data[8:16])[0]
    assert n_tensors == 0

def test_n_kv_is_one():
    """n_kv doit être 1."""
    data = build_gguf_bytes()
    n_kv = struct.unpack('<Q', data[16:24])[0]
    assert n_kv == 1

def test_key_content():
    """La clé KV doit être 'general.architecture' avec sa longueur correcte."""
    data = build_gguf_bytes()
    key_len = struct.unpack('<Q', data[24:32])[0]
    key = data[32:32+key_len]
    assert key_len == len(b'general.architecture')
    assert key == b'general.architecture'

def test_write_seed_creates_file(tmp_path):
    """write_seed() doit créer un fichier lisible avec le bon contenu."""
    output = tmp_path / 'test_seed.gguf'
    write_seed(str(output))
    assert output.exists()
    with open(output, 'rb') as f:
        content = f.read()
    assert content[:4] == b'GGUF'

def test_parse_valid_header():
    """Un header valide doit être parsé correctement."""
    data = build_gguf_bytes()
    result = parse_gguf_header(data)
    assert result['version'] == 3
    assert result['n_tensors'] == 0
    assert result['n_kv'] == 1

def test_parse_empty_file_raises():
    """Un fichier vide doit lever une erreur claire, pas un crash silencieux."""
    with pytest.raises(ValueError, match="trop court"):
        parse_gguf_header(b'')

def test_parse_wrong_magic_raises():
    """Un mauvais magic number doit être rejeté explicitement."""
    with pytest.raises(ValueError, match="Magic number invalide"):
        parse_gguf_header(b'FAKE' + b'\x00' * 20)

def test_parse_truncated_header_raises():
    """Un header coupé en plein milieu doit être détecté, pas planter avec une erreur struct obscure."""
    with pytest.raises(ValueError, match="trop court"):
        parse_gguf_header(b'GGUF' + b'\x00' * 5)
