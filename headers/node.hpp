#pragma once
#include <map>
#include <vector>
#include <string>
#include "xtensor/xarray.hpp"

class node
{
    public:
        std::string op_name;
        std::vector<std::string> inputs;
        std::vector<std::string> outputs;
        std::map<std::string, xt::xarray<float>> attributes;
        unsigned int numInputs;
        unsigned int numOutputs;
        unsigned int numAttributes;

    public:
        node();
};