def create_empty_map(filename, width, height):
    with open(filename, "w") as f:
        for _ in range(height):
            row = " ".join(["1"] * width)
            f.write(row + "\n")

if __name__ == "__main__":
    width = int(input("Map width (tiles): "))
    height = int(input("Map height (tiles): "))
    filename = "map_data.txt"
    create_empty_map(filename, width, height)
    print(f"'{filename}' written in size {width}x{height}")
