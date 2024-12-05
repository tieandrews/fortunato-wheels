# Fortunato Wheels
(Fortunato: Latin word for "lucky")

Fortunato wheels takes the guesswork out of buying a used car. It does this by compiling datasets of used cars from multiple websites, analyzing the data to identify trends and baselines for car prices, then make this information available to users in an interactive tool to evaluate car prices.

**Try it out here!** *June 2024 Update: I've stopped hosting the site for now to reduce my hosting costs, please reach out if you'd like to see it in action
![](assets/fortunato-wheels-homepage.png)

## Goal: Help myself buy a new car at a good price and learn along the way

At the start of this project I was planning to buy a new car in 6 months time and had some fresh data science skills I wanted to apply. I decided to build Fortunato Wheels to:
- monitor used car site prices for me
- help me know if a price was good or bad
- explore a large (>3M) ads dataset to see what might be lurking in the data

The original proposal for this personal project is located [here](PROPOSAL.md).

## Exploration of the 3M+ ads dataset

To start using Fortunato wheels you *could browse through the database of used car ads. You can filter by make, model, year, price, and condition. You can also use the slider to filter by mileage.

![](assets/fortunato-wheels-demo.gif)

1. Use the dropdowns on the left to filter by make, model, year and price. Once happy with your filters click the "Apply Filters" button. The number of matching ads will be displayed at the bottom of the filters so you know how many ads you're looking at.
2. Look at the price by manufacturer and year on the right and observe how the best fit line (LOWESS model) changes based on your filters
3. Check out what the distribution of vehicles condition/mileage looks like on the bottom two plots

## Analyze an Ad

Once you have an ad you're interested in, you can analyze it to see how it compares to the rest of the ads in the dataset. You can see the ad's price, mileage, condition, and location. You can also see how the ad compares to the rest of the ads in the dataset in terms of predicted price and our confidence intervals for that make, model, year, and condition.

![](src/assets/2023-07-12_when-will-used-car-prices-go-down/)

## References

- Craigslist Used Cars Dataset, Austin Reese, https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data