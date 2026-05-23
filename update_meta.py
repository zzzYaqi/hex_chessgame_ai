# used in the run_hex.bat file to modify the parameters in agents/Group3/meta.py
import sys

def update_meta(file_path, exploration_value, rave_const_value):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip().startswith('EXPLORATION'):
                file.write(f'    EXPLORATION = {exploration_value}\n')
            elif line.strip().startswith('RAVE_CONST'):
                file.write(f'    RAVE_CONST = {rave_const_value}\n')
            else:
                file.write(line)

if __name__ == "__main__":
    file_path = 'agents/Group3/meta.py'
    exploration_value = sys.argv[1]
    rave_const_value = sys.argv[2]
    update_meta(file_path, exploration_value, rave_const_value)
