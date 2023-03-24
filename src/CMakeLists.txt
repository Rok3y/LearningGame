set(ARCADE_LIB_SRCS
	utils/Vec2D.h
	utils/Vec2D.cpp
	utils/Utils.h
	utils/Utils.cpp
	utils/DynamicIntArray.h
	utils/DynamicIntArray.cpp
	Graphics/color.h
	Graphics/color.cpp
	Graphics/ScreenBuffer.h
	Graphics/ScreenBuffer.cpp
	Graphics/Screen.h
	Graphics/Screen.cpp
	Shapes/Line2D.h)

include_directories(utils)
include_directories(Graphics)
include_directories(Shapes)
file(GLOB SOURCES ${ARCADE_LIB_SRCS})
	
add_executable(${PROJECT_NAME} main.cpp ${SOURCES} "Shapes/Line2D.cpp" "Shapes/Star.h" "Shapes/Star.cpp" "Shapes/Shape.h" "Shapes/Shape.cpp" "Shapes/Triangle.h" "Shapes/Triangle.cpp" "Shapes/AARectangle.h" "Shapes/AARectangle.cpp" "Shapes/Circle.h" "Shapes/Circle.cpp")

link_libraries(SDL2::SDL2 ${SDL2_LIBRARIES})
target_link_libraries(${PROJECT_NAME} ${SDL2_LIBRARIES})

file(COPY ${SDL2_BINDIR}/SDL2.dll DESTINATION ${CMAKE_BINARY_DIR}/src/${CMAKE_BUILD_TYPE})