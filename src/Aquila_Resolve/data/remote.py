# Access and checks for remote data
from warnings import warn
import requests
import shutil
from . import DATA_PATH

_model = DATA_PATH.joinpath('model.pt')
_model_url = "https://huggingface.co/ionite/Aquila-Resolve/resolve/main/model.pt"  # Download URL
_model_ptr = "https://huggingface.co/ionite/Aquila-Resolve/raw/main/model.pt"  # Git LFS Pointer URL


def check_model() -> bool:
    """Checks if the model matches checksums"""
    result = requests.get(_model_ptr).text.split()
    if result is None or len(result) < 6 or not result[3].startswith('sha256:'):
        warn("Could not retrieve remote model checksum")
        return False
    remote_sha256 = result[3][7:]
    actual_sha256 = get_checksum(_model)
    return remote_sha256 == actual_sha256


def download(update: bool = True) -> bool:
    """Downloads a file from a URL and saves it to a file_name"""
    # Check if the model is already downloaded
    if not update and _model.exists():
        return True
    if update and _model.exists() and check_model():
        return True
    # Download the model
    with requests.get(_model_url, stream=True) as r:
        r.raise_for_status()  # Raise error for download failure
        with _model.open('wb') as f:
            shutil.copyfileobj(r.raw, f)
    return _model.exists()  # Return existence of the model


def ensure_download():
    """Ensures the model is downloaded"""
    if not download(update=False):
        raise RuntimeError("Model could not be downloaded. Visit "
                           "https://huggingface.co/ionite/Aquila-Resolve/blob/main/model.pt "
                           "to download the model checkpoint manually and place it within the "
                           "Aquila_Resolve/data/ folder.")


def check_updates() -> None:
    """Checks if the model matches the latest checksum"""
    if not check_model():
        warn("Local model checkpoint did not match latest remote checksum. "
             "You can use Aquila_Resolve.download() to download the latest model.")


def get_checksum(file: str, block_size: int = 65536) -> str:
    """Calculates the checksum of a file"""
    import hashlib
    s = hashlib.sha256()
    with open(file, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            s.update(block)
    return s.hexdigest()