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
	Shapes/Line2D.h
	Shapes/Line2D.cpp
	Shapes/Star.h
	Shapes/Star.cpp
	Shapes/Shape.h
	Shapes/Shape.cpp
	Shapes/Triangle.h
	Shapes/Triangle.cpp
	Shapes/AARectangle.h
	Shapes/AARectangle.cpp
	Shapes/Circle.h
	Shapes/Circle.cpp
	Scenes/Scene.h
	Scenes/ArcadeScene.h
	Scenes/ArcadeScene.cpp
	Input/InputAction.h
	Input/GameController.h
	Input/GameController.cpp
	Input/InputController.h
	Input/InputController.cpp
)

include_directories(utils)
include_directories(Graphics)
include_directories(Shapes)
include_directories(App)
include_directories(Scenes)
include_directories(Input)
file(GLOB SOURCES ${ARCADE_LIB_SRCS})
	
add_executable(${PROJECT_NAME} main.cpp ${SOURCES} "Scenes/ArcadeScene.cpp" "Scenes/ArcadeScene.h"   "Scenes/Scene.h" "Scenes/Game/GameObject.h" "Scenes/Game/Rect.h" "Scenes/Game/Rect.cpp" "Scenes/Game/GamePhysicsObject.h" "Shapes/Rocket.h" "Shapes/Rocket.cpp" "Scenes/Game/Rocketship.h" "Scenes/Game/Rocketship.cpp")

link_libraries(SDL2::SDL2 ${SDL2_LIBRARIES})
target_link_libraries(${PROJECT_NAME} ${SDL2_LIBRARIES})

file(COPY ${SDL2_BINDIR}/SDL2.dll DESTINATION ${CMAKE_BINARY_DIR}/src/${CMAKE_BUILD_TYPE})
