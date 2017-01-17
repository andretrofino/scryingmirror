LOCAL_PATH:=$(call my-dir)/../../Source/Scrying_Mirror

# ScryingMirror Lib

include $(CLEAR_VARS)
LOCAL_MODULE := scrying_mirror

LOCAL_SRC_FILES :=  Hash.cpp \
				    ImageHash.cpp \
				    ScryingMirror.cpp

LOCAL_CFLAGS += -ffast-math -Wall -pedantic

LOCAL_CPPFLAGS += -frtti -fexceptions -std=c++11

LOCAL_C_INCLUDES += $(LOCAL_PATH)

LOCAL_LDLIBS += -llog -ldl

LOCAL_EXPORT_C_INCLUDES := $(LOCAL_PATH)

include $(BUILD_SHARED_LIBRARY)
