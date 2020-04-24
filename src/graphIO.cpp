#include "../headers/graphIO.hpp"

graphIO::graphIO(std::string name, unsigned int dims, std::vector<size_t> shape)
{
    this->name = name;
    this->dims = dims;
    this->shape = shape;
}