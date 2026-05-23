import subprocess

def run_command():
    count = 0
    round = 100
    for _ in range(round):
        command = r'python Hex.py "a=aa;python agents\DefaultAgents\NaiveAgent.py" "a=Cap;python agents\GroupAgent\CapAgent.py" -v'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        output = result.stdout.decode()
        if 'Cap has' in output:
            count += 1
    return count / round

print(run_command())
