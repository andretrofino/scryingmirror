APP_STL := gnustl_static

ifeq ($(NDK_DEBUG),)
    #Release
    APP_CFLAGS := -DNDEBUG -O3
else
    #Debug
    APP_CFLAGS := -O0 -g
endif

APP_PLATFORM := android-21

APPLICATION_MK_PATH := $(call my-dir)
APP_BUILD_SCRIPT := $(APPLICATION_MK_PATH)/Android.mk

ifeq ($(NDK_DEBUG),)
    APP_OPTIM := release
    NDK_APP_OUT := $(call my-dir)/../../Object/ARM/Release/
else
    APP_OPTIM := debug
    NDK_APP_OUT := $(call my-dir)/../../Object/ARM/Debug/
endif

APP_MODULES := scrying_mirror

NDK_TOOLCHAIN_VERSION := 4.9
