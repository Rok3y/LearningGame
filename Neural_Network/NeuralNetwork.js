function sigmoid(x)
{
    return 1 / (1 + Math.exp(-x));
}

function derivative_sigmoid(y)
{
    //return sigmoid(x) * (1 - sigmoid(x));
    return y * (1 - y);
}

class NeuralNetwork
{
    constructor(nInput, nHidden, nOutput)
    {
        this.inputNodes = nInput;
        this.hiddenNodes = nHidden;
        this.outputNodes = nOutput;

        this.weights_input_hidden = new Matrix(this.hiddenNodes, this.inputNodes);
        this.weights_hidden_output = new Matrix(this.outputNodes, this.hiddenNodes);

        // Pick random weigths for starters
        this.weights_input_hidden.randomize();
        this.weights_hidden_output.randomize();

        this.bias_hidden = new Matrix(this.hiddenNodes, 1);
        this.bias_output = new Matrix(this.outputNodes, 1);
        this.bias_hidden.randomize();
        this.bias_output.randomize();

        this.learnign_rate = .1;
    }

    feedForward(input_array)
    {
        // Generating the Hidden Outputs

        let input = Matrix.fromArray(input_array);

        // Multipy weights with inputs
        // Add bias to that product
        // Send every result through sigmoid function to flatten it between -1 and 1
        let hidden = Matrix.multipy(this.weights_input_hidden, input);
        hidden.add(this.bias_hidden);
        // Activation function!
        hidden.map(sigmoid);

        // Generating the output's output
        let output = Matrix.multipy(this.weights_hidden_output, hidden);
        output.add(this.bias_output);
        output.map(sigmoid);

        // Sending back to the caller
        return output.toArray();
    }

    // Train data
    /**
     * Supervised learning
     * Get guess (feed forward)
     * Calucalte the error = guess - target
     * Back propagate the error through the nodes
     * 
     * For Weigth from hidden to output
     *      dWho = learnignRate * Error * (output *(1 - output)) * Hiddent_transpose
     * 
     * For weigths from input to hidden
     *      dWih = learnignRate * Hidden_node_error * (Hidden_nodes * (1 - Hidden_nodes)) * Input_transpose
     * @param {*} inputs 
     * @param {*} answers 
     */

    train(inputs, answers)
    {
        // Get guess and then compare with the answer
        //let outputs = this.feedForward(inputs);

        let input = Matrix.fromArray(input_array);

        // Multipy weights with inputs
        // Add bias to that product
        // Send every result through sigmoid function to flatten it between -1 and 1
        let hidden = Matrix.multipy(this.weights_input_hidden, input);
        hidden.add(this.bias_hidden);
        // Activation function!
        hidden.map(sigmoid);

        // Generating the output's output
        let outputs = Matrix.multipy(this.weights_hidden_output, hidden);
        outputs.add(this.bias_output);
        outputs.map(sigmoid);


        
        // Convert array to matrix objects
        //outputs = Matrix.fromArray(outputs);
        answers = Matrix.fromArray(answers);

        // Calculcate the error
        // ERROR = ANSWER - OUTPUTS

        // First calculate error between output and answer
        let output_errors = Matrix.subtract(answers, outputs);

        // Calculate gradient
        // gradient = outputs * (1 - outputs)
        let gradients = Matrix.map(outputs, derivative_sigmoid);
        gradients.multipy(output_errors);
        gradients.multipy(this.learnign_rate);

        // Calculate deltas
        let hidden_t = Matrix.transpose(hidden);
        let weights_ho_deltas = Matrix.multipy(gradients, hidden_t);

        // Check ???????????????
        this.weights_hidden_output.add(weights_ho_deltas);
        
        // #############################################################################
        // Calculate the hidden layer errors
        // Backpropagate the error and calcualte error in hidden nodes
        let weights_hidden_output_T = Matrix.transpose(this.weights_hidden_output);
        let hidden_errors = Matrix.multipy(weights_hidden_output_T, output_errors);

        // Calculate hidden gradient
        let hidden_gradient = Matrix.map(hidden, derivative_sigmoid);
        hidden_gradient.multipy(hidden_errors);
        hidden_errors.multipy(this.learnign_rate);

        // Calculate input to hidden deltas
        let inputs_T = Matrix.transpose(inputs);
        let weights_ih_deltas = Matrix.multipy(hidden_gradient, inputs_T);

        this.weights_input_hidden.add(weights_ih_deltas);

        output.print();
        answers.print();
        output_errors.print();
    }
}
