#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#include <sys/types.h>

#define AUDIOTYPE int16_t
#define AUDIOMAX  32767

AUDIOTYPE* sierpinski( int max )
{
    int i;
    int x[max+2];
    AUDIOTYPE* value;
    value = malloc( sizeof(AUDIOTYPE) * max );
    
    for(i=0;i<max+2;i++){
        x[i] = 0;
    }
    
    x[1] = 1;
    
    value[0] = 1;
    for(i=1;i<max;i++){
        int j;
        int n=0;
        for( j = max+1; 1 <= j; j-- ){
            x[j] ^= x[j-1];
            if ( x[j] ) n++;
#ifdef VERBOSE
            fprintf( stderr, "%d", x[j] );
#endif
        }
#ifdef VERBOSE
        fprintf( stderr, "\n" );
#endif
        value[i] = n;
    }
    return value;
}


int main(int argc, char* argv[])
{
    int len;
    int i;
    AUDIOTYPE* value;
    
    if ( argc == 2 ){
        len = atoi( argv[1] );
    }
    else{
        len = 32767;
    }
    if ( 32767 < len ){
        exit(1);
    }
    
    value = sierpinski( len );
#ifdef VERBOSE
    for( i=0; i<len; i++ ){
        printf( "%d\n", value[i] );
    }
#else
    fwrite(value, sizeof(AUDIOTYPE), len, stdout);
#endif
    exit(0);
    
}

