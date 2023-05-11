#ifndef SCENES_ARCADESCENE_H_
#define SCENES_ARCADESCENE_H_

#include "Scene.h"
#include "Game/Particle.h"
#include "AARectangle.h"
#include <memory>

class Screen;

class ArcadeScene : public Scene
{
public:
	ArcadeScene(uint32_t width, uint32_t height);
	virtual void Init() override;
	virtual void Update(uint32_t dt) override;
	virtual void Draw(Screen& theScreen) override;
	virtual const std::string& GetSceneName() const override;

private:
	uint32_t mWidth, mHeight;
	AARectangle mBoundary;
	Particle mRocket;
	Particle mHeavyRocket;
	Vec2D mGravity;
	//std::unique_ptr<Scene> GetScene(eGame game);
};

#endif /* SCENES_ARCADESCENE_H_ */