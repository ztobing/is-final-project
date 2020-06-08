import React, { Component } from 'react';

class Movie extends Component {
    constructor(props) {
        super(props);
        this.state = {  }
    }

    render() { 
        return ( 
            <div className="movie" style={{backgroundImage: `url('${this.props.artwork}')`}}>
                <span className={`title ${ this.props.artwork ? "hidden" : "" }`}>
                    { this.props.title }
                </span>             
            </div>
         );
    }
}
 
export default Movie;