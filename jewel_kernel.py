"""jewel_kernel.py -- a real ipykernel.kernelbase.Kernel subclass for PARENA.

Real, working v0 (see CLAUDE.md's own "How It Works" section for the full design note).
Each cell must define one entry point:

    (defn cell-main [(dest : Arena @ Region)] : Unit
      ...)

do_execute compiles that cell (real `parena build`, real gcc link against
runtime/parena_runtime.c), runs the resulting binary with a real timeout (a hung/infinite-loop
cell can't wedge the kernel forever), and streams its real stdout/stderr back as the cell's own
output. `stdlib/log.prn`'s `info`/`warn`/`error` (stderr, "LEVEL msg\\n") is the real, already-
existing way to print something visible from a cell -- no new "print" primitive invented here
just for this kernel.

A real compile error (parena itself, or the rare case gcc rejects the emitted C) surfaces as a
real Jupyter error (ename/evalue/traceback), not swallowed or silently treated as "no output".
A non-zero exit from the compiled program is ALSO reported as a real error, with its own real
stderr as the traceback -- a crash is not success.
"""

import os
import re
import shutil
import subprocess
import tempfile

from ipykernel.kernelbase import Kernel

PARENA_ROOT = "/home/fatbaby/PARENA"
PARENA_BIN = os.path.join(PARENA_ROOT, "parena")
RUNTIME_C = os.path.join(PARENA_ROOT, "runtime", "parena_runtime.c")
RUNTIME_DIR = os.path.join(PARENA_ROOT, "runtime")

CELL_WRAPPER_C = """\
#include "parena_runtime.h"
void cell_main(Arena *dest);
int main(void) {
    Arena a;
    arena_init(&a);
    cell_main(&a);
    arena_free_all(&a);
    return 0;
}
"""

RUN_TIMEOUT_SEC = 10


