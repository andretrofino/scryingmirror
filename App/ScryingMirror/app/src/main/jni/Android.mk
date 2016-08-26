LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

# I want ARM, not thumb.
LOCAL_ARM_MODE := arm

# Name of the local module
LOCAL_MODULE    := scryingmirror_cpp
# The files that make up the source code
LOCAL_SRC_FILES := mainactivity.cpp
LOCAL_LDLIBS +=  -llog -ldl
LOCAL_STATIC_LIBRARIES := cpufeatures
include $(BUILD_STATIC_LIBRARY)

$(call import-module,android/cpufeatures)
