#ifndef UTILS_VEC2D_H_
#define UTILS_VEC2D_H_

#include <iostream>

class Vec2D
{
public:
    Vec2D() : Vec2D(0, 0) {}
    Vec2D(float x, float y) : mX(x), mY(y) {}

    static const Vec2D Zero;

    inline void SetX(float x) { mX = x; }
    inline void SetY(float y) { mY = y; }
    inline float GetX() const { return mX; }
    inline float GetY() const { return mY; }

    friend std::ostream& operator<<(std::ostream& consoleOut, const Vec2D& vec);

    bool operator==(const Vec2D& vec) const;
    bool operator!=(const Vec2D& vec) const;

    Vec2D operator-() const;

    Vec2D operator*(float scale) const;
    Vec2D operator/(float scale) const;
    Vec2D& operator*=(float scale);
    Vec2D& operator/=(float scale);

    Vec2D operator+(const Vec2D& vec) const;
    Vec2D operator-(const Vec2D& vec) const;
    Vec2D& operator+=(const Vec2D& vec);
    Vec2D& operator-=(const Vec2D& vec);

    float Mag2() const;
    float Mag() const;

    Vec2D GetUnitVec() const;
    Vec2D& Normalize();

    float Distance(const Vec2D& vec) const;
    float Dot(const Vec2D& vec) const;

    Vec2D ProjectOnto(const Vec2D& vec) const;
    Vec2D Reflect(const Vec2D& normal) const;
    float AngleBetween(const Vec2D& vec) const;

    void Rotate(float angle, const Vec2D& aroundPoint);     // not a const since we rotate ourselfs
    Vec2D RotationResult(float angle, Vec2D& aroundPoint) const;

    friend Vec2D operator*(float scalar, const Vec2D& vec); // To use scalar before vec (e.g 3 * vec)

private:
    float mX, mY;
};

#endif /* UTILS_VEC2D_H_ */