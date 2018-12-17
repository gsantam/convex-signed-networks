/*  This file is part of libDAI - http://www.libdai.org/
 *
 *  Copyright (c) 2006-2011, The libDAI authors. All rights reserved.
 *
 *  Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
 */


#include <iostream>
#include <map>
#include <dai/alldai.h>  // Include main libDAI header file
#include <dai/jtree.h>
#include <dai/bp.h>
#include <dai/decmap.h>


using namespace dai;
using namespace std;

vector<string> split(string str, char delimiter) {
  vector<string> internal;
  stringstream ss(str); // Turn the string into a stream.
  string tok;
  
  while(getline(ss, tok, delimiter)) {
    internal.push_back(tok);
  }
  
  return internal;
}


int main( int argc, char *argv[] ) {
#if defined(DAI_WITH_BP) && defined(DAI_WITH_JTREE)
    if ( argc != 2 && argc != 3 ) {
        cout << "Usage: " << argv[0] << " <filename.fg> [maxstates]" << endl << endl;
        cout << "Reads factor graph <filename.fg> and runs" << endl;
        cout << "Belief Propagation, Max-Product and JunctionTree on it." << endl;
        cout << "JunctionTree is only run if a junction tree is found with" << endl;
        cout << "total number of states less than <maxstates> (where 0 means unlimited)." << endl << endl;
        return 1;
    } else {
        // Report inference algorithms built into libDAI
        cout << "Builtin inference algorithms: " << builtinInfAlgNames() << endl << endl;

        // Read FactorGraph from the file specified by the first command line argument
        FactorGraph fg;
        fg.ReadFromFile(argv[1]);
	
	string factorGraphName = split(argv[1], '.')[0];
	string exactMapOutput = factorGraphName + "Exact.comm";
	char * charExactMapOutput = new char [exactMapOutput.length()+1];
	std::strcpy (charExactMapOutput, exactMapOutput.c_str());
	
	
        size_t maxstates = 50000000;
        if( argc == 3 )
            maxstates = fromString<size_t>( argv[2] );

        // Set some constants
        size_t maxiter = 10000;
        Real   tol = 1e-9;
        size_t verb = 1;

        // Store the constants in a PropertySet object
        PropertySet opts;
        opts.set("maxiter",maxiter);  // Maximum number of iterations
        opts.set("tol",tol);          // Tolerance for convergence
        opts.set("verbose",verb);     // Verbosity (amount of output generated)

        // Bound treewidth for junctiontree
        bool do_jt = true;
        try {
            boundTreewidth(fg, &eliminationCost_MinFill, maxstates );
        } catch( Exception &e ) {
            if( e.getCode() == Exception::OUT_OF_MEMORY ) {
                do_jt = false;
                cout << "Skipping junction tree (need more than " << maxstates << " states)." << endl;
            }
            else
                throw;
        }

        JTree jt, jtmap;
        vector<size_t> jtmapstate;
        if( do_jt ) {
            // Construct a JTree (junction tree) object from the FactorGraph fg
            // using the parameters specified by opts and an additional property
            // that specifies the type of updates the JTree algorithm should perform
            jt = JTree( fg, opts("updates",string("HUGIN")) );
            // Initialize junction tree algorithm
            jt.init();
            // Run junction tree algorithm
            jt.run();

            // Construct another JTree (junction tree) object that is used to calculate
            // the joint configuration of variables that has maximum probability (MAP state)
            jtmap = JTree( fg, opts("updates",string("HUGIN"))("inference",string("MAXPROD")) );
            // Initialize junction tree algorithm
            jtmap.init();
            // Run junction tree algorithm
            jtmap.run();
            // Calculate joint state of all variables that has maximum probability
            jtmapstate = jtmap.findMaximum();
        }


        // Note that inference is set to MAXPROD, which means that the object
        // will perform the max-product algorithm instead of the sum-product algorithm
        BP mp(fg, opts("updates",string("SEQRND"))("logdomain",false)("inference",string("MAXPROD"))("damping",string("0.1")));
        // Initialize max-product algorithm
        mp.init();
        // Run max-product algorithm
        mp.run();
        // Calculate joint state of all variables that has maximum probability
        // based on the max-product result
        vector<size_t> mpstate = mp.findMaximum();


        if( do_jt ) {
            // Report variable marginals for fg, calculated by the junction tree algorithm
            cout << "Exact variable marginals:" << endl;
            for( size_t i = 0; i < fg.nrVars(); i++ ) // iterate over all variables in fg
                cout << jt.belief(fg.var(i)) << endl; // display the "belief" of jt for that variable
        }

        if( do_jt ) {
            // Report factor marginals for fg, calculated by the junction tree algorithm
            cout << "Exact factor marginals:" << endl;
            for( size_t I = 0; I < fg.nrFactors(); I++ ) // iterate over all factors in fg
                cout << jt.belief(fg.factor(I).vars()) << endl;  // display the "belief" of jt for the variables in that factor
        }

        if( do_jt ) {
            // Report log partition sum (normalizing constant) of fg, calculated by the junction tree algorithm
            cout << "Exact log partition sum: " << jt.logZ() << endl;
        }


        if( do_jt ) {
            // Report exact MAP variable marginals
            cout << "Exact MAP variable marginals:" << endl;
            for( size_t i = 0; i < fg.nrVars(); i++ )
                cout << jtmap.belief(fg.var(i)) << endl;
        }

        if( do_jt ) {
            // Report exact MAP factor marginals
            cout << "Exact MAP factor marginals:" << endl;
            for( size_t I = 0; I < fg.nrFactors(); I++ )
                cout << jtmap.belief(fg.factor(I).vars()) << " == " << jtmap.beliefF(I) << endl;
        }



        if( do_jt ) {
            // Report exact MAP joint state
	    ofstream mapJointOutfile;
	    mapJointOutfile.open( charExactMapOutput);
            cout << "Exact MAP state (log score = " << fg.logScore( jtmapstate ) << "):" << endl;
            for( size_t i = 0; i < jtmapstate.size(); i++ )
                mapJointOutfile << fg.var(i) << ": " << jtmapstate[i] << endl;
	    mapJointOutfile.close();
        }

    }

    return 0;
#else
    cout << "libDAI was configured without BP or JunctionTree (this can be changed in include/dai/dai_config.h)." << endl;
#endif
}
