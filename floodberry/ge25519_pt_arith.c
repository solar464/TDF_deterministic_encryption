#include "ge25519_pt_arith.h"
const bignum25519 BIG_ONE = {1,0,0,0,0};
const ge25519 ZERO_PT = { .x = {0,0,0,0,0}, 
                          .y = {1,0,0,0,0}, 
                          .z = {1,0,0,0,0}, 
                          .t = {0,0,0,0,0}};

void ge25519_scalarmult_base(ge25519 *r, bignum256modm s) {
  ge25519_scalarmult_base_niels(r, ge25519_niels_base_multiples, s);
}

//copied from donna-impl-base ge25519_double_scalarmult_vartime
void ge25519_scalarmult(ge25519 *r, const ge25519 *p1, const bignum256modm s1) {
  signed char slide1[256];
  ge25519_pniels pre1[S1_TABLE_SIZE];
  ge25519 d1;
  ge25519_p1p1 t;
  int32_t i;

  contract256_slidingwindow_modm(slide1, s1, S1_SWINDOWSIZE);

  ge25519_double(&d1, p1);
  ge25519_full_to_pniels(pre1, p1);
  for (i = 0; i < S1_TABLE_SIZE - 1; i++)
    ge25519_pnielsadd(&pre1[i+1], &d1, &pre1[i]);

  /* set neutral */
  memset(r, 0, sizeof(ge25519));
  r->y[0] = 1;
  r->z[0] = 1;

  i = 255;
  while ((i >= 0) && !(slide1[i]))
    i--;

  for (; i >= 0; i--) {
    ge25519_double_p1p1(&t, r);

    if (slide1[i]) {
      ge25519_p1p1_to_full(r, &t);
      ge25519_pnielsadd_p1p1(&t, r, &pre1[abs(slide1[i]) / 2], (unsigned char)slide1[i] >> 7);
    }

    ge25519_p1p1_to_partial(r, &t);
  }
  //partial to full
  curve25519_mul(r->t, r->x, r->y);
  curve25519_mul(r->x, r->x, r->z);
  curve25519_mul(r->y, r->y, r->z);
  curve25519_square(r->z, r->z);
}

void ge25519_to_affine(ge25519 *p) {
  if(bignum_eq(p->z, BIG_ONE))
    return;
 
  bignum25519 zi;
  curve25519_recip(zi, p->z);
  curve25519_mul(p->x, p->x, zi);
  curve25519_mul(p->y, p->y, zi);
  curve25519_mul(p->t, p->x, p->y);
  curve25519_copy(p->z, BIG_ONE);
}

bool bignum_eq(const bignum25519 a, const bignum25519 b) {
  return (a[0] == b[0]) && 
         (a[1] == b[1]) && 
         (a[2] == b[2]) && 
         (a[3] == b[3]) &&
         (a[4] == b[4]);
}

bool ge25519_eq(const ge25519 *a, const ge25519 *b) {
  return bignum_eq(a->x,b->x) && bignum_eq(a->y, b->y) && bignum_eq(a->z, b->z);
}

bool ge25519_validate(const ge25519 *a) {
  /*
    -x^2 + y^2 = 1 + dx^2y^2
    Z^2(-X^2 + Y^2) = Z^4 + dX^2Y^2
  */
  bignum25519 temp;

  bignum25519 xy, zt;
  curve25519_mul(xy, a->x, a->y);
  curve25519_mul(zt, a->z, a->t);
  if (!bignum_eq(xy, zt))
    return false;

  bignum25519 x2, y2, z2, x2y2, z4;
  bignum25519 left, right;
  
  curve25519_square(x2, a->x);
  curve25519_square(y2, a->y);
  curve25519_mul(x2y2, x2, y2);
  curve25519_square(z2, a->z);
  curve25519_square(z4, z2);
  
  curve25519_sub_reduce(temp, y2, x2);
  curve25519_mul(left, z2, temp);

  curve25519_mul(temp, ge25519_ecd, x2y2);
  curve25519_add_reduce(right, temp, z4);

  return bignum_eq(left, right);   
}

void ge25519_copy(ge25519* r, const ge25519* p) {
  curve25519_copy(r->x, p->x);
  curve25519_copy(r->y, p->y);
  curve25519_copy(r->z, p->z);
  curve25519_copy(r->t, p->t);
}
/*
void scale_pt(ge25519 *r, const ge25519 *p, const bignum256modm s) {
  signed char exp[256];
  contract256_slidingwindow_modm(exp, s, 2); 
  
  ge25519 base;
  ge25519_double(&base, p); 
  
  ge25519 subresult;
  ge25519_add(&subresult, 
              exp[1] ? &base : &ZERO_PT, 
              exp[0] ? p: &ZERO_PT);

  for (int i = 2; i < 252; i++) {
    ge25519_double(&base, &base);
    ge25519_add(&subresult, &subresult, exp[i] ? &base : &ZERO_PT);
  }

  ge25519_double(&base, &base);
  ge25519_add(r, &subresult, exp[252] ? &base : &ZERO_PT);
}

void scale_pt_fast(ge25519 *r, const ge25519 *p, const bignum256modm s) {
  signed char exp[256];
  contract256_slidingwindow_modm(exp, s, 2); 
  
  ge25519 base;
  memcpy(&base, p, sizeof(ge25519));

  ge25519 subresult;
  memcpy(&subresult, exp[0] ? p: &ZERO_PT, sizeof(ge25519));

  for (int i = 1; i < 252; i++) {
    ge25519_double(&base, &base);
    if(exp[i])
      ge25519_add(&subresult, &subresult, &base);
  }

  if(exp[252]) {
    ge25519_double(&base, &base);
    ge25519_add(r, &subresult, &base);
  } else {
    memcpy(r, &subresult, sizeof(ge25519));
  }
}
*/
