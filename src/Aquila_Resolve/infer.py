from __future__ import annotations
from .models.dp.phonemizer import Phonemizer
from .data import DATA_PATH
from .data.remote import ensure_download, check_updates
from .models import MODELS_PATH
import sys

sys.path.insert(0, str(MODELS_PATH))


class Infer:
    def __init__(self, device='cpu'):
        ensure_download()  # Download checkpoint if necessary
        check_updates()  # Check for checkpoint updates
        checkpoint_path = DATA_PATH.joinpath('model.pt')
        self.model = Phonemizer.from_checkpoint(checkpoint_path, device=device)
        self.lang = 'en_us'
        self.batch_size = 32

    def __call__(self, words: list[str]) -> list[str]:
        """
        Infers phonemes for a list of words.
        :param words: list of words
        :return: dict of {word: phonemes}
        """
        res = self.model.phonemise_list(words, lang=self.lang, batch_size=self.batch_size).phonemes
        # Replace all occurrences of '][' with spaces, remove remaining brackets
        res = [r.replace('][', ' ').replace('[', '').replace(']', '') for r in res]
        return res
