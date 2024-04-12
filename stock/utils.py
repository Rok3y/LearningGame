def bytes_to_megabytes(num_bytes):
    """
    Convert bytes to megabytes, where 1 MB = 2^20 bytes = 1,048,576 bytes.
    
    Args:
    num_bytes (int): The number of bytes.

    Returns:
    float: The number of megabytes.
    """
    return num_bytes / 1048576  # 1048576 is 2^20