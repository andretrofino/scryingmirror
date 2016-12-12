#include <jni.h>
#include <opencv2/core/core.hpp>



extern "C" {
JNIEXPORT jint JNICALL
Java_mcorp_scryingmirror_MainActivity_main_1jni(JNIEnv *env, jclass type) {
    cv::Mat m;
    return 10;
}
}