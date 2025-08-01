### gui/components/form_inputs.py

import os
import importlib
import gui

logging.basicConfig(level=logging.INFO)

def validate_metadata(meta, required_keys):
    """Validate that all required keys exist in the module metadata."""
    missing_keys = [key for key in required_keys if key not in meta]
    if missing_keys:
        logging.warning(f"Missing metadata keys: {', '.join(missing_keys)}")
        return False
    return True

def load_exploits(filter_tags=None, only_enabled=True):
    """
    Dynamically loads exploit modules based on filter criteria.

    Args:
        filter_tags (list): List of tags to filter exploits.
        only_enabled (bool): Whether to load only enabled exploits.

    Returns:
        list: List of loaded exploit modules with metadata.
    """
    modules = []
    exploits_dir = os.path.dirname(__file__)
    for file in os.listdir(exploits_dir):
        if file.endswith(".py") and file != "__init__.py":
            name = file[:-3]
            try:
                mod = importlib.import_module(f"core.exploits.{name}")
                
                # Validate metadata
                if not hasattr(mod, "metadata"):
                    logging.warning(f"Exploit {name} missing metadata, skipping.")
                    continue

                meta = mod.metadata
                if only_enabled and not meta.get("enabled", False):
                    continue

                if filter_tags and not set(filter_tags).intersection(meta.get("tags", [])):
                    continue

                # Add to modules list
                modules.append((meta.get("name", name), mod))

            except ModuleNotFoundError as e:
                logging.error(f"Module {name} not found: {e}")
            except Exception as e:
                logging.error(f"Failed to load module {name}: {e}")
    return modules

def run_all_exploits(target_url, filter_tags=None):
    """
    Runs all loaded exploits on the specified target URL.

    Args:
        target_url (str): The target URL to run exploits against.
        filter_tags (list): List of tags to filter exploits.

    Returns:
        list: List of tuples containing exploit names and their results.
    """
    results = []
    exploits = load_exploits(filter_tags=filter_tags)
    for name, mod in exploits:
        logging.info(f"Running exploit: {name}")
        try:
            result = mod.run_exploit(target_url)
            results.append((name, result))
        except Exception as e:
            logging.error(f"Exploit {name} failed: {e}")
            results.append((name, None))
    return results
