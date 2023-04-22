# usage example -- very simple
import minigebra
try:
    minigebra.run("CLI")
except SystemExit as code:
    if str(code) == "0":
        print("App terminated successfully.")
    else:
        print(f"App terminated prematurely with exit code {code}.") 
except Exception as e:
    print(e)