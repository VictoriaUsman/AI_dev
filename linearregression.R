# Machine Learning Algorithm: Linear Regression

# Step 1: Load the dataset
data(mtcars)

# Step 2: Split the dataset into training and testing sets
# Set a random seed for reproducibility
set.seed(123)
# Generate random indices for training set
train_indices <- sample(1:nrow(mtcars), 0.7 * nrow(mtcars))
# Create the training set
train_data <- mtcars[train_indices, ]
# Create the testing set
test_data <- mtcars[-train_indices, ]

# Step 3: Train the model
# Linear regression model with 'mpg' as the target variable
model <- lm(mpg ~ ., data = train_data)

# Step 4: Make predictions on the testing set
predictions <- predict(model, newdata = test_data)

# Step 5: Evaluate the model
# Mean Squared Error
mse <- mean((test_data$mpg - predictions)^2)
cat("Mean Squared Error:", mse)

# Step 6: Use the trained model for making predictions on new data
# Select the first 5 rows as new data for prediction
new_data <- mtcars[1:5, ]
new_predictions <- predict(model, newdata = new_data)
