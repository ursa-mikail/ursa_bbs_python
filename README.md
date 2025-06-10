# ursa_bbs_python

## Pairing-Based Cryptography and Group Signatures

The method uses a group signature approach with bi-linear maps. This produces a signature that is around the same size of the RSA signature (around 200 bytes). 

With elliptic curve pairing-based cryptography, we have two cyclic groups: $$\( 𝔾_1 \)$$ and $$\( 𝔾_2 \)$$, which are both of prime order $$\( n \)$$. A pairing on $$\((G_1, G_2, G_T)\)$$ defines a function:

$$
e : G_1 \times G_2 \rightarrow G_T
$$

Let $$\( g_1 \)$$ be a generator for $$\( G_1 \)$$, and $$\( g_2 \)$$ be a generator for $$\( G_2 \)$$. If we have points:

$$\( U_1, U_2 \in G_1 \)$$  
$$\( V_1, V_2 \in G_2 \)$$

If we have the points of $$\ U1 \$$ and $$\ U2 \$$ on $$\ 𝔾𝟙 \$$ and $$\ V1 $$ and $$\ V2 \$$ on $$\ 𝔾𝟚 \$$, Then we get the bilinear mappings:

$$
e(U_1 + U_2, V_1) = e(U_1, V_1) \cdot e(U_2, V_1)
$$

$$
e(U_1, V_1 + V_2) = e(U_1, V_1) \cdot e(U_1, V_2)
$$

If $$\ U \$$ is a point on $$\ 𝔾_𝟙 \$$, and $$\ V \$$ is a point on $$\ 𝔾_𝟚 \$$, we get:
$$\ ê (aU,bV) = ê (U,V)^{ab} \$$ 

Within BBS, using elliptic curve pairs, we have $$\ 𝔾_𝟙 \$$ and $$\ 𝔾_𝟚 \$$ which are BN256 curves, and these map to $$\ 𝔾_𝕋 \$$, and which is also on a BN256 curve. This is the pairing function.

---

## Group Signatures

Can we produce a **digital signature** for a group of members such that it is **not possible to know who signed** within the group?

This problem was solved in **2004** with **BBS signatures**, defined by Boneh, Boyen, and Shacham in [1].

The methods were then advanced by Camenisch and Lysyanakaya, and where modern implementations are based on methods such as [2].

For example, the government could digitally sign a whole lot of attributes about Alice, such as her gender, her name, her address, her telephone number and her ID number. Then, Alice can create zero-knowledge proofs about the signature when selecting revealing parts of his signed identity. In this way, Alice has control over which part of her identity she reveals. For example, if she just has to reveal his telephone number for a credit card application, she can selectively reveal just that part, but where the rest is masked off. The verifier will still be able to check that the credential has been signed by the government.



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
# Generating the signature

We initially create a private key (`sk`) of `x`:
sk = x

The public key is then:
$$ pk = x.G_2 $$

and where `G2` is the base point on curve.

## Generate the signature

Next we take the message of `M1`, `M2`, ... `Mn` to produce `m1`, `m2` ... `mn`. We can then hash each of these to give the elliptic points of `m1.H1`, `m2.H2` ... `mn.Hn`, and where `H1` ... `Hn` are on the $$ 𝔾_𝟙 $$ curve, and are known points by everyone involved in the signature.

We then compute with point of:
c = G1 + ∑i mi.Hi

text

This will be a point on 𝔾𝟙 curve. Next, we generate a random value of `e`, and then compute:
A = 1/(x + e).c

text

The signature is then:
σ = (A, e)

text

## Verify the signature

To verify, we test the pairing of:
ê (A, e.G2 + pk) = ê (c, G2)

text

This works because:
ê (1/(x + e).c, e.G2 + x.G2) = ê (c, G2)^(1/(x + e)(x + e)) = ê (c, G2)

text

Overall, the verifier will have to rebuild the value of `c` to verify the signature.

---

## Coding

In this example:

- A message is hashed using **SHA-256**.
- The resulting digest is signed using the **group private key**.

### References

[1] Dan Boneh, Xavier Boyen, and Hovav Shacham. (2004, August). Short group signatures. In Annual International Cryptology Conference (pp. 41-55). Springer, Berlin, Heidelberg.

[2] Tessaro, S., & Zhu, C. (2023, April). Revisiting BBS signatures. In Annual International Conference on the Theory and Applications of Cryptographic Techniques (pp. 691-721). Cham: Springer Nature Switzerland.

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
