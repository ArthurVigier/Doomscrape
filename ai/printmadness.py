import random

# List of ASCII drawings
ascii_drawings = [
    """
     __
    /__\ 
   (    ) 
   _\__/_
    """,
    """
    _____
   /     \
  |       |
  |       |
   \_____/
    """,
    """
    /\
   /  \
  /    \
 /      \
/________\
    """
    """
 /\     /\
{  `---'  }
{  O   O  }
~~>  V  <~~
  \ \|/ /
  `-----'____
 /     \    \_
{       }\  )_\_   _
 |  \_/  |/ /  \_\_/ )
  \__/  /(_/     \__/
    (__/
"""
]

while True:
    # Generate a string of 50 random ASCII characters
    ascii_chars = ''.join(chr(random.randint(33, 126)) for _ in range(50))
    print(ascii_chars)

    # Generate a string of 50 random binary numbers
    binary_nums = ' $$$$$$$ WINTER IS COMING $$$$$$$ '.join(bin(random.randint(0, 255)) for _ in range(50))
    print(binary_nums)

    # Print a random ASCII drawing
    if random.random() < 0.1:  # 10% chance to print a drawing
        print(random.choice(ascii_drawings))