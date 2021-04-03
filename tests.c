#include <stdio.h>
#include <math.h>
#include <stdint.h>

void hello(float_t i){
    float_t f = sin(i);
    printf("this is the value: sin(%f) = %f\n", f, i);
}
