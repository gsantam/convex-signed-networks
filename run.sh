allSolvers=$1
if $allSolvers; then
        rm Exact.comm
        rm Aprox.comm
        #run the exact inference (using junction tree)
        ./libdai/examples/tesis/exactInference ./libdai/examples/tesis/test.fg
        #run the aproximate inference (using loopy maxprod)
        ./libdai/examples/tesis/aproxInference ./libdai/examples/tesis/test.fg
fi
cd psl/psl-example
#run the psl hinge-loss inference
time  java -Xmx2048m -cp ./target/classes:`cat classpath.out` edu.umd.cs.example.PottsCommunities

cd ../../
python psl-converter.py
