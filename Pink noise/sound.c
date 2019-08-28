/*
 * Generate pink and brown noise by partial-rank integration
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "ft.h"
#include <unistd.h>

#define AUDIOTYPE unsigned short
#define AUDIOMAX  65535

#define A .009765625
#define N 65536
#define PW 16
#define PI 3.14159265358
#define B (1.0/(A*N))
void ftinit();
void fft(double *x,double *y);
void rft(double *x,double *y);

double sine[PW],cosine[PW];

void ftinit()
{
    int i;
    double x=PI;
    for(i=0;i<PW;i++)
      {
	  cosine[i]=cos(x);
	  sine[i]=sin(x);
	  x*=0.5;
      }
}

void	fft(double *x,double *y)
{
    int	i,i0,i1,j,l1,ns,n1,k;
    double	s,c,s1,c1,x1,y1,t,tmp;
    int	q;
    
    n1=N/2;
    q=0;
    
    j=0;
    for(i=0;i<N-1;i++){
	if(i<=j)
	  {
	      tmp=x[i];
	      x[i]=x[j];
	      x[j]=tmp;
	      tmp=y[i];
	      y[i]=y[j];
	      y[j]=tmp;
	  }
	
	k=N/2;
	while(k<=j)
	  j-=k,k/=2;
	j+=k;
    }
    
    ns=1;
    while(ns<=N/2){
	c1=cosine[q];
	s1=-sine[q];
	c=1;
	s=0;
	for(l1=0;l1<ns;l1++){
	    for(i0=l1;i0<N;i0+=(2*ns)){
		i1=i0+ns;
		x1=x[i1]*c-y[i1]*s;
		y1=y[i1]*c+x[i1]*s;
		x[i1]=x[i0]-x1;
		y[i1]=y[i0]-y1;
		x[i0]+=x1;
		y[i0]+=y1;
	    }
	    t=c1*c-s1*s;
	    s=s1*c+c1*s;
	    c=t;
	}
	ns*=2;
	q++;
    }
    for(i=0;i<N;i++)
      x[i]/=(double)N,y[i]/=(double)N;
}

void	rft(double *x,double *y)
{
    int	i,i0,i1,j,l1,ns,n1,k;
    double	s,c,s1,c1,x1,y1,t,tmp;
    int	q;
    
    n1=N/2;
    q=0;
    
    j=0;
    for(i=0;i<N-1;i++){
	if(i<=j)
	  {
	      tmp=x[i];
	      x[i]=x[j];
	      x[j]=tmp;
	      tmp=y[i];
	      y[i]=y[j];
	      y[j]=tmp;
	  }
	
	k=N/2;
	while(k<=j)
	  j-=k,k/=2;
	j+=k;
    }
    
    ns=1;
    while(ns<=N/2){
	c1=cosine[q];
	s1=sine[q];
	c=1;
	s=0;
	for(l1=0;l1<ns;l1++){
	    for(i0=l1;i0<N;i0+=(2*ns)){
		i1=i0+ns;
		x1=x[i1]*c-y[i1]*s;
		y1=y[i1]*c+x[i1]*s;
		x[i1]=x[i0]-x1;
		y[i1]=y[i0]-y1;
		x[i0]+=x1;
		y[i0]+=y1;
	    }
	    t=c1*c-s1*s;
	    s=s1*c+c1*s;
	    c=t;
	}
	ns*=2;
	q++;
    }
}


int main(int argc,char *argv[])
{
    int i;
    double r,x[N],y[N],alpha,max,min,width;
    AUDIOTYPE out[N];
    ftinit();
    srand48(getpid());
    if(argc!=2)
	{
	    fprintf(stderr,"usage : %s alpha\n\tProduce a noise with 1/f^alpha power spectrum\n",argv[0]);
	    exit(1);
	}
    alpha = -atof(argv[1])*0.5;
    
    for(i=1;i<N;i++)
      {
	  double intensity = exp(alpha*log((double)i));
	  double phase = drand48()*2.0*3.14159265358L;
	  x[i]=intensity*sin(phase);
	  y[i]=intensity*cos(phase);
      }
    rft(x,y);
    max=min=0;
    for(i=0;i<N;i++)
	{
	    if(x[i]>max)max=x[i];
	    if(x[i]<min)min=x[i];
	}
    width = AUDIOMAX/(max-min);
    for(i=0;i<N;i++)
	out[i] = (AUDIOTYPE)((x[i]-min)*width);
#ifdef VERBOSE
    for(i=0;i<N;i++)
	printf("%u\n",out[i]);
#else
    fwrite(out,sizeof(AUDIOTYPE),N,stdout);
#endif
    exit (0);
}
