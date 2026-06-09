import subprocess
import tempfile


# ================= PYTHON =================
def run_python(code):
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)


# ================= JAVA =================
def run_java(code):
    try:
        with tempfile.TemporaryDirectory() as temp:
            file_path = f"{temp}/Main.java"

            with open(file_path, "w") as f:
                f.write(code)

            compile = subprocess.run(
                ["javac", file_path],
                capture_output=True,
                text=True
            )

            if compile.returncode != 0:
                return compile.stderr

            run = subprocess.run(
                ["java", "-cp", temp, "Main"],
                capture_output=True,
                text=True,
                timeout=5
            )

            return run.stdout or run.stderr
    except Exception as e:
        return str(e)


# ================= C++ =================
def run_cpp(code):
    try:
        with tempfile.TemporaryDirectory() as temp:
            cpp_file = f"{temp}/main.cpp"
            exe_file = f"{temp}/a.out"

            with open(cpp_file, "w") as f:
                f.write(code)

            compile = subprocess.run(
                ["g++", cpp_file, "-o", exe_file],
                capture_output=True,
                text=True
            )

            if compile.returncode != 0:
                return compile.stderr

            run = subprocess.run(
                [exe_file],
                capture_output=True,
                text=True,
                timeout=5
            )

            return run.stdout or run.stderr
    except Exception as e:
        return str(e)


# ================= C =================
def run_c(code):
    try:
        with tempfile.TemporaryDirectory() as temp:
            c_file = f"{temp}/main.c"
            exe_file = f"{temp}/a.out"

            with open(c_file, "w") as f:
                f.write(code)

            compile = subprocess.run(
                ["gcc", c_file, "-o", exe_file],
                capture_output=True,
                text=True
            )

            if compile.returncode != 0:
                return compile.stderr

            run = subprocess.run(
                [exe_file],
                capture_output=True,
                text=True,
                timeout=5
            )

            return run.stdout or run.stderr
    except Exception as e:
        return str(e)


# ================= NODE JS =================
def run_node(code):
    try:
        result = subprocess.run(
            ["node", "-e", code],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)


# ================= HTML (preview only) =================
def run_html(code):
    return code


# ================= CSS (preview only) =================
def run_css(code):
    return f"<style>{code}</style><div>CSS Loaded Successfully</div>"