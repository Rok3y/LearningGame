#include "Screen.h"
#include "InputController.h"
#include "Scene.h"
#include "ArcadeScene.h"
#include <SDL.h>
#include <iostream>
#include <memory>
#include <stdint.h>

const int SCREEN_WIDTH = 480;
const int SCREEN_HEIGHT = 640;
const int MAGNIFICATION = 1;



int main(int argc, char* argv[]) 
{
    std::cout << "test SDL\n";
    Screen screen;
    SDL_Window* window = screen.Init(SCREEN_WIDTH, SCREEN_HEIGHT, MAGNIFICATION);
    //std::unique_ptr<SDL_Window> window(std::move(tmpWindow));
    InputController inputController;

    if (window)
    {
        bool running = true;

        // We need stable frame rate. Update our game or screen every 10 milliseconds
        uint32_t lastTick = SDL_GetTicks();
        uint32_t currTick = lastTick;

        uint32_t dt = 10; // in milliseconds
        uint32_t accumulator = 0;

        // Initialize input controller and give it action when quitting
        inputController.Init([&running](uint32_t dt, InputState state)
            {
                running = false;
            });

        std::unique_ptr<Scene> arcadeScene = std::make_unique<ArcadeScene>(SCREEN_WIDTH, SCREEN_HEIGHT);
        arcadeScene->Init();
        inputController.SetGameController(arcadeScene->GetGameController());
        SDL_SetWindowTitle(window, arcadeScene->GetSceneName().c_str());

        while (running)
        {
            currTick = SDL_GetTicks();
            // Get number of ticks sinc our last frame
            uint32_t frameTime = currTick - lastTick;

            // Set upper limit for the time frame
            if (frameTime > 300)
            {
                frameTime = 300;
            }

            lastTick = currTick;
            accumulator += frameTime;

            // Input
            inputController.Update(dt);

            // Update
            while (accumulator >= dt)
            {
                // Here we update object for every dt (10) milliseconds
                // And draw when accumulator is below dt
                arcadeScene->Update(dt);
                accumulator -= dt;
            }

            // Draw
            arcadeScene->Draw(screen);

            // Swap screen buffer
            screen.SwapScreen();
        }

    }

    return 0;
}