import React, { Component } from 'react';

class SearchForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            query: ""
        }

        // Bind functions
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e) {
        const { name, value } = e.target;
        this.setState({ [name]: value });
    }

    render() { 
        return (
            <div className="search-container-bg">
                <div className="search-container">
                    <div className="container">
                        <h1>Looking for recommendations?</h1>
                        <p>Rate movies and get personalized recommendations</p>
                        <div className="input-wrapper">
                            <div className="row">
                                <div className="col">
                                    <input type="text" name="query" value={this.state.query} onChange={this.handleChange} placeholder="Search for Movies" autoFocus/>
                                </div>
                                <div className="col-2">
                                    <button onClick={() => {if (this.props.onClick) this.props.onClick(this.state.query)}}>Search</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
 
export default SearchForm;