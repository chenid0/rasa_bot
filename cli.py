import subprocess
from typing import Optional, Tuple

def execute_command(cmd: str, run_in_background: bool = False, max_time: Optional[int] = None) -> Tuple[str, str, Optional[int]]:
    if run_in_background:
        cmd += " &"
        
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr, exit_code = "", "", None
    if not run_in_background:
        try:
            stdout, stderr = process.communicate(timeout=max_time)
            exit_code = process.poll()
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            exit_code = process.poll()
            
    return stdout, stderr, exit_code


def run_sarbot_build_r_dash():
    "sarbot BuildRDashBoard -db /path/project.db -is /path/scaffold2.mol -ic Structure_ID -ac '612285_Ki(nM)' "
    db_path = "/path/project.db"
    is_path = "/path/scaffold2.mol"
    ic = "Structure_ID"
    ac = "'612285_Ki(nM)'"
    build = "BuildRDashBoard"
    cmd = f"./bin/sarbot {build} -db {db_path} -is {is_path} -ic {ic} -ac {ac}"
    execute_command(cmd, run_in_background=False)


def run_sarbot_import_mols():
    "sarbot BuildRDashBoard -db /path/project.db -is /path/scaffold2.mol -ic Structure_ID -ac '612285_Ki(nM)' "
    db_path = "/path/project.db"
    is_path = "/path/scaffold2.mol"
    ic = "Structure_ID"
    ac = "'612285_Ki(nM)'"
    sar_command = "ImportMols"
    cmd = f"./bin/sarbot {sar_command} -db {db_path} -is {is_path} -ic {ic} -ac {ac}"
    execute_command(cmd, run_in_background=False)

    
def run_sarbot_import_mols():    
    db_path = "/path/project.db"
    is_path = "/path/scaffold2.mol"
    ic = "Structure_ID"
    ac = "'612285_Ki(nM)'"
    sar_command = "ImportScaffold"
    cmd = f"./bin/sarbot {sar_command} -db {db_path} -is {is_path} -ic {ic} -ac {ac}"
    execute_command(cmd, run_in_background=False)

def run_sarbot_import_scaffold():    
    db_path = "/path/project.db"
    is_path = "/path/scaffold2.mol"
    ic = "Structure_ID"
    ac = "'612285_Ki(nM)'"
    sar_command = "ImportScaffold"
    cmd = f"./bin/sarbot {sar_command} -db {db_path} -is {is_path} -ic {ic} -ac {ac}"
    execute_command(cmd, run_in_background=False)