#ifndef __SM_IMAGE_HASH_H__
#define __SM_IMAGE_HASH_H__
#define _USE_MATH_DEFINES
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/core.hpp>
#include <opencv2/core/core.hpp>

#include <cmath>
#include <cstdlib>
#include <string>
#include <iostream>
#include <fstream>

#include "Hash.hpp"

Hash dct_hash(const cv::Mat &img, int rsz = 32, int block_size = 8, bool crop = false);

void hash_dir(const std::string dir, const std::string filename);

std::vector<std::pair<std::string, Hash>> load_hash(std::string hash_path);

std::vector<std::pair<std::string, int>> match(Hash target_hash, std::vector<std::pair<std::string, Hash>> &hash_list, int top = 5);


#endif
