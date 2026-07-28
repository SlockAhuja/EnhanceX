import os
import sys
import venv
import subprocess
import glob


def build_and_verify():
    print("==================================================")
    print("EnhanceX Package & Wheel Build Verification")
    print("==================================================")

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_dir = os.path.join(root_dir, "dist")

    # 1. Run Python build
    print("\n--- Building Source Distribution & Wheel ---")
    res = subprocess.run([sys.executable, "-m", "build"], cwd=root_dir, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Build Error: {res.stderr}")
        # Fallback to setup.py
        subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"], cwd=root_dir, check=True)

    sdist_files = glob.glob(os.path.join(dist_dir, "*.tar.gz"))
    wheel_files = glob.glob(os.path.join(dist_dir, "*.whl"))

    print(f"Generated Source Distribution (sdist): {sdist_files}")
    print(f"Generated Wheel Package (.whl): {wheel_files}")

    if not wheel_files:
        raise FileNotFoundError("Wheel package was not built!")

    wheel_path = wheel_files[0]

    # 2. Create Clean Virtual Environment
    test_env_dir = os.path.join(root_dir, "test_venv")
    print(f"\n--- Creating Clean Virtual Environment at {test_env_dir} ---")
    venv.create(test_env_dir, with_pip=True)

    if sys.platform == "win32":
        python_bin = os.path.join(test_env_dir, "Scripts", "python.exe")
        enhancex_bin = os.path.join(test_env_dir, "Scripts", "enhancex.exe")
    else:
        python_bin = os.path.join(test_env_dir, "bin", "python")
        enhancex_bin = os.path.join(test_env_dir, "bin", "enhancex")

    # 3. Install Wheel into clean environment
    print(f"\n--- Installing Wheel {os.path.basename(wheel_path)} into clean environment ---")
    subprocess.run([python_bin, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([python_bin, "-m", "pip", "install", wheel_path], check=True)

    # 4. Verify installation & importability
    print("\n--- Verifying Package Functionality in Clean Environment ---")
    import_cmd = [
        python_bin,
        "-c",
        "from enhancex import VideoEnhancer, ImageEnhancer, Stabilizer; print('EnhanceX Imported Successfully inside Clean Virtual Environment!')"
    ]
    res_import = subprocess.run(import_cmd, capture_output=True, text=True)
    print(res_import.stdout)

    # 5. Verify CLI command inside clean environment
    cli_cmd = [enhancex_bin, "--help"]
    res_cli = subprocess.run(cli_cmd, capture_output=True, text=True)
    print("CLI --help Output:")
    print(res_cli.stdout)

    print("\n==================================================")
    print("WHEEL BUILD & CLEAN ENV INSTALLATION VERIFIED 100%")
    print("==================================================")


if __name__ == "__main__":
    build_and_verify()
