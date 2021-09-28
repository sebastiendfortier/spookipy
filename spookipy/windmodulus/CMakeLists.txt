cmake_minimum_required(VERSION 3.10)

add_library(windmodulus MODULE windmodulus.cpp)

# Without this, any build libraries automatically have names "lib{x}.so"
# set(CMAKE_SHARED_MODULE_PREFIX "")