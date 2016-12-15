#ifndef __SM_SCRYING_MIRROR_H_
#define __SM_SCRYING_MIRROR_H_

#include "ImageHash.hpp"
#include <vector>

std::vector<cv::Point2d> get_perspetive(cv::Point2d &p1, cv::Point2d &p2, cv::Point2d &p3, cv::Point2d &p4);

std::vector<std::string> get_cards(cv::Mat &frame);

#endif
