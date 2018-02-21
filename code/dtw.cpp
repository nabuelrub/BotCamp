

#include "mex.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#define inf 1e19;


double dtw_G(double *s, double *t, int w, int ns, int nt , int *len)
{
    double d=0;
       int sizediff=ns-nt>0 ? ns-nt : nt-ns;
    double * D , *P , *T , *tttmp , * M , *MP;
    int i,j,tttml,j1,j2,k;

    double cost,temp;
    if(w!=-1 && w<sizediff) w=sizediff; 
    
    //Take the longer signal in S
    if( nt > ns )
    {
        tttmp = s;
        s = t;
        t = tttmp;
        tttml = ns;
        ns = nt;
        nt = tttml;
    }
    
     
     
    D =(double *)malloc((nt+1)*sizeof(double));
    P =(double *)malloc((nt+1)*sizeof(double));
    M =(double *)malloc((nt+1)*sizeof(double));
    MP =(double *)malloc((nt+1)*sizeof(double));
    
    
    for(i=0;i<nt+1;i++)
    {
       P[i]= inf;
       D[i] = inf;
       M[i] = 0;
       MP[i] = 0;
    }

       //printf("%d",w);
    P[0]=0;
    D[0]=inf;
    for(i=1;i<=ns;i++)
    {
  
        if(w==-1)
        {
            j1=1;
            j2=nt;
        }
        else
        {
            j1= i-w>1 ? i-w : 1;
            j2= i+w<nt ? i+w : nt;
        }
        
         D[j1-1] = inf;
         M[j1-1] = inf;

        for(j=j1;j<=j2;j++)
        {
            cost= (s[i-1]-t[j-1])*(s[i-1]-t[j-1]);
            
            if( P[j] < P[j-1] )
                temp = P[j]; 
            else
                temp = P[j-1];
            
            if(temp > D[j-1])
            { 
                temp=D[j-1];
                M[j] = M[j-1]+1; 
            }
            else if( P[j] < P[j-1] ) 
            {
                M[j] = MP[j] + 1;
            }
            else
            {
                M[j] = MP[j-1] + 1;
            }
            
            
            D[j]=cost+temp;
        }

       //Swap D and P , swap M and MP. P means prior. D means Data and M means 
        T = P;
        P = D;
        D = T;
        T = MP;
        MP = M;
        M = T;

    }
    

    d=sqrt(P[nt]);
    *len = MP[nt];
    
    
    free(D);
    free(P);
    free(M);
    free(MP);


    return d;//(double)matchLength;
}


void mexFunction( int nlhs, mxArray *plhs[],
        int nrhs, const mxArray *prhs[])
{
    double *s,*t;
    int w;
    int ns,nt,len;
    double *dp;
    
    
    if(nrhs!=2&&nrhs!=3)
    {
        mexErrMsgIdAndTxt( "MATLAB:dtw_c:invalidNumInputs",
                "Two or three inputs required.");
    }
    if(nlhs>1)
    {
        mexErrMsgIdAndTxt( "MATLAB:dtw_c:invalidNumOutputs",
                "dtw_c: One output required.");
    }
    
    
    if(nrhs==2)
    {
        w=-1;
    }
    else if(nrhs==3)
    {
        if( !mxIsDouble(prhs[2]) || mxIsComplex(prhs[2]) ||
                mxGetN(prhs[2])*mxGetM(prhs[2])!=1 )
        {
            mexErrMsgIdAndTxt( "MATLAB:dtw_c:wNotScalar",
                    "dtw: Input W must be a scalar.");
        }
        
       
        w = (int) mxGetScalar(prhs[2]);
    }
    
    
    
    s = mxGetPr(prhs[0]);
    
    t = mxGetPr(prhs[1]);
    
    ns = mxGetM(prhs[0])*mxGetN(prhs[0]);
    
    nt = mxGetM(prhs[1])*mxGetN(prhs[1]);
    
    plhs[0] = mxCreateDoubleMatrix( 1, 2, mxREAL);
    
    dp = mxGetPr(plhs[0]);
    
    dp[0]=dtw_G(s,t,w,ns,nt,&len);
    dp[1] = len;
    
    return;
    
}
