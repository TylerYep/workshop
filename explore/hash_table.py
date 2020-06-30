import sys

from src.structures.hash_table import Cuckoo, HashTable, LinearProbing, RobinHood


def main() -> None:
    num_buckets = get_num_buckets()
    hash_table = choose_hash_table_type(num_buckets)
    print(hash_table)
    curr_elements = set()

    while True:
        user_input = input("Enter command: ")
        if user_input == "" or user_input[0] == "q":
            return
        interpreted = user_input.split()
        if len(interpreted) != 2:
            continue
        command, data_str = interpreted
        method = command[0].lower()
        data = int(data_str)
        if method == "i":
            hash_table.insert(data)
            print(f"    Called table.insert({data})")
            curr_elements.add(data)
        elif method == "c":
            ans = hash_table.contains(data)
            print(f"    Called table.contains({data}). Returned {ans}.")
        elif method == "r":
            hash_table.remove(data)
            print(f"    Called table.remove({data})")
            if data in curr_elements:
                curr_elements.remove(data)
        print(hash_table)

        # assert curr_elements | set([-1]) == hash_table.get_elems() | set([-1])


def get_num_buckets() -> int:
    size = -1
    while size <= 1:
        if size != -1:
            print("For safety, the minimum hash table size is 2.")
        try:
            size = int(input("Enter hash table size: "))
        except ValueError:
            continue
    return size


def choose_hash_table_type(num_buckets: int) -> HashTable:
    prompt = (
        "Please select the hash table you'd like to explore.\n"
        "  (L)inear Probing\n"
        "  (R)obin Hood Hashing\n"
        "  (C)uckoo Hashing\n"
        "Or just hit ENTER to quit."
    )
    while True:
        print(prompt)
        user_input = input("Your choice: ")
        letter = user_input[0].lower()
        if user_input == "" or letter == "q":
            sys.exit(0)

        if letter == "l":
            return LinearProbing(num_buckets)
        if letter == "r":
            return RobinHood(num_buckets)
        if letter == "c":
            return Cuckoo(num_buckets)
        print("  Sorry, I didn't understand that.")


if __name__ == "__main__":
    main()