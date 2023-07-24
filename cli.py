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
