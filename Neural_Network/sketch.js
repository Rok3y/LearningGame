var pause = true;

var perceptron;

var points = new Array(100);
var trainingIndex = 0;
var matrix;


function setup() {
    createCanvas(800, 800);
    background(220, 220, 220);

    for(var i = 0; i < points.length; i++)
    {
        points[i] = new Point();
    }

    matrix = new Matrix(2,3);
    perceptron = new Perceptron(3);
    // test is perceptron works
    // var inputs = [-1, .5];
    // var guess = perceptron.guessOutput(inputs);
    // print(guess);

    // getFrameRate() --> display current fps
    frameRate(60);
}

function draw() {
    background(220, 220, 220);

    stroke(0);
    // line(0,height, width, 0);

    // Create a line here out of points
    var p1 = new Point(-1, f(-1));
    var p2 = new Point(1, f(1));
    line(p1.getPixelX(), p1.getPixelY(), p2.getPixelX(), p2.getPixelY());

    var p3 = new Point(-1, perceptron.guessY(-1));
    var p4 = new Point(1, perceptron.guessY(1));
    line(p3.getPixelX(), p3.getPixelY(), p4.getPixelX(), p4.getPixelY());

    for(var i = 0; i < points.length; i++)
    {
        points[i].show();
    }

    for(var i = 0; i < points.length; i++)
    {
        var pointInputs = [points[i].x, points[i].y, points[i].bias];
        var target = points[i].label;
        // perceptron.train(pointInputs, target);  //Now are trained by mousePress

        var guess = perceptron.guessOutput(pointInputs);
        if(guess == target)
        {
            fill(0, 255, 0);
        }
        else
        {
            fill(255, 0, 0);
        }
        noStroke();
        ellipse(points[i].getPixelX(), points[i].getPixelY(), 16, 16);
    }

    //noLoop();
    var training = points[trainingIndex];
    var pointInputs = [training.x, training.y, training.bias];
    var target = training.label;
    perceptron.train(pointInputs, target);

    trainingIndex++;
    if(trainingIndex == points.length)
    {
        trainingIndex = 0;
    }

}

function mousePressed()
{
    for(var i = 0; i < perceptron.weights.length; i++)
    {
        print("w" + i + " " + perceptron.weights[i]);
    }
}
