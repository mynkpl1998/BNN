#include "../headers/utils.hpp"
bool checkFileExists(std::string filePath)
{
    return fs::exists(filePath);
}