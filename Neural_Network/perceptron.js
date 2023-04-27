class Perceptron
{
    // N is a number of inputs + one bias which is always 1
    constructor(n)
    {
        // Initialize the weigth randomly
        this.weights = new Array(n); // Two inputs and one bias input which is always 1
        this.learningRate = .01;
        for(var i = 0; i < this.weights.length; i++)
        {
            this.weights[i] = random(-1, 1); // Random number between -1 and 1
        }
    }

    // Activation function
    sign(n)
    {
        if (n > 0)
            return 1;
        else
            return -1;
    }

    // Sum of all inputs multiplied by weigth
    guessOutput(inputs)
    {
        var sum = 0;
        for(var i = 0; i < this.weights.length; i++)
        {
            sum += inputs[i] * this.weights[i];
        }

        var output =  this.sign(sum);
        return output;
    }

    // error = answer - guess
    // dW = error * input * learningRate
    train(inputs, target)
    {
        var guess = this.guessOutput(inputs);
        // Compute the factor for changing the weight based on the error
        // Error = desired output - guessed output
        // Note this can only be 0, -2, or 2
        // Multiply by learning constant
        var error = target - guess;
        
        // Tune all the weigths based on an error
        for(var i = 0; i < this.weights.length; i++)
        {
            this.weights[i] += error * inputs[i] * this.learningRate;
        }
    }

    // A new line formula based on weights
    // output = x*w0 + y*w1 + b*w2
    // To get and Y of this we rearange and get
    // y = - (w2/w1) * b - (w0/w1) * x
    guessY(x)
    {
        // var m = this.weights[1] / this.weights[0];
        // var b = this.weights[2];

        var w0 = this.weights[0];
        var w1 = this.weights[1];
        var w2 = this.weights[2];
        
        return -(w2/w1) - (w0/w1) * x; // Bias is always 1 so I left it out
    }

}