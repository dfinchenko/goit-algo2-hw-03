import csv
import timeit
from BTrees.OOBTree import OOBTree

def load_data(file_path):
    """Завантажує дані з CSV-файлу у список словників."""
    with open(file_path, "r") as file:
        return list(map(lambda row: {
            "ID": int(row["ID"]),
            "Name": row["Name"],
            "Category": row["Category"],
            "Price": float(row["Price"]),
        }, csv.DictReader(file)))

def add_items_to_structures(data):
    """Додає всі товари в OOBTree та dict."""
    tree, dictionary = OOBTree(), {}
    for item in data:
        tree[item["ID"]] = dictionary[item["ID"]] = item
    return tree, dictionary

def range_query_tree(tree, min_price, max_price):
    """Шукає товари у заданому ціновому діапазоні в OOBTree."""
    return [item for _, item in tree.items(min_price, max_price)]

def range_query_dict(dictionary, min_price, max_price):
    """Шукає товари у заданому ціновому діапазоні у звичайному словнику."""
    return [item for item in dictionary.values() if min_price <= item["Price"] <= max_price]

def measure_time(func, *args, number=100):
    """Вимірює середній час виконання функції за 100 запусків."""
    return timeit.timeit(lambda: func(*args), number=number)

def main():
    file_path = "generated_items_data.csv"
    data = load_data(file_path)
    
    tree, dictionary = add_items_to_structures(data)
    
    min_price, max_price = 50, 150

    # Вимірюємо час виконання
    tree_time = measure_time(range_query_tree, tree, min_price, max_price)
    dict_time = measure_time(range_query_dict, dictionary, min_price, max_price)

    # Вивід результатів
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if __name__ == "__main__":
    main()
