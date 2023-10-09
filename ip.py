import subprocess


def check_if_is_up(ip: str) -> bool:
    """
    Checks if the provided IP address is reachable via a single ICMP ping.

    Args:
        ip (str): The IP address to be checked.

    Returns:
        bool: True if the IP address is reachable, False otherwise.
    """
    output = subprocess.run([f'ping -c 1 {ip}'], capture_output=True, shell=True)
    if 'cannot resolve' in output.stderr.decode('utf8').lower():
        return False
    else:
        return True