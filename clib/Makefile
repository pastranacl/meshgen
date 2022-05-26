CC := g++
CPPFLAGS := -std=c++11 -lm -O3 -fPIC -shared
LIBS := -fopenmp -lCGAL -I /usr/include -lgmp  -lmpfr -lm

COMP_FNAME := meshgen.so
SRCS := meshgen.cpp

meshgen:
	@echo -n "Compiling meshgen lib... "
	@${CC} ${SRCS} ${CPPFLAGS} ${LIBS} -o ${COMP_FNAME}
	@echo "Done!" 

