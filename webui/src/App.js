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
      movies: []
    }

    // Bind functions
    this.loadRecommendations = this.loadRecommendations.bind(this);
    this.loadPoster = this.loadPoster.bind(this);
  }

  loadRecommendations() {
    Recommender.getRecommendations().then(movies => {
      this.setState({ movies });
      this.state.movies.forEach(movie => {
        this.loadPoster(movie.id)
      })
    });
  }

  loadPoster(tmdbId) {
    Recommender.getPosterUrl(tmdbId).then(url => this.setState({ [tmdbId]: url }));
  }

  componentDidMount() {
    this.loadRecommendations()
  }

  render() {
    return (
      <div className="root">
        <Navbar/>
        <div className="container">
          <SearchForm/>
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
        </div>
      </div>
    );
  }
}


export default App;
