var nn;

function setup()
{
        let nn = new NeuralNetwork(2, 2, 2); // 2 inputs, 2 hidden nodes, 1 output

        let input = [1, 0];
        let answer = [1, 0];

        // let output = nn.feedForward(input);
        // console.log(output);

        nn.train(input, answer);
}

function draw()
{

}