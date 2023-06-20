---
permalink: /blog/2023-06-19-ai-for-used-cars
title: "AI for Used Cars"
author: "Fortunato Wheels"
tab_title: "Fortunato Wheels | AI for Used Cars"
description: "How we use AI to Price Used Cars."
image: /assets/2023-06-19-ai-for-used-cars/ai-used-cars-image_wide.jpg
date: 2023-06-19
---

# How we use AI to Price Used Cars

 If you're reading this, you're probably A) looking to buy a used car, or B) looking to sell a used car. Either way, you're in the right place, we're here to shed light onto what contributes to vehicle prices and hopefully this article will give you some insight into how we use AI and machine learning to predict the price of used cars.

## Where We Get Our Data

We scour the internet for open source datasets and have compiled a **database of over 3M+ used car ads from Canada and the US**. This includes all of the make, model, trim and much more. We then used open source **historical exchange rate data** to convert the prices to Canadian dollars. 

## How We Train Our Machine Learning Models

We trained multiple machine learning models **to predict not only the price but also the upper and lower bands of the expected price**. This is what we call the "confidence interval". The confidence interval is the range of values that we are 95% confident that the actual price will fall within.

After spending months prototyping and training different models and doing feature engineering, we finally settled on a model and set of features that balances accuracy predicted price and ease of use.

We found that the most important features for predicting the price of a used car are:
- **Age of Vehicle at Posting (years)**: this is the age of the vehicle at the time the ad was posted which allows the models to learn from all historical data and not just the most recent data.
- **Yearly Mileage (kms)**: this is the average yearly mileage of the vehicle. This is a good indicator of how much the vehicle has been used and how much wear and tear it has in conjunction with the age of the vehicle.
- **Vehicle Drive System (AWD, 4WD, etc.)**: this is the drive system of the vehicle. This is a good indicator of the type of vehicle and can dramatically change the price of the vehicle.

We tuned and **trained our models over 100+hrs to get the best accuracy** and confidence intervals. 

