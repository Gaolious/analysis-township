CC = g++
INCS = -I./
# CFLAGS = -O3 -std=c++11 -pipe -Wno-unused-result
CFLAGS = -g -std=c++11 -pipe -Wno-unused-result
LDFLAGS = -lm 
TARGET = ./bin/township
.SUFFIXES : .cpp .c .o 

SRC = $(wildcard src/*.cpp)
OBJ = $(patsubst src/%.cpp, obj/%.o, $(SRC))

$(TARGET): $(OBJ)
	[ -d bin ] || mkdir -p bin
	$(CC) $(CFLAGS) $(LDFLAGS) $(INCS) $(OBJ) -o $(TARGET)
	echo "Complete"

obj/%.o: src/%.cpp
	[ -d obj ] || mkdir -p obj
	$(CC) $(CFLAGS) $(LDFLAGS) $(INCS) -c $< -o $@

clean:
	rm -rf $(OBJ) $(TARGET) core bin obj