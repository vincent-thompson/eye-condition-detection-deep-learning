# Eye Condition Detection with Deep Learning

### Introduction

The COVID-19 pandemic has accelerated countless changes in the digital health space, including telehealth policy changes aimed at supporting increased access to care during and after the pandemic.

There are still major hurdles to telehealth adoption though, with the key hurdle being lack of access and awareness. Only **1 in 10** Americans use telehealth services, but nearly **75%** say they don't have access or are unaware of telehealth options.<sup>1</sup>  On top of that, many practices lack interstate licensing, making it difficult to continue care with established in different states, and there are numerous other logistical barries including inconsistent reimbursement, regulatory challenges, privacy concerns, and a lack of evidence regarding impact on healthcare costs.

In the interim while telehealth continues to scale while tackling the short- and long-term consequences of doing so, many patients are forced to weigh the added complications associated with in-person healthcare visits during a pandemic, things like office closures/limited operating hours, the effects of patient surge on facilities, and increased COVID-19 exposure for themselves and healthcare workers (especially those in high-risk categories), to name just a few.

I was interested in exploring how computer vision could help patients with visual symptoms better understand the likelihood of a certain condition existing, allowing them to make more informed choices about wehter an in-person visit with a healthcare professional might be necessary.  Obviously a machine learning algorithm cannot conduct physical examinations, schedule imaging, or do a host of other things that a healthcare professional can to make a proper diagnosis.  My goal was merely to create a tool that could connect visual symptoms to potential conditions, so that, in the absence of telehealth access, patients can better assess the urgency of a healthcare visit. To that end, I created a convolutional neural network that, given an image, can detect the existence of various eye conditions such as styes, conjunctivitis, and cataracts.

### Project Workflow and Tools Used

- To generate my dataset, I scraped images from various search engines, including Google and Bing Images, using Selenium and Beautiful Soup.<sup>2,3</sup>  I scraped the images using a diverse set of search terms in relatively small chunks (30-40 results per search term) to ensure a dataset that was as balanced as possible across eye colors, age range, sex, and skin complexion. 

- The model was built using the [Keras](https://keras.io/api/) Deep Learning API, with Tensorflow as the computational backend, and the code for my model building and tuning can be found in the [model_tuning](https://github.com/vincent-thompson/eye-condition-detection-deep-learning/blob/main/model_tuning.ipynb) Jupyter notebook.<sup>4</sup>  All model building was done on a GPU via Google Compute Engine.

- The weights associated with the model that achieved the highest validation accuracy were saved and stored in the weights folder to be used for predictions.  

- In order to put the model into production, I built a Flask application that leverages a module I wrote for generating predictions which can be found [here](https://github.com/vincent-thompson/eye-condition-detection-deep-learning/blob/main/website/personal_website/generate_prediction.py). The code used to build the web application is contained in the [website](https://github.com/vincent-thompson/eye-condition-detection-deep-learning/tree/main/website) directory, and the application was hosted with Google App Engine.

**TL;DR:**

Web Scraping: BeautifulSoup/Selenium  
Model Building: Keras/Tensorflow  
Cloud Computing: GCP  
Web Application: Flask, GAE  

<hr>

### References

1. [One in 10 Americans Use Telehealth, But Nearly 75% Lack Awareness or Access, J.D. Power Finds](https://www.americantelemed.org/industry-news/one-in-10-americans-use-telehealth-but-nearly-75-lack-awareness-or-access-j-d-power-finds/#:~:text=COSTA%20MESA%2C%20Calif.%3A%2031,and%20real%2Dworld%20patient%20concerns.)
2. [Bing Image Scraper Example](https://gist.github.com/stephenhouser/c5e2b921c3770ed47eb3b75efbc94799)
3. [Scraping image from Google](https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d)
4. [Transfer learning & fine-tuning in Keras](https://keras.io/guides/transfer_learning/)