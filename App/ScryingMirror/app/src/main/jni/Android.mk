LOCAL_PATH := $(call my-dir)

SCRYING_MIRROR_MODULE_PATH := $(LOCAL_PATH)/../../../../../../Projects/Android/

include $(CLEAR_VARS)

# OpenCV
OPENCVROOT:= C:/Users/andre.trofino/Development/OpenCV-android-sdk
OPENCV_CAMERA_MODULES:=on
OPENCV_INSTALL_MODULES:=on
OPENCV_LIB_TYPE:=SHARED
include ${OPENCVROOT}/sdk/native/jni/OpenCV.mk

# The files that make up the source code
LOCAL_SRC_FILES := mainactivity.cpp
LOCAL_LDLIBS +=  -llog -ldl
LOCAL_MODULE    := scryingmirror_jni

LOCAL_ARM_MODE := arm

LOCAL_SHARED_LIBRARIES := scrying_mirror
LOCAL_CFLAGS += -ffast-math -Wall -pedantic
LOCAL_CPPFLAGS += -frtti -fexceptions -std=c++11

LOCAL_C_INCLUDES += $(LOCAL_PATH) $(LOCAL_PATH)/../../../../../../Source/ScryingMirror/

include $(BUILD_SHARED_LIBRARY)

$(call import-add-path, $(SCRYING_MIRROR_MODULE_PATH))
