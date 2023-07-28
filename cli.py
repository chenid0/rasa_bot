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
    # SARbot.exe ImportMols -i c:/tmp/Chembl_612285and6.csv -db c:/tmp/Chembl_612285and6.db
    db_path = "/path/project.db"
    is_path = "/path/scaffold2.mol"
    ic = "Structure_ID"
    ac = "'612285_Ki(nM)'"
    sar_command = "ImportScaffold"
    cmd = f"./bin/sarbot {sar_command} -db {db_path} -is {is_path} -ic {ic} -ac {ac}"
    execute_command(cmd, run_in_background=False)

def run_sarbot_import_scaffold():    
    # SARbot.exe ImportScaffold -i c:/tmp/scaffold2.mol -db c:/tmp/Chembl_612285and6.db
    db_path = "/path/project.db"
    is_path = "/path/scaffold2.mol"
    ic = "Structure_ID"
    ac = "'612285_Ki(nM)'"
    sar_command = "ImportScaffold"
    cmd = f"./bin/sarbot {sar_command} -db {db_path} -is {is_path} -ic {ic} -ac {ac}"
    execute_command(cmd, run_in_background=False)

    
def run_sarbot_render_scaffold():
    # SARbot.exe RenderScaffold -sid 1 -db c:/tmp/Chembl_612285and6.db -o c:/tmp/scaf1.mol -o c:/tmp/scaf1.svg
    db_path = "/path/project.db"
    is_path = "/path/scaffold2.mol"
    ic = "Structure_ID"
    ac = "'612285_Ki(nM)'"
    sar_command = "ImportScaffold"
    cmd = f"./bin/sarbot {sar_command} -db {db_path} -is {is_path} -ic {ic} -ac {ac}"
    execute_command(cmd, run_in_background=False)

    
def run_sarbot_render_molecule_mkey():
    # SARbot.exe RenderMolecule -mkey VPNRFNXGBHPYEB-UHFFFAOYSA-N -db c:/tmp/Chembl_612285and6.db -o c:/tmp/mol1.mol -o c:/tmp/mol1.svg
    db_path = "/path/project.db"
    is_path = "/path/scaffold2.mol"
    ic = "Structure_ID"
    ac = "'612285_Ki(nM)'"
    sar_command = "ImportScaffold"
    cmd = f"./bin/sarbot {sar_command} -db {db_path} -is {is_path} -ic {ic} -ac {ac}"
    execute_command(cmd, run_in_background=False)


def run_sarbot_render_molecule_sid():
    # SARbot.exe RenderMolecule -sid 1 -mid 10 -db c:/tmp/Chembl_612285and6.db -o c:/tmp/mol2.mol -o c:/tmp/mol2.svg
    db_path = "/path/project.db"
    is_path = "/path/scaffold2.mol"
    ic = "Structure_ID"
    ac = "'612285_Ki(nM)'"
    sar_command = "ImportScaffold"
    cmd = f"./bin/sarbot {sar_command} -db {db_path} -is {is_path} -ic {ic} -ac {ac}"
    execute_command(cmd, run_in_background=False)