import os
from datetime import datetime

def main():
    name = os.getenv("USER_NAME", "User")
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"Hello, {name}! Today is {date_str}. Have a great day!")

if __name__ == "__main__":
    main()
