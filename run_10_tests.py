import os
def get_workspace_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.abspath(__file__))

import os
import time
import subprocess
import glob

NUM_RUNS = 10
LOG_FILE = os.path.join(get_workspace_root(), \"test_10_runs_results.txt\")

def modify_run_all(headless, sleep_time):
    with open("run_all.sh", "r") as f:
        content = f.read()
    
    if headless:
        content = content.replace("headless:=false", "headless:=true")
    else:
        content = content.replace("headless:=true", "headless:=false")
        
    import re
    content = re.sub(r'sleep \d+', f'sleep {sleep_time}', content)
    content = re.sub(r'Aguardando \d+ segundos', f'Aguardando {sleep_time} segundos', content)
    
    with open("run_all.sh", "w") as f:
        f.write(content)

def cleanup():
    os.system('pkill -9 -f "run_all.sh|gz|gazebo|rviz2|ros2|ruby|mission_coverage|tracker|monitor" || true')
    time.sleep(3)

def run_single_test(run_idx):
    print(f"--- Iniciando Run {run_idx} ---")
    cleanup()
    
    os.system('rm -f full_log.txt slam_log.txt monitor.log')
    
    start_time = time.time()
    
    proc_sim = subprocess.Popen(["./run_all.sh"], stdout=open("full_log.txt", "w"), stderr=subprocess.STDOUT)
    proc_mon = subprocess.Popen(["python3", "/home/tales/.gemini/antigravity/brain/3935fd9a-171b-40f6-9112-82086df72826/scratch/monitor.py"], stdout=open(f"monitor_run_{run_idx}.log", "w"), stderr=subprocess.STDOUT)
    
    timeout = 360 
    success = False
    mission_time = 0
    
    while time.time() - start_time < timeout:
        if os.path.exists("full_log.txt"):
            with open("full_log.txt", "r") as f:
                content = f.read()
                if "Missao finalizada com sucesso!" in content:
                    success = True
                    mission_time = time.time() - start_time
                    break
        time.sleep(2)
        
    proc_sim.terminate()
    proc_mon.terminate()
    cleanup()
    
    # Extrair a ultima pose do monitor
    last_pose = "Unknown"
    if os.path.exists(f"monitor_run_{run_idx}.log"):
        with open(f"monitor_run_{run_idx}.log", "r") as f:
            lines = f.readlines()
            for line in reversed(lines):
                if "Pose:" in line:
                    last_pose = line.strip().split("Pose:")[1].split("Thrust:")[0].strip()
                    break
                    
    return success, mission_time, last_pose

def main():
    with open(LOG_FILE, "w") as f:
        f.write("Resultados de 10 Iterações:\n")
        f.write("===========================\n")
        
    modify_run_all(headless=True, sleep_time=25) # headless loads faster
    
    for i in range(1, NUM_RUNS + 1):
        success, mission_time, last_pose = run_single_test(i)
        
        status = "SUCESSO" if success else "FALHA/TIMEOUT"
        result_str = f"Run {i}: {status} | Tempo: {mission_time:.1f}s | Ultima Pose: {last_pose}\n"
        print(result_str)
        
        with open(LOG_FILE, "a") as f:
            f.write(result_str)
            
    # Restaura run_all original
    modify_run_all(headless=False, sleep_time=35)
    print("Testes finalizados!")

if __name__ == "__main__":
    main()
