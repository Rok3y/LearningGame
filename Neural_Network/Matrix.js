class Matrix
{
    constructor(rows, cols)
    {
        this.rows = rows;
        this.cols = cols;

        this.values = [];

        for(var i = 0; i < this.rows; i++)
        {
            this.values[i] = [];
            for(var j = 0; j < this.cols; j++)
            {
                this.values[i][j] = 0;
            }
        }
    }

    randomize()
    {
        for(var i = 0; i < this.rows; i++)
        {
            for(var j = 0; j < this.cols; j++)
            {
                this.values[i][j] = Math.random() * 2 -1 ; // Between -1 and 1
            }
        }
    }

    static fromArray(arr)
    {
        let m = new Matrix(arr.length, 1);
        for(let i = 0; i < arr.length; i++)
        {
            m.values[i][0] = arr[i];
        }
        
        return m;
    }

    static subtract(a, b)
    {
        // return a new Matrix a -b 

        let result = new Matrix(a.rows, a.cols);

        for(var i = 0; i < result.rows; i++)
        {
            for(var j = 0; j < result.cols; j++)
            {
                result.values[i][j] = a.values[i][j] - b.values[i][j];
            }
        }

        return result;

    }

    toArray()
    {
        let arr = [];
        for(var i = 0; i < this.rows; i++)
        {
            for(var j = 0; j < this.cols; j++)
            {
                arr.push(this.values[i][j]);
            }
        }

        return arr;
    }

    add(n) // If n is Matrix add element wise
    {
        if(n instanceof Matrix)
        {
            for(var i = 0; i < this.rows; i++)
            {
                for(var j = 0; j < this.cols; j++)
                {
                    this.values[i][j] += n.values[i][j];
                }
            }
        }
        else
        {
            for(var i = 0; i < this.rows; i++)
            {
                for(var j = 0; j < this.cols; j++)
                {
                    this.values[i][j] += n;
                }
            }       
        }
    }

    static multipy(m1, m2)
    {
        // Matrix product
        if(m1.cols !== m2.rows)
        {
            console.log("Columns of A must match rows of B");
            return undefined;
        }
        
        var result = new Matrix(m1.rows, m2.cols);
        
        for(var i = 0; i < result.rows; i++)
        {
            for(var j = 0; j < result.cols; j++)
            {
                // Dot product of values in col
                var sum = 0;
                for(var k = 0; k < m1.cols; k++)
                {
                    sum += m1.values[i][k] * m2.values[k][j];
                }
                result.values[i][j] = sum;
            }
        }
        
        return result;
    }

    multipy(n)
    {
        // Scalar product
        for(var i = 0; i < this.rows; i++)
        {
            for(var j = 0; j < this.cols; j++)
            {
                this.values[i][j] *= n;
            }
        }     
    }

    map(fn)
    {
        // Apllay a function to every element of a matric
        for(var i = 0; i < this.rows; i++)
        {
            for(var j = 0; j < this.cols; j++)
            {
                var val = this.values[i][j];
                this.values[i][j] = fn(val);
            }
        }
    }

    static map(mat, fn)
    {
        let result = new Matrix(mat.rows, mat.cols);
        // Apllay a function to every element of a matric
        for(var i = 0; i < mat.rows; i++)
        {
            for(var j = 0; j < mat.cols; j++)
            {
                var val = mat.values[i][j];
                mat.values[i][j] = fn(val);
            }
        }

        return result;
    }


    static transpose(mat)
    {
        var result = new Matrix(mat.cols, mat.rows);
        
        for(var i = 0; i < mat.rows; i++)
        {
            for(var j = 0; j < mat.cols; j++)
            {
                result.values[j][i] = mat.values[i][j];
            }
        }

        return result;
    }

    print()
    {
        console.table(this.values);
    }
}