#include "App.h"
#include <SDL.h>
#include <iostream>
#include "ArcadeScene.h"
#include <cassert>

App& App::Singleton() // Allows one object of this type
{
	static App theApp;
	return theApp;
}

bool App::Init(uint32_t width, uint32_t height, uint32_t mag)
{
	mnoptrWindow = mScreen.Init(width, height, mag);

    std::unique_ptr<ArcadeScene> arcadeScene = std::make_unique<ArcadeScene>();
    PushScene(std::move(arcadeScene));

	return mnoptrWindow != nullptr;
}

void App::Run()
{
    if (mnoptrWindow)
    {
        bool running = true;

        /*
        * Stable framerate. We update our game or sceen in every 10 millisecond intervals
        */
        uint32_t lastTick = SDL_GetTicks();
        uint32_t currentTick = lastTick;

        uint32_t dt = 10; // in milliseconds
        uint32_t accumulator = 0;

        // Input controller init
        mInputController.Init([&running](uint32_t dt, InputState state)
            {
                running = false;
            });

        while (running)
        {
            currentTick = SDL_GetTicks();
            uint32_t frameTime = currentTick - lastTick; // This is how many tick has happened since our last frame

            if(frameTime > 300)
            {
                frameTime = 300;
            }

            lastTick = currentTick;
            accumulator += frameTime;

            // Input
            mInputController.Update(dt);

            Scene* topScene = App::TopScene();
            assert(topScene && "Why don't have a scene?");
            if (topScene)
            {
                // Update
                while (accumulator >= dt)
                {
                    // update current scene by dt
                    // Meaning if we skip frame or lag we update current sceen by for example 3 dt
                    topScene->Update(dt);
                    //std::cout << "Delta time step: " << dt << std::endl;
                    accumulator -= dt;
                }

                // Render
                topScene->Draw(mScreen);
            }

            mScreen.SwapScreen();
        }
    }
}

void App::PushScene(std::unique_ptr<Scene> scene)
{
    assert(scene && "Don't push nullptr");
    if (scene)
    {
        scene->Init();
        mInputController.SetGameController(scene->GetGameController());

        mSceneStack.emplace_back(std::move(scene)); // emplace moves not copies
        SDL_SetWindowTitle(mnoptrWindow, TopScene()->GetSceneName().c_str());
    }
}

void App::PopScene()
{
    if (mSceneStack.size() > 1)
    {
        mSceneStack.pop_back();
    }

    if (TopScene())
    {
        mInputController.SetGameController(TopScene()->GetGameController());
        SDL_SetWindowTitle(mnoptrWindow, TopScene()->GetSceneName().c_str());
    }
}

Scene* App::TopScene()
{
    if (mSceneStack.empty())
    {
        return nullptr;
    }

    return mSceneStack.back().get();
}