#include <jni.h>

extern "C" {
JNIEXPORT jint JNICALL
Java_mcorp_scryingmirror_MainActivity_main_1jni(JNIEnv *env, jclass type) {

    return 10;
}
}