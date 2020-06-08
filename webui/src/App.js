import React from 'react';
import './App.css';

// CSS
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// Components
import Navbar from './components/Navbar';
import MovieContainer from './components/MovieContainer';
import Movie from './components/Movie';
import SearchForm from './components/SearchForm';

function App() {
  return (
    <div className="root">
      <Navbar/>
      <div className="container">
        <SearchForm/>
        <MovieContainer title="Popular Movies">
          <Movie title="Test Movie 1" artwork="https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_UX182_CR0,0,182,268_AL_.jpg"/>
          <Movie title="Test Movie 2"/>
          <Movie title="Test Movie 2"/>
          <Movie title="Test Movie 2"/>
          <Movie title="Test Movie 2"/>
          <Movie title="Test Movie 2"/>
          <Movie title="Test Movie 2"/>
          <Movie title="Test Movie 2"/>
          <Movie title="Test Movie 2"/>
          <Movie title="Test Movie 2"/>
        </MovieContainer>
      </div>
    </div>
  );
}

export default App;
