"""Inventory management system for adding, removing, and saving stock data."""
import json
import logging
from datetime import datetime
stock_data = {}
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def add_item(item="default", qty=0, logs=None):
    """
    Add an item to the inventory.

    Args:
        item (str): Item name (must be string)
        qty (int): Quantity to add (must be non-negative integer)
        logs (list): Optional list to append log messages

    Returns:
        bool: True if successful, False otherwise
    """
    if logs is None:
        logs = []

    # Input validation
    if not isinstance(item, str) or not item:
        logging.error("Item name must be a non-empty string")
        return False

    if not isinstance(qty, int) or qty < 0:
        logging.error("Quantity must be a non-negative integer")
        return False

    stock_data[item] = stock_data.get(item, 0) + qty
    log_message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_message)
    logging.info(log_message)
    return True


def remove_item(item, qty):
    """
    Remove an item from the inventory.

    Args:
        item (str): Item name to remove
        qty (int): Quantity to remove

    Returns:
        bool: True if successful, False otherwise
    """
    if item not in stock_data:
        logging.warning("Item '%s' not found in inventory", item)
        return False

    if not isinstance(qty, int) or qty < 0:
        logging.error("Quantity must be a non-negative integer")
        return False

    try:
        if stock_data[item] < qty:
            logging.warning(
                "Cannot remove %d of '%s'. Only %d in stock.",
                qty, item, stock_data[item]
            )
            return False

        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info("Item '%s' removed (quantity <= 0)", item)
        else:
            logging.info("Removed %d of '%s'", qty, item)
        return True

    except KeyError as error:
        # Should be caught by 'item not in stock_data' check, but good for safety
        logging.error("Error: Item '%s' not found during removal. %s", item, error)
        return False
    except TypeError as error:
        logging.error("Error removing item due to type mismatch: %s", error)
        return False


def get_qty(item):
    """
    Get the quantity of an item in inventory.

    Args:
        item (str): Item name to query

    Returns:
        int: Quantity of item, or 0 if not found
    """
    return stock_data.get(item, 0)
def load_data(filename="inventory.json"):
    """
    Load inventory data from a JSON file.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)
        stock_data.clear()
        stock_data.update(data)
        logging.info("Data loaded successfully from %s", filename)
        return True

    except FileNotFoundError:
        logging.warning("File %s not found. Starting with empty inventory.", filename)
        stock_data.clear()
        return False

    except json.JSONDecodeError as decode_error:
        logging.error("Error decoding JSON: %s", decode_error)
        return False


def save_data(filename="inventory.json"):
    """
    Save inventory data to a JSON file.

    Args:
        filename (str): Path to the JSON file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, "w", encoding="utf-8") as file_handle:
            json.dump(stock_data, file_handle, indent=2)
        logging.info("Data saved successfully to %s", filename)
        return True

    except IOError as io_error:
        logging.error("Error saving data: %s", io_error)
        return False


def print_data():
    """Print a formatted report of all items in inventory."""
    print("\n" + "=" * 40)
    print("Items Report")
    print("=" * 40)
    if not stock_data:
        print("No items in inventory")
    else:
        for item, quantity in stock_data.items():
            print(f"{item} -> {quantity}")
    print("=" * 40 + "\n")


def check_low_items(threshold=5):
    """
    Check for items below a specified threshold.

    Args:
        threshold (int): Minimum quantity threshold (default: 5)

    Returns:
        list: List of items below threshold
    """
    result = []
    for item, quantity in stock_data.items():
        if quantity < threshold:
            result.append(item)
    return result


def main():
    """Main function to demonstrate inventory system functionality."""
    logging.info("Starting inventory system")

    # # Load initial data (will likely start with empty inventory if file is new)
    # load_data()
    stock_data.update(load_data())

    # Test adding items
    add_item("apple", 10)
    add_item("banana", 5)
    add_item("orange", 3)
    add_item("grape", 15)

    # Test removing items
    remove_item("apple", 3)
    remove_item("orange", 1)
    remove_item("grape", 15)  # Should remove the item completely
    remove_item("non_existent_item", 1) # Should log a warning

    # Test querying quantity
    apple_qty = get_qty("apple")
    print(f"Apple stock: {apple_qty}")
    grape_qty = get_qty("grape")
    print(f"Grape stock: {grape_qty}")

    # Check for low stock items (threshold=5)
    low_items = check_low_items()
    print(f"Low items: {low_items}")

    # Save data to inventory.json
    save_data()

    # Print final report
    print_data()

    # Demonstrate a fresh load overwrites current stock for the example
    load_data()
    print("Data loaded back from file:")
    print_data()

    logging.info("Inventory system operations completed")


if __name__ == "__main__":
    main()
