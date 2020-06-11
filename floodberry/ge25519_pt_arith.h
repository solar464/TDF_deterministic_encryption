#include <stdbool.h>
#include "donna/ed25519-donna.h"

void ge25519_to_affine(ge25519 *p);
void ge25519_scalarmult_base(ge25519 *r, bignum256modm s);
void ge25519_scalarmult(ge25519 *r, const ge25519 *p, const bignum256modm s);

bool bignum_eq(const bignum25519 a, const bignum25519 b);
bool ge25519_eq(const ge25519 *a, const ge25519* b);
bool ge25519_validate(const ge25519 *a);
void ge25519_copy(ge25519* r, const ge25519* p);
