import React, { useState, useEffect } from 'react';

function Rating(props) {
  const {
    post, i, deleteComment, handleRate,
  } = props;
  /* This creates our forms. Note: &nbsp; is for a single white space*/
  return (
    <form htmlFor="individual_comment_rating">
      <label htmlFor="movie id">
        Movie Id:&nbsp;
        {post.movie_id}
      </label>
      <label>
        rating:&nbsp;
      </label>
      <input type="number" name="rating" onChange={(e) => handleRate(e.target.value, i)} value={post.rating} />
      <label>comment:&nbsp;</label>
      <textarea value={post.comment} />
      <input type="submit" value="DELETE" onClick={(e) => deleteComment(e, i)} />
    </form>
  );
}
function App() {
  const [jsonData, setJsonData] = useState([]);

  const handleRating = (event, index) => {
    const newJson = jsonData.slice();
    newJson[index].rating = event;
    setJsonData(newJson);
  }
  const handleDelete = (event, index) => {
    event.preventDefault();
    alert('Leave rating as negative for comment to be deleted when saved');
    const newJson = jsonData.slice();
    newJson[index].rating = -10;
    setJsonData(newJson);
  }
  /* This is where we will receive our initial data*/
  useEffect(() => {
    const fetchJSON = async () => {
      const response = await fetch("/get_my_comments");
      let json = await response.json();
      setJsonData(json);
    };
    fetchJSON();
  }, []);
  function submitData() {
    /* When we hit save, we'll call this function, which will send back our data to our python files*/
    const data = jsonData;
    fetch('/update_my_comments', {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then(res => res.json())
      .then(res => console.log(res));
    alert("Changes Saved successfully!");
  };
  var p = 0;
  /*  Here we will iterate through our array of dictionaries holding our
      ratings and comments, and we will create forms for them which will be editable*/
  return (
    <div>
      <div>
        <h1>Your reviewed Comments</h1>
        {jsonData.map(postDetails => {
          return <p> <Rating post={postDetails} i={p++} deleteComment={handleDelete} handleRate={handleRating} /> </p>
        })}
      </div>
      <input type="submit" value="Save" onClick={submitData} />
    </div>
  );
}
export default App;