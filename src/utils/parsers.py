def parse_bin_packing_config(file_path):
    configurations = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        i = 0

        while i < len(lines):
            if lines[i].startswith("u"):
                parts = lines[i].split()
                id = parts[0]
                bin_capacity = int(parts[1])
                num_items = int(parts[2])
                good_solution = int(parts[3])
                i += 1
                items = []

                while i < len(lines) and not lines[i].startswith("u"):
                    item = int(lines[i])
                    items.append(item)
                    i += 1
                
                configuration = {
                    'id': id,
                    'bin_capacity': bin_capacity,
                    'num_items': num_items,
                    'good_solution': good_solution,
                    'items': items
                }
                configurations.append(configuration)
            else:
                i += 1

    return configurations

def parse_sudoku_configurations(file_path):
    configurations = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_board = []
        for line in lines:
            if line.strip():
                row = [int(num) for num in line.split()]
                current_board.append(row)
                if len(current_board) == 9:
                    configurations.append(current_board)
                    current_board = []
    return configurations




