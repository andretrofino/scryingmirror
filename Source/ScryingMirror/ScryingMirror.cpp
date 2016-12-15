#include "ScryingMirror.hpp"

using namespace std;
using namespace cv;

vector<Point2d> get_perspetive(Point2d &p1, Point2d &p2, Point2d &p3, Point2d &p4) {
	
	// Follows the order: top_left, top_right, bottom_left, bottom_right
	vector<Point2d> ret(4);

	if (p1.x > p2.x) {
		ret[0] = p2;
		ret[1] = p1;
	}
	else {
		ret[0] = p1;
		ret[1] = p2;
	}

	if (p3.x > p4.x) {
		ret[2] = p4;
		ret[3] = p3;
	}
	else {
		ret[2] = p3;
		ret[3] = p4;
	}

	return ret;
}

vector<string> get_cards(Mat &frame) {

	vector<string> s(5);

	int gaussian_kernel = 11;
	int gaussian_subtract = 2;

	int width = frame.cols;
	int height = frame.rows;

	int frame_area = width * height;
	int frame_perimeter = width + width + height + height;

	Mat gray;
	cvtColor(frame, gray, CV_BGR2GRAY);

	adaptiveThreshold(gray, gray, 255, CV_ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, gaussian_kernel, gaussian_subtract);

	Mat kernel = Mat::ones(3, 3, CV_8UC1);

	
	erode(gray, gray, kernel);
	dilate(gray, gray, kernel);
	Canny(gray, gray, 300, 500);
	vector<vector<Point> > contours;
	findContours(gray, contours, RETR_TREE, CHAIN_APPROX_SIMPLE);

	if (contours.size() > 1) {
		for (vector<Point> contour : contours) {
			double area = contourArea(contour);
			if (area / frame_area > 0.005) {
				double perimeter = arcLength(contour, false);
				if (perimeter / frame_perimeter > 0.0075) {
					if (area / perimeter > 20) {
						vector<Point> poly;
						double epsilon = 0.05 * arcLength(contour, true);
						approxPolyDP(contour, poly, epsilon, true);
					}
				}
			}
		}
	}

	return s;
}
