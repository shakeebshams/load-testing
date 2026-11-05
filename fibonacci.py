def fibonacci(n: int) -> int:
    """
    Returns the n-th Fibonacci number.
    F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n >= 2.
    
    Args:
        n (int): The index of the Fibonacci number to retrieve. Must be a non-negative integer.
        
    Returns:
        int: The n-th Fibonacci number.
        
    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_sequence(n: int) -> list:
    """
    Returns a list of the first n Fibonacci numbers.
    
    Args:
        n (int): The number of Fibonacci elements to generate. Must be a non-negative integer.
        
    Returns:
        list: A list containing the first n Fibonacci numbers.
        
    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    if n == 0:
        return []
    if n == 1:
        return [0]
    
    seq = [0, 1]
    for _ in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq
