#ifndef GRAPHICS_COLOR_H
#define GRAPHICS_COLOR_H

#include <stdint.h>

// forward declaration
struct SDL_PixelFormat;

class Color
{
	uint32_t mColor;

public:

	static const SDL_PixelFormat* mFormat;
	static void InitColorFormat(const SDL_PixelFormat* format);

	static Color Black(){ return Color(0, 0, 0, 255); }
	static Color White() { return Color(255, 255, 255, 255); }
	static Color Blue() { return Color(0, 0, 255, 255); }
	static Color Red() { return Color(255, 0, 0, 255); }
	static Color Green() { return Color(0, 255, 0, 255); }
	static Color Yellow() { return Color(255, 255, 0, 255); }
	static Color Magenta() { return Color(255, 0, 255, 255); }
	static Color Cyan() { return Color(37, 240, 217, 255); }
	static Color Pink() { return Color(252, 197, 224, 255); }
	static Color Orange() { return Color(245, 190, 100, 255); }

	Color(): Color(0) {}
	Color(uint32_t color) : mColor(color) {}
	Color(uint32_t r, uint32_t g, uint32_t b, uint32_t a);

	inline bool operator==(const Color& c) const { mColor == c.mColor; }
	inline bool operator!=(const Color& c) const { return !(*this == c); }
	inline uint32_t GetPixelColor() const { return mColor; }

	void SetRGBA(uint32_t r, uint32_t g, uint32_t b, uint32_t a);

	void SetRed(uint32_t red);
	void SetGreen(uint32_t green);
	void SetBlue(uint32_t blue);
	void SetAlpha(uint32_t alpha);

	uint8_t GetRed() const;
	uint8_t GetGreen() const;
	uint8_t GetBlue() const;
	uint8_t GetAlpha() const;
};

#endif /* GRAPHICS_COLOR_H */