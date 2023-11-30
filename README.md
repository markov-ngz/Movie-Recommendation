# Movie Recommendation System 

<h2>A. Presentation</h2>
Project introducing MLOps approach <br>
The goal is for a user to make recommendations based on a given title or a  descritption. <br>
<br>
<h1>B. How does the system work ? </h1>
<h3> 0. System Schema </h3>
<img src="images/app_schema_1.jpg" width=80%><br>
<br>
<br>
<h2> 1. Data's API </h2>
1. Raw data is extracted ( imdb scrapping and api requests ), transformed and loaded in the database.<br>
2. Data is created (<b> see database_conception.pdf </b> ) <br>
3. An API have access to the database <br>
4. Data can then be request with prior JWT authentication <br>
<h2> 2. Model's API </h2>
1. With the data, the vector's embeddings of the movies's description are computed by a BERT model.<br>
2. Having all the embeddings, the cosine similarity matrix is then saved as a static file in the model's API.<br>
3. An API with the cosine matrix can then compare from a given title , the most similar descriptions vectors. Also the API can compute with the model the embeddings and directly compare it with the one it has. <br>
<h2>3. Website</h2> 
An authenticated user can : <br>
- access all the movies data  <br>
- get the recommendations
<h3> A few peeks at the result : </h3>
 Homepage<br>
 <br>
<img src="images/website_view1.PNG" width=95%><br>
<br>
Recommendation page <br>
<br>
<img src="images/website_view2.PNG" width=95%><br>

<h2>Notes</h2>
This was a school project, no safety for production or whatsoever is ensured as it was not the goal.<br>
For the same reason , tests were not done. 
