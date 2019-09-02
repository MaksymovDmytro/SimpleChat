# Network constants
HOST = '127.0.0.1'
PORT = 65432
ADDRESS = (HOST, PORT)

# Preferred encoding
ENC = 'utf-8'

# Lambda expressions
to_b = lambda x: bytes(f'{x}', ENC)
