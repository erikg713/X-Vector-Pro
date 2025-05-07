import logging
from core.recon import passive_recon
from core.scanner import run_port_scan
from core.brute import brute_force_login
from core.exploit_01 import run as run_exploit_01
from core.report import generate_report
import os
from concurrent.futures import ThreadPoolExecutor

# Configure logging for better debugging and tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(), logging.FileHandler("operations_log.log")])
logger = logging.getLogger(__name__)

def run_step(step_name: str, operation, target: str) -> str:
    """
    Executes a single operation and returns its result.

    Args:
        step_name (str): The name of the step.
        operation (callable): The function to run for the operation.
        target (str): The target IP or hostname.

    Returns:
        str: The result of the operation.
    """
    try:
        logger.info(f"Starting {step_name}...")
        result = operation(target)
        logger.info(f"{step_name} completed successfully.")
        return f"[*] {step_name}:\n{result}"
    except Exception as e:
        error_message = f"[ERROR] {step_name} failed: {e}"
        logger.error(error_message)
        return error_message

def run_sequence(target: str = "127.0.0.1") -> str:
    """
    Executes a sequence of cybersecurity operations on a specified target.

    Args:
        target (str): The target IP or hostname to perform the operations on. Defaults to "127.0.0.1".

    Returns:
        str: A formatted string containing the results of each operation.
    """
    sequence_steps = [
        ("Passive Recon", passive_recon),
        ("Port Scan", run_port_scan),
        ("Brute Force Login", brute_force_login),
        ("Default Exploit", run_exploit_01),
        ("Report Generation", generate_report),
    ]
    
    results = []
    
    # Use ThreadPoolExecutor for concurrent execution of steps (if needed)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for step_name, operation in sequence_steps:
            futures.append(executor.submit(run_step, step_name, operation, target))

        for future in futures:
            results.append(future.result())
    
    return "\n\n".join(results)

if __name__ == "__main__":
    # Example usage
    target_ip = "192.168.1.1"  # Replace with the desired target
    output = run_sequence(target_ip)
    print(output)
