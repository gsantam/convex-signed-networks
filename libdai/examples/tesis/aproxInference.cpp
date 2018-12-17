/*  This file is part of libDAI - http://www.libdai.org/
 *
 *  Copyright (c) 2006-2011, The libDAI authors. All rights reserved.
 *
 *  Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
 */
//

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
      // Read FactorGraph from the file specified by the first command line argument
        FactorGraph fg;
        fg.ReadFromFile(argv[1]);
	
	string factorGraphName = split(argv[1], '.')[0];
	string exactMapOutput = factorGraphName + "Aprox.comm";
	char * charExactMapOutput = new char [exactMapOutput.length()+1];
	std::strcpy (charExactMapOutput, exactMapOutput.c_str());
	
	
	
        size_t maxstates = 10000000;
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

        // Construct a BP (belief propagation) object from the FactorGraph fg
        // using the parameters specified by opts and two additional properties,
        // specifying the type of updates the BP algorithm should perform and
        // whether they should be done in the real or in the logdomain
        //
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

        // Construct a decimation algorithm object from the FactorGraph fg
        // using the parameters specified by opts and three additional properties,
        // specifying that the decimation algorithm should use the max-product
        // algorithm and should completely reinitalize its state at every step
        DecMAP decmap(fg, opts("reinit",true)("ianame",string("BP"))("iaopts",string("[damping=0.1,inference=MAXPROD,logdomain=0,maxiter=1000,tol=1e-9,updates=SEQRND,verbose=1]")) );
        decmap.init();
        decmap.run();
        vector<size_t> decmapstate = decmap.findMaximum();


        // Report max-product MAP joint state
	ofstream mapJointOutfile;
	mapJointOutfile.open( charExactMapOutput);
        cout << "Approximate (max-product) MAP state (log score = " << fg.logScore( mpstate ) << "):" << endl;
        for( size_t i = 0; i < mpstate.size(); i++ )
            mapJointOutfile << fg.var(i) << ": " << mpstate[i] << endl;
	mapJointOutfile.close();

    }

    return 0;
#else
    cout << "libDAI was configured without BP or JunctionTree (this can be changed in include/dai/dai_config.h)." << endl;
#endif
}
