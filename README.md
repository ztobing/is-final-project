# Movie Recommender System
A movie recommendation system that uses content based filtering based on the movie's metadata.

An Intelligent System final project.

Made by
- David Amadeo - [GitHub](https://github.com/davidamadeo)
- Ryo Yenata - [GitHub](https://github.com/ryoyen1)
- Zefanya Tobing

![](https://github.com/zefryuuko/is-final-project/blob/master/img/preview.png?raw=true)

## Implementation
We chose to create recommendations based on the tags of the movies such as keywords, genres and actors. This yields better results compared to a recommender that relies on the movie summary. That is because we are using vectorizer to create a vector from the movie metadata. Using summary causes a lot of unrelated movies to be put together as a recommendation because the summary may have several keywords that are the same. For example, `Toy Story` has a character named `Andy`, and it got matched with other movies with `Andy` in the summary, which is not optimal.

For searching, we used a fuzzy search library named `fuzzywuzzy`. It allowed us to make the movie searching experience much better for the user because the users do not have to type the exact movie title to get a result.

For the user interface, we implemented a simple web-based user interface that interacts using REST API. We used `react` as our front-end framework of choice, and `flask` as our back-end framework. For the recommender engine itself, we used several libraries such as `numpy`, `pandas` and `sklearn`.

## Dataset used
We used `The Movies Dataset` from [Kaggle](https://s.zef.sh/isdataset), which contains 45.000 movies with 26 million ratings from 270.000 users.

## How to use
To run this program, you need to install all of the dependencies first. For the API, you need Python with all of the libraries required by this program installed. We recommend installing Anaconda as it has all of the libraries that this program needs, except `flask` and `fuzzywuzzy`, which you could install manually using `pip`. 

For the web UI, you need Node.js to run the web server. After cloning the repo, you need to select to the `webui` directory and run the following commands.
```
npm install
npm start
```
You only need to run `npm install` once. React will automatically open a browser window for you directly to the page.

A demo video can be found on [s.zef.sh/isvideo](https://s.zef.sh/isvideo)
