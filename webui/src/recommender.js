import axios from 'axios';

class Recommender {
    constructor() {
        this.API_ENDPOINT = "http://localhost:5000";
    }

    async getRecommendations() {
        const apiUrl = `${this.API_ENDPOINT}/recommend`;
        let response;
        if (!sessionStorage.getItem('ratings')) 
            response = await axios.get(apiUrl);
        else
            response = await axios.post(apiUrl, JSON.parse(sessionStorage.getItem('ratings')))
        const cleanResponse = response.data.replace(/NaN/g, "null")
        return JSON.parse(cleanResponse);
    }
    
    async getPosterUrl(tmdbId) {
        const apiUrl = `https://api.themoviedb.org/3/movie/${tmdbId}?api_key=da60083dc78c5bfd885126e1bcce45b3`;
        const response = await axios.get(apiUrl);
        return response.data.poster_path ? `https://image.tmdb.org/t/p/w188_and_h282_bestv2${response.data.poster_path}` : undefined;
    }
    
    async searchByTitle(title) {
        const apiUrl = `${this.API_ENDPOINT}/search-movie-name/${encodeURI(title)}`;
        const response = await axios.get(apiUrl);
        const cleanResponse = response.data.replace(/NaN/g, "null")
        return JSON.parse(cleanResponse);
    }

    setRating(movieIdx, rating) {
        let currentRatings = sessionStorage.getItem('ratings');
        if (!currentRatings) currentRatings = "{}";
        currentRatings = JSON.parse(currentRatings);

        currentRatings[movieIdx] = rating;
        sessionStorage.setItem('ratings', JSON.stringify(currentRatings));
    }

    getRating(movieIdx) {
        let currentRatings = sessionStorage.getItem('ratings');
        if (!currentRatings) return 0;
        currentRatings = JSON.parse(currentRatings);
        if (!currentRatings[movieIdx]) return 0;
        return currentRatings[movieIdx];
    }

    getRatings() {
        let currentRatings = sessionStorage.getItem('ratings');
        if (!currentRatings) return undefined;
        return JSON.parse(currentRatings);
    }
}

export default new Recommender();