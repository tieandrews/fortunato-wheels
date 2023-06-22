---
permalink: /blog/can-chatgpt-buy-used-cars
title: "Can ChatGPT Buy Used Cars?"
author: "Fortunato Wheels"
tab_title: "Fortunato Wheels"
description: "Does ChatGPT have the power to price and buy used cars?"
image: /assets/2023-06-20_chatgpt-car-pricing/dalle-robot-negotiating-car-price.png
date: 2023-06-20
---

Welcome to this weeks blog, where we dive into the fascinating world of buying and pricing used cars! Today, we explore an intriguing question: Can ChatGPT, an advanced AI language model, price vehicles accurately and potentially buy cars? Join us on this journey as we unravel the potential of AI technology in the automotive world.

**Contents:**

- [The Rise of AI (a.k.a. ChatGPT)](#the-rise-of-ai-aka-chatgpt)
- [How Does ChatGPT Price Cars?](#how-does-chatgpt-price-cars)
- [Bing's Aftermarket Upgrades on ChatGPT](#bings-aftermarket-upgrades-on-chatgpt)
- [How does it Compare to Fortunato Wheels?](#how-does-it-compare-to-fortunato-wheels)
- [ChatGPT is Down but Not Out: LangChain](#chatgpt-is-down-but-not-out-langchain)
- [Conclusion: Rise of the Bots?](#conclusion-rise-of-the-bots)
- [Links](#links)

## The Rise of AI (a.k.a. ChatGPT)

Artificial Intelligence (AI) has revolutionized numerous industries, and the automotive market is no exception. With AI-powered systems assisting in various aspects of car manufacturing, it's only natural to wonder if AI can extend its reach to help us buy or price used cars. One such AI language model, ChatGPT, has garnered attention for its ability to understand and generate human-like text. But can it truly aid us in this complex endeavor? Let's find out.

## How Does ChatGPT Price Cars?

ChatGPT is designed to generate human-like responses based on the data it has been trained on. However, it's important to note that ChatGPT is an AI language model and lacks real-time access to current market data, pricing trends, or specific details about individual used cars. As a result, it cannot directly buy or price used cars on its own.

We prompted ChatGPT with **"How much do you think a used 2020 Honda CRV with 80000km's on it and all wheel drive is worth? Provide a mean price as well as upper/lower 95% confidence intervals"** and this was it's response:

![ChatGPT pricing a Honda CRV](../../../assets/2023-06-20_chatgpt-car-pricing/chatgpt-honda-crv-pricing.png#article)

So....not very useful, it clearly hasn't ingested much information from car ads it was trained on. Let's see if we can get it to do better.

## Bing's Aftermarket Upgrades on ChatGPT

While ChatGPT has vast knowledge stored within its virtual brain, it relies on historical information available up until September 2021. This means it lacks up-to-date market data, including fluctuations in demand, location-specific pricing, or a vehicle's history. Bing has made the ChatGPT interface able to interact and query the internet so we figured we'd see if it can do any better!

![Bing chat asked the same question to price a Honda CRV](../../../assets/2023-06-20_chatgpt-car-pricing/bing-honda-crv-pricing.png#article)

This is much better! Bing was able to find a listing for a 2020 Honda CRV with 80000km's on it and all wheel drive and price it at $30,000 CAD. This is much closer to the actual price of a 2020 Honda CRV with 80000km's on it and all wheel drive which is around $32,000 CAD. However, it's still not perfect and it's not able to provide the upper and lower 95% confidence intervals.

## How does it Compare to Fortunato Wheels?

We took the middle of Bing's price estimate (~$37k CAD) and fed it into our tool and it looks like ChatGPT might be a ways off!

![Fortunato Wheels pricing a Honda CRV](../../../assets/2023-06-20_chatgpt-car-pricing/fwheels-honda-crv-price.png#article)

How do the standard sites people turn to fair? Kelly Blue Book and Carfax are two common tools used to price cars and here's how their prices compare. **NOTE: both sites required providing more info about trim, extra options, service, etc.**

![Carfax and Kelly Blue Book price estimates for CRV](../../../assets/2023-06-20_chatgpt-car-pricing/kbb-carfax-side-by-side.png#article)

So looks like ChatGPT is still a ways off from being able to price cars accurately. However, it's still a very powerful tool for researching used cars and can be used to get a rough estimate of what a car is worth.

## ChatGPT is Down but Not Out: LangChain

Now pricing a vehicle is only one part of the car buying process. Arguably the more time consuming process is contacting buyers, coordinating viewings, negotiating price, etc. This is where ChatGPT can really shine and by integrating Fortunato Wheels with LangChain. LangChain is a framework for developing applications powered by language models. It enables applications that are data-aware and allow a language model to interact with its environment.

It's not hard to imagine ChatGPT or any of the plethora of LLM'sdoing:

1. Contacting dealers with the vehicle you're looking for and rough specs
2. Dealing with initial **negotiations using Fortunato Wheels pricing**
3. Pushing back and dealing with counter offers

![ChatGPT offering and negotiating to buy a car](../../../assets/2023-06-20_chatgpt-car-pricing/chatgpt-car-buying.png#article)

## Conclusion: Rise of the Bots?

While ChatGPT cannot directly buy or price used cars due to its limitations, it serves as a valuable research tool for prospective buyers. By leveraging its vast knowledge and combining it with tools like Fortunato Wheels it's conceivable you could make an end to end car scouting and buying tool.

Embrace the power of AI as a valuable companion in your used car buying journey, but never underestimate the importance of human expertise and real-time information!

## Links

- https://www.carfax.ca/
- https://www.kbb.ca/
- https://chat.openai.com/
