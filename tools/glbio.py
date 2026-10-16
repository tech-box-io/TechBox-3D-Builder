"""Minimal GLB reader and writer (numpy only).

The writer emits quantized geometry (KHR_mesh_quantization) and, when asked, compresses every
buffer view with EXT_meshopt_compression so the file the browser downloads stays small.
"""
import json
import struct

import numpy as np

COMPONENT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
COMPONENT_CODE = {np.dtype(v): k for k, v in COMPONENT.items()}
NCOMP = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}
ARRAY_BUFFER, ELEMENT_ARRAY_BUFFER = 34962, 34963


def read_glb(path):
    """Return (json dict, binary chunk bytes)."""
    with open(path, 'rb') as f:
        magic, version, _length = struct.unpack('<III', f.read(12))
        if magic != 0x46546C67 or version != 2:
            raise ValueError(f'{path} is not a GLB v2 file')
        clen, _ctype = struct.unpack('<II', f.read(8))
        doc = json.loads(f.read(clen))
        header = f.read(8)
        blob = f.read(struct.unpack('<II', header)[0]) if len(header) == 8 else b''
    return doc, blob


def accessor(doc, blob, index):
    """Read an accessor as an (n, components) numpy array."""
    a = doc['accessors'][index]
    view = doc['bufferViews'][a['bufferView']]
    offset = view.get('byteOffset', 0) + a.get('byteOffset', 0)
    n = NCOMP[a['type']]
    dtype = np.dtype(COMPONENT[a['componentType']])
    stride = view.get('byteStride')
    if stride and stride != dtype.itemsize * n:
        raw = np.frombuffer(blob, dtype=np.uint8, count=stride * a['count'], offset=offset).reshape(a['count'], stride)
        return np.frombuffer(raw[:, :dtype.itemsize * n].tobytes(), dtype=dtype).reshape(a['count'], n)
    return np.frombuffer(blob, dtype=dtype, count=a['count'] * n, offset=offset).reshape(a['count'], n)


def node_matrix(node):
    """A node's local transform as a 4x4 (column-vector convention)."""
    if 'matrix' in node:
        return np.array(node['matrix'], dtype=np.float64).reshape(4, 4).T
    m = np.eye(4)
    if 'scale' in node:
        m = np.diag(list(node['scale']) + [1.0]) @ m
    if 'rotation' in node:
        x, y, z, w = node['rotation']
        r = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w), 0],
                      [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w), 0],
                      [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y), 0],
                      [0, 0, 0, 1]])
        m = r @ m
    if 'translation' in node:
        t = np.eye(4)
        t[:3, 3] = node['translation']
        m = t @ m
    return m


class GlbWriter:
    """Accumulates buffer views and accessors, then writes one GLB."""

    def __init__(self, compress=True):
        self.compress = compress
        self.views = []      # dicts: data, stride, target, mode, count
        self.accessors = []

    def _view(self, data, stride, target, mode, count):
        self.views.append(dict(data=data, stride=stride, target=target, mode=mode, count=count))
        return len(self.views) - 1

    def add_vertices(self, array, kind, normalized=False, with_bounds=False):
        """array: (n, c) of a fixed dtype whose row size is a multiple of 4 bytes."""
        array = np.ascontiguousarray(array)
        stride = array.dtype.itemsize * array.shape[1]
        if stride % 4:
            raise ValueError('vertex stride must be a multiple of 4 bytes')
        view = self._view(array, stride, ARRAY_BUFFER, 'ATTRIBUTES', len(array))
        acc = dict(bufferView=view, componentType=COMPONENT_CODE[array.dtype], count=len(array), type=kind)
        if normalized:
            acc['normalized'] = True
        if with_bounds:
            n = NCOMP[kind]
            acc['min'] = array[:, :n].min(0).tolist()
            acc['max'] = array[:, :n].max(0).tolist()
        self.accessors.append(acc)
        return len(self.accessors) - 1

    def add_indices(self, indices, triangles=True):
        indices = np.ascontiguousarray(indices.reshape(-1))
        dtype = np.uint16 if (indices.max() if len(indices) else 0) < 65535 else np.uint32
        indices = indices.astype(dtype)
        view = self._view(indices, indices.dtype.itemsize, ELEMENT_ARRAY_BUFFER, 'TRIANGLES' if triangles else 'INDICES', len(indices))
        self.accessors.append(dict(bufferView=view, componentType=COMPONENT_CODE[indices.dtype], count=len(indices), type='SCALAR'))
        return len(self.accessors) - 1

    def write(self, path, doc):
        """doc: glTF JSON without buffers/bufferViews/accessors (they are filled in here)."""
        if self.compress:
            import meshoptimizer as mo
            mo.encode_vertex_version(0)   # the codec versions EXT_meshopt_compression specifies
            mo.encode_index_version(1)
        packed, plain_len, views_json = bytearray(), 0, []
        for v in self.views:
            raw = v['data'].tobytes()
            entry = dict(byteLength=len(raw), target=v['target'])
            if v['target'] == ARRAY_BUFFER:
                entry['byteStride'] = v['stride']
            if self.compress:
                if v['mode'] == 'ATTRIBUTES':
                    enc = mo.encode_vertex_buffer(v['data'].view(np.uint8).reshape(v['count'], v['stride']), v['count'], v['stride'])
                elif v['mode'] == 'TRIANGLES':
                    enc = mo.encode_index_buffer(v['data'], v['count'], int(v['data'].max()) + 1 if v['count'] else 0)
                else:
                    enc = mo.encode_index_sequence(v['data'], v['count'], int(v['data'].max()) + 1 if v['count'] else 0)
                entry.update(buffer=1, byteOffset=plain_len)
                entry['extensions'] = {'EXT_meshopt_compression': dict(buffer=0, byteOffset=len(packed), byteLength=len(enc), byteStride=v['stride'], count=v['count'], mode=v['mode'])}
                packed += enc
            else:
                entry.update(buffer=0, byteOffset=len(packed))
                packed += raw
            packed += b'\x00' * (-len(packed) % 4)
            plain_len += len(raw) + (-len(raw) % 4)
            views_json.append(entry)
        doc = dict(doc)
        doc['bufferViews'] = views_json
        doc['accessors'] = self.accessors
        doc['buffers'] = [dict(byteLength=len(packed))]
        used = set(doc.get('extensionsUsed', [])) | {'KHR_mesh_quantization'}
        if self.compress:
            doc['buffers'].append(dict(byteLength=plain_len, extensions={'EXT_meshopt_compression': {'fallback': True}}))
            used.add('EXT_meshopt_compression')
        doc['extensionsUsed'] = sorted(used)
        doc['extensionsRequired'] = sorted(used)
        text = json.dumps(doc, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        text += b' ' * (-len(text) % 4)
        with open(path, 'wb') as f:
            f.write(struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(text) + 8 + len(packed)))
            f.write(struct.pack('<II', len(text), 0x4E4F534A))
            f.write(text)
            f.write(struct.pack('<II', len(packed), 0x004E4942))
            f.write(packed)
        return 12 + 8 + len(text) + 8 + len(packed)
