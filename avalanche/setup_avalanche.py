import subprocess

def setup_avalanche():
    # Pull the latest Avalanche image
    subprocess.run(["docker", "pull", "avaplatform/avalanchego"])
    
    # Set up flags and ENV variables
    docker_flags = [
        "docker", "run", "-d",
        "-p", "9650:9650",
        "-p", "9651:9651",
        "--name", "snowscape-avalanche-node",
        "-e", "NETWORK_ID=local",
        "-e", "HTTP_HOST=",
        "-e", "HTTP_PORT=9650",
        "-e", "STAKING_PORT=9651"
    ]
    
    docker_image = ["avaplatform/avalanchego:latest"]
    
    subprocess.run(docker_flags + docker_image)

if __name__ == "__main__":
    setup_avalanche()
