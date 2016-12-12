LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

SCRYING_MIRROR_MODULE_PATH := $(LOCAL_PATH)/../../../../../../Source

# OpenCV
OPENCVROOT:= C:/Users/andre.trofino/Development/OpenCV-android-sdk
OPENCV_CAMERA_MODULES:=on
OPENCV_INSTALL_MODULES:=on
OPENCV_LIB_TYPE:=SHARED
include ${OPENCVROOT}/sdk/native/jni/OpenCV.mk

# I want ARM, not thumb.
LOCAL_ARM_MODE := arm

# Name of the local module
LOCAL_MODULE    := scryingmirror_cpp

# The files that make up the source code
LOCAL_SRC_FILES := mainactivity.cpp
LOCAL_LDLIBS +=  -llog -ldl

include $(BUILD_SHARED_LIBRARY)

$(call import-add-path, $(SCRYING_MIRROR_MODULE_PATH))
# $(call import-module,android/cpufeatures)
