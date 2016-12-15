#ifndef __SM_HASH_H__
#define __SM_HASH_H__
#include <string>
#include <vector>
#include <iomanip>
#include <iostream>
#include <sstream>

class Hash
{
public:
    Hash(unsigned int hash);
    Hash(std::vector<bool> &hash_array);

    std::string to_hex();

    bool operator==(Hash &h);
    unsigned int operator-(Hash &h);

    unsigned int hash_value;

private:
    int hex_len = sizeof(unsigned int) << 1;
};
#endif