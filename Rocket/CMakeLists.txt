cmake_minimum_required(VERSION 3.0.0)
project(Arcade VERSION 0.1.0)

# We need C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(SDL2 REQUIRED CONFIG REQUIRED COMPONENTS SDL2)    
# 1. Look for a SDL2 package, 2. Look for the SDL2maincomponent and 3. DO NOT fail when SDL2main is not available 
#find_package(SDL2 REQUIRED CONFIG COMPONENTS SDL2main)

INCLUDE_DIRECTORIES(${SDL2_INCLUDE_DIRS})

add_subdirectory(src)