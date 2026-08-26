## 2026-08-26
- systemd unit: route through the broker (allow_origin='*' for the broker's legitimate Host rewrite), drop the direct-nginx-auth assumption (sess-20260825-1938-f6bd411e)

- shipped v0: real ipykernel.kernelbase.Kernel subclass compiling+running PARENA cells via parena build + gcc; live behind jewel-jupyter.service (persistent user systemd, 127.0.0.1:8890) (sess-20260825-1938-f6bd411e)

