# Cesar Lopez Pastrana, 2022
# Instrucitons:
# make        // Compile the library
# make clean  // Remove the library

CC := g++
CPPFLAGS := -std=c++11 -O3 -fPIC 
LIBS := -fopenmp -lCGAL -I /usr/include -lgmp  -lmpfr 
LINKERFLAG := -shared -lCGAL -lm -lgmp -lmpfr

COMP_FNAME := meshgen.so
OBJ_FNAME := meshgen.o
SRCS := meshgen.cpp


.PHONY = all clean


all: meshgen 

meshgen: meshgen.o
	@echo -n " - Linking... "
	@${CC}  meshgen.o ${LINKERFLAG} ${LIBS} -o ${COMP_FNAME}
	@echo "Done"

meshgen.o: ${SRCS}
	@echo "Compiling meshgen library:"
	@echo -n " - Compiling object file... "
	@${CC} ${CPPFLAGS} ${LIBS} -c ${SRCS}
	@echo "Done"
	
clean:
	@echo -n "Cleaning object files... "
	@rm ${OBJ_FNAME}
	@echo "Done"

#g++ -c meshgen.cpp -fopenmp  -I /usr/include  -std=c++11 -O3 -fPIC -o  meshgen.o
#g++ meshgen.o  -o meshgen.so

