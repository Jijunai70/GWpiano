
if __name__ == "__main__":
    file_path = "songs/有形的翅膀.txt"
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            if line[0] != '/':
                continue
            num_end_pos = line.find('-')
            if num_end_pos == -1:
                num_end_pos = len(line)
            num = int(line[1:num_end_pos])
            page_num = int((num - 1) / 4) + 1
            page_num_index = (num-1) % 4 + 1
            new_line = "/{}-{}.{}\n".format(num, page_num, page_num_index)
            lines[index] = new_line

    with open('temp.txt', 'w') as file:
        file.writelines(lines)
