#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "great_game.h"

#define MAXW 12     /* up to 100 decimal digits ≃ 333 bits ≃ 11 limbs */

typedef struct { int l; uint32_t d[MAXW]; } BI;

/* trim leading zero‑limbs */
static void bn(BI*a){
  while(a->l>1 && a->d[a->l-1]==0) {a->l--;}
}

/* duplicate a C string */
static char* dupstr(const char*s){
  char*x=malloc(strlen(s)+1);
  strcpy(x,s);
  return x;
}

/* parse decimal into big‑int: a = a*10 + digit */
static void from_dec(const char*s, BI*a){
  a->l=1; a->d[0]=0;
  for(;*s;s++){
    uint32_t c = *s - '0';
    uint64_t carry = 0;
    for(int i=0;i<a->l;i++){
      uint64_t t = (uint64_t)a->d[i]*10 + carry;
      a->d[i] = (uint32_t)t;
      carry  = t >> 32;
    }
    if(carry) {a->d[a->l++] = (uint32_t)carry;}
    carry = c;
    for(int i=0;i<a->l;i++){
      uint64_t t = (uint64_t)a->d[i] + carry;
      a->d[i] = (uint32_t)t;
      carry  = t >> 32;
      if(!carry) {break;}
    }
    if(carry) {a->d[a->l++] = (uint32_t)carry;}
  }
}

/* divide by small v, return remainder */
static uint32_t div_small(BI*a, uint32_t v){
  uint64_t rem = 0;
  for(int i=a->l-1;i>=0;i--){
    uint64_t t = (rem<<32) | a->d[i];
    a->d[i] = (uint32_t)(t / v);
    rem       = t % v;
  }
  bn(a);
  return (uint32_t)rem;
}

/* compare two big‑ints */
static int cmpBI(const BI*a,const BI*b){
  if(a->l!=b->l) {return a->l<b->l?-1:1;}
  for(int i=a->l-1;i>=0;i--){
    if(a->d[i]!=b->d[i]) {
        return a->d[i]<b->d[i]?-1:1;
    }
  }
  return 0;
}

/* a = a - b  (assumes a>=b) */
static void subBI(BI*a,const BI*b){
  uint64_t br=0;
  for(int i=0;i<a->l;i++){
    uint64_t ai=a->d[i],
             bi=(i<b->l?b->d[i]:0),
             t;
    if(ai<bi+br){
      t = ai + ((uint64_t)1<<32) - bi - br;
      br=1;
    } else {
      t = ai - bi - br;
      br=0;
    }
    a->d[i]=(uint32_t)t;
  }
  bn(a);
}

/* a = a + b */
static void addBI(BI*a,const BI*b){
  uint64_t cr=0;
  int i=0;
  for(; i<a->l||i<b->l; i++){
    uint64_t ai=(i<a->l?a->d[i]:0),
             bi=(i<b->l?b->d[i]:0),
             t=ai+bi+cr;
    if(i<a->l) {a->d[i]=(uint32_t)t;}
    else        {a->d[a->l++]=(uint32_t)t;}
    cr = t>>32;
  }
  if(cr) {a->d[a->l++]=(uint32_t)cr;}
}

/* shift right by 1 bit */
static void shr1(BI*a){
  uint32_t c=0;
  for(int i=a->l-1;i>=0;i--){
    uint32_t nc=a->d[i]&1;
    a->d[i]=(a->d[i]>>1)|(c<<31);
    c=nc;
  }
  bn(a);
}

/* r = (a + b) mod m */
static void modadd(const BI*a,const BI*b,const BI*m,BI*r){
  *r = *a;
  addBI(r,b);
  if(cmpBI(r,m)>=0) {subBI(r,m);}
}

/* r = (a * b) mod m via double‑and‑add */
static void modmul(const BI*a,const BI*b,const BI*m,BI*r){
  BI x=*a, y=*b, s;
  s.l=1; s.d[0]=0;
  while(y.l>1||y.d[0]){
    if(y.d[0]&1){
      BI t; modadd(&s,&x,m,&t);
      s = t;
    }
    BI t; modadd(&x,&x,m,&t);
    x = t;
    shr1(&y);
  }
  *r = s;
}

/* r = 2^k mod m */
static void modpow2(const BI*k,const BI*m,BI*r){
  BI res;  res.l=1; res.d[0]=1;
  BI base; base.l=1; base.d[0]=2;
  BI e = *k;
  while(e.l>1||e.d[0]){
    if(e.d[0]&1){
      BI t; modmul(&res,&base,m,&t);
      res = t;
    }
    BI t; modmul(&base,&base,m,&t);
    base = t;
    shr1(&e);
  }
  *r = res;
}

/* convert BI to decimal string */
static char* tostr(const BI*a){
  if(a->l==1 && a->d[0]==0) {return dupstr("0");}
  char buf[350]; int p=0;
  BI t = *a;
  while(t.l>1 || t.d[0]){
    uint32_t d = div_small(&t,10);
    buf[p++] = '0' + d;
  }
  char*x=malloc(p+1);
  for(int i=0;i<p;i++) {x[i]=buf[p-1-i];}
  x[p]=0;
  return x;
}

char *num_ways(const char *n,const char *m){
  BI N,M;
  /* if n%3!=0, no tiling */
  from_dec(n,&N);
  if(div_small(&N,3)!=0) {return dupstr("0");}
  BI K = N;
  /* parse modulus */
  from_dec(m,&M);
  /* compute 2^K mod M */
  BI R;
  modpow2(&K,&M,&R);
  return tostr(&R);
}

int main(){
    printf("%s\n", num_ways("2","2")); // Example said it should be 2
    printf("%s\n", num_ways("1","2")); // 2x1 board => 1 way
    printf("%s\n", num_ways("3","2")); // 2x3 board => F4=3 ways
    printf("%s\n", num_ways("3","33")); // 2x3 board => F4=3 ways

    // Very large test:
    // e.g. 2 x 100 => F101 has 21 digits, etc.
    return 0;
}
