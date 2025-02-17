import os
import re
import subprocess
import sys
from tqdm import tqdm

def run_pg_repack_in_docker():
    # Build the docker command
    docker_command = [
        "docker", "run", "--rm",
        "--entrypoint", "/usr/lib/postgresql/13/bin/pg_repack",
        "--network=rankly_default",
        "-e", "PGPASSWORD=secret",
        "my-pg-repack",
        "--host=laravel-db",
        "--port=5432",
        "--dbname=rankly-db1",
        "--username=laravel",
        "--table=plugin_keyword_stats"
   
    ]
    
    print("Running Docker command:")
    print(" ".join(docker_command))
    
    process = subprocess.Popen(
        docker_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Set up a progress bar (total 100 for percentage)
    pbar = tqdm(total=100, desc="Repack Progress", unit="%", dynamic_ncols=True)
    last_progress = 0
    # Regex pattern to capture percentage values
    progress_pattern = re.compile(r'(\d+)%')
    
    for line in process.stdout:
        # Print each line so you see the raw output
        sys.stdout.write(line)
        sys.stdout.flush()
        
        # Look for percentage values in the line
        match = progress_pattern.search(line)
        if match:
            try:
                progress = int(match.group(1))
                delta = progress - last_progress
                if delta > 0:
                    pbar.update(delta)
                    last_progress = progress
            except ValueError:
                pass
    
    process.wait()
    pbar.close()

if __name__ == "__main__":
    run_pg_repack_in_docker()
