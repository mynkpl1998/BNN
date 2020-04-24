CC=g++
FILE_SYSTEM_LINKER=-lstdc++fs
YAML_LINKER=-L/usr/local/lib -lyaml-cpp

all: archParser.o utils.o graphIO.o main.cpp
	${CC} archParser.o utils.o graphIO.o main.cpp ${FILE_SYSTEM_LINKER} ${YAML_LINKER}

utils.o: headers/utils.hpp src/utils.cpp
	${CC} -c src/utils.cpp

graphIO.o: headers/graphIO.hpp src/graphIO.cpp
	${CC} -c src/graphIO.cpp

archParser.o: headers/archParser.hpp src/archParser.cpp
	${CC} -c src/archParser.cpp

clean:
	rm -rf *.o