# GitHub save path check

Verification save of a gcd function, made to prove the Save on GitHub button on aienos.com/aien/ works.

gcd.om is scalar Omega in IR mode. To build it with the pinned seeded compiler and the IR to WebAssembly translator:

```sh
{ printf 'ir\n'; cat gcd.om; } | omc > gcd.ir
irwasm < gcd.ir > gcd.wasm
```

Learn about Omega: https://www.aienos.com/omega/