class JewelKernel(Kernel):
    implementation = "JEWEL"
    implementation_version = "0.1.0"
    language = "parena"
    language_version = "0.0.0"
    language_info = {
        "name": "parena",
        "mimetype": "text/x-parena",
        "file_extension": ".prn",
    }
    banner = (
        "JEWEL -- a real Jupyter kernel for PARENA. Each cell needs a "
        "(defn cell-main [(dest : Arena @ Region)] : Unit ...) entry point. "
        "Use stdlib/log.prn's info/warn/error to print (stderr, real output -- "
        "no separate print primitive exists yet)."
    )

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False, *, cell_id=None
    ):
        if not code.strip():
            return {"status": "ok", "execution_count": self.execution_count, "payload": [], "user_expressions": {}}

        workdir = tempfile.mkdtemp(prefix="jewel_cell_")
        try:
            result = self._run_cell(code, workdir)
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

        if not silent:
            if result["stdout"]:
                self.send_response(self.iopub_socket, "stream", {"name": "stdout", "text": result["stdout"]})
            if result["stderr"]:
                self.send_response(self.iopub_socket, "stream", {"name": "stderr", "text": result["stderr"]})

        if result["ok"]:
            return {
                "status": "ok",
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }

        ename = result["ename"]
        evalue = result["evalue"]
        traceback = result["traceback"]
        if not silent:
            self.send_response(
                self.iopub_socket,
                "error",
                {"ename": ename, "evalue": evalue, "traceback": traceback},
            )
        return {
            "status": "error",
            "execution_count": self.execution_count,
            "ename": ename,
            "evalue": evalue,
            "traceback": traceback,
        }

    _IMPORT_RE = re.compile(r"\(import\s+([A-Za-z0-9_/-]+)\)")

    def _resolve_stdlib_imports(self, code):
        """Real, transitive (import X) -> stdlib/X.prn resolution.

        `parena build` does NOT auto-resolve imports across files -- every real build path in
        this monorepo (turbogrep's own Makefile target is the clearest example) lists every
        stdlib dependency explicitly, by hand. A notebook cell can't reasonably ask its own
        author to do that -- this walks (import ...) forms, including the ones INSIDE each
        resolved stdlib file itself (so importing "regex/pcre" also pulls in whatever IT
        imports, e.g. "string"), to a fixed point. Anything named that isn't a real file under
        stdlib/ is silently skipped -- parena build's own real "unbound identifier" error at
        compile time is the honest failure mode for a genuinely missing/misspelled import, not
        a guess here.
        """
        seen = set()
        worklist = list(self._IMPORT_RE.findall(code))
        resolved_paths = []
        while worklist:
            name = worklist.pop()
            if name in seen:
                continue
            seen.add(name)
            path = os.path.join(PARENA_ROOT, "stdlib", f"{name}.prn")
            if not os.path.isfile(path):
                continue
            resolved_paths.append(path)
            with open(path) as f:
                worklist.extend(self._IMPORT_RE.findall(f.read()))
        return resolved_paths

    def _run_cell(self, code, workdir):
        prn_path = os.path.join(workdir, "cell.prn")
        with open(prn_path, "w") as f:
            f.write(code)

        gen_c_path = os.path.join(workdir, "cell_gen.c")
        import_paths = self._resolve_stdlib_imports(code)
        compile_proc = subprocess.run(
            [PARENA_BIN, "build", *import_paths, prn_path, "-o", gen_c_path],
            capture_output=True,
            text=True,
        )
        if compile_proc.returncode != 0:
            msg = compile_proc.stderr.strip() or compile_proc.stdout.strip() or "parena build failed with no output"
            return {
                "ok": False,
                "stdout": "",
                "stderr": "",
                "ename": "ParenaCompileError",
                "evalue": msg,
                "traceback": [msg],
            }

        wrapper_c_path = os.path.join(workdir, "wrapper.c")
        with open(wrapper_c_path, "w") as f:
            f.write(CELL_WRAPPER_C)

        bin_path = os.path.join(workdir, "cell_bin")
        link_proc = subprocess.run(
            [
                "gcc", "-std=c99", "-O2", "-I", RUNTIME_DIR,
                gen_c_path, wrapper_c_path, RUNTIME_C,
                "-o", bin_path, "-lm",
            ],
            capture_output=True,
            text=True,
        )
        if link_proc.returncode != 0:
            msg = link_proc.stderr.strip() or "gcc failed with no output"
            return {
                "ok": False,
                "stdout": "",
                "stderr": "",
                "ename": "LinkError",
                "evalue": (
                    "gcc rejected the C parena emitted -- often a real cell mistake "
                    "(e.g. calling an undefined function; VS0's own parena build doesn't "
                    "validate every call target, only gcc's own linker catches an unresolved "
                    "reference), occasionally a real compiler bug. See the traceback for gcc's "
                    "own real error."
                ),
                "traceback": [msg],
            }

        try:
            run_proc = subprocess.run([bin_path], capture_output=True, text=True, timeout=RUN_TIMEOUT_SEC)
        except subprocess.TimeoutExpired:
            msg = f"cell-main did not return within {RUN_TIMEOUT_SEC}s -- killed (an infinite loop?)"
            return {
                "ok": False,
                "stdout": "",
                "stderr": "",
                "ename": "TimeoutError",
                "evalue": msg,
                "traceback": [msg],
            }

        if run_proc.returncode != 0:
            msg = f"cell-main exited with status {run_proc.returncode}"
            return {
                "ok": False,
                "stdout": run_proc.stdout,
                "stderr": run_proc.stderr,
                "ename": "RuntimeError",
                "evalue": msg,
                "traceback": [msg, run_proc.stderr.strip()] if run_proc.stderr.strip() else [msg],
            }

        return {"ok": True, "stdout": run_proc.stdout, "stderr": run_proc.stderr}


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp

    IPKernelApp.launch_instance(kernel_class=JewelKernel)
