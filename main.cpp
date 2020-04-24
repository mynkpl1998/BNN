#include "headers/archParser.hpp"

int main()
{
    archParser arch("out/arch.yml");
    arch.parse();
    
    return 0;
}