#include <stdio.h>

#include "inc/data.h"
#include "inc/utils.h"
#include "inc/decode.h"
#include "inc/encode.h"

int main(int argc, char **argv, char **env)
{
    decode("input/input.xml", "output/1.decode.xml");
    
    encode("output/1.decode.xml", "output/2.encode.xml");    
    decode("output/2.encode.xml", "output/2.deocde.xml");

    return 0;
}