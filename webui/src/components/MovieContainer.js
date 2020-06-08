import React, { Component } from 'react';

class MovieContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }

    render() { 
        return (
            <div className="movie-container">
                <h2 className="mt-3">{this.props.title ? this.props.title : "! MISSING TITLE ATTRIBUTE !"}</h2>
                <div className="d-flex flex-wrap justify-content-around">
                    {this.props.children}
                </div>
            </div>
        );
    }
}
 
export default MovieContainer;