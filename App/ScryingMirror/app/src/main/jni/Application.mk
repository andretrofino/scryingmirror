APP_STL := gnustl_static
ifeq ($(NDK_DEBUG),)
    APP_CPPFLAGS := -O3 -ffast-math -mfpu=neon -frtti -fexceptions -std=c++11 -marm
else
    APP_CPPFLAGS := -O0 -g -ffast-math -mfpu=neon -frtti -fexceptions -std=c++11
endif
APP_ABI := armeabi-v7a
APP_PLATFORM := android-19
APP_OPTIM := release
NDK_TOOLCHAIN_VERSION := 4.9