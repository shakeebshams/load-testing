import unittest
from fibonacci import fibonacci, fibonacci_sequence

class TestFibonacci(unittest.TestCase):
    def test_fibonacci_base_cases(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)

    def test_fibonacci_values(self):
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(3), 2)
        self.assertEqual(fibonacci(4), 3)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(6), 8)
        self.assertEqual(fibonacci(10), 55)

    def test_fibonacci_sequence_base_cases(self):
        self.assertEqual(fibonacci_sequence(0), [])
        self.assertEqual(fibonacci_sequence(1), [0])
        self.assertEqual(fibonacci_sequence(2), [0, 1])

    def test_fibonacci_sequence_values(self):
        self.assertEqual(fibonacci_sequence(5), [0, 1, 1, 2, 3])
        self.assertEqual(fibonacci_sequence(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)
        with self.assertRaises(ValueError):
            fibonacci_sequence(-5)
        with self.assertRaises(TypeError):
            fibonacci("string")
        with self.assertRaises(TypeError):
            fibonacci(3.5)
        with self.assertRaises(TypeError):
            fibonacci(True)
        with self.assertRaises(TypeError):
            fibonacci_sequence(False)

if __name__ == "__main__":
    unittest.main()
