# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""
import hashlib
from typing import List, Tuple, Optional, Dict

from actionflow.embs.base import Emb


class HashEmb(Emb):
    """A Literal Hash Embedding Function, which hashes the input text as a list of floats."""
    model: str = "literal_hash_emb"
    dimensions: int = 32

    def get_embedding(self, text: str) -> List[float]:
        # Calculate the SHA-256 hash of the text
        hash_object = hashlib.sha256(text.encode())
        hash_list = list(hash_object.digest())
        float_list = [float(x) / 255.0 for x in hash_list]
        return float_list

    def get_embedding_and_usage(self, text: str) -> Tuple[List[float], Optional[Dict]]:
        usage = None
        embedding = self.get_embedding(text)
        return embedding, usage
