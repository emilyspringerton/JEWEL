## 2026-08-28

- SARENA_NOTEBOOK v0: real custom PARENA notebook frontend (notebook/index.html) against the live JEWEL kernel, TYLER-style title cards, note cells, verified end-to-end. commit f697c89. (sess-20260825-1938-f6bd411e)

## 2026-08-26
- systemd unit: route through the broker (allow_origin='*' for the broker's legitimate Host rewrite), drop the direct-nginx-auth assumption (sess-20260825-1938-f6bd411e)

- shipped v0: real ipykernel.kernelbase.Kernel subclass compiling+running PARENA cells via parena build + gcc; live behind jewel-jupyter.service (persistent user systemd, 127.0.0.1:8890) (sess-20260825-1938-f6bd411e)

