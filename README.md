In this project, I have trained a machine learning model to predict the earning per share (EPS) by a bank. 
For this, we use the data which is avaliable on  public plateform to train the model.
Following we disuss the steps we followed:
1. We first import the data, and check for outliers in columns by calculating IQR.
2. We check for multicollinearity between columns, for this we calculate VIF and drop the columns having VIF > 200.
3. We use the XGBoost technique to train our model and checked its accuracy.
4. We hypertune the parameter from basics using basic for loop. Subsequenlty, we store all the  outputs in an excel sheet.
