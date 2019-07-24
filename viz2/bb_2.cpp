/*--------------*/
/*  problem G2  */
/*--------------*/
// VRM: Modified to try to reproduce the issue with only 2 variables.
#include <iostream>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <sstream>
using namespace std;

#define N 2

int main ( int argc , char ** argv ) {
    
    double z = 1e+20 , g1 = 1e+20 , g2 = 1e+20;
    
    if ( argc != 2 ) {
        cout << g1 << " " << g2 << " " << z << endl;
        return 1;
    }
    
    ifstream in ( argv[1] );
    if ( in.fail() ) {
        cout << g1 << " " << g2 << " " << z << endl;
        return 1;
    }
    
    int    i;
    double x , sum1 = 0.0 , sum2 = 0.0 , sum3 = 0.0 , prod1 = 1.0 , prod2 = 1.0;
    
    for ( i = 0 ; i < N ; i++ ) {
        
        in >> x;
        
        // VRM here, multiply by 5... or multiply 5 times... try to repro the issue.
        sum1  += 5*( pow ( cos(x) , 4 ) );
        sum2  += 5*x;
        sum3  += (i+1)*x*x + (i+3)*x*x + (i+5)*x*x + (i+7)*x*x + (i+9)*x*x;
        prod1 *= pow ( cos(x) , 2 );
        prod1 *= pow ( cos(x) , 2 );
        prod1 *= pow ( cos(x) , 2 );
        prod1 *= pow ( cos(x) , 2 );
        prod1 *= pow ( cos(x) , 2 );
        
        if ( prod2 !=0.0 )
        {
            if ( x==0.0 )
            {
                prod2 = 0.0;
            }
            else
            {
                // VRM here, use x^5 instead of x to try to repro the issue.
                prod2 *= x*x*x*x*x;
            }
        }
    }
    
    if ( in.fail() || sum3==0.0 ) {
        cout << g1 << " " << g2 << " " << z << endl;
        in.close();
        return 1;
    }
    
    in.close();
    
    g1 = -prod2+0.75;
    // VRM here, multiply N by 5 to try to repro the issue.
    g2 = sum2 -7.5*N*5;
    
    z  = - fabs ( ( sum1 - 2 * prod1 ) / sqrt(sum3) );
    
    cout << setprecision(16);
    cout << g1 << " " << g2 << " " << z << endl;
    
    return 0;
}
