# ursa_bbs_python

## Build Instructions

Currently requires Rust nightly (`rustup toolchain install nightly`).

```sh
cargo build
cp target/debug/{libursa_bbs.dylib,libursa_bbs.so,ursa_bbs.dll} ursa_bbs.so
python test.py
```

Python wheel packages can be built as follows:

```sh
pip install maturin
maturin build
```

Effectively:
```
"""
!curl https://sh.rustup.rs -sSf | sh -s -- -y && \
. $HOME/.cargo/env && \
cargo --version && \
git clone https://github.com/ursa-mikail/ursa_bbs_python.git && \
cd ursa_bbs_python && \
cargo build
"""

"""
!cp ursa_bbs_python/target/debug/libursa_bbs.so ursa_bbs_python/ursa_bbs.so
!python3 ursa_bbs_python/test.py
"""
```
