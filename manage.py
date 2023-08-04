import subprocess
import sys

if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit("Too much args")
    
    if "up" in sys.argv:
        subprocess.run(["docker-compose", "up"])

    elif "build" in sys.argv:
        subprocess.run(["docker-compose", "up", "--build"])

    elif "init" in sys.argv:
        print("INIT")