#include <jni.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui.hpp>

extern "C" {

using namespace std;
using namespace cv;
JNIEXPORT jint JNICALL
Java_mcorp_scryingmirror_MainActivity_main_1jni(JNIEnv *env, jclass type) {

    Mat m = imread("fake.jpg");


    return 10;
}
}