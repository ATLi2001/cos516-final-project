# A Visualization Web Application for BDDs
COS 516 Fall 2023 with Professor Aarti Gupta

Authors: Austin Li, Kenny Poor

## Dependencies
This application uses Python 3. It is powered by [Flask](https://flask.palletsprojects.com/en/3.0.x/), [networkx](https://networkx.org/) and [matplotlib](https://matplotlib.org/). See the `requirements.txt` file for a full list of dependencies.


## How to run the application
```
cd flaskr/
bash run.sh
```
This will start up the web application on `127.0.0.1:5000`. Using your preferred browser, navigate to this address. You should see the following screen.

![image](https://github.com/ATLi2001/cos516-final-project/assets/42742696/9c928d2a-c4ad-4fc2-8f10-0d0b429ab85f)

1. Enter the desired boolean formula. Variables can be arbitrary alphanumeric strings. Only the boolean operators AND, OR, NOT, and parenthesis are allowed (`&&, ||, !, ()` respectively).
2. Enter the variable ordering. Use `<` to indicate the order between variables. The order will go left to right (i.e., if entering `a < b < c`, the BDD will interpret this as first variable `a`, then variable `b`, and then finally variable `c`.).
3. As desired, toggle the settings for level order reduction vs dfs reduction, and smallest duplicate subtree vs largest duplicate subtree first.
4. Press submit. This will trigger the BDD generation, as well as the complete reduction process. WARNING - because we are generating an entire BDD, the time is exponential in the number of variables provided. As such, it is best to use smaller boolean formulas (i.e., fewer than 6 or 7 variables). When using more variables, toggle largest duplicate subtree first to speed up the reduction. You will see a "Waiting..." button appear as the back end runs.
5. Once the full reduction is complete, you will see the BDD.
6. You can toggle Previous/Next to step through the reduction.
7. Furthermore, there is an "Adjust Nodes" button at the bottom to adjust the node positions if the visualization ever gets too crowded. It is recommended to only do this near the end of the reduction, as the adjustment can break the expected tree structure in the beginning. You can also "Revert Adjust" afterward as well.
8. After stepping through to the end of the reduction, there will be a "Reset" button to go back to the initial screen and start over. 
