// Get a cookie by a given name and return content
function getCookieByName(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}


// Run on page loaded
document.addEventListener('DOMContentLoaded', () => {

  // Remove the login button if the user has a cookie
  if (getCookieByName('token')) {
    document.getElementById('login-link').remove();
  }


  // Add login functionality if this page is login.html
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      form = document.getElementById('login-form');
      // Send form data to login function
      loginUser(form.elements['email'].value, form.elements['password'].value)
    });
  }


  // Run this if page is index
  const index = document.getElementById('places-list');
  if (index) {
    // Add options to select box
    const select = document.getElementById('price-filter');
    const optionAll = document.createElement('option');
    optionAll.text = 'All'
    const option100 = document.createElement('option');
    option100.text = '100'
    const option50 = document.createElement('option');
    option50.text = '50'
    const option10 = document.createElement('option');
    option10.text = '10'
    select.add(optionAll);
    select.add(option100);
    select.add(option50);
    select.add(option10);
    select.addEventListener('change', (event) => {
      // Get the selected price value
      const filter = parseInt(document.getElementById('price-filter').value);
      // Iterate over the places and show/hide them based on the selected price
      const list = document.getElementById('places-list').children[0].children;
      for (let i = 0; i < list.length; i++) {
        if (isNaN(filter) || filter > parseInt(list[i].classList[1])) {
          list[i].style.display = 'flex';
        } else {
          list[i].style.display = 'none';
        }
      }
    });
    // Load all places and fill page
    getAllPlaces();
  }


  // Run this if page is place detail
  const detail = document.getElementById('place-details')
  if (detail) {
    // review form should be hidden by default
    document.getElementById('add-review').style.display = 'None';
    // Load place details from ID
    const param = window.location.search.split("=")[1];
    getPlace(param);
  }
});


