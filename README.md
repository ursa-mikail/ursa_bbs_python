# ursa_bbs_python

## Pairing-Based Cryptography and Group Signatures

With pairing-based cryptography, we have two cyclic groups: $$\( G_1 \)$$ and $$\( G_2 \)$$, which are both of prime order $$\( n \)$$. A pairing on $$\((G_1, G_2, G_T)\)$$ defines a function:

$$
e : G_1 \times G_2 \rightarrow G_T
$$

Let $$\( g_1 \)$$ be a generator for $$\( G_1 \)$$, and $$\( g_2 \)$$ be a generator for $$\( G_2 \)$$. If we have points:

$$\( U_1, U_2 \in G_1 \)$$  
$$\( V_1, V_2 \in G_2 \)$$

Then we get the bilinear mappings:

$$
e(U_1 + U_2, V_1) = e(U_1, V_1) \cdot e(U_2, V_1)
$$

$$
e(U_1, V_1 + V_2) = e(U_1, V_1) \cdot e(U_1, V_2)
$$


---

## Group Signatures

Can we produce a **digital signature** for a group of members such that it is **not possible to know who signed** within the group?

This problem was solved in **2004** with **BBS signatures**, defined by Boneh, Boyen, and Shacham in [1].

In a group signature scheme:

- Each **member** has a **private key**.
- The **signature** does not reveal the **signer’s public key**.
- A **group manager** is responsible for managing the group, issuing keys, and tracing signatures if needed.

---

## Key Features of Group Signatures

- **Soundness and Completeness**: Valid signatures are always accepted; invalid ones are always rejected.
- **Unforgeability**: Only group members can generate valid signatures.
- **Anonymity**: The identity of the signer remains hidden, unless revealed by the group manager.
- **Traceability**: The group manager can reveal the signer using their secret key.
- **Unlinkability**: It’s not possible to tell if two signatures came from the same signer.
- **Coalition Resistance**: Signatures cannot be generated without at least one group member’s consent.

---

## Revocation and Group Management

- A **group private key** can generate member keys and reveal signers.
- If a member must be revoked, a **public revocation** is made.
- A new group key may be issued to update the group membership.

---

## Coding

In this example:

- A message is hashed using **SHA-256**.
- The resulting digest is signed using the **group private key**.

References
[1] Dan Boneh, Xavier Boyen, and Hovav Shacham. (2004, August). Short group signatures. In Annual International Cryptology Conference (pp. 41-55). Springer, Berlin, Heidelberg.

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
