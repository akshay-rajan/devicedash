document.addEventListener('DOMContentLoaded', () => {

  // Viewphones
  let viewphones = document.getElementsByClassName('viewphone');
  for (let i = 0; i < viewphones.length; i++) {
    let viewbutton = viewphones[i];
    viewbutton.addEventListener('click', () => displayPhone(viewbutton));
  }

  // Backbutton
  let backButton = document.querySelector('.backbutton');
  let phoneListDiv = document.getElementById('phonelist');
  let viewPhoneDiv = document.getElementById('viewphone');
  if (backButton) {
    backButton.addEventListener('click', () => {
      phoneListDiv.style.display = 'block';
      viewPhoneDiv.style.display = 'none';
    });
  }
})


function displayPhone(viewbutton) {

  // Fetch the data about the phone using the phone id and display it using javascript
  let phone_id = viewbutton.dataset.id;
  console.log(phone_id);
  fetch(`/find/${phone_id}`)
  .then(response => {
    if (!response.ok) {
      throw new Error(`Response not ok: ${response.status}`);
    }
    return response.json();
    })
  .then(data => {
    console.log(data);

    // Use the fetched data
    const phoneListDiv = document.getElementById('phonelist');
    const viewPhoneDiv = document.getElementById('viewphone');
    phoneListDiv.style.display = 'none';
    viewPhoneDiv.style.display = 'block';
    viewPhoneDiv.textContent = JSON.stringify(data, null, 2);

    // Create 'Back' button
    let backButton = document.querySelector('.backbutton');
    if (!backButton) {
      backButton = document.createElement('button');
      backButton.classList.add('btn', 'btn-primary', 'backbutton');
      backButton.textContent = "Back";
      viewPhoneDiv.appendChild(backButton);
    }
    backButton.addEventListener('click', () => {
      phoneListDiv.style.display = 'block';
      viewPhoneDiv.style.display = 'none';
    });

  })
  .catch(error => {
    console.log('Error: ', error);
  })
}

