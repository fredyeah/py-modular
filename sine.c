#include <stdio.h>
#include <math.h>
#include <stdint.h>
#include "portaudio.h"

#define PI          (float_t)(3.141592)
#define TWOPI       (float_t)(PI * 2.0)

void sine(void){
    printf("sine");
}

float_t sine_node(float_t freq, float_t time){
    return (freq * time * TWOPI);
}
