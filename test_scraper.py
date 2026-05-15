# test_scraper.py
from scraper import get_price

if __name__ == "__main__":
    # Try Amul Milk first
    data = get_price("Amul Milk")
    print("Result for Amul Milk:")
    print(data)

    # Try Ruchi Gold Oil
    data2 = get_price("Ruchi Gold Oil")
    print("\nResult for Ruchi Gold Oil:")
    print(data2)
