import subprocess
import time
#https://developer.ibm.com/tutorials/awb-local-ai-copilot-ibm-granite-code-ollama-continue/
def start_ollama_model( timeout=10):
    try:
        process = subprocess.Popen(
            ["ollama", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        start_time = time.time()

        while True:
            if process.poll() is not None:  # Process finished
                break
            if time.time() - start_time > timeout:
                print("Process timed out.")
                process.kill()
                break
            time.sleep(0.1)

        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print("Model started successfully.")
        else:
            print("Error starting model:")
            print(stderr.strip())
    except FileNotFoundError:
        print("Ollama is not installed or not found in your PATH.")

# Replace 'your_model_name' with the actual model name
start_ollama_model()
