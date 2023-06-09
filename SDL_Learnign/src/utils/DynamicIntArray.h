#ifndef UTILS_DYNAMICINTARRAY_H_
#define UTILS_DYNAMICINTARRAY_H_

#include <iostream>
#include <cassert>

using namespace std;

class DynamicIntArray
{
public:
	DynamicIntArray()
		: moptrData(nullptr), mSize(0), mCapacity(0)
	{}

	DynamicIntArray(const DynamicIntArray& otherArray); // Copy constructor (Deep copy
	
	DynamicIntArray& operator=(const DynamicIntArray& otherArray);
	~DynamicIntArray();

	inline size_t Size() const { return mSize; }
	inline size_t Capacity() const{ return mCapacity; }

	// Allocates the dynamic array
	bool Init(size_t capacity = INITIAL_CAPACITY);

	bool Reserve(size_t capacity);

	bool Resize(size_t newSize);

	bool PushBack(int newVal);
	bool PopBack(int& value);

	const int& operator[](size_t index) const;
	int& operator[](size_t index);
	
private:
	int* moptrData;
	size_t mSize;
	size_t mCapacity;

	static const size_t INITIAL_CAPACITY = 10;
	static const size_t RESIZE_MULTIPLIER = 2;
};

#endif // !UTILS_DYNAMICINTARRAY_H_
