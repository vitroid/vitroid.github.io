/*Cantor set -> sound*/
#include <stdio.h>

int main(int argc,char *argv[])
{
    char *buf;
    int n,i,d;
    if(argc!=2)
      {
	  fprintf(stderr,"usage: %s depth\n",argv[0]);
	  exit(1);
      }
    d=atoi(argv[1]);
    n=1;
    for(i=1;i<d;i++)
      n*=3;
    buf=calloc(n,sizeof(char));
    buf[0]=255;
    n=1;
    for(i=1;i<d;i++)
      {
	  int j;
	  for(j=0;j<n;j++)
	    buf[j+n*2]=buf[j];
	  n*=3;
      }
#ifdef VERBOSE
    for( i=0; i<n; i++ ){
        printf( "%u\n", buf[i] );
    }
#else
    fwrite(buf,sizeof(char),n,stdout);
#endif
    exit (0);
}

	  
	  
