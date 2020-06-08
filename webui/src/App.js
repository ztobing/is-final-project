import React, { Component } from 'react';
import './App.css';

// Services
import Recommender from './recommender';

// CSS
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// Components
import Navbar from './components/Navbar';
import MovieContainer from './components/MovieContainer';
import Movie from './components/Movie';
import SearchForm from './components/SearchForm';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      movies: [],
      searchResults: [],
      searchQuery: "",
      isLoading: true
    }

    // Bind functions
    this.loadRecommendations = this.loadRecommendations.bind(this);
    this.loadPoster = this.loadPoster.bind(this);
    this.handleSearchBox = this.handleSearchBox.bind(this);
  }

  loadRecommendations() {
    Recommender.getRecommendations().then(movies => {
      this.setState({ movies, searchResults: [], searchQuery: "", isLoading: false });
      this.state.movies.forEach(movie => {
        this.loadPoster(movie.id)
      });
    });
  }

  loadPoster(tmdbId) {
    Recommender.getPosterUrl(tmdbId).then(url => this.setState({ [tmdbId]: url }));
  }

  componentDidMount() {
    this.loadRecommendations()
  }

  handleSearchBox(searchQuery) {
    if (searchQuery === "") { this.loadRecommendations(); return; }

    this.setState({ isLoading: true });
    Recommender.searchByTitle(searchQuery).then(searchResults => {
      this.setState({ searchResults, searchQuery, isLoading: false });
      this.state.searchResults.forEach(movie => {
        this.loadPoster(movie.id);
      });
    });
  }

  render() {
    console.log(this.state);
    return (
      <div className="root">
        {/* <Navbar/> */}
        <SearchForm onClick={this.handleSearchBox}/>
        <div className="container">
          { this.state.isLoading ?
            <div style={{textAlign: "center"}}>
              <h3>Loading...</h3>
            </div>
          : null}          
          
          { this.state.searchResults.length > 0  && !this.state.isLoading ?
            <MovieContainer title={`Search results for "${this.state.searchQuery}"`}>
              { this.state.searchResults.map(movie => {
                  return <Movie 
                    key={movie.id}
                    id={movie.id}
                    artwork={this.state[movie.id] ? this.state[movie.id] : null}
                    title={movie.title}
                  />
                })
              }
            </MovieContainer>
          : null }

          { this.state.searchResults.length === 0 && !this.state.isLoading ?
            <MovieContainer title="All-time Popular">
              { this.state.movies.length > 0 ?
                this.state.movies.map(movie => {
                  return <Movie 
                    key={movie.id}
                    id={movie.id}
                    artwork={this.state[movie.id] ? this.state[movie.id] : null}
                    title={movie.title}
                  />
                })
              : null }
            </MovieContainer>
          : null }
        </div>
      </div>
    );
  }
}


export default App;
