import json
from pathlib import Path
from typing import Optional


def load_targets(filename: str) -> dict:
    targets_path = Path(__file__).parent / "targets" / filename
    return json.loads(targets_path.read_text())

def load_mock_data(filename: str, base_dir: Optional[str] = None) -> str:
    """
    Load mock HTML data from the specified directory.
    
    Args:
        filename: Name of the file to load (e.g., 'index/sample_index.html')
        base_dir: Optional base directory for mock data. If not provided,
                 defaults to 'tests/data' relative to the project root.
    
    Returns:
        str: Contents of the mock data file
    
    Raises:
        FileNotFoundError: If the mock data file doesn't exist
    """
    if base_dir is None:
        # Get the project root directory (2 levels up from this file)
        project_root = Path(__file__).parent.parent.parent
        base_path = project_root / 'tests' / 'data'
    else:
        base_path = Path(base_dir)
    
    file_path = base_path / filename
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
