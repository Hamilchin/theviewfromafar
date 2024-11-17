// App.js
import React, { Component } from 'react';
import './App.css';
import PostList from './PostList'; 
import Tree from './Tree'; 

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedCategory: null, // No posts rendered initially
      posts: [], // Will hold the posts fetched from the posts.json
      postsLoading: true, // Loading state
    };
  }

  componentDidMount() {
    fetch('/posts.json')
      .then(response => response.json())
      .then(posts => {
        this.setState({ posts:posts, postsLoading: false });
      })
      .catch(error => this.setState({ error, postsLoading: false }));
    }


  handleCategoryChange = (category) => {
    if (this.state.selectedCategory === category) {
      this.setState({ selectedCategory: null });
    } else {
      this.setState({ selectedCategory: category });
    }
  };
  

  render() {
    const { selectedCategory, posts } = this.state;
    console.log(posts)
    console.log(selectedCategory)

    const filteredPosts = selectedCategory && posts[selectedCategory]
    ? posts[selectedCategory] // If category exists, get posts for that category
    : [];

    return (
      <div className="container">
        <Tree onSelectCategory={this.handleCategoryChange} />
        {selectedCategory && <PostList category={selectedCategory} posts={filteredPosts} />}
      </div>
    );
  }
}

export default App;
