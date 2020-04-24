#pragma once
#include <string>
#include <experimental/filesystem>

namespace fs = std::experimental::filesystem;
bool checkFileExists(std::string filePath);