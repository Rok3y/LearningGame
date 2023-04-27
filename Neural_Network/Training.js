// Known training data
// Points that are above line are white, below are black

// Represents a line 
function f(x)
{
    // y = mx + b
    return 3 * x - 2;
}

class Point
{
    constructor(x = random(-1, 1), y = random(-1, 1))
    {
        this.x = x;
        this.y = y;
        this.bias = 1;
        this.label;

        var lineY = f(x); // Get Y value. To see if point is about a line of below a line
        if(this.y > lineY)
        {
            this.label = 1;    
        }
        else
        {
            this.label = -1;
        }
    }

    getPixelX()
    {
        return map(this.x, -1, 1, 0, width);
    }

    getPixelY()
    {
        return map(this.y, -1, 1, height, 0);
    }

    show()
    {
        stroke(0);
        if(this.label == 1)
        {
            fill(255);
        }
        else
        {
            fill(0);
        }

        var px = this.getPixelX();
        var py = this.getPixelY();
        ellipse(px, py, 32,32);
    }
}