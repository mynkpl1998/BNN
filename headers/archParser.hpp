#include <iostream>
#include "yaml-cpp/yaml.h"
#include "../headers/utils.hpp"
#include "../xtensor/xarray.hpp"
#include "../xtensor/xadapt.hpp"
#include "../headers/graphIO.hpp"


class archParser
{
    private:
        std::string archFilePath;
    
    public:
        YAML::Node root;
        graphIO *graphInput;
    
    public:
        archParser(std::string archFilePath);
        void parseNodes();
        void parse();
        ~archParser();
};