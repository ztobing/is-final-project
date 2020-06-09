import React, { Component } from 'react';

// Services
import Recommender from '../recommender';

class Movie extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rating: Recommender.getRating(this.props.id)
        };

        // Bind functions
        this.handleStarChange = this.handleStarChange.bind(this);
    }

    handleStarChange(e) {
        const { id } = e.target;
        this.setState({ rating: Number.parseInt(id) });
        Recommender.setRating(this.props.id, id);
    }

    render() { 
        return ( 
            <div className="movie" style={{backgroundImage: `url('${this.props.artwork}')`}} id={this.props.id}>
                <div className={`title ${ this.props.artwork ? "hidden" : "" }`}>
                    <div>{ this.props.title }</div>
                    <div className="user-rating mt-3">
                        <div><small>Your rating:</small></div>
                        <i className={`fas fa-star ${this.state.rating >= 1 ? "checked" : ""}`} id="1" onClick={this.handleStarChange}/>
                        <i className={`fas fa-star ${this.state.rating >= 2 ? "checked" : ""}`} id="2" onClick={this.handleStarChange}/>
                        <i className={`fas fa-star ${this.state.rating >= 3 ? "checked" : ""}`} id="3" onClick={this.handleStarChange}/>
                        <i className={`fas fa-star ${this.state.rating >= 4 ? "checked" : ""}`} id="4" onClick={this.handleStarChange}/>
                        <i className={`fas fa-star ${this.state.rating >= 5 ? "checked" : ""}`} id="5" onClick={this.handleStarChange}/>
                    </div>
                </div>             
            </div>
         );
    }
}
 
export default Movie;