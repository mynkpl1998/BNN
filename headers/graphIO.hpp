#pragma once
#include <string>
#include <vector>

class graphIO
{
    public:
        unsigned int dims;
        std::string name;
        std::vector<size_t> shape;
    
    public:
        graphIO(std::string name, unsigned int dims, std::vector<size_t> shape);
};