// Handle login request
async function loginUser(email, password) {
  // Add a loading / message box while waiting
  const message = document.getElementById('login-form-message');
  message.textContent = 'Processing your request...';
  const response = await fetch('http://localhost:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });
  // Handle the response
  console.log(response);
  // If login failed
  if (response.status === 401) {
    message.textContent = 'Your email or password is incorrect, please try again.';
  } else if (response.status !== 200) {
    message.textContent = 'Something unexpected happened, please try again later.';
  } else if (response.status === 200) {
    message.textContent = 'Login successful, please wait...';
    document.cookie = `token=${(await response.json()).access_token}; path=/`;
    document.location.href = 'index';
  }
}


// Send request for all places from api
async function getAllPlaces() {
  const headerObj = {
    'Content-Type': 'application/json'
  };
  // Add JWT if we have it in cookie
  const cookie = getCookieByName('token');
  if (cookie) {
    headerObj['Authorizaton'] = 'bearer ' + cookie;
  }
  // Send fetch
  const response = await fetch('http://localhost:5000/api/v1/places/', {
    method: 'GET',
    headers: headerObj
  })
  const data = await response.json();
  section = document.getElementById('places-list');
  // Check if there are no places in response
  if (data.length === 0) {
    const message = document.createElement('h2');
    message.className = 'place-card';
    message.textContent = 'There are no places here yet!';
    section.appendChild(message);
    return;
  }

  // Make unordered list
  const list = document.createElement('ul');
  // Make item for each place in list
  for (let i = 0; i < data.length; i++) {
    const item = document.createElement('li');
    // Title
    const title = document.createElement('h2');
    title.textContent = data[i].title;
    // Price
    const price = document.createElement('p');
    price.textContent = 'Price per night: $' + data[i].price;
    // Details
    const details = document.createElement('a');
    details.textContent = 'View Details';
    details.href = 'place?id=' + data[i].id;
    details.className = 'details-button';
    item.appendChild(title);
    item.appendChild(price);
    item.appendChild(details);
    item.className = 'place-card';
    // Set id depending on price for use with filter
    priceNum = parseInt(data[i].price);
    if (priceNum > 100) {
      item.classList.add('All');
    } else if (priceNum > 50) {
      item.classList.add('100');
    } else if (priceNum > 10) {
      item.classList.add('50');
    } else {
      item.classList.add('10');
    }
    list.appendChild(item);
  }
  // Add unordered list to section
  section.appendChild(list);
}


// Send request for one place from API
async function getPlace(id) {
  const headerObj = {
    'Content-Type': 'application/json'
  };
  // Add JWT if we have it in cookie
  const cookie = getCookieByName('token');
  if (cookie) {
    headerObj['Authorization'] = 'Bearer ' + cookie;
  }
  // Send fetch
  const placeResponse = await fetch('http://localhost:5000/api/v1/places/' + id, {
    method: 'GET',
    headers: headerObj
  })
  // Handle response
  section1 = document.getElementById('place-details');
  // Error response
  if (placeResponse.status !== 200) {
    const message = document.createElement('h2');
    message.textContent = 'The requested place could not be found.';
    section1.appendChild(message);
    return;
  }


  const placeData = await placeResponse.json();
  console.log(placeData);
  const placeCard = document.createElement('dl');
  placeCard.id = 'place-info';

  // Add place info elements
  // Heading
  const title = document.createElement('h1');
  title.textContent = placeData.title;
  section1.appendChild(title);
  // Host
  const hostt = document.createElement('dt');
  hostt.textContent = 'Host:';
  const hostd = document.createElement('dd');
  hostd.textContent = placeData.owner.first_name + ' ' + placeData.owner.last_name;
  // Price
  const pricet = document.createElement('dt');
  pricet.textContent = 'Price:';
  const priced = document.createElement('dd');
  priced.textContent = placeData.price;
  // Description
  const desct = document.createElement('dt');
  desct.textContent = 'Description:';
  const descd = document.createElement('dd');
  descd.textContent = placeData.description;
  // Amenities
  const ament = document.createElement('dt');
  ament.textContent = 'Amenities:';
  const amend = document.createElement('dd');
  // Build string based on amenities
  string = '';
  for (let i = 0; i < placeData.amenities.length; i++) {
    if (i !== 0) {
      string = string + ', ';
    }
    string = string + placeData.amenities[i];
  }
  if (placeData.amenities.length === 0) {
    string = 'None';
  }
  amend.textContent = string;
  placeCard.appendChild(hostt);
  placeCard.appendChild(hostd);
  placeCard.appendChild(pricet);
  placeCard.appendChild(priced);
  placeCard.appendChild(desct);
  placeCard.appendChild(descd);
  placeCard.appendChild(ament);
  placeCard.appendChild(amend);
  section1.appendChild(placeCard);


  // Add reviews
  const heading = document.createElement('h2');
  heading.textContent = 'Reviews'
  section2 = document.getElementById('reviews');
  section2.appendChild(heading);
  // fetch reviews
  const reviewsResponse = await fetch('http://localhost:5000/api/v1/places/' + id + '/reviews', {
    method: 'GET',
    headers: headerObj
  });
  if (reviewsResponse.status !== 200) {
    const message = document.createElement('h3');
    message.textContent = 'Reviews could not be retrived';
    section2.appendChild(message);
    return;
  }

  const reviewsData = await reviewsResponse.json();
  console.log(reviewsData);
  if (reviewsData.length === 0) {
    const message = document.createElement('h3');
    message.textContent = 'This place has no reviews yet';
    section2.appendChild(message);
    return;
  }
  const reviewsList = document.createElement('ul');
  // Iterate over and add reviews
  for (let i = 0; i < reviewsData.length; i++) {
    // Get user's name by fetching from ID
    const userResponse = await fetch('http://localhost:5000/api/v1/users/' + reviewsData[i].user_id, {
      method: 'GET',
      headers: headerObj
    });
    if (userResponse.status !== 200) {
      continue;
    }
    // populate review
    const reviewCard = document.createElement('li');
    reviewCard.className = 'review-card';
    // Name
    const userData = await userResponse.json();
    console.log(userData);
    const name = document.createElement('h3');
    name.textContent = userData.first_name + ' ' + userData.last_name;
    // Text
    const text = document.createElement('p');
    text.textContent = reviewsData[i].text;
    // Rating
    const rating = document.createElement('p');
    rating.textContent = 'Rating: ' + reviewsData[i].rating + '/5';
    // Add elements
    reviewCard.appendChild(name);
    reviewCard.appendChild(text);
    reviewCard.appendChild(rating);
    reviewsList.appendChild(reviewCard);
  }
  // Add list to section
  section2.appendChild(reviewsList);

  // Add function to review form at bottom of page
  if (cookie) {
    document.getElementById('add-review').style.display = 'flex';
  }
  const form = document.getElementById('review-form');
  form.addEventListener('submit', async event => {
    event.preventDefault();
    // Send data to submit function
    submitResponse = await submitReview(form, id);
  })
}


// Function to submit a review on either place details page or add_review
async function submitReview(form, place) {
  // Add a loading / message box while waiting
  const message = document.createElement('p');
  message.textContent = 'Processing your request...'
  form.appendChild(message);
  const headerObj = {
    'Content-Type': 'application/json'
  };
  // Add JWT if we have it in cookie
  const cookie = getCookieByName('token');
  if (cookie) {
    headerObj['Authorization'] = 'Bearer ' + cookie;
  }
  const response = await fetch('http://localhost:5000/api/v1/reviews', {
    method: 'POST',
    headers: headerObj,
    body: JSON.stringify({ text: form['review'].value, rating: parseInt(form['rating'].value), place_id: place})
  });
  if (response.status === 403) {
    message.textContent = 'Sorry, you aren\'t permitted to do this.';
  } else if (response.status !== 201) {
    message.textContent = 'Something went wrong, please try again.';
  } else {
    message.textContent = 'Thank you for your review!';
    for (let i = 0; i < form.children.length; i++) {
      form.children[i].style.display = 'none';
    }
    message.style.display = 'block';
  }
}
