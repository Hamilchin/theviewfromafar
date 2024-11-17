// PostList.js
import React, { Component } from 'react';
import './App.css';

class PostList extends Component {
  constructor(props) {
        super(props);
        this.state = {};
    }

  renderPosts() {
    const {posts} = this.props;

    return posts.map((post, index) => (
      <li key={index}>
        <div className="separator">~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</div>
        <span className="post-title"><a href={"posts/" + post.slug + ".html"}>{post.title}</a></span>
        <span className="post-date">{post.written}</span>
      </li>
    ));
  }

  render() {
    const renderedPosts = this.renderPosts();

    return (
      <main>
        <ul className="post-list">
          {renderedPosts}
          {renderedPosts.length !== 0 && <div className="separator">~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</div>}
          {renderedPosts.length <= 2 && <div className="separator">More to come...</div>}
        </ul>

      </main>
    );
  }
}

export default PostList;
