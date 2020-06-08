import axios from 'axios';

class Recommender {
    constructor() {
        this.API_ENDPOINT = "http://localhost:5000";
    }

    async getRecommendations() {
        // TODO: Check localStorage for recommendation data
        const apiUri = `${this.API_ENDPOINT}/recommend`;
        const response = await axios.get(apiUri);
        const cleanResponse = response.data.replace(/NaN/g, "null")
        return JSON.parse(cleanResponse);
    }

    async getPosterUrl(tmdbId) {
        const apiUrl = `https://api.themoviedb.org/3/movie/${tmdbId}?api_key=da60083dc78c5bfd885126e1bcce45b3`;
        const response = await axios.get(apiUrl);
        return `https://image.tmdb.org/t/p/w188_and_h282_bestv2${response.data.poster_path}`;
    }
}

export default new Recommender();