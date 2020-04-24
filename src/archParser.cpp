#include "../headers/archParser.hpp"

archParser::archParser(std::string archFilePath)
{
    this->archFilePath = archFilePath;
    this->graphInput = NULL;

    std::cout<<"INFO: Looking the architecture file to parse network from."<<std::endl;
    int status = checkFileExists(this->archFilePath);
    if(status == false)
        throw std::invalid_argument("ERROR: Architecture file not found.");
    std::cout<<"INFO: Found the architecture file."<<std::endl;
}

void archParser::parse()
{
    std::cout<<"INFO: Parsing model architecture."<<std::endl;
    this->root = YAML::LoadFile(this->archFilePath);
    
    // Parse graph input
    this->graphInput = new graphIO(this->root["input_shape"]["name"].as<std::string>(), this->root["input_shape"]["dims"].as<int>(), this->root["input_shape"]["shape"].as<std::vector<size_t>>());

    // Parse Nodes
    this->parseNodes();

    std::cout<<"INFO: Completed model parsing."<<std::endl;
}

void archParser::parseNodes()
{
    unsigned int numLayers = this->root["layers"].size();
    for(unsigned int nodeID=0; nodeID<numLayers; nodeID++)
    {   
        // Parse op name
        std::string op_name = this->root["layers"][nodeID]["op_name"].as<std::string>();

        // Parse attributes
        std::map<std::string, xt::xarray<float>> attrbs;
        for(unsigned attr=0; attr<this->root["layers"][nodeID]["attributes"].size(); attr++)
        {
            std::string attr_name = this->root["layers"][nodeID]["attributes"][attr]["name"].as<std::string>();
            std::vector<float> data = this->root["layers"][nodeID]["attributes"][attr]["data"].as<std::vector<float>>();
            std::vector<std::size_t> shape = {data.size()};
            attrbs[attr_name] = xt::xadapt(data, shape);
        }
    }
}

archParser::~archParser()
{
    delete this->graphInput;
}