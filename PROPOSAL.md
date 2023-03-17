# Fortunato Wheels Proposal
(fortunato: Latin for "lucky")

Author: Ty Andrews
Date: March 9, 2023

Statement of Purpose: Turning buying used cars from luck into a science.

## Motivation & Purpose

The primary motivation for buying a used car is price. Used cars are cheaper than new cars. This comes at a cost, reliability, condition, and sometimes more importantly, is it the car you WANT. Used car market places such as Craigslist or Kijiji make it easy to post a car for sale with spots for all the information mentioned above and more. 

The challenge becomes: how do you comb these sights for what you want, look over the ads that match your needs, then decide if it's a good enough deal to make an offer. Each step takes time and has hidden complexities. How much should a 2 year old Toyota Rav4 with 100k km's on it compare to a 5 year old Rav4 with 60k km's? Is a Toyota Rav 4 from 2019 with 70k km's, in car entertainment system but no winter tires cost $22k or $24k? 

Those questions are difficult to answer for the average user of those websites and shows a gap between having cars able to be posted easily and being able to have them be bought easily. Fortunato wheels is meant to reduce the time and mental load to look for and purchase a used car. It will do this by compiling datasets of used cars from multiple websites, analyzing the data to identify trends and baselines for car prices, then make this information available to users in an interactive tool to evaluate car prices.

The dashboard will first focus on Toyota Rav4's and Honda CRV's as these are of personal interest to me buying one this coming summer.

## Data Description

For the purposes of DSCI 532 the dashboard tool will use the Kaggle Craigslist used car ads dataset created by [AustinReese](https://github.com/AustinReese/UsedVehicleSearch). The dataset contains XXXX car ads posted up to 2019 from across the US. The primary fields include:

| Field          | Description                                                   | Quality                                                                                         |
| -------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `price`        | the posted price of the car in $USD                           | Every ad has a price but some ads have nonsenicl values which are removed ($12345, $9999999999) |
| `condition`    | user chosen condition of the car, values include: new, ...... | Majority of the vehicles (XX%) have a condition                                                 |
| `region`       | the local craigslist region in which the ad was posted        | All ads have a region value                                                                     |
| `model`        | the model of the car                                          | there are inconsistencies in naming of similar car models which have been cleaned               |
| `odometer_mi`  | the current odometer reading of the vehicle in miles          |                                                                                                 |
| `manufacturer` | the name of the car manufacturer                              | very few missing values, < XX                                                                   |
| `transmission` | what type of transmission, e.g. automatic, manual etc.        | many missing inputs for this                                                                    |

## Research Questions

The tool will primarily focus on two primary questions:

1. **Exploratory** - How do used car prices vary between manufacturers, models, years, etc.?
	- **Exploration** - when starting on the journey of buying a used car it is useful to understand options in terms of balancing budget, quality and personal preferences
	- the Explore tab will contain:
		- Filter options for make, manufacturer, condition
		- Sliders to select year range and price range
		- Visualizations to observe the effect of slicing the data into the areas of interest for each user (more details in the example layout)
2. **Analysis** (stretch goal for Ind. Ass.) - Given a used car ads info about the vehicle, how does the price compare to similar vehicles?
	- once settled on specifics of a vehicle it is useful to be able to understand what influences a vehicles price and be able to compare a currently listed vehicle with past listings of similar model, year, etc.
	- the Analysis tab will contain:
		- a place to enter the info of the vehicle the user is considering
		- an "Analyze" button will start a filtering/analysis process and display results below including:
			- a price distribution plot for vehicles matching the chosen criteria
			- a value saying the input info is in the top/bottom X% of similar vehicles base don percentiles

## User Personas

Alison Meiers
Age: 31
Gender: Female
Job: Mechanical Engineer
Description:
- she is saving for a house but needs to buy a new vehicle to be able to carry skis and mountain bikes into the mountains
- reliability is important because she is often on quiet backroads far from repair shops
- she has driven beater cars in the past and wants to find a good deal on a medium used Honda CRV or Toyota Rav4 as they have the space needed and are known to be reliable
- she works full time and likes to spend his evenings outdoors so hunting used car sites is a pain in the butt

Tyrone Andrews
Age: 38
Gender: Male
Job: stay at home dad
Description:
- he has one 4 year old daughter with autism who he takes care of full time
- he wants to replace his Volkswagen golf with something like a Toyota Rav4 or Honda CRV to be able to take his wife and daughter on more weekend trips
- the process of monitoring multiple sites and watching for car ads manually is daunting and time consuming to understand what options there are for vehicles
- he just wants to know what to look for that's in his budget so he can find a good deal and have fun with his family

## Proposed Layout

Below is the proposed layout for the "Explore Ads" page that is the focus for this milestone:
![](/assets/fortunato-wheels-explre-ads-proposal-layout.png)