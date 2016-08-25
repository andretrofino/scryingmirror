#include "Hash.hpp"

using namespace std;

unsigned int hamming(unsigned int x, unsigned int y, int base = 2)
{
    unsigned int distance = 0;
    unsigned int z = x^y;
    while (z) {
        ++distance;
        z &= z - 1;
    }

    return distance;
}


Hash::Hash(unsigned int hash) :
                hash_value(hash)
{
}

Hash::Hash(vector<bool> &hash_array) :
                hash_value(0)
{
    size_t size = hash_array.size();

    for (int i = 0; i < size - 1; ++i) {
        hash_value += (unsigned int)hash_array.at(i);
        hash_value = hash_value << 1;
    }
    // Last value doesn't need shift
    hash_value += (unsigned int)hash_array.at(size-1);
}

string Hash::to_hex()
{
    stringstream stream;
    stream << "0x" << std::hex << this->hash_value;

    return stream.str();
}

bool Hash::operator==(Hash &h)
{
    if (hamming(this->hash_value, h.hash_value)) {
        return false;
    } else {
        return true;
    }
}

unsigned int Hash::operator-(Hash &h)
{
    return hamming(this->hash_value, h.hash_value);
}
