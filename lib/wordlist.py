"""
lib.wordlist:
Framework for working with wordlists
"""

import lib.log as log
import chardet
from pathlib import Path
from typing import List, Union

class Wordlist:
    """
    Obtains words from a wordlist, where words are separated by newlines.
    - `words`: List of words.
    """
    def __init__(self, wordlist_filepath: str):
        """
        Defines a wordlist.
        - `wordlist_filepath`: String containing the filepath of the wordlist.
        """
        if not isinstance(wordlist_filepath, str) or len(wordlist_filepath) == 0:
            raise ValueError("Wordlist.__init__: Expected string value for wordlist_filepath.")
        self._p = Path(wordlist_filepath)
        words = []
        if self._p.is_file():
            words = self._file_extract(self._p)
        elif self._p.is_dir():
            # Scan for files in directory
            files = [p for p in self._p.iterdir() if p.is_file()]
            for p in files:
                try:
                    file_words = self._file_extract(p)
                    words += file_words
                except Exception as e:
                    log.warn(f"Failed to extract words from {str(p)}, error: {e}")
        else:
            raise ValueError(f"Wordlist.__init__: Invalid file {self._p}")
        self.words = words

    def _predict_encoding(self, p: Path) -> str:
        """ Predict encoding of file using chardet, stolen from https://stackoverflow.com/a/45167602"""
        max_bytes = 100000  # maximum bytes to read from file, useful for huge files
        with p.open("rb") as fp_raw:
            prediction = chardet.detect(fp_raw.read(max_bytes))
            encoding = prediction["encoding"]
            confidence = prediction["confidence"]
            log.debug(f"Assessed {p} to be {encoding} with confidence {confidence}")
            return encoding

    def _file_extract(self, p: Path) -> List[str]:
        """ Extract words from a file. """
        lines = []
        with p.open(encoding=self._predict_encoding(p), errors='ignore') as fp:
            lines = fp.readlines()
        return [line.strip() for line in lines]
        